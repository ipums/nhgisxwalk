# ==============================================================================
# 1990
# Code to descriptive lookup
code_desc_1990 = {
    "Persons": {
        "Universe": "Persons",
        "Source code": "NP1",
        "NHGIS code": "ET1",
        "ET1001": "Total",
    },
    "Families": {
        "Universe": "Families",
        "Source code": "NP2",
        "NHGIS code": "EUD",
        "EUD001": "Total",
    },
    "Households": {
        "Universe": "Households",
        "Source code": "NP3",
        "NHGIS code": "EUO",
        "EUO001": "Total",
    },
    "Housing Units": {
        "Universe": "Housing Units",
        "Source code": "NH1",
        "NHGIS code": "ESA",
        "ESA001": "Total",
    },
}
# Descriptive to code lookup
desc_code_1990 = {K: {v: k for k, v in V.items()} for K, V in code_desc_1990.items()}


# ==============================================================================
# 2000
# Code to descriptive lookup ----------------------------- SF1b
code_desc_2000_SF1b = {
    "Persons": {
        "Universe": "Persons",
        "Source code": "NP001A",
        "NHGIS code": "FXS",
        "FXS001": "Total",
    },
    "Families": {
        "Universe": "Families",
        "Source code": "NP031A",
        "NHGIS code": "F2V",
        "F2V001": "Total",
    },
    "Households": {
        "Universe": "Households",
        "Source code": "NP010A",
        "NHGIS code": "FY4",
        "FY4001": "Total",
    },
    "Housing Units": {
        "Universe": "Housing Units",
        "Source code": "NH001A",
        "NHGIS code": "FV5",
        "FV5001": "Total",
    },
    "Population by Urban and Rural": {
        "Universe": "Persons",
        "Source code": "NP002A",
        "NHGIS code": "FXT",
        "FXT001": "Urban",
        "FXT002": "Rural",
        "FXT003": "Not defined for this file",
    },
}

# Descriptive to code lookup
desc_code_2000_SF1b = {
    K: {v: k for k, v in V.items()} for K, V in code_desc_2000_SF1b.items()
}

# Code to descriptive lookup ----------------------------- SF3b
code_desc_2000_SF3b = {
    "Persons": {
        "Universe": "Persons",
        "Source code": "NP001A",
        "NHGIS code": "HAK",
        "HAK001": "Total",
    },
    "Families": {
        "Universe": "Families",
        "Source code": "NP015A",
        "NHGIS code": "HBT",
        "HBT001": "Total",
    },
    "Households": {
        "Universe": "Households",
        "Source code": "NP010A",
        "NHGIS code": "HA2",
        "HA2001": "Total",
    },
    "Housing Units": {
        "Universe": "Housing Units",
        "Source code": "NH001A",
        "NHGIS code": "G5S",
        "G5S001": "Total",
    },
}
# Descriptive to code lookup
desc_code_2000_SF3b = {
    K: {v: k for k, v in V.items()} for K, V in code_desc_2000_SF3b.items()
}


# ==============================================================================
# 2010
# Block Table Breakdown --------------------------------------------------------
# Code to descriptive lookup

# Descriptive to code lookup
