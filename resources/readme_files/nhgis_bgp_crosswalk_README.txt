----------------------------------------------------------------------------------------------------
Documentation for NHGIS crosswalk files...
    from 1990 or 2000 block group parts...
    to 2010 block groups, census tracts, or counties
----------------------------------------------------------------------------------------------------

Contents
    - Data Summary
    - Zone Identifiers
    - Notes
    - Citation and Use

Additional documentation on NHGIS crosswalks is available at:
    https://www.nhgis.org/user-resources/geographic-crosswalks


----------------------------------------------------------------------------------------------------
Data Summary
----------------------------------------------------------------------------------------------------

Each NHGIS crosswalk file provides interpolation weights for allocating census counts from a 
specified set of source zones to a specified set of target zones.

Crosswalk file naming scheme:
    nhgis_[source level code][source year]_[target level code][target year]{_state FIPS code*}.csv

    * A state code suffix indicates the extent covered for a file that is limited to single state. 
      Such files may contain some source zones from neighboring states in cases where the Census 
      Bureau adjusted state boundary lines between censuses. Files with no state code suffix in 
      their names cover the entire nation (excluding Puerto Rico and other U.S. territories).

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
        bgp1990gj OR bgp2000gj:           NHGIS GISJOIN identifier for the source block group part. 
	                                  (See specifications below.)
        bg2010gj, tr2010gj OR co2010gj:   NHGIS GISJOIN identifier for the 2010 target zone. (See 
	                                  specifications below.)
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


----------------------------------------------------------------------------------------------------
Zone Identifiers
----------------------------------------------------------------------------------------------------

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
        - Block group code:         1 digit

Target zones:
    - 2010 block groups
        - GISJOIN (bg2010gj): 15-character concatenation of:
            - "G"                 1 character
            - State NHGIS code:   3 digits (FIPS + "0")
            - County NHGIS code:  4 digits (FIPS + "0")
            - Census tract code:  6 digits
            - Block group code:   1 digit
        - GEOID (bg2010ge): 12-character concatenation of:
            - State FIPS code:    2 digits
            - County FIPS code:   3 digits
            - Census tract code:  6 digits
            - Block group code:   1 digit
    - 2010 census tracts
        - GISJOIN (tr2010gj): 14-character concatenation of:
            - "G"                 1 character
            - State NHGIS code:   3 digits (FIPS + "0")
            - County NHGIS code:  4 digits (FIPS + "0")
            - Census tract code:  6 digits
        - GEOID (tr2010ge): 11-character concatenation of:
            - State FIPS code:    2 digits
            - County FIPS code:   3 digits
            - Census tract code:  6 digits
    - 2010 counties
        - GISJOIN (co2010gj): 8-character concatenation of:
            - "G"                 1 character
            - State NHGIS code:   3 digits (FIPS + "0")
            - County NHGIS code:  4 digits (FIPS + "0")
        - GEOID (co2010ge): 5-character concatenation of:
            - State FIPS code:    2 digits
            - County FIPS code:   3 digits


----------------------------------------------------------------------------------------------------
Notes
----------------------------------------------------------------------------------------------------

* In crosswalks with 1990 source zones, the zone identifier fields may contain blank values. Blank 
    values are given in cases where a source or target zone lies entirely offshore in coastal or 
    Great Lakes waters. In these cases we are unable to use NHGIS boundary files, which exclude 
    offshore areas, to determine relationships between 1990 and later census zones. (For censuses 
    after 1990, we use block relationship files from the Census Bureau to identify intersections 
    in offshore areas.) None of the block group parts with a "blank" target zone had any reported 
    population or housing units. We include the records with blank values to ensure that all source 
    and target zones are represented in the file.

* Crosswalk files contain only GISJOIN identifiers for block group parts, not GEOIDs, due to the 
    long length of identifiers for block group parts and the lack of other known data sources that 
    use GEOIDs to identify block group parts

* We derive NHGIS crosswalks for block group parts from the NHGIS block-to-block crosswalks 
    (nhgis_blk1990_blk2010_gj and nhgis_blk2000_blk2010_gj). We also use block-level data tables 
    from 1990 Summary Tape File 1 (NHGIS dataset 1990_STF1) and 2000 Summary File 1 (NHGIS dataset 
    2000_SF1b). Because the source 1990 block data tables include records only for inhabited blocks
    (those with nonzero population or housing unit counts), we use 1990 data tables for block group 
    parts (geographic level blck_grp_598) to ensure that all 1990 block group parts are identified 
    in the crosswalks.
    
* For documentation of the models and procedures used to derive the crosswalks, see 
    https://www.nhgis.org/user-resources/geographic-crosswalks


----------------------------------------------------------------------------------------------------
Citation and Use
----------------------------------------------------------------------------------------------------

All persons are granted a limited license to use this documentation and the accompanying data, 
subject to the following conditions:

* REDISTRIBUTION: You will not redistribute the data without permission.

  You may publish a subset of the data to meet journal requirements for accessing data related to 
  a particular publication. Contact us for permission for any other redistribution; we will 
  consider requests for free and commercial redistribution.

* CITATION: You will cite NHGIS appropriately.

    * Publications and research reports employing NHGIS data should include the following citation:

        Steven Manson, Jonathan Schroeder, David Van Riper, Tracy Kugler, and Steven Ruggles.
        IPUMS National Historical Geographic Information System: Version 15.0 [dataset].
        Minneapolis, MN: IPUMS. 2020. http://doi.org/10.18128/D050.V15.0

    * For policy briefs, online resources, or articles in the popular press, we 
      recommend that you cite the use of NHGIS data as follows:

        IPUMS NHGIS, University of Minnesota, www.nhgis.org.

These terms of use are a legally binding agreement. You can use the data only in accordance with 
these terms, and any other use is a violation of the agreement. Violations may result in revocation
of the agreement and prohibition from using other IPUMS data. If IPUMS or our partners are harmed 
from your violation, you are responsible for all damages, including reasonable attorney's fees and 
expenses.

In addition, we request that users send us a copy of any publications, research reports, or 
educational material making use of the data or documentation.

Send electronic material to: nhgis@umn.edu

Printed matter should be sent to:

    IPUMS NHGIS
    Institute for Social Research and Data Innovation
    University of Minnesota
    50 Willey Hall
    225 19th Ave S
    Minneapolis, MN 55455

