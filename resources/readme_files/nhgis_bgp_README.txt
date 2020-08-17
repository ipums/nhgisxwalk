--------------------------------------------------------------------------------
Documentation for NHGIS crosswalk files...
    from 1990 or 2000 block group parts...
    to 2010 block groups, census tracts, or counties
--------------------------------------------------------------------------------

Contents
    - Data Summary
    - Zone Identifiers
    - Notes
    - Citation and Use

Additional documentation on NHGIS crosswalks is available at:
    https://www.nhgis.org/user-resources/geographic-crosswalks


--------------------------------------------------------------------------------
Data Summary
--------------------------------------------------------------------------------

Each NHGIS crosswalk file provides interpolation weights for allocating census counts from a 
specified set of source zones to a specified set of target zones.

Crosswalk file naming scheme:
    nhgis_[source level code][source year]_[target level code][target year]{_state FIPS}.csv

Geographic level codes:
    blk - Block
    bgp - Block group part (intersections between block groups, places, county subdivisions, etc.)
            - 1990 NHGIS level ID: blck_grp_598
            - 2000 NHGIS level ID: blck_grp_090
    bg  - Block group
    tr  - Census tract
    co  - County

Crosswalk file content:
	- The top row is a header row
	- Each subsequent row represents a spatial intersection (an "atom") between a source block group 
      part and a target zone
    - Fields:
        bgp1990gj OR bgp2000gj:           NHGIS standard GISJOIN identifier for the source block 
                                          group part. (See specifications below.)
        bg2010gj, tr2010gj OR co2010gj:   NHGIS standard GISJOIN identifier for the 2010 target 
                                          zone. (See specifications below.)
        bg2010ge, tr2010ge OR co2010ge:   Census Bureau standard GEOID identifier for the 2010 
                                          target zone. (See specifications below.)
        wt_pop:     Interpolation weight, total population
                    (Expected proportion of source zone's population located in target zone)
        wt_fam:     Interpolation weight, total families
                    (Expected proportion of source zone's families located in target zone)
        wt_hh:      Interpolation weight, total households
                    (Expected proportion of source zone's households located in target zone)
        wt_hu:      Interpolation weight, total housing units
                    (Expected proportion of source zone's housing units located in target zone)


--------------------------------------------------------------------------------
Zone Identifiers
--------------------------------------------------------------------------------

Source zones:
    - GISJOIN for 1990 block group parts (bgp1990gj): 37- or 39-character concatenation of:
        - "G"                                                1 character
        - State NHGIS code:                                  3 digits (FIPS + "0")
        - County NHGIS code:                                 4 digits (FIPS + "0")
        - County subdivision code:                           5 digits
        - Place/remainder code:                              5 digits
        - Census tract code:                                 4 or 6 digits
        - Congressional District (1987-1993, 100th-102nd 
            Congress) code:                                  2 digits
        - American Indian/Alaska Native area/remainder code: 4 digits
        - Reservation/trust lands/remainder code:            1 digit
        - Alaska Native regional corporation/remainder code: 2 digits
        - Urbanized area/remainder code:                     4 digits
        - Urban/Rural code:                                  1 digit
        - Census block group code:                           1 digit
    - GISJOIN for 2000 block group parts (bgp2000gj): 26-character concatenation of:
        - "G"                       1 character
        - State NHGIS code:         3 digits (FIPS + "0")
        - County NHGIS code:        4 digits (FIPS + "0")
        - County subdivision code:  5 digits
        - Place/remainder code:     5 digits
        - Census tract code:        6 digits
        - Urban/rural code:         1 character ("U" for urban, "R" for rural)
        - Census block group code:  1 digit

Target zones:
    - 2010 block groups
        - GISJOIN (bg2010gj): 15-character concatenation of:
            - "G"                                   1 character
            - State NHGIS code (STATEA):            3 digits (FIPS + "0")
            - County NHGIS code (COUNTYA):          4 digits (FIPS + "0")
            - Census tract code (TRACTA):           6 digits
            - Census block group code (BLCK_GRPA):  1 digit
        - GEOID (bg2010ge): 12-character concatenation of:
            - State FIPS code:                      2 digits
            - County FIPS code:                     3 digits
            - Census tract code (TRACTA):           6 digits
            - Census block group code (BLCK_GRPA):  1 digit
    - 2010 census tracts
        - GISJOIN (tr2010gj): 14-character concatenation of:
            - "G"                                   1 character
            - State NHGIS code (STATEA):            3 digits (FIPS + "0")
            - County NHGIS code (COUNTYA):          4 digits (FIPS + "0")
            - Census tract code (TRACTA):           6 digits
        - GEOID (tr2010ge): 11-character concatenation of:
            - State FIPS code:                      2 digits
            - County FIPS code:                     3 digits
            - Census tract code (TRACTA):           6 digits
    - 2010 counties
        - GISJOIN (co2010gj): 8-character concatenation of:
            - "G"                                   1 character
            - State NHGIS code (STATEA):            3 digits (FIPS + "0")
            - County NHGIS code (COUNTYA):          4 digits (FIPS + "0")
        - GEOID (co2010ge): 5-character concatenation of:
            - State FIPS code:                      2 digits
            - County FIPS code:                     3 digits


--------------------------------------------------------------------------------
Notes
--------------------------------------------------------------------------------

* The Census Bureau standard GEOID is included for all target units for convenience. GEOIDs
    for source units are not included due to block group parts not being a Census Bureau geography.
* The bgp1990gj field may contain blank values. These represent cases where the only 1990
    block group parts intersecting the corresponding larger geographic units are offshore,
    lying in coastal or Great Lakes waters, which are excluded from NHGIS's block boundary
    files. None of the missing 1990 blocks had any reported population or housing units.
    The blank values are included here to ensure that all target 2000 and 2010 geographic
    units are represented in the file.
* The algorithmic workflow for calculating atomic weights is detailed in
    https://github.com/jGaboardi/nhgisxwalk/blob/master/resources/frameworks/general-crosswalk-construction-framework.pdf
    and https://github.com/jGaboardi/nhgisxwalk/blob/master/resources/frameworks/handling-1990-no-data-blocks-in-crosswalks.pdf.
* NHGIS uses the nhgis_blk1990_blk2010_gj and nhgis_blk2000_blk2010_gj crosswalk as a base to build
    this crosswalk. The 1990 block group parts (1990_blck_grp_598_103) dataset is also used as a
    supplement in order to correctly identify all possible 1990 block group parts. This is necessary
    due to uninhabited census blocks not being included in the tabular data as mentioned above.

Zone identifiers:
    gj  - GISJOIN; the NHGIS standard identifier
    ge  - GEOID; the Census Bureau standard identifier

    https://jgaboardi.github.io/nhgisxwalk/
    https://github.com/jGaboardi/nhgisxwalk/wiki/FAQ-&-Resources

--------------------------------------------------------------------------------
Citation and Use
--------------------------------------------------------------------------------

All persons are granted a limited license to use this documentation and the
accompanying data, subject to the following conditions:

* Publications and research reports employing NHGIS data must cite it appropriately.
    The citation should include the following:

    Steven Manson, Jonathan Schroeder, David Van Riper, and Steven Ruggles.
    IPUMS National Historical Geographic Information System: Version 12.0 [Database].
    Minneapolis: University of Minnesota. 2017.
    http://doi.org/10.18128/D050.V12.0

* For policy briefs or articles in the popular press, we recommend that you cite the use of NHGIS data as follows:

    IPUMS NHGIS, University of Minnesota, www.nhgis.org.

In addition, we request that users send us a copy of any publications, research
reports, or educational material making use of the data or documentation.
Printed matter should be sent to:

    IPUMS NHGIS
    Minnesota Population Center
    University of Minnesota
    50 Willey Hall
    225 19th Ave S
    Minneapolis, MN 55455

Send electronic material to: nhgis@umn.edu

