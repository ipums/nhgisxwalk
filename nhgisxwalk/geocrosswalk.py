"""IPUMS/NHGIS Census Crosswalk and Atom Generator


TO DO:

    * v0.0.2
        * 1990 BGP SF1 file for **ALL** BGP IDS...
        * ID generator: -- blk_id, bkg_id, cty_id...

"""


from .id_codes import bgp_id, trt_id, id_from, id_code_components
from .id_codes import code_cols, _add_ur_code_blk2000

import numpy
import pandas

import pickle


# used to fetch/vectorize ID generation functions
id_generator_funcs = [
    # blk_id,
    bgp_id,
    # bkg_id,
    trt_id,
    # cty_id
]
id_generators = {f.__name__: f for f in id_generator_funcs}


class GeoCrossWalk:
    """ Generate a temporal crosswalk for census geography data and 
    built from the smallest intersecting units (atoms). Each row in
    a crosswalk represents a single atom, and comprised of a source
    ID (geo+year), and target ID (geo+year), and at least one column
    of weights. The weights are the interpolated proportions of source
    attributes that are are calculated as being within the target units.
    
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
    
    code_type : str
        Either ``gj`` for the GISJOIN (NHGIS) code formatting or ``ge`` for
        the original census GEOID code formatting. Default is ``gj``. For more
        information see the specifics of the
        `technical details <https://www.nhgis.org/user-resources/geographic-crosswalks#details>`_.
    
    stfips : str
        If a state-level subset is desired, set the state FIPS code.
    
    weight : str
        The column tags to use for the atomic interpolated variables.
    
    keep_base : bool
        Keep the base crosswalk when building of the atomic crosswalk
        is complete (``True``). Default is ``False``.
    
    vectorized : bool
        Vectorize the ``id_codes.id_from()`` function for (potential)
        speedups (``True``). Default is ``True``.
    
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
    
    nhgis : bool
        See the ``code_type`` parameter.
    
    source_id_components : pandas.DataFrame
        The ``source`` result from ``id_codes.id_code_components()``.
    
    target_id_components : pandas.DataFrame
        The ``target`` result from ``id_codes.id_code_components()``.
    
    Notes
    -----
    
    For more information see the ``nhgisxwalk`` FAQ
    `page <https://github.com/jGaboardi/nhgisxwalk/wiki/FAQ-&-Resources>`_.
    
    Examples
    --------
    
    Ex. 1: Instantiate the example data and calculate an atomic crosswalk.
    
    >>> import nhgisxwalk
    >>> df = nhgisxwalk.example_crosswalk_data()
    >>> df
      bgp1990 blk1990 blk2010 trt2010   wt  pop_1990  hh_1990
    0       A     A.1     X.1       X  1.0      60.0     25.0
    1       A     A.2     X.2       X  0.3     100.0     40.0
    2       A     A.2     Y.1       Y  0.7     100.0     40.0
    3       B     B.1     X.3       X  1.0      50.0     20.0
    4       B     B.2     Y.2       Y  1.0      80.0     30.0
    
    This synthetic data is comprised of 1990 and 2010 census blocks (``blk1990``
    and ``blk2010``, respectively); the base atomic crosswalk. Since the
    boundaries of census blocks are subject to change over time, the 1990
    blocks don't nest perfectly in the 2010 blocks. The magnitude of this
    imperfect nesting is represented in the weight column (``wt``), which
    records the areal portion of the 1990 block that intersects with the 2010
    blocks. Further, the population and household counts for the 1990 blocks
    are available through the ``pop_1990`` and ``hh_1990`` columns.
    Finally, the associated 1990 census block group parts and the 2010 census
    tracts are also represented with ``bgp1990`` and ``trt2010``. With this 
    information it is possible to create a (synthetic) 1990 block group part
    to 2010 tract crosswalk.
    
    >>> atoms = nhgisxwalk.calculate_atoms(
    ...             df,
    ...             weight="wt",
    ...             input_var=["pop_1990", "hh_1990"],
    ...             weight_var=["pop", "hh"],
    ...             weight_prefix="wt_",
    ...             source_id="bgp1990",
    ...             groupby_cols=["bgp1990", "trt2010"]
    ...         )
    >>> atoms
      bgp1990 trt2010    wt_pop     wt_hh
    0       A       X  0.562500  0.569231
    1       A       Y  0.437500  0.430769
    2       B       X  0.384615  0.400000
    3       B       Y  0.615385  0.600000
    
    The result is four atomic intersections between the synthetic 1990 census
    block group parts and the 2010 census tracts with varying population
    and household proportional weights.
    
    Ex. 2: Instantiate the example data and calculate atomic crosswalk.
    
    >>> import nhgisxwalk
    
    
    
    
    
    
    
    
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
        code_type="gj",
        base_weight="WEIGHT",
        weight_prefix="wt_",
        keep_base=False,
        vectorized=True,
    ):

        # Set class attributes -------------------------------------------------
        # source and target class attributes
        self.source_year, self.target_year = source_year, target_year
        self.source_geo, self.target_geo = source_geo, target_geo
        # source and target names
        self.source = self.source_geo + self.source_year
        self.target = self.target_geo + self.target_year
        self.xwalk_name = "%s_to_%s" % (self.source, self.target)
        # input, summed, and weight variable names
        self.input_var, self.weight_var = input_var, weight_var
        self.base_weight = base_weight
        self.wt = weight_prefix
        # set for gj (nhgis ID) vs. ge (census ID)
        self.code_type = code_type
        self.nhgis = True if self.code_type == "gj" else False
        if self.code_type == "gj":
            self.code_label = "GJOIN"
            self.tabular_code_label = "GISJOIN"
        elif self.code_type == "ge":
            self.code_label = "GEOID"
            self.tabular_code_label = self.code_label
            msg = "%s functionality is not currently supported." % self.code_label
            raise RuntimeError(msg)
        else:
            msg = "%s is not a recognized `code_type`." % self.code_type
            raise RuntimeError(msg)
        # source geographies within the base crosswalk
        self.base_source_geo = base_source_geo
        # columns within the base crosswalk
        self.base_source_col = self.code_label + self.source_year
        self.base_target_col = self.code_label + self.target_year
        # path to the tabular data for the base source units
        self.base_source_table = base_source_table

        # if creating a single state subset
        self.stfips = stfips

        # Prepare base for output crosswalk ------------------------------------
        self.base = base
        # initial subset of national base crosswalk to target state (if desired)
        if self.stfips:
            self.subset_target_to_state()

        # fetch all components of that constitute various geographic IDs
        self.fetch_id_code_components()

        # join the (base) source tabular data to the base crosswalk
        self.join_source_base_tabular()

        # add source geographic unit ID to the base crosswalk
        self.generate_ids("source", vectorized)

        # add target geographic unit ID to the base crosswalk
        self.generate_ids("target", vectorized)

        # Create atomic crosswalk
        # calculate the source to target atom values
        self.xwalk = calculate_atoms(
            self.base,
            weight=self.base_weight,
            input_var=self.input_var,
            weight_var=self.weight_var,
            weight_prefix=self.wt,
            source_id=self.source,
            groupby_cols=[self.source, self.target],
        )

        # discard building base if not needed
        if not keep_base:
            del self.base

    def subset_target_to_state(self):
        """Subset a national crosswalk to state-level (within target year)."""

        def _state(rec):
            """Slice out a particular state by FIPS code."""
            return rec[1:3] == self.stfips

        self.base = self.base[self.base[self.base_target_col].map(lambda x: _state(x))]

    def fetch_id_code_components(self):
        """Fetch dataframe that describes each component of a geographic unit ID."""
        self.base_source_id_components = id_code_components(
            self.source_year, self.base_source_geo
        )
        self.source_id_components = id_code_components(
            self.source_year, self.source_geo
        )
        self.target_id_components = id_code_components(
            self.target_year, self.target_geo
        )

    def join_source_base_tabular(self):
        """Join tabular attributes to base crosswalk."""

        # read in national tabular data
        data_types = str_types(self.base_source_id_components["Variable"])
        tab_df = pandas.read_csv(self.base_source_table, dtype=data_types)

        # special case for 2000 blocks (of 2000 bgp)-- needs Urban/Rural code
        if self.base_source_geo == "blk" and self.source == "bgp2000":
            tab_df = _add_ur_code_blk2000(tab_df)

        # do left merge
        self.base = pandas.merge(
            left=self.base,
            right=tab_df,
            how="left",
            left_on=self.base_source_col,
            right_on=self.tabular_code_label,
            validate="many_to_many",
        )

    def generate_ids(self, id_type, vect):
        """Add source or target geographic unit ID to the base crosswalk."""

        # declare id type-specific variables
        if id_type == "source":
            cname, year = self.source, self.source_year
            geog, base_col = self.source_geo, self.base_source_col
        else:
            cname, year = self.target, self.target_year
            geog, base_col = self.target_geo, self.base_target_col
        # generate IDS
        if geog == "bgp":
            cols, func = code_cols(geog, year), bgp_id
            args = self.base, cols
            self.base = func(*args, cname=cname, nhgis=self.nhgis)
        else:
            if id_type == "source" and geog == "blk":
                raise AttributeError()
            func = id_generators["%s_id" % geog]
            args = func, year, self.base[base_col], self.nhgis, vect
            self.base[cname] = id_from(*args)

    def xwalk_to_csv(self, loc="", fext=".zip"):
        """Write the produced crosswalk to .csv.zip."""
        if self.stfips:
            self.xwalk_name += "_" + self.stfips
        self.xwalk.to_csv(loc + self.xwalk_name + ".csv" + fext)

    def xwalk_to_pickle(self, loc="", fext=".pkl"):
        """Write the produced ``GeoCrossWalk`` object."""
        if self.stfips:
            self.xwalk_name += "_" + self.stfips
        with open(self.xwalk_name + fext, "wb") as pkl_xwalk:
            pickle.dump(self, pkl_xwalk, protocol=2)

    @staticmethod
    def xwalk_from_csv(fname, fext=".zip"):
        """Read in a produced crosswalk from .csv.zip."""
        xwalk = pandas.read_csv(fname + ".csv" + fext)
        return xwalk

    @staticmethod
    def xwalk_from_pickle(fname, fext=".pkl"):
        """Read in a produced crosswalk from a pickled ``GeoCrossWalk``."""
        with open(fname + fext, "rb") as pkl_xwalk:
            self = pickle.load(pkl_xwalk)
        return self


def calculate_atoms(
    df,
    weight=None,
    input_var=None,
    weight_var=None,
    weight_prefix=None,
    source_id=None,
    groupby_cols=None,
):
    """ Calculate the atoms (intersecting parts) of census geographies
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
    
    Returns
    -------
    
    atoms : pandas.DataFrame
        All intersections between ``source`` and ``target`` geographies, and 
        the interpolated weight calculations for the propotion of
        source area attributes that are in the target area.
    
    """

    if type(input_var) == str:
        input_var = [input_var]
    if type(weight_var) == str:
        weight_var = [weight_var]

    n_input_var, n_weight_var = len(input_var), len(weight_var)

    if n_input_var != n_weight_var:
        msg = "The 'input_var' and 'weight_var' should be the same length. "
        msg += "%s != %s" % (n_input_var, n_weight_var)
        raise RuntimeError(msg)

    if weight_prefix:
        weight_var = [weight_prefix + wvar for wvar in weight_var]

    # iterate over each pair of input/interpolation variables
    for ix, (ivar, wvar) in enumerate(zip(input_var, weight_var)):

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


def str_types(var_names):
    """String-type formatting for ID characters."""
    dtype = {c: str for c in var_names}
    return dtype


def valid_geo_shorthand(shorthand_name=True):
    """Shorthand lookups for census geographies."""
    lookup = {
        "blk": "block",
        "bgp": "block group part",
        "bkg": "block group",
        "trt": "tract",
        "cty": "county",
    }
    if not shorthand_name:
        lookup = {v: k for k, v in lookup.items()}
    return lookup


def example_crosswalk_data():
    """Create an example dataframe to demonstrate atom generation."""
    cols = ["bgp1990", "blk1990", "blk2010", "trt2010", "wt", "pop_1990", "hh_1990"]
    bgp1990 = ["A", "A", "A", "B", "B"]
    blk1990 = ["A.1", "A.2", "A.2", "B.1", "B.2"]
    blk2010 = ["X.1", "X.2", "Y.1", "X.3", "Y.2"]
    trt2010 = ["X", "X", "Y", "X", "Y"]
    wt = [1.0, 0.3, 0.7, 1.0, 1.0]
    pop_1990 = [60.0, 100.0, 100.0, 50.0, 80.0]
    hh_1990 = [25.0, 40.0, 40.0, 20.0, 30.0]
    col_data = [bgp1990, blk1990, blk2010, trt2010, wt, pop_1990, hh_1990]
    example_data = pandas.DataFrame(columns=cols)
    for cn, cd in zip(cols, col_data):
        example_data[cn] = cd
    return example_data
