"""IPUMS/NHGIS Census Crosswalk and Atom Generator
"""


from .identifiers import str_types, get_context, code_cols
from .identifiers import bgp_id, trt_id, id_from
from .codes import code_desc_1990_blk, desc_code_1990_blk

import numpy
import pandas


__all__ = ["GeoCrossWalk", "calculate_atoms"]


# stuff from data prep as class here...


class GeoCrossWalk:
    """
    
    
    Parameters
    ----------
    
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
    
    code : str
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
    
    
    Methods
    -------
    
    
    
    """

    def __init__(
        self,
        source_year=None,
        target_year=None,
        source_geo=None,
        target_geo=None,
        input_var=None,
        xwalk_base_y1=None,
        xwalk_base_y2=None,
        code=None,
        stfips=None,
        nhgis=True,
        write_xwalk=None,  ###############################################################
        write_atoms=None,  ###############################################################
        weight="WEIGHT",
    ):
        """
        
        
        
        """

        # set class attributes
        self.source_year, self.target_year = source_year, target_year
        self.source_geo, self.target_geo = source_geo, target_geo

        # Perform step one
        self.step_one()

        # Perform step two
        self.step_two()

        # Perform step three
        self.step_three()

        # Perform step four
        self.step_four()

        # method for atom to returns dataframe ----- atoms ARE crosswalk -- see Jonathan notes....

    def step_one(self):
        """Read in base crosswalk, prepare, and subset (if needed)"""

        pass

    def step_two():
        """Read in and join year 1 tabular data to crosswalk."""  ######################### step 2(1) from data_generator

        pass

    def step_three():
        """Prepare and add year 1 (source) ID to crosswalk."""  ######################### step 2(2) from data_generator

        pass

    def step_four():
        """Calculate atomic crosswalk."""

        pass

    @staticmethod
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
        toy_df = pandas.DataFrame(columns=cols)
        for cn, cd in zip(cols, col_data):
            toy_df[cn] = cd
        return toy_df


# To Do ----- v0.0.1
#
# ID generator: -- blk_id, bkg_id, cty_id...
#
# API structure
#   -- only import the class here

# switch class!

# base.py

# from .base import GeoXwalk


# atom calculator as a method in GeoXwalk

#


def calculate_atoms(
    df, weight=None, input_var=None, sum_var=None, source_id=None, groupby_cols=None
):
    """ Calculate the atoms (intersecting parts) of census geographies.
    
    Parameters
    ----------
    
    df : pandas.DataFrame
        input data
    
    weight : str
        weight colum name
    
    input_var : str or iterable
        input variable column name
    
    sum_var : str or iterable
        groupby and summed variable column name
    
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

    if type(input_var) == str:
        input_var = [input_var]
    if type(sum_var) == str:
        sum_var = [sum_var]

    # iterate over each pair of input/interpolation variables
    for ivar, svar in zip(input_var, sum_var):
        # calculate numerators
        df[svar] = df[weight] * df[ivar]
        df = df.groupby(groupby_cols)[svar].sum().to_frame()
        df.reset_index(inplace=True)

        # calculate denominators
        denominators = df.groupby(source_id)[svar].sum()

        # interpolate weights
        df[svar] = df[svar] / df[source_id].map(denominators)

    return df
