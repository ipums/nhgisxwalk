
#### 1990 Block Table Breakdown ------------------------------------------------
#  Code to descriptive lookup
code_desc_1990_blk = {
    "Persons": {
        "Universe":    "Persons",
        "Source code": "NP1",
        "NHGIS code":  "ET1",
        "ET1001":      "Total"
    },
    "Race": {
        "Universe":    "Persons",
        "Source code": "NP6",
        "NHGIS code":  "EUY",
        "ET1001":      "Total",
        "EUY001":      "White",
        "EUY002":      "Black",
        "EUY003":      "American Indian, Eskimo, or Aleut",
        "EUY004":      "Asian or Pacific Islander",
        "EUY005":      "Other race"
    },
    "Housing Units": {
        "Universe":    "Housing Units",
        "Source code": "NH1",
        "NHGIS code":  "ESA",
        "ET1001":      "Total"
    },
    "Tenure": {
        "Universe":    "Occupied housing units",
        "Source code": "NH3",
        "NHGIS code":  "ES1",
        "ES1001":      "Owner occupied",
        "ES1002":      "Renter occupied"
    }
}
# Descriptive to code lookup
desc_code_1990_blk = {
    K: {v:k for k, v in V.items()} for K, V in code_desc_1990_blk.items()
}
