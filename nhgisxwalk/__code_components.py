# This file is part of the Minnesota Population Center's NHGISXWALK.
# For copyright and licensing information, see the NOTICE and LICENSE files
# in this project's top-level directory, and also on-line at:
#   https://github.com/ipums/nhgisxwalk

"""
The variables here provide raw-string descriptions for columns in the
'context cookbooks' provided with NHGIS data downloads. These are used to
create pandas.DataFrame objects in code_components.CodeComponents().
"""

# ------------------------------------------------------------------------- 1990
blk1990 = r"""
GISJOIN,     GIS Join Match Code
YEAR,        Data File Year
ANRCA,       Alaska Native Regional Corporation Code
AIANHHA,     American Indian Area/Alaska Native Area/Hawaiian Home Land Code
RES_ONLYA,   American Indian Reservation [excluding trust lands] Code
TRUSTA,      American Indian Reservation [trust lands only] Code
RES_TRSTA,   Reservation/Trust Lands Code
BLOCKA,      Block Code
BLCK_GRPA,   Block Group Code
TRACTA,      Census Tract Code
CD101A,      Congressional District (101st) Code
C_CITYA,     Consolidated City Code
COUNTY,      County Name
COUNTYA,     County Code
CTY_SUBA,    County Subdivision Code
DIVISIONA,   Division Code
MSA_CMSAA,   Metropolitan Statistical Area/Consolidated Metropolitan Statistical Area Code
PLACEA,      Place Code
PMSAA,       Primary Metropolitan Statistical Area Code
REGIONA,     Region Code
STATE,       State Name
STATEA,      State Code
URBRURALA,   Urban/Rural Code
URB_AREAA,   Urban Area Code
CD103A,      Congressional District (103rd) Code
ANPSADPI,    Area Name/PSAD Term/Part Indicator"""  # noqa E501

bgp1990 = r"""
GISJOIN,     GIS Join Match Code
YEAR,        Data File Year
ANRCA,       Alaska Native Regional Corporation Code
AIANHH,      American Indian Area/Alaska Native Area/Hawaiian Home Land Name
AIANHHA,     American Indian Area/Alaska Native Area/Hawaiian Home Land Code
RES_ONLYA,   American Indian Reservation [excluding trust lands] Code
TRUSTA,      American Indian Reservation [trust lands only] Code
RES_TRSTA,   Reservation/Trust Lands Code
BLOCKA,      Block Code
BLCK_GRPA,   Block Group Code
TRACTA,      Census Tract Code
CD101A,      Congressional District (101st) Code
C_CITYA,     Consolidated City Code
COUNTY,      County Name
COUNTYA,     County Code
CTY_SUB,     County Subdivision Name
CTY_SUBA,    County Subdivision Code
DIVISIONA,   Division Code
MSA_CMSAA,   Metropolitan Statistical Area/Consolidated Metropolitan Statistical Area Code
PLACE,       Place Name
PLACEA,      Place Code
PMSAA,       Primary Metropolitan Statistical Area Code
REGIONA,     Region Code
STATE,       State Name
STATEA,      State Code
URBRURALA,   Urban/Rural Code
URB_AREA,    Urban Area Name
URB_AREAA,   Urban Area Code
CD103A,      Congressional District (103rd) Code
ANPSADPI,    Area Name/PSAD Term/Part Indicator"""  # noqa E501

bg1990 = r"""
"""

tr1990 = r"""
"""

co1990 = r"""
"""

# ------------------------------------------------------------------------- 2000
# *** NOTE *** The URBRURALA code is added. For more details see,
# https,//gist.github.com/ipums/36c7640af1f228cdc8a691505262e543
blk2000 = r"""
GISJOIN,     GIS Join Match Code
YEAR,        Data File Year
STATE,       State Name
STATEA,      State Code
COUNTY,      County Name
COUNTYA,     County Code
CTY_SUBA,    County Subdivision Code
PLACEA,      Place Code
TRACTA,      Census Tract Code
BLCK_GRPA,   Block Group Code
BLOCKA,      Block Code
AIANHHA,     American Indian Area/Alaska Native Area/Hawaiian Home Land Code
URBRURALA,   Urban/Rural Code
NAME,        Area Name-Legal/Statistical Area Description (LSAD) Term-Part Indicator"""  # noqa E501

bgp2000 = r"""
GISJOIN,     GIS Join Match Code
YEAR,        Data File Year
STATE,       State Name
STATEA,      State Code
COUNTY,      County Name
COUNTYA,     County Code
CTY_SUB,     County Subdivision Name
CTY_SUBA,    County Subdivision Code
PLACE,       Place Name
PLACEA,      Place Code
TRACTA,      Census Tract Code
BLCK_GRPA,   Block Group Code
AIANHHA,     American Indian Area/Alaska Native Area/Hawaiian Home Land Code
URBRURALA,   Urban/Rural Code
NAME,        Area Name-Legal/Statistical Area Description (LSAD) Term-Part Indicator"""

bg2000 = r"""
"""

tr2000 = r"""
"""

co2000 = r"""
"""


# ------------------------------------------------------------------------- 2010
blk2010 = r"""
"""

bgp2010 = r"""
"""

bg2010 = r"""
GISJOIN,     GIS Join Match Code
YEAR,        Data File Year
REGIONA,     Region Code
DIVISIONA,   Division Code
STATE,       State Name
STATEA,      State Code
COUNTY,      County Name
COUNTYA,     County Code
COUSUBA,     County Subdivision Code
PLACEA,      Place Code
TRACTA,      Census Tract Code
BLKGRPA,     Block Group Code
CONCITA,     Consolidated City Code
AIANHHA,     American Indian Area/Alaska Native Area/Hawaiian Home Land Code
RES_ONLYA,   American Indian Area/Alaska Native Area (Reservation or Statistical Entity Only) Code
TRUSTA,      American Indian Reservation with Trust Lands; trust lands only Code
AITSCEA,     Tribal Subdivision/Remainder Code
ANRCA,       Alaska Native Regional Corporation Code
CBSAA,       Metropolitan Statistical Area/Micropolitan Statistical Area Code
CSAA,        Combined Statistical Area Code
METDIVA,     Metropolitan Division Code
NECTAA,      New England City and Town Area Code
CNECTAA,     Combined New England City and Town Area Code
NECTADIVA,   New England City and Town Area Division Code
UAA,         Urban Area Code
CDCURRA,     Congressional District (111th Congress) Code
SLDUA,       State Legislative District (Upper Chamber) Code
SLDLA,       State Legislative District (Lower Chamber) Code
SUBMCDA,     Subminor Civil Division Code
SDELMA,      School District (Elementary)/Remainder Code
SDSECA,      School District (Secondary)/Remainder Code
SDUNIA,      School District (Unified)/Remainder Code
PUMA5A,      Public Use Microdata Sample Area (PUMA) Code
BTTRA,       Tribal Census Tract Code
BTBGA,       Tribal Block Group Code
"""  # noqa E501

tr2010 = r"""
GISJOIN,     GIS Join Match Code
YEAR,        Data File Year
REGIONA,     Region Code
DIVISIONA,   Division Code
STATE,       State Name
STATEA,      State Code
COUNTY,      County Name
COUNTYA,     County Code
COUSUBA,     County Subdivision Code
PLACEA,      Place Code
TRACTA,      Census Tract Code
BLKGRPA,     Block Group Code
CONCITA,     Consolidated City Code
AIANHHA,     American Indian Area/Alaska Native Area/Hawaiian Home Land Code
RES_ONLYA,   American Indian Area/Alaska Native Area (Reservation or Statistical Entity Only) Code
TRUSTA,      American Indian Reservation with Trust Lands; trust lands only Code
AITSCEA,     Tribal Subdivision/Remainder Code
ANRCA,       Alaska Native Regional Corporation Code
CBSAA,       Metropolitan Statistical Area/Micropolitan Statistical Area Code
CSAA,        Combined Statistical Area Code
METDIVA,     Metropolitan Division Code
NECTAA,      New England City and Town Area Code
CNECTAA,     Combined New England City and Town Area Code
NECTADIVA,   New England City and Town Area Division Code
UAA,         Urban Area Code
CDCURRA,     Congressional District (111th Congress) Code
SLDUA,       State Legislative District (Upper Chamber) Code
SLDLA,       State Legislative District (Lower Chamber) Code
SUBMCDA,     Subminor Civil Division Code
SDELMA,      School District (Elementary)/Remainder Code
SDSECA,      School District (Secondary)/Remainder Code
SDUNIA,      School District (Unified)/Remainder Code
PUMA5A,      Public Use Microdata Sample Area (PUMA) Code
BTTRA,       Tribal Census Tract Code
BTBGA,       Tribal Block Group Code"""  # noqa E501

co2010 = r"""
GISJOIN,     GIS Join Match Code
YEAR,        Data File Year
REGIONA,     Region Code
DIVISIONA,   Division Code
STATE,       State Name
STATEA,      State Code
COUNTY,      County Name
COUNTYA,     County Code
COUSUBA,     County Subdivision Code
PLACEA,      Place Code
TRACTA,      Census Tract Code
BLKGRPA,     Block Group Code
BLOCKA,      Block Code
CONCITA,     Consolidated City Code
AIANHHA,     American Indian Area/Alaska Native Area/Hawaiian Home Land Code
RES_ONLYA,   American Indian Reservation with Trust Lands; reservation only Code
TRUSTA,      American Indian Reservation with Trust Lands; trust lands only Code
AITSCEA,     Tribal Subdivision/Remainder Code
TTRACTA,     Tribal Census Tract Code
TBLKGRPA,    Tribal Block Group Code
ANRCA,       Alaska Native Regional Corporation Code
CBSAA,       Metropolitan Statistical Area/Micropolitan Statistical Area Code
METDIVA,     Metropolitan Division Code
CSAA,        Combined Statistical Area Code
NECTAA,      New England City and Town Area Code
NECTADIVA,   NECTA Division Code
CNECTAA,     Combined New England City and Town Area Code
UAA,         Urban Area Code
URBRURALA,   Urban/Rural Code
CDA,         Congressional District (111th Congress) Code
SLDUA,       State Legislative District (Upper Chamber) Code
SLDLA,       State Legislative District (Lower Chamber) Code
ZCTA5A,      5-Digit Zip Code Tabulation Area Code
SUBMCDA,     Subminor Civil Division Code
SDELMA,      School District (Elementary)/Remainder Code
SDSECA,      School District (Secondary)/Remainder Code
SDUNIA,      School District (Unified)/Remainder Code
NAME,        Area Name-Legal/Statistical Area Description (LSAD) Term-Part Indicator
SABINSA,     School Attendance Area Code
"""
