"""IPUMS/NHGIS Census Crosswalk and Atom Generator
"""


from .id_codes import code_cols, bgp_id, trt_id, id_from, id_code_components


# from .identifiers import str_types, get_context, code_cols
# from .identifiers import bgp_id, trt_id, id_from
# from .codes import code_desc_1990_blk, desc_code_1990_blk

import numpy
import pandas


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
    
    xwalk_base : pandas.DataFrame
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
    
    """

    def __init__(
        self,
        xwalk_base,
        source_year=None,
        target_year=None,
        source_geo=None,
        target_geo=None,
        input_var=None,
        weight_var=None,
        stfips=None,
        code_type="gj",
        weight="wt_",
    ):

        # Set class attributes -------------------------------------------------
        # building base crosswalk
        self.xwalk_base = xwalk_base
        # source and target class attributes
        self.source_year, self.target_year = source_year, target_year
        self.source_geo, self.target_geo = source_geo, target_geo
        # source and target names
        self.source = self.source_geo + self.source_year
        self.target = self.target_geo + self.target_year
        self.xwalk_name = "%s_to_%s" % (self.source, self.target)
        # input, summed, and weight variable names
        self.input_var, self.weight_var = input_var, weight_var
        self.wt = weight_var

        # set for gj (nhgis ID) vs. ge (census ID)
        self.code_type = code_type
        self.nhgis = True if self.code_type == "gj" else False

        # if creating a single state subset
        self.stfips = stfips
        if self.stfips:
            self.subset_target_to_state()

        #
        self.fetch_id_code_components()

        return

        # Perform step one
        self.step_one()

        # Perform step two
        self.step_two()

        # Perform step three
        self.step_three()

        # Perform step four
        self.step_four()

    def subset_target_to_state(self):
        """
        """

    def fetch_id_code_components(self):
        """Fetch dataframe that describes each component of a geographic unit ID."""
        self.source_id_components = id_code_components(
            self.source_year, self.source_geo
        )
        self.target_id_components = id_code_components(
            self.target_year, self.target_geo
        )

    def step_one(self):
        """Read in base crosswalk, prepare, and subset (if needed)"""

    def step_two(self):
        """Read in and join year 1 tabular data to crosswalk."""  ######################### step 2(1) from data_generator

        pass

    def step_three(self):
        """Prepare and add year 1 (source) ID to crosswalk."""  ######################### step 2(2) from data_generator

        pass

    def step_four(self):
        """Calculate atomic crosswalk."""

        pass

    def write_xwalk(self):
        """"""

        pass


# To Do ----- v0.0.1
#
# ID generator: -- blk_id, bkg_id, cty_id...


def calculate_atoms(
    df, weight=None, input_var=None, sum_var=None, source_id=None, groupby_cols=None
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
    
    sum_var : str or iterable
        groupby and summed variable column name(s)
    
    source_id : str
        Source ID column name.
    
    groupby_cols : list
        dataframe columns to perform groupby
    
    Returns
    -------
    
    df : pandas.DataFrame
        atom data (all intersections between source and target geographies)
        -- the "weight" column calculates the propotion of source area
            attributes are in target area.
    
    """

    if type(weight) == str:
        weight = [weight]
    if type(input_var) == str:
        input_var = [input_var]
    if type(sum_var) == str:
        sum_var = [sum_var]

    # iterate over each set of weight/input/interpolation variables
    for w, ivar, svar in zip(weight, input_var, sum_var):
        # calculate numerators
        df[svar] = df[w] * df[ivar]
        df = df.groupby(groupby_cols)[svar].sum().to_frame()
        df.reset_index(inplace=True)

        # calculate denominators
        denominators = df.groupby(source_id)[svar].sum()

        # interpolate weights
        df[svar] = df[svar] / df[source_id].map(denominators)

    return df


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
    cols = ["id_bgp90", "id_bk90", "id_bk10", "id_tract10", "wt", "pop_bk90"]
    id_bgp90 = ["A", "A", "A", "B", "B"]
    id_bk90 = ["A.1", "A.2", "A.2", "B.1", "B.2"]
    id_bk10 = ["X.1", "X.2", "Y.1", "X.3", "Y.2"]
    id_tract10 = ["X", "X", "Y", "X", "Y"]
    wt = [1.0, 0.3, 0.7, 1.0, 1.0]
    pop_bk90 = [60.0, 100.0, 100.0, 50.0, 80.0]
    col_data = [id_bgp90, id_bk90, id_bk10, id_tract10, wt, pop_bk90]
    example_data = pandas.DataFrame(columns=cols)
    for cn, cd in zip(cols, col_data):
        example_data[cn] = cd
    return example_data
