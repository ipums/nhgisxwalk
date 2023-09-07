"""
# `nhgisxwalk` --- IPUMS/NHGIS Census Crosswalk and Atom Generator

# This file is part of the Minnesota Population Center's NHGISXWALK.
# For copyright and licensing information, see the NOTICE and LICENSE files
# in this project's top-level directory, and also on-line at:
#   https://github.com/ipums/nhgisxwalk

"""

__author__ = "James Gaboardi <jgaboardi@gmail.com>"
__date__ = "2020-04"


import contextlib
from importlib.metadata import PackageNotFoundError, version

from .geocrosswalk import (
    CSV,
    ID_COLS,
    SORT_BYS,
    SORT_PARAMS,
    TXT,
    ZIP,
    GeoCrossWalk,
    calculate_atoms,
    example_crosswalk_data,
    extract_state,
    extract_unique_stfips,
    generate_data_product,
    prepare_data_product,
    regenerate_blk_blk_xwalk,
    round_weights,
    split_xwalk,
    str_types,
    valid_geo_shorthand,
    xwalk_df_from_csv,
    xwalk_df_to_csv,
)
from .variable_codes import (
    code_desc_1990,
    code_desc_2000_SF1b,
    code_desc_2000_SF3b,
    desc_code_1990,
    desc_code_2000_SF1b,
    desc_code_2000_SF3b,
)

with contextlib.suppress(PackageNotFoundError):
    __version__ = version("nhgisxwalk")
