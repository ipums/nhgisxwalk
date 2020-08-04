__version__ = "0.0.8"
"""
:mod:`nhgisxwalk` --- IPUMS/NHGIS Census Crosswalk and Atom Generator
=====================================================================
"""

__author__ = "James Gaboardi <jgaboardi@gmail.com>"
__date__ = "2020-04"


from .geocrosswalk import GeoCrossWalk
from .geocrosswalk import calculate_atoms, round_weights, str_types
from .geocrosswalk import valid_geo_shorthand, example_crosswalk_data
from .geocrosswalk import prepare_data_product, generate_data_product
from .geocrosswalk import xwalk_df_to_csv, xwalk_df_from_csv
from .geocrosswalk import extract_state, extract_unique_stfips
from .geocrosswalk import regenerate_blk_blk_xwalk, split_blk_blk_xwalk
from .geocrosswalk import SORT_PARAMS, SORT_BYS
from .geocrosswalk import ID_COLS, CSV, ZIP, TXT, W, R

from .variable_codes import code_desc_1990, desc_code_1990
from .variable_codes import code_desc_2000_SF1b, desc_code_2000_SF1b
from .variable_codes import code_desc_2000_SF3b, desc_code_2000_SF3b
