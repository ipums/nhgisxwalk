__version__ = "0.0.1"
"""
:mod:`nhgisxwalk` --- IPUMS/NHGIS Census Crosswalk and Atom Generator
====================================================================
"""
__author__ = "James Gaboardi <jgaboardi@gmail.com>"
__date__ = "2020-04"


from .geocrosswalk import GeoCrossWalk, calculate_atoms


# from .identifiers import str_types, get_context, code_cols
# from .identifiers import bgp_id, trt_id, id_from
# from .codes import code_desc_1990_blk, desc_code_1990_blk


# To Do ----- v0.0.1
#
# ID generator: -- blk_id, bkg_id, cty_id...
#
# API structure
#   -- only import the class here
