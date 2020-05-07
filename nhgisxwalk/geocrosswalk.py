"""IPUMS/NHGIS Census Crosswalk and Atom Generator
"""


from .id_codes import code_cols, bgp_id, trt_id, id_from, id_code_components

import numpy
import pandas


# used to fetch/vectorize ID generation fucntions
id_generators = {f.__name__: f for f in [bgp_id, trt_id]}


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
        Base-level crosswalk containing composite atoms of smallest units
        to build larger crosswalk atoms of larger source and target units.
    
    source_year : str
        Census source units year.
    
    target_year : str
        Census target units year.
    
    source_geo : str
        Census source geographic units.
    
    target_geo : str
        Census target geographic units.
    
    base_source_geo : str
        base-level crosswalk's source geographic units.
    
    base_source_table : str
        path to the source year's base tabular data
    
    input_var : str or iterable
        ....
    
    xwalk_base_y1 : str
        ....
    
    xwalk_base_y2 : str
        ....
    
    code_type : str
        ....
    
    stfips : str
        ....
    
    nhgis : str
        ....
    
    write_xwalk : str
        ...
    
    write_atoms : str
        ...
    
    weight : str
        ....
    
    keep_base : bool
        Keep the base crosswalk when building of the atomic crosswalk
        is complete (True). Default is False.
    
    Attributes
    ----------
    
    source : str
        ...
    
    target : str
        ...
    
    xwalk_name : str
        ...
    
    xwalk : str
        ...
    
    wt : str
        see `weight` parameter
    
    nhgis : bool
        see `code_type` parameter
    
    source_id_components : pandas.DataFrame
        ...
    
    target_id_components : pandas.DataFrame
        ...
    
    
    Notes
    -----
    
    
    Examples
    --------
    
    Instantiate the example data.
    
    >>> import nhgisxwalk
    >>> df = nhgisxwalk.example_crosswalk_data()
    >>> df
      bgp1990 blk1990 blk2010 trt2010   wt  pop_1990  hh_1990
    0       A     A.1     X.1       X  1.0      60.0     25.0
    1       A     A.2     X.2       X  0.3     100.0     40.0
    2       A     A.2     Y.1       Y  0.7     100.0     40.0
    3       B     B.1     X.3       X  1.0      50.0     20.0
    4       B     B.2     Y.2       Y  1.0      80.0     30.0
    
    
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
        else:
            self.code_label = "GEOID"
            self.tabular_code_label = code_label
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
        self.generate_source_ids()

        # add target geographic unit ID to the base crosswalk
        self.generate_target_ids()

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
        """subset a national crosswalk to state-level (within target year)."""

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

        # do left merge
        self.base = pandas.merge(
            left=self.base,
            right=tab_df,
            how="left",
            left_on=self.base_source_col,
            right_on=self.tabular_code_label,
            validate="many_to_many",
        )

    def generate_source_ids(self):
        """Add source geographic unit ID to the base crosswalk."""
        cols = code_cols(self.source_geo, self.source_year)
        if self.source_geo == "blk":
            raise AttributeError()
        elif self.source_geo == "bgp":
            func = bgp_id
        elif self.source_geo == "bkg":
            raise AttributeError()
        elif self.source_geo == "trt":
            raise AttributeError()
        elif self.source_geo == "cty":
            raise AttributeError()
        else:
            raise AttributeError()
        # generate source geographic ID
        self.base = func(self.base, cols, cname=self.source, nhgis=self.nhgis)

    def generate_target_ids(self):
        """Add target geographic unit ID to the base crosswalk."""
        func = id_generators["%s_id" % self.target_geo]
        self.base[self.target] = id_from(
            func, self.target_year, self.base[self.base_target_col]
        )

    def xwalk_to_file(self, loc="", fext=".csv.zip"):
        """Write the produced crosswalk to .csv."""
        if self.stfips:
            self.xwalk_name += "_" + self.stfips
        self.xwalk.to_csv(loc + self.xwalk_name + fext)

    @staticmethod
    def xwalk_from_file(fname, fext=".csv.zip"):
        """Write the produced crosswalk to .csv."""
        xwalk = pandas.read_csv(fname + fext)
        return xwalk


def calculate_atoms(
    df,
    weight=None,
    input_var=None,
    weight_var=None,
    weight_prefix=None,
    source_id=None,
    groupby_cols=None,
):
    """ Calculate the atoms (intersecting parts) of census geographies and
    interpolate a "weight" of the source attribute that lies within the
    target geography.
    
    Parameters
    ----------
    
    df : pandas.DataFrame
        input data
    
    weight : str
        weight colum name(s)
    
    input_var : str or iterable
        input variable column name(s)
    
    weight_var : str or iterable
        groupby and summed variable column name(s)
    
    weight_prefix : str
        Prepend this prefix to the the `weight_var` column name.
    
    source_id : str
        Source ID column name.
    
    groupby_cols : list
        dataframe columns to perform groupby
    
    Returns
    -------
    
    atoms : pandas.DataFrame
        all intersections between source and target geographies, and 
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
