--------------------------------------------------------------------------------
Documentation for NHGIS crosswalks from block group parts to larger geographic units
--------------------------------------------------------------------------------

Contents
    - Data Summary
      - Composition of 1990 NHGIS block group part IDs
      - Composition of 2000 NHGIS block group part IDs
    - Content
      - 1990 block group parts to 2010 block groups
      - 1990 block group parts to 2010 tracts
      - 1990 block group parts to 2010 counties
      - 2000 block group parts to 2010 block groups
      - 2000 block group parts to 2010 tracts
      - 2000 block group parts to 2010 counties
    - Notes
    - Citation and Use

Additional documentation on NHGIS crosswalks is available at:
    https://www.nhgis.org/user-resources/geographic-crosswalks
    https://jgaboardi.github.io/nhgisxwalk/
    https://github.com/jGaboardi/nhgisxwalk/wiki/FAQ-&-Resources


--------------------------------------------------------------------------------
Data Summary
--------------------------------------------------------------------------------
 
Each NHGIS crosswalk file provides interpolation weights for allocating census counts from a specified
set of source zones to a specified set of target zones. Each record in the crosswalk represents a spatial
intersection between a single source zone and a single target zone, which we refer to as an atom.
The Census Bureau standard GEOID is included for all target units for convenience. GEOIDs
for source units are not included due to block group parts not being a Census Bureau geography.

File naming scheme:  nhgis_[source geog][source year]_[target geog][target year]{_state FIPS}.csv

Geographic unit codes:
    blk - Block 
    bgp - Block group part (intersections between block groups, places, county subdivisions, etc.)
    bg  - Block group
    tr  - Census tract
    co  - County

ID codes:
    gj  - GISJOIN; the NHGIS standard code
    ge  - GEOID; the Census Bureau standard code

Composition of NHGIS block group part IDs:
    - 1990
        - A 1990 GISJOIN block group part ID is a 41-44 character concatenation of:
            - "G"
            - State NHGIS code (STATEA): 3 digits (FIPS + "0")
            - County NHGIS code (COUNTYA): 4 digits (FIPS + "0")
            - County subdivision NHGIS code (CTY_SUBA): 5 digits
            - County place/remainder code (PLACEA): 5 digits
            - Census tract code (TRACTA): 4 or 6 digits in 1990
            - Congressional district (1993-1995, 101st Congress) code (CDA): 2 digits
            - American Indian/Alaska Native area/remainder code (AIANHHA): 4 digits
            - Reservation/trust lands/remainder code (RES_TRSTA): 4 digits
            - Alaska Native regional corporation/remainder code (ANRCA): 2 digits
            - Urbanized area/remainder code (URB_AREAA): 4 digits
            - Urban/Rural code (URBRURALA): 1 digit
            - Census block group code (BLCK_GRPA): 3 or 4 digits in 1990
    - 2000
        - A 2000 GISJOIN block group part ID is a 25 character concatenation of:
            - "G"
            - State NHGIS code (STATEA): 3 digits (FIPS + "0")
            - County NHGIS code (COUNTYA): 4 digits (FIPS + "0")
            - County subdivision NHGIS code (CTY_SUBA): 5 digits
            - County place/remainder code (PLACEA): 5 digits
            - Census tract code (TRACTA): 6 digits in 2000
            - Urban/Rural code (URBRURALA): 1 character; U for urban, R for rural
            - Census block group code (BLCK_GRPA): 1 digit in 2000


--------------------------------------------------------------------------------
Content:
--------------------------------------------------------------------------------
    - The top row is a header row
    - Each subsequent row represents a potential intersection between a block group part and a large geographic unit.
    - All files contain fields for source and target unit GISJOIN ID and target unit GEOID (explained below).
    - All files contain fields for weighted proportional values of four variables:
        - (wt_pop) total population
        - (wt_fam) total families
        - (wt_hh) total households
        - (wt_hu) total housing units
    
    - 1990 to 2010
        - block group parts to block groups
            - The bgp1990gj field contains NHGIS-standard 1990 block group part identifiers (see above).
                - See important information regarding the bgp1990gj field in the Notes section.
            - The bg2010gj field contains NHGIS-standard GISJOIN block group identifiers.
                - A block group GISJOIN is a concatenation of:
                    - "G"
                    - State NHGIS code (STATEA): 3 digits (FIPS + "0")
                    - County NHGIS code (COUNTYA): 4 digits (FIPS + "0")
                    - Census tract code (TRACTA): 6 digits
                    - Block group code (BLCK_GRPA): 1 digit
                - The bg2010gj field may contain blank values.
            - The bg2010ge field contains Census-standard GEOID block group identifiers.
                - A block group GEOID is a concatenation of:
                    - State Census code: 2 digits (FIPS)
                    - County Census code: 3 digits (FIPS)
                    - Census tract code: 6 digits
                    - Block group code (BLCK_GRPA): 1 digit
                - The bg2010ge field may contain blank values.
            - The wt_pop field contains the atomic weight of the total population variable (NHGIS: ET1001).
            - The wt_fam field contains the atomic weight of the total families variable (NHGIS: EUD001).
            - The wt_hh field contains the atomic weight of the total households variable (NHGIS: EUO001).
            - The wt_hu field contains the atomic weight of the total housing units variable (NHGIS: ESA001).
        - block group parts to tracts
            - The bgp1990gj field contains NHGIS-standard 1990 block group part identifiers (see above).
                - See important information regarding the bgp1990gj field in the Notes section.
            - The tr2010gj field contains NHGIS-standard GISJOIN tract identifiers.
                - A tract GISJOIN is a concatenation of:
                    - "G"
                    - State NHGIS code (STATEA): 3 digits (FIPS + "0")
                    - County NHGIS code (COUNTYA): 4 digits (FIPS + "0")
                    - Census tract code (TRACTA): 6 digits in 2010
                - The tr2010gj field may contain blank values.
            - The tr2010ge field contains Census-standard GEOID tract identifiers.
                - A tract GEOID is a concatenation of:
                    - State Census code: 2 digits (FIPS)
                    - County Census code: 3 digits (FIPS)
                    - Census tract code: 6 digits
                - The tr2010ge field may contain blank values.
            - The wt_pop field contains the atomic weight of the total population variable (NHGIS: ET1001).
            - The wt_fam field contains the atomic weight of the total families variable (NHGIS: EUD001).
            - The wt_hh field contains the atomic weight of the total households variable (NHGIS: EUO001).
            - The wt_hu field contains the atomic weight of the total housing units variable (NHGIS: ESA001).
        - block group parts to counties
            - The bgp1990gj field contains NHGIS-standard 1990 block group part identifiers (see above).
                - See important information regarding the bgp1990gj field in the Notes section.
            - The co2010gj field contains NHGIS-standard GISJOIN county identifiers.
                - A county GISJOIN is a concatenation of:
                    - "G"
                    - State NHGIS code (STATEA): 3 digits (FIPS + "0")
                    - County NHGIS code (COUNTYA): 4 digits (FIPS + "0")
                - The co2010gj field may contain blank values.
            - The co2010ge field contains Census-standard GEOID county identifiers.
                - A county GEOID is a concatenation of:
                    - State Census code: 2 digits (FIPS)
                    - County Census code: 3 digits (FIPS)
                - The co2010ge field may contain blank values.
            - The wt_pop field contains the atomic weight of the total population variable (NHGIS: ET1001).
            - The wt_fam field contains the atomic weight of the total families variable (NHGIS: EUD001).
            - The wt_hh field contains the atomic weight of the total households variable (NHGIS: EUO001).
            - The wt_hu field contains the atomic weight of the total housing units variable (NHGIS: ESA001).
    
    - 2000 to 2010
        - block group parts to block groups
            - The bgp2000gj field contains NHGIS-standard 2000 block group part identifiers (see above).
            - The bg2010gj field contains NHGIS-standard 2000 block group identifiers.
            - The co2010ge field contains Census-standard GEOID tract identifiers (see above).
            - The wt_pop field contains the atomic weight of the total population variable (NHGIS: FXS001).
            - The wt_fam field contains the atomic weight of the total families variable (NHGIS: F2V001).
            - The wt_hh field contains the atomic weight of the total households variable (NHGIS: FY4001).
            - The wt_hu field contains the atomic weight of the total housing units variable (NHGIS: FV5001).
        - block group parts to tracts
            - The bgp2000gj field contains NHGIS-standard 2000 block group part identifiers (see above).
            - The tr2010gj field contains NHGIS-standard 2010 tract identifiers.
            - The tr2010ge field contains Census-standard GEOID tract identifiers (see above).
            - The wt_pop field contains the atomic weight of the total population variable (NHGIS: FXS001).
            - The wt_fam field contains the atomic weight of the total families variable (NHGIS: F2V001).
            - The wt_hh field contains the atomic weight of the total households variable (NHGIS: FY4001).
            - The wt_hu field contains the atomic weight of the total housing units variable (NHGIS: FV5001).
        - block group parts to counties
            - The bgp2000gj field contains NHGIS-standard 2000 block group part identifiers (see above).
            - The co2010gj field contains NHGIS-standard 2010 tract identifiers.
            - The co2010ge field contains Census-standard GEOID tract identifiers (see above).
            - The wt_pop field contains the atomic weight of the total population variable (NHGIS: FXS001).
            - The wt_fam field contains the atomic weight of the total families variable (NHGIS: F2V001).
            - The wt_hh field contains the atomic weight of the total households variable (NHGIS: FY4001).
            - The wt_hu field contains the atomic weight of the total housing units variable (NHGIS: FV5001).


--------------------------------------------------------------------------------
Notes
--------------------------------------------------------------------------------

* The bgp1990gj field may contain blank values. These represent cases where the only 1990
    block group parts intersecting the corresponding larger geographic units are offshore,
    lying in coastal or Great Lakes waters, which are excluded from NHGIS's block boundary
    files. None of the missing 1990 blocks had any reported population or housing units.
    The blank values are included here to ensure that all larger 2000 and 2010 geographic
    units are represented in the file.
* The algorithmic workflow for calculating atomic weights is detailed in
    https://github.com/jGaboardi/nhgisxwalk/blob/master/resources/frameworks/general-crosswalk-construction-framework.pdf
    and https://github.com/jGaboardi/nhgisxwalk/blob/master/resources/frameworks/handling-1990-no-data-blocks-in-crosswalks.pdf.
* NHGIS uses the nhgis_blk1990_blk2010_gj and nhgis_blk2000_blk2010_gj crosswalk as a base to build
    this crosswalk. The 1990 block group parts (1990_blck_grp_598_103) dataset is also used as a
    supplement in order to correctly identify all possible 1990 block group parts. This is necessary
    due to uninhabited census blocks not being included in the tabular data as mentioned above.


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

