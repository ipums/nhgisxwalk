"""IPUMS/NHGIS Census Crosswalk and Atom Generator
"""

from .id_codes import code_cols, generate_atom_id, generate_geoid, id_from
from .id_codes import blk_gj, bgp_gj, bg_gj, tr_gj, co_gj, gj_code_components

import numpy
import pandas

import pickle

# used to fetch/vectorize ID generation functions
id_generator_funcs = [blk_gj, bgp_gj, bg_gj, tr_gj, co_gj]
id_generators = {f.__name__: f for f in id_generator_funcs}

# sorting parameters -- all crosswalks are sorted accordingly
sort_params = {
    "ascending": True,
    "na_position": "last",
    "ignore_index": True,
    "inplace": True,
}

CSV = "csv"


class GeoCrossWalk:
    """Generate a temporal crosswalk for census geography data 
    built from the smallest intersecting units (atoms). Each row in
    a crosswalk represents a single atom and is comprised of a source
    ID (geo+year), a target ID (geo+year), and at least one column
    of weights. The weights are the interpolated proportions of source
    attributes that are are calculated as being within the target units.
    For a description of the algorithmic workflow see the
    `General Crosswalk Construction Framework <https://github.com/jGaboardi/nhgisxwalk/blob/master/resources/general-crosswalk-construction-framework.pdf>`_.
    For a description of the algorithmic workflow
    in the 1990 "no data" scenarios see
    `Handling 1990 No-Data Blocks in Crosswalks <https://github.com/jGaboardi/nhgisxwalk/blob/master/resources/handling-1990-no-data-blocks-in-crosswalks.pdf>`_.
    For more information of the base crosswalks see their
    `technical details <https://www.nhgis.org/user-resources/geographic-crosswalks#details>`_
    here.
    
    For further description see:
      * Schroeder, J. P. 2007. Target-density weighting interpolation
            and uncertainty evaluation for temporal analysis of census
            data. Geographical Analysis 39 (3):311–335.
    
    Parameters
    ----------
    
    base : pandas.DataFrame
        The base-level crosswalk containing composite atoms of smallest units
        to build larger crosswalk atoms of larger source and target units.
    
    source_year : str
        The census source units year.
    
    target_year : str
        The census target units year.
    
    source_geo : str
        The census source geographic units.
    
    target_geo : str
        The census target geographic units.
    
    base_source_geo : str
        The base-level crosswalk's source geographic units.
    
    base_source_table : str
        The path to the source year's base tabular data.
    
    input_var : str or iterable
        Demographic or housing census variables. For currently available
        variables call ``nhgisxwalk.desc_code_YYYY()`` where YYYY is the
        census year.
    
    weight_var : str or iterable
        The column tags to use for the atomic interpolated variables.
    
    weight_prefix : str
        Optional prefix to add to the weights columns. Default is "wt_".
    
    base_weight : str
        Name for the weight column in the base crosswalk. Default is "WEIGHT".
    
    base_parea : str
        Name for the area column in the base crosswalk. Default is "PAREA".
        Note: 1990 is "PAREA_VIA_BLK00".
    
    stfips : str
        If a state-level subset is desired, set the state FIPS code.
    
    add_geoid : bool
        Add in the corresponding Census GEOID (``True``). Default is ``True``.
        This options is not available for "bgp" (block group parts).
        The associated method is ``generate_geoids()``.
    
    keep_base : bool
        Keep the base crosswalk when building of the atomic crosswalk
        is complete (``True``). Default is ``False``.
    
    drop_base_cols : bool
        Flag to remove unnecessary columns from the base crosswalk. Default is ``True``.
    
    vectorized : bool
        Vectorize the ``id_codes.id_from()`` function for (potential)
        speedups (``True``). Default is ``True``.
    
    supp_source_table : str
        The path to the source year's base supplementary tabular data. Default is ``None``.
        
    drop_supp_col : bool
        Drop the supplementary containing ID generated with the 1990 "no data" process.
        Default is ``True``.
    
    weights_precision : int
        Round the resultant crosswalk weights to this many decimals. Default is 10.
    
    Attributes
    ----------
    
    source : str
        The combination of the source census geographic unit and census year.
    
    target : str
        The combination of the target census geographic unit and census year.
    
    xwalk_name : str
        The combination of ``source` and ``target``.
    
    xwalk : pandas.DataFrame
        The actual crosswalk generated between ``source`` and ``target``.
    
    wt : str
        See ``weight`` parameter.
    
    source_id_components : pandas.DataFrame
        The ``source`` result from ``id_codes.gj_code_components()``.
    
    target_id_components : pandas.DataFrame
        The ``target`` result from ``id_codes.gj_code_components()``.
    
    base_tab_df : pandas.DataFrame
        Summary file tabular for associated base crosswalk.
    
    all_base_ids : numpy.array
        All source IDs from the base crosswalk. Declared in ``handle_1990_no_data``.

    pop_base_ids : numpy.array
        Source IDs associated with some population/housing value
        from the base crosswalk. Declared in ``handle_1990_no_data``.
        
    nopop_base_ids : numpy.array
        Source IDs associated with no population/housing value
        from the base crosswalk. Declared in ``handle_1990_no_data``.
        
    nopop_base : pandas.DataFrame
        The base-level crosswalk associated with no population/housing value containing
        composite atoms of smallest units to build larger crosswalk atoms of larger
        source and target units. Declared in ``handle_1990_no_data``.
        
    nod_xwalk : pandas.DataFrame
        The actual crosswalk associated with no population/housing value 
        generated between ``source`` and ``target``. Declared in ``handle_1990_no_data``.
        
    weight_var : list
        See ``weight_var`` parameter.
        
    weight_col : str or iterable
        Full weight column names (including prefixes).
        Declared in ``handle_1990_no_data``.
    
    supp_geo : str
        Type of geographic unit needed to determine unpopulated units. Currently
        this can only be 1990 block groups ('bg') for determining unpopulated
        1990 NHGIS block group parts ('bgp').
    
    supp_source : str or None
        The source supplementary unit.
    
    supp_target : str or None
        The target supplementary unit.
    
    src_unacc : numpy.array
        Unaccounted for / potential source IDs.
        Declared in ``handle_1990_no_data`` or ``accounting``.
        
    trg_unacc : numpy.array
        Unaccounted for / potential target IDs. Declared in ``accounting``.
    
    Notes
    -----
    
    For more information see the ``nhgisxwalk`` FAQ
    `page <https://github.com/jGaboardi/nhgisxwalk/wiki/FAQ-&-Resources>`_.
    
    Examples
    --------
    
    **Ex. 1:** Instantiate the example data and calculate an atomic crosswalk.
    
    >>> import nhgisxwalk
    >>> df = nhgisxwalk.example_crosswalk_data()
    >>> df
      bgp1990 blk1990 blk2010 tr2010   wt  pop_1990  hh_1990
    0       A     A.1     X.1      X  1.0      60.0     25.0
    1       A     A.2     X.2      X  0.3     100.0     40.0
    2       A     A.2     Y.1      Y  0.7     100.0     40.0
    3       B     B.1     X.3      X  1.0      50.0     20.0
    4       B     B.2     Y.2      Y  1.0      80.0     30.0
    
    This synthetic data is comprised of 1990 and 2010 census blocks (``blk1990``
    and ``blk2010``, respectively); the base atomic crosswalk. Since the
    boundaries of census blocks are subject to change over time, the 1990
    blocks don't nest perfectly in the 2010 blocks. The magnitude of this
    imperfect nesting is represented in the weight column (``wt``), which
    records the areal portion of the 1990 block that intersects with the 2010
    blocks. Further, the population and household counts for the 1990 blocks
    are available through the ``pop_1990`` and ``hh_1990`` columns.
    Finally, the associated 1990 census block group parts and the 2010 census
    tracts are also represented with ``bgp1990`` and ``tr2010``. With this 
    information it is possible to create a (synthetic) 1990 block group part
    to 2010 tract crosswalk.
    
    >>> atoms = nhgisxwalk.calculate_atoms(
    ...             df,
    ...             weight="wt",
    ...             input_var=["pop_1990", "hh_1990"],
    ...             weight_var=["pop", "hh"],
    ...             weight_prefix="wt_",
    ...             source_id="bgp1990",
    ...             groupby_cols=["bgp1990", "tr2010"]
    ...         )
    >>> atoms
      bgp1990 tr2010    wt_pop     wt_hh
    0       A      X  0.562500  0.569231
    1       A      Y  0.437500  0.430769
    2       B      X  0.384615  0.400000
    3       B      Y  0.615385  0.600000
    
    The result is four atomic intersections between the synthetic 1990 census
    block group parts and the 2010 census tracts with varying population
    and household proportional weights.
    
    **Ex. 2:** Generate an empirical crosswalk between block group parts from
    the 2000 Decennial Census and tracts from the 2010 Decennial Census.
    
    >>> import nhgisxwalk
    
    Set the source and target years to 2000 and 2010, respectively.
    
    >>> source_year, target_year = "2000", "2010"
    
    Read in the base unit crosswalk. This is the crosswalk that is used
    to build up the source and and target units from the source and and target
    years. Currently supported base crosswalks are 1990-2010 blocks and
    2000-2010 blocks, which can be downloaded from
    `NHGIS <https://github.com/jGaboardi/nhgisxwalk/wiki/FAQ-&-Resources#where-can-i-download-the-base-geographic-crosswalks>`_.
    The versions found within ``nhgisxwalk`` (see 
    `./testing_data_subsets/ <https://github.com/jGaboardi/nhgisxwalk/tree/master/testing_data_subsets>`_)
    are single state subsets (Delaware) for testing and demonstration purposes.
    
    >>> subset_data_dir = "./testing_data_subsets"
    >>> base_xwalk_name = "/nhgis_blk%s_blk%s_gj.zip" % (source_year, target_year)
    >>> base_xwalk_file = subset_data_dir + base_xwalk_name
    >>> data_types = nhgisxwalk.str_types(["GJOIN%s"%source_year, "GJOIN%s"%target_year])
    >>> base_xwalk = pandas.read_csv(base_xwalk_file, index_col=0, dtype=data_types)
    >>> base_xwalk.head()
                GJOIN2000           GJOIN2010    WEIGHT     PAREA
    0  G10000100401001000  G10000100401001000  1.000000  1.000000
    1  G10000100401001001  G10000100401001001  0.999981  0.999988
    2  G10000100401001001  G10000100401001003  0.000019  0.000012
    3  G10000100401001002  G10000100401001002  1.000000  1.000000
    4  G10000100401001003  G10000100401001003  1.000000  1.000000
    
    This base unit crosswalk shows the areal portion (``WEIGHT``) of the
    source units (``GJOIN2000``) in the target units (``GJOIN2010``).
    For example, the vast majority of 2000 block ``G10000100401001001``
    intersects with 2010 block ``G10000100401001001``, but a minute portion
    intersects with 2010 block ``G10000100401001003``.
    Next, use the shorthand lookup tool for geography abbreviations and set
    the source and target geographies to ``bgp`` and ``tr``, respectively.
    
    >>> nhgisxwalk.valid_geo_shorthand(shorthand_name=False)
    {'block': 'blk', 'block group part': 'bgp', 'block group': 'bg', 'tract': 'tr', 'county': 'co'}
    >>> source_geog, target_geog = "bgp", "tr"
    
    Select the Persons and Families variables with the lookup tool
    for the 2000 Summary File 1b (``desc_code_2000_SF1b``), and set
    column tags for the weights to be interpolated.
    
    >>> input_vars = [
    ...    nhgisxwalk.desc_code_2000_SF1b["Persons"]["Total"],
    ...    nhgisxwalk.desc_code_2000_SF1b["Families"]["Total"],
    ... ]
    >>> input_vars
    ['FXS001', 'F2V001']
    >>> input_var_tags = ["pop", "fam"]
    
    At this point an ``nhgisxwalk.GeoCrossWalk`` object can be instantiated,
    which will be a state-level crosswalk for Delaware (state FIPS code 10).
    
    >>> subset_state = "10"
    >>> bgp2000_to_tr2010 = nhgisxwalk.GeoCrossWalk(
    ...     base_xwalk,
    ...     source_year=source_year,
    ...     target_year=target_year,
    ...     source_geo=source_geog,
    ...     target_geo=target_geog,
    ...     base_source_table=subset_data_dir+"/2000_block.csv.zip",
    ...     input_var=input_vars,
    ...     weight_var=input_var_tags,
    ...     add_geoid=True,
    ...     stfips=subset_state
    ... )
    >>> bgp2000_to_tr2010.xwalk[1020:1031][["bgp2000gj", "tr2010gj", "wt_pop", "wt_fam"]]
                           bgp2000gj        tr2010gj    wt_pop    wt_fam
    1020  G10000509355299999051302R1  G1000050051302  1.000000  1.000000
    1021  G10000509355299999051302R2  G1000050051302  1.000000  1.000000
    1022  G10000509355299999051302U1  G1000050051302  1.000000  1.000000
    1023  G10000509355299999051303R1  G1000050051303  1.000000  1.000000
    1024  G10000509355299999051303U1  G1000050051303  1.000000  1.000000
    1025  G10000509355299999051304R1  G1000050051305  0.680605  0.633909
    1026  G10000509355299999051304R1  G1000050051306  0.319167  0.365782
    1027  G10000509355299999051304R1  G1000050051400  0.000227  0.000309
    1028  G10000509355299999051304R2  G1000050051305  0.802661  0.817568
    1029  G10000509355299999051304R2  G1000050051306  0.197339  0.182432
    1030  G10000509355299999051304U2  G1000050051305  0.530658  0.557464
    
    The above slice of the generated crosswalk provides two key insights.
    First, the initial 6 atoms show that the corresponding 2000 block group
    parts nest entirely within the intersecting 2010 tracts. However, the
    following 5 atoms partially intersect to varying degrees. Second,
    the proportional weight for each variable will likely differ based on
    the counts used for interpolation. This is the reason why a single
    weighted portion can't be used for all variables.
    
    The corresponding census-assigned GEOIDs are also available within the crosswalk.
    The block group parts have no corresponding GEOIDs because they are a direct product
    of the NHHGIS.
    
    >>> bgp2000_to_tr2010.xwalk[1020:1031][["bgp2000gj", "tr2010gj", "tr2010ge"]]
                           bgp2000gj        tr2010gj     tr2010ge
    1020  G10000509355299999051302R1  G1000050051302  10005051302
    1021  G10000509355299999051302R2  G1000050051302  10005051302
    1022  G10000509355299999051302U1  G1000050051302  10005051302
    1023  G10000509355299999051303R1  G1000050051303  10005051303
    1024  G10000509355299999051303U1  G1000050051303  10005051303
    1025  G10000509355299999051304R1  G1000050051305  10005051305
    1026  G10000509355299999051304R1  G1000050051306  10005051306
    1027  G10000509355299999051304R1  G1000050051400  10005051400
    1028  G10000509355299999051304R2  G1000050051305  10005051305
    1029  G10000509355299999051304R2  G1000050051306  10005051306
    1030  G10000509355299999051304U2  G1000050051305  10005051305
    
    
    """

    def __init__(
        self,
        base,
        source_year=None,
        target_year=None,
        source_geo=None,
        target_geo=None,
        base_source_table=None,
        input_var=None,
        weight_var=None,
        stfips=None,
        base_source_geo="blk",
        base_weight="WEIGHT",
        base_parea="PAREA",
        weight_prefix="wt_",
        add_geoid=True,
        keep_base=False,
        drop_base_cols=True,
        vectorized=True,
        supp_source_table=None,
        drop_supp_col=True,
        weights_precision=10,
    ):

        # Set class attributes -------------------------------------------------
        # source and target class attributes
        self.source_year, self.target_year = source_year, target_year
        self.source_geo, self.target_geo = source_geo, target_geo

        # check that supplemental table is declared if 1990 block group parts
        if self.source_year == "1990" and self.source_geo == "bgp":
            if not supp_source_table:
                msg = "The 'supp_source_table' parameter must be declared (and valid) "
                msg += "when creating a crosswalk sourced from 1990 blocks/block group "
                msg += "parts. The current value is '%s'." % supp_source_table
                raise RuntimeError(msg)

        # set for gj (nhgis ID)
        self.code_type, self.code_label = "gj", "GJOIN"
        self.tabular_code_label = "GISJOIN"

        # source and target names
        self.source = self.source_geo + self.source_year + self.code_type
        self.target = self.target_geo + self.target_year + self.code_type
        self.xwalk_name = "nhgis_%s_%s" % (self.source[:-2], self.target[:-2])
        self.stfips = stfips

        # input, summed, and weight variable names
        self.input_var, self.weight_var = input_var, weight_var
        self.base_weight = base_weight
        self.base_parea = base_parea
        self.wt = weight_prefix

        # source geographies within the base crosswalk
        self.base_source_geo = base_source_geo

        # columns within the base crosswalk
        self.base_source_col = self.code_label + self.source_year
        self.base_target_col = self.code_label + self.target_year

        # path to the tabular data for the base source units
        self.base_source_table = base_source_table

        # Prepare base for output crosswalk ------------------------------------
        self.base = base

        # fetch all components of that constitute various geographic IDs -------
        self.fetch_gj_code_components()

        # join the (base) source tabular data to the base crosswalk ------------
        self.join_source_base_tabular()

        # add source geographic unit ID to the base crosswalk ------------------
        self.generate_ids("source", vectorized)

        # add target geographic unit ID to the base crosswalk ------------------
        self.generate_ids("target", vectorized)

        # Create atomic crosswalk ----------------------------------------------
        # calculate the source to target atom values
        self.xwalk = calculate_atoms(
            self.base,
            weight=self.base_weight,
            input_var=self.input_var,
            weight_var=self.weight_var,
            weight_prefix=self.wt,
            source_id=self.source,
            groupby_cols=[self.source, self.target],
            overwrite_attrs=self,
        )

        # Special case for handling 1990 data, where blocks --------------------
        # without population/housing where excluded from the
        # publicly-released summary files
        if self.source_year == "1990" or self.target_year == "1990":

            if self.source_geo == "bgp" or self.target_geo == "bgp":
                # block group IDs are needed to determine
                # populated blocks in 1990
                self.supp_geo = "bg"

                if self.source_geo == "bgp":
                    self.supp_source = self.supp_geo + self.source_year + self.code_type
                    self.supp_target = None
                else:
                    self.supp_source = None
                    self.supp_target = self.supp_geo + self.target_year + self.code_type

                # call special function
                handle_1990_no_data(self, vectorized, supp_source_table, drop_supp_col)

            else:
                raise RuntimeError("Only 'bgp' as is functional.")

        # keep only the necessary base columns ---------------------------------
        if drop_base_cols:
            self._drop_base_cols()

        # Step 9 from the General Workflow -------------------------------------
        self.accounting()

        # discard building base if not needed ----------------------------------
        if not keep_base:
            del self.base

        # add column(s) for the original Census GEOID --------------------------
        # -- this options is not available for "bgp" (block group parts)
        if add_geoid:
            for xdir in [self.source, self.target]:
                if xdir.startswith("bgp"):
                    continue
                else:
                    col = "tr%s" % target_year
                    self.xwalk[xdir[:-2] + "ge"] = self.xwalk[xdir].map(
                        lambda x: generate_geoid(x)
                    )

            # reorder columns
            _id_cols = [c for c in self.xwalk.columns if c not in self.weight_col]
            self.xwalk = self.xwalk[_id_cols + self.weight_col]

        # extract a subset of national resultant crosswalk to target state (if desired)
        if self.stfips:
            self.xwalk = extract_state(
                self.xwalk, self.stfips, self.xwalk_name, self.target
            )
            self.xwalk_name += "_" + self.stfips

        # round the weights in the resultant crosswalk (if desired)
        if weights_precision:
            self.xwalk = round_weights(self.xwalk, decimals=weights_precision)

        # sort the resultant values
        self.xwalk.sort_values(by=[self.source, self.target], **sort_params)

    def _drop_base_cols(self):
        """Retain only ID columns and original weights in the base crosswalk."""
        retain = [
            self.source,
            self.base_source_col,
            self.base_target_col,
            self.target,
            self.base_weight,
            self.base_parea,
        ]
        order = [c for r in retain for c in self.base.columns if c.startswith(r)]
        self.base = self.base[order]

    def fetch_gj_code_components(self):
        """Fetch dataframe that describes each component of a geographic unit ID."""
        self.base_source_gj_components = gj_code_components(
            self.source_year, self.base_source_geo
        )
        self.source_gj_components = gj_code_components(
            self.source_year, self.source_geo
        )
        self.target_gj_components = gj_code_components(
            self.target_year, self.target_geo
        )

    def join_source_base_tabular(self):
        """Join tabular attributes to base crosswalk."""
        # read in national tabular data
        data_types = str_types(self.base_source_gj_components["Variable"])
        self.base_tab_df = pandas.read_csv(self.base_source_table, dtype=data_types)

        # Special case for 2000 blocks (of 2000 bgp)-- needs Urban/Rural code
        # For more details see:
        # https://gist.github.com/jGaboardi/36c7640af1f228cdc8a691505262e543
        # and
        # nhgisxwalk/notebooks/build_subset.ipynb

        # do left merge
        self.base = pandas.merge(
            left=self.base,
            right=self.base_tab_df,
            how="left",
            left_on=self.base_source_col,
            right_on=self.tabular_code_label,
            validate="many_to_many",
        )

    def generate_ids(self, id_type, vect, supp=False, supp_base=None, return_df=False):
        """Add source or target geographic unit ID to the base crosswalk.
        
        Parameters
        ----------
        
        id_type : str
            Either ``source`` or ``target``.
        
        vect : bool
            See the ``vectorized`` parameter in ``GeoCrossWalk``.
        
        supp : bool
            Use the supplementary (unpopulated) base crosswalk. Default is ``False``.
        
        supp_base : pandas.DataFrame
            The supplementary (unpopulated) base crosswalk. See ``self.nopop_base``.
            Default is ``None``.
        
        return_df : bool
            Set to ``True`` to return ``df`` instead of updating ``self.base``.
        
        Returns
        -------
        
        df : pandas.DataFrame
            The updated crosswalk dataframe.
        
        """
        # set the crosswalk to be used
        df = supp_base if return_df else self.base

        # declare id type-specific variables
        if id_type == "source":
            cname = self.source if not supp else self.supp_source
            year, geog, base_col = (
                self.source_year,
                self.source_geo,
                self.base_source_col,
            )
        else:
            cname = self.target if not supp else self.supp_target
            year, geog, base_col = (
                self.target_year,
                self.target_geo,
                self.base_target_col,
            )

        # flag supplemental block group parts scenario
        supp_bgp = supp and geog == "bgp"

        # generate IDS
        if not supp and geog == "bgp":
            cols, func = code_cols(geog, year), bgp_gj
            args = df, cols
            df = func(*args, cname=cname)
        elif id_type == "target" or supp_bgp:
            if id_type == "source" and geog == "blk":
                raise AttributeError()
            func = id_generators[
                "%s_gj" % geog if not supp else "%s_gj" % self.supp_geo
            ]
            df[cname] = id_from(func, year, df[base_col], vect)
        else:
            msg = "(id_type: %s, supp: %s, cname: %s, year: %s, geog: %s)"
            msg = msg % (id_type, supp, cname, year, geog)
            msg = "Error in generate_ids params: " + msg
            raise RuntimeError(msg)

        # return the dataframe for supplementary scenarios
        if return_df:
            return df

    def accounting(self):
        """Step 9 in the General Workflow."""

        # Isolate unaccounted for source geographies
        if not hasattr(self, "src_unacc"):
            self.src_unacc = numpy.setdiff1d(
                self.base[self.source].tolist(), self.xwalk[self.source].tolist(),
            )

        # Isolate unaccounted for target geographies
        self.trg_unacc = numpy.setdiff1d(
            self.base[self.target].tolist(), self.xwalk[self.target].tolist(),
        )

        # Append unaccounted source and target atoms
        # start with the last index of the resultant crosswalk
        endex = self.xwalk.index[-1]
        # dict for source and target 'unaccounted for' ids
        unaccounted = {self.source_geo: self.src_unacc, self.target_geo: self.trg_unacc}

        # confirm variable data types
        if not hasattr(self, "weight_col"):
            self.weight_var = _check_vars(self.weight_var)
            self.weight_col = _weight_columns(
                self.wt if self.wt else "", self.weight_var
            )

        # iterate over {geography_type: unaccounted_for_ids}
        for geo, unaccs in unaccounted.items():
            # move to the geography type if there are no missing IDs
            if unaccs.size == 0:
                continue
            # iterate over each unaccounted for id}
            for idx, unacc in enumerate(unaccs, 1):
                endex += idx
                # append one record to the dataframe
                self.xwalk.loc[endex] = [
                    unacc
                    if c.split("_")[0][:3] == geo
                    else 0.0
                    if c in self.weight_col
                    else numpy.nan
                    for c in self.xwalk.columns
                ]

    def xwalk_to_pickle(self, path="", fext=".pkl"):
        """Write the produced ``GeoCrossWalk`` object."""
        with open(path + self.xwalk_name + fext, "wb") as pkl_xwalk:
            pickle.dump(self, pkl_xwalk, protocol=2)

    @staticmethod
    def xwalk_from_pickle(fname, fext=".pkl"):
        """Read in a produced crosswalk from a pickled ``GeoCrossWalk``."""
        with open(fname + fext, "rb") as pkl_xwalk:
            self = pickle.load(pkl_xwalk)
        return self


def extract_state(in_xwalk, stfips, xwalk_name, endpoint, code="gj", sort_by=None):
    """Subset a national crosswalk to state-level (within target year).
    
    Parameters
    ----------
    
    in_xwalk : pandas.DataFrame
        The original full crosswalk.  See the ``xwalk`` attribute or ``base``
        parameter in ``GeoCrossWalk``.
    
    stfips : str
        See the ``stfips`` parameter in ``GeoCrossWalk``.
        Set to 'nan' to extract geographies with no associated state.
    
    xwalk_name : str
        See the ``xwalk_name`` parameter in ``GeoCrossWalk``.
    
    endpoint : str
        Column name to extract from.
    
    code : str
        The code type used in indexing unique states. Default is ``'gj'``.
    
    sort_by : list
        Columns to sort by. This is used along with ``sort_params``. Default is ``None``.
    
    Returns
    -------
    
    out_xwalk : pandas.DataFrame
        A state-level (target) crosswalk.
    
    """

    # make sure the crosswalk isn't already an extracted state or overwritten
    check_state_label = xwalk_name.split("_")[-1]
    if check_state_label.isnumeric() or check_state_label == "nan":
        msg = "This crosswalk may already be a state subset. "
        msg += "Check the name/attributes.\n"
        msg += "\txwalk_name: '%s', stfips: %s'" % (xwalk_name, stfips)
        raise RuntimeError(msg)

    # set NaN (null) extraction condition
    nan = True if stfips.lower() == "nan" else False

    # set extraction condition
    extract_lambda = (
        lambda x: nan if str(x) == "nan" else _state(x, stfips=stfips, code=code)
    )
    condition = in_xwalk[endpoint].map(extract_lambda)
    out_xwalk = in_xwalk[condition].copy()

    if sort_by:
        out_xwalk.sort_values(by=sort_by, **sort_params)

    return out_xwalk


def extract_unique_stfips(cls=None, df=None, endpoint="target", code="gj"):
    """Return a set of unique state FIPS codes.
    
    Parameters
    ----------
    
    cls : nhgisxwalk.GeoCrossWalk
        Instance of a crosswalk object. When this parameter is used, the 
        ``df`` parameter should not be used. Default is ``None``.
    
    df : pandas.DataFrame
        A crosswalk of spatio-temporal census geographies. Default is ``None``.
        When the ``cls`` parameter is not used, this parameter should be used.
    
    endpoint : str
        The column from which unique states should extracted. Default is ``'target'``,
        which represents the ``target`` attribute of an ``nhgisxwalk.GeoCrossWalk``.
    
     code : str
        The code type used in indexing unique states. Default is ``'gj'``.
    
    Returns
    -------
    
    unique_stfips : 
        All unique states from the specified column.
    
    """

    if cls:
        endpoint = getattr(cls, endpoint.lower())
        df = cls.xwalk

    unique_stfips = set(df[endpoint].map(lambda x: _state(x, code=code)))

    return unique_stfips


def xwalk_df_to_csv(cls=None, dfkwds=dict(), path="", fext="zip"):
    """Write the produced crosswalk to .csv or .csv.zip.
    
    Parameters
    ----------
    
    cls : nhgisxwalk.GeoCrossWalk
        Instance of a crosswalk object. When this parameter is used, the 
        ``dfkwds`` parameter should not be used. Default is ``None``.
    
    dfkwds : dict()
        When the ``cls`` parameter is not used, this parameter should be used.
        It should contain three keys in the form:
        ``{"df":<pandas.DataFrame>, "stfips": <str>, "xwalk_name": <str>}``.
        Default is ``dict()``.
    
    path : str
        Directory path without the file name.  Default is ``''``.
    
    fext : str
        Compression file extension. Default is ``'zip'``.
    
    """

    if cls:
        stfips = cls.stfips
        xwalk_name = cls.xwalk_name
        xwalk = cls.xwalk
    else:
        try:
            stfips = dfkwds["stfips"]
        except KeyError:
            stfips = None
        xwalk_name = dfkwds["xwalk_name"]
        xwalk = dfkwds["df"]
    if stfips and xwalk_name.split("_")[-1] != stfips:
        xwalk_name += "_" + stfips
    if fext:
        compression_opts = dict(method=fext, archive_name="%s.%s" % (xwalk_name, CSV))
        file_name = "%s%s.%s" % (path, xwalk_name, fext)
    else:
        compression_opts = None
        file_name = "%s%s.%s" % (path, xwalk_name, CSV)
    xwalk.to_csv(file_name, compression=compression_opts, index=False)


def xwalk_df_from_csv(fname, fext="zip", **kwargs):
    """Read in a produced crosswalk from .csv or .csv.zip."""

    if fext:
        file_path = "%s.%s" % (fname, fext)
    else:
        file_path = "%s.%s" % (fname, CSV)
    xwalk = pandas.read_csv(file_path, **kwargs)
    return xwalk


def calculate_atoms(
    df,
    weight=None,
    input_var=None,
    weight_var=None,
    weight_prefix=None,
    source_id=None,
    groupby_cols=None,
    overwrite_attrs=None,
):
    """Calculate the atoms (intersecting parts) of census geographies
    and interpolate a proportional weight of the source attribute that
    lies within the target geography.
    
    Parameters
    ----------
    
    df : pandas.DataFrame
        The input data. See ``GeoCrossWalk.base``.
    
    weight : str
        The weight colum name(s).
    
    input_var : str or iterable
        The input variable column name(s).
    
    weight_var : str or iterable
        The groupby and summed variable column name(s).
    
    weight_prefix : str
        Prepend this prefix to the the ``weight_var`` column name.
    
    source_id : str
        The source ID column name.
    
    groupby_cols : list
        The dataframe columns on which to perform groupby.
    
    overwrite_attrs : None or GeoCrossWalk
        Setting this parameter to a ``GeoCrossWalk`` object overwrites the
        ``input_var`` and ``weight_var`` attributes. Default is ``None``.
    
    Returns
    -------
    
    atoms : pandas.DataFrame
        All intersections between ``source`` and ``target`` geographies, and 
        the interpolated weight calculations for the propotion of
        source area attributes that are in the target area.
    
    Notes
    -----
    
    See example 1 in the ``GeoCrossWalk`` Examples section.
    
    """

    # confirm variable data types
    input_var, weight_var = _check_vars(input_var), _check_vars(weight_var)

    # determine length of variable lists
    n_input_var, n_weight_var = len(input_var), len(weight_var)

    # check variable lists are equal length
    if n_input_var != n_weight_var:
        msg = "The 'input_var' and 'weight_var' should be the same length. "
        msg += "%s != %s" % (n_input_var, n_weight_var)
        raise RuntimeError(msg)

    # add prefix (if desired)
    weight_col = _weight_columns(weight_prefix if weight_prefix else "", weight_var)

    if str(overwrite_attrs) != "None":
        overwrite_attrs.input_var = input_var
        overwrite_attrs.weight_col = weight_col

    # iterate over each pair of input/interpolation variables
    for ix, (ivar, wvar) in enumerate(zip(input_var, weight_col)):

        # calculate numerators
        df[wvar] = df[weight] * df[ivar]
        if ix == 0:
            # on the first iteration create an atom dataframe
            atoms = df.groupby(groupby_cols)[wvar].sum().to_frame()
            atoms.reset_index(inplace=True)
        else:
            # on tsubsequent iterations add weights as a column
            atoms[wvar] = df.groupby(groupby_cols)[wvar].sum().values

        # calculate denominators
        denominators = atoms.groupby(source_id)[wvar].sum()

        # interpolate weights
        atoms[wvar] = atoms[wvar] / atoms[source_id].map(denominators)

        # if any weights are NaN, replace with 0.
        atoms[wvar].fillna(0.0, inplace=True)

    return atoms


def handle_1990_no_data(geoxwalk, vect, supp_src_tab, drop_supp_col):
    """Step 1 in this workflow is handled as a normal case. See the algorithmic workflow in
    `Handling 1990 No-Data Blocks in Crosswalks <https://github.com/jGaboardi/nhgisxwalk/blob/master/resources/handling-1990-no
    
    Parameters
    ----------
    
    geoxwalk : nhgisxwalk.GeoCrossWalk
        A full crosswalk object.
    
    vect : bool
        See ``vectorized`` parameter in ``GeoCrossWalk.__init__``.
    
    supp_src_tab: str
        See ``supp_source_table`` parameter in ``GeoCrossWalk.__init__``.
    
    drop_supp_col : bool
        See ``drop_supp_col`` parameter in ``GeoCrossWalk.__init__``.
    
    Returns
    -------
    
    geoxwalk : nhgisxwalk.GeoCrossWalk
        The updated full crosswalk object.
    
    """

    # Step 2(a) ----------------------------------------------------------------------
    # isolate all unique source block IDs in the base crosswalk
    all_base_ids = geoxwalk.base[~geoxwalk.base[geoxwalk.base_source_col].isna()][
        geoxwalk.base_source_col
    ].copy()
    geoxwalk.all_base_ids = all_base_ids.unique()

    # isolate all unique **populated** base IDs from the base summary data
    geoxwalk.pop_base_ids = (
        geoxwalk.base_tab_df[geoxwalk.tabular_code_label].copy().to_numpy()
    )

    # isolate all unique **unpopulated** base IDs
    geoxwalk.nopop_base_ids = numpy.setdiff1d(
        geoxwalk.all_base_ids.tolist(), geoxwalk.pop_base_ids.tolist()
    )

    # create a "no-data" slice of the base crosswalk
    geoxwalk.nopop_base = geoxwalk.base[
        geoxwalk.base[geoxwalk.base_source_col].isin(geoxwalk.nopop_base_ids)
    ].copy()
    geoxwalk.nopop_base = geoxwalk.nopop_base[
        [geoxwalk.base_source_col, geoxwalk.base_target_col]
    ].copy()

    # Step 2(b) ----------------------------------------------------------------------
    # Generate the (supplement) IDs for source and target
    geoxwalk.nopop_base = geoxwalk.generate_ids(
        "source", vect, supp=True, supp_base=geoxwalk.nopop_base, return_df=True
    )

    # drop unneeded weight/area columns (these should all be zero anyway)
    _id_cols_ = [
        geoxwalk.supp_source,
        geoxwalk.base_source_col,
        geoxwalk.base_target_col,
    ]
    geoxwalk.nopop_base = geoxwalk.nopop_base[_id_cols_]

    # add target geographic unit ID to the base crosswalk
    geoxwalk.nopop_base = geoxwalk.generate_ids(
        "target", vect, supp=False, supp_base=geoxwalk.nopop_base, return_df=True
    )

    # Step 2(c) ----------------------------------------------------------------------
    # Drop records with a null value for GJOIN1990 block IDs (if present)
    geoxwalk.nopop_base = geoxwalk.nopop_base[
        ~geoxwalk.nopop_base[geoxwalk.base_source_col].isna()
    ]

    # groupby the source and target
    src_trg_cols = [geoxwalk.supp_source, geoxwalk.target]
    nod_xwalk = geoxwalk.nopop_base.groupby(src_trg_cols).size().reset_index()
    geoxwalk.nod_xwalk = nod_xwalk[src_trg_cols]

    # Step 2(d/e) -------------------------------------------------------------------
    # Assign a weight of 0. for all records in the "no-data" crosswalk
    if not hasattr(geoxwalk, "weight_col"):
        geoxwalk.weight_var = _check_vars(geoxwalk.weight_var)
        geoxwalk.weight_col = _weight_columns(
            geoxwalk.wt if geoxwalk.wt else "", geoxwalk.weight_var
        )
    for wcol in geoxwalk.weight_col:
        geoxwalk.nod_xwalk[wcol] = 0.0

    # Step 3 — Combine the result of Step 1 & Step 2
    ## 3(a) --------------------------------------------------------------------------
    ### 1990 Block Group Part Summary Data (National)
    # confirm variable data types
    if not hasattr(geoxwalk, "input_var"):
        geoxwalk.input_var = _check_vars(geoxwalk.input_var)
    supp_src_tab_sf = pandas.read_csv(supp_src_tab, dtype=str)
    for iv in geoxwalk.input_var:
        supp_src_tab_sf[iv] = supp_src_tab_sf[iv].astype(float)

    # GISJOIN ID Correction
    # *** this will be deprecated following the update of NHGIS GBP data ***
    src_idcols = code_cols(geoxwalk.source_geo, geoxwalk.source_year)
    supp_src_tab_sf = id_generators["%s_gj" % geoxwalk.source_geo](
        supp_src_tab_sf, src_idcols, cname=geoxwalk.tabular_code_label
    )

    # 3(b) ---------------------------------------------------------------------------
    # Identify containing geography IDs in Summary File (block groups)
    supp_idcols = code_cols(geoxwalk.supp_geo, geoxwalk.source_year)
    supp_src_tab_sf = id_generators["%s_gj" % geoxwalk.supp_geo](
        geoxwalk.source_year,
        None,
        df=supp_src_tab_sf,
        order=supp_idcols,
        cname=geoxwalk.supp_source,
    )
    # subset columns
    susbet_cols = [geoxwalk.tabular_code_label] + supp_idcols + [geoxwalk.supp_source]
    supp_src_tab_sf = supp_src_tab_sf[susbet_cols]

    # 3(c) ---------------------------------------------------------------------------
    # Identify containing block group IDs in Populated src1990trg-year crosswalk
    _map = dict(
        supp_src_tab_sf[[geoxwalk.tabular_code_label, geoxwalk.supp_source]].values
    )
    geoxwalk.xwalk[geoxwalk.supp_source] = geoxwalk.xwalk[geoxwalk.source].map(_map)
    reorder_cols = [
        geoxwalk.source,
        geoxwalk.supp_source,
        geoxwalk.target,
    ] + geoxwalk.weight_col
    geoxwalk.xwalk = geoxwalk.xwalk[reorder_cols]

    # 3(d) ---------------------------------------------------------------------------
    # "Expand" the no-data supplement_src1990target-year crosswalk
    nod_xwalk_exp = pandas.merge(
        left=supp_src_tab_sf,
        right=geoxwalk.nod_xwalk,
        how="left",
        left_on=geoxwalk.supp_source,
        right_on=geoxwalk.supp_source,
        validate="many_to_many",
    )
    keep_cols = [geoxwalk.tabular_code_label, geoxwalk.supp_source, geoxwalk.target]
    keep_cols += geoxwalk.weight_col
    nod_xwalk_exp = nod_xwalk_exp[keep_cols].copy()
    nod_xwalk_exp.rename(
        columns={geoxwalk.tabular_code_label: geoxwalk.source}, inplace=True
    )

    # 3(e) ---------------------------------------------------------------------------
    # Remove records from the expanded xwalk that are already in the populated xwalk
    # Generate a single atom IDs to perform a set difference
    atom_id = "atom_id"
    # Atom ID for populated crosswalk
    geoxwalk.xwalk = generate_atom_id(
        geoxwalk.xwalk, geoxwalk.source, geoxwalk.target, atom_id
    )

    # Atom ID for "no-data" crosswalk
    nod_xwalk_exp = generate_atom_id(
        nod_xwalk_exp, geoxwalk.source, geoxwalk.target, atom_id
    )

    # Keep these atoms from the expanded "no-data" crosswalk
    nod_atoms = nod_xwalk_exp[atom_id].tolist()
    pop_atoms = geoxwalk.xwalk[atom_id].tolist()
    keep_nod_atoms = numpy.setdiff1d(nod_atoms, pop_atoms)

    # Remove the duplicated atoms
    nod_xwalk_exp = nod_xwalk_exp[nod_xwalk_exp[atom_id].isin(keep_nod_atoms)]
    nod_xwalk_exp.reset_index(inplace=True, drop=True)
    geoxwalk.xwalk.drop(columns=atom_id, inplace=True)
    nod_xwalk_exp.drop(columns=atom_id, inplace=True)

    # 3(f) ---------------------------------------------------------------------------
    # Append the "no-data" crosswalk to the populated crosswalk
    geoxwalk.xwalk = geoxwalk.xwalk.append(nod_xwalk_exp, ignore_index=True)

    # pre-step 9 - # Isolate unaccounted for source geographies ----------------------
    geoxwalk.src_unacc = numpy.setdiff1d(
        supp_src_tab_sf[geoxwalk.tabular_code_label].unique().tolist(),
        geoxwalk.xwalk[geoxwalk.source].unique().tolist(),
    )

    if drop_supp_col:
        geoxwalk.xwalk.drop(columns=geoxwalk.supp_source, inplace=True)

    return geoxwalk


def round_weights(df, decimals):
    """Round the weights in a crosswalk."""
    df = df.round(decimals)
    return df


def _state(rec, stfips=None, code="gj"):
    """Slice out a particular state by FIPS code."""
    if code == "gj":
        # for GISJOIN IDs
        idx1, idx2 = 1, 3
    else:
        # for GEOIDs
        idx1, idx2 = 0, 2
    if stfips:
        # extract_state()
        return rec[idx1:idx2] == stfips
    else:
        # extract_unique_stfips()
        return "nan" if str(rec) == "nan" else rec[idx1:idx2]


def _check_vars(_vars):
    """If the input is a single, named variable (str), insert it into a list."""
    if type(_vars) == str:
        _vars = [_vars]
    return _vars


def _weight_columns(weight_prefix, weight_var):
    """Return the weight column headers."""
    weight_vars = [weight_prefix + wvar for wvar in weight_var]
    return weight_vars


def str_types(var_names):
    """String-type formatting for ID characters."""
    dtype = {c: str for c in var_names}
    return dtype


def valid_geo_shorthand(shorthand_name=True):
    """Shorthand lookups for census geographies."""
    lookup = {
        "blk": "block",
        "bgp": "block group part",
        "bg": "block group",
        "tr": "tract",
        "co": "county",
    }
    if not shorthand_name:
        lookup = {v: k for k, v in lookup.items()}
    return lookup


def example_crosswalk_data():
    """Create an example dataframe to demonstrate atom generation."""
    cols = ["bgp1990", "blk1990", "blk2010", "tr2010", "wt", "pop_1990", "hh_1990"]
    bgp1990 = ["A", "A", "A", "B", "B"]
    blk1990 = ["A.1", "A.2", "A.2", "B.1", "B.2"]
    blk2010 = ["X.1", "X.2", "Y.1", "X.3", "Y.2"]
    tr2010 = ["X", "X", "Y", "X", "Y"]
    wt = [1.0, 0.3, 0.7, 1.0, 1.0]
    pop_1990 = [60.0, 100.0, 100.0, 50.0, 80.0]
    hh_1990 = [25.0, 40.0, 40.0, 20.0, 30.0]
    col_data = [bgp1990, blk1990, blk2010, tr2010, wt, pop_1990, hh_1990]
    example_data = pandas.DataFrame(columns=cols)
    for cn, cd in zip(cols, col_data):
        example_data[cn] = cd
    return example_data


def split_blk_blk_xwalk(df, endpoint, fname, fpath="", sort_by=None):
    """Split and write out an original NHGIS base-level (block) crosswalk.
    
    Parameters
    ----------
    
    df : pandas.DataFrame
        An original NHGIS base-level (block) crosswalk
    
    endpoint : str
        The column from which unique states should extracted.
    
    fname : str
        Crosswalk (file) name.
    
    fpath : str
        Crosswalk (file) path. Default is ``''``.
    
    sort_by : list
        See ``sort_by`` parameters in ``extract_state``. Default is ``None``.
    
    """

    # extract and sort all unique state FIPS codes
    code = fname[-2:]
    unique_stfips = extract_unique_stfips(df=df, endpoint=endpoint, code=code)
    unique_stfips = list(unique_stfips)
    unique_stfips.sort()

    # iterate over each unique state FIPS code
    for stfips in unique_stfips:
        # create a subset for each endpoint (source/target) state
        stdf = extract_state(df, stfips, fname, endpoint, code=code, sort_by=sort_by)
        xwalk_name = fname + "_" + stfips
        # write the subset to a zipped .csv
        dfkwds = {"df": stdf, "stfips": stfips, "xwalk_name": xwalk_name}
        xwalk_df_to_csv(dfkwds=dfkwds, path=fpath)
