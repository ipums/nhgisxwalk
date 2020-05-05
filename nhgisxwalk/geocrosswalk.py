"""IPUMS/NHGIS Census Crosswalk and Atom Generator
"""


from .identifiers import str_types, get_context, code_cols
from .identifiers import bgp_id, trt_id, id_from
from .codes import code_desc_1990_blk, desc_code_1990_blk

import numpy
import pandas


__all__ = ["GeoCrossWalk"]


# stuff from data prep as class here...


class GeoCrossWalk:
    """
    
    
    Parameters
    ----------
    
    
    
    
    
    Attributes
    ----------
    
    
    Methods
    -------
    
    
    
    """

    def __init__(
        self,
        y1=None,
        y2=None,
        y1geo=None,
        y2geo=None,
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

        pass

        # set class attributes

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
