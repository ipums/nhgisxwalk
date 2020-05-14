__version__ = "0.0.2"
"""
:mod:`nhgisxwalk` --- IPUMS/NHGIS Census Crosswalk and Atom Generator
=====================================================================
"""

__author__ = "James Gaboardi <jgaboardi@gmail.com>"
__date__ = "2020-04"


from .geocrosswalk import GeoCrossWalk
from .geocrosswalk import calculate_atoms, str_types
from .geocrosswalk import valid_geo_shorthand, example_crosswalk_data

from .variable_codes import code_desc_1990, desc_code_1990
from .variable_codes import code_desc_2000_SF1b, desc_code_2000_SF1b
from .variable_codes import code_desc_2000_SF3b, desc_code_2000_SF3b
