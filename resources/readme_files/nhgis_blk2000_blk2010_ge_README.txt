--------------------------------------------------------------------------------
Documentation for nhgis_blk2000_blk2010_ge.csv
NHGIS crosswalk from 2000 to 2010 census blocks with GEOID identifiers
--------------------------------------------------------------------------------
 
Contents
    - Data Summary
    - Notes
    - References
    - Citation and Use
 
Additional documentation on NHGIS crosswalks is available at:
    https://www.nhgis.org/user-resources/geographic-crosswalks


--------------------------------------------------------------------------------
Data Summary
--------------------------------------------------------------------------------
 
File name:  nhgis_blk2000_blk2010_ge.csv
Content:
	- The top row is a header row
	- Each subsequent row represents an intersection between a 2000 block and 2010 block
	- The GEOID00 and GEOID10 fields contain contain standard census block identifiers
		- A block GEOID is a concatenation of:
			- State FIPS code: 2 digits
			- County FIPS code: 3 digits
			- Census tract code: 6 digits
			- Census block code: 4 digits
	- The WEIGHT field contains the interpolation weights NHGIS uses to allocate portions of 2000 block counts to 2010 blocks for geographically standardized time series tables
	- The PAREA column contains the portion of the 2000 block's land* area in each 2010 block. NHGIS uses this info to compute lower and upper bounds on standardized counts.
		* If a 2000 block's area is entirely water, then this value is based on the block's total area including water


--------------------------------------------------------------------------------
Notes
--------------------------------------------------------------------------------

The interpolation weights are derived from two different models: an advanced model for "blocks of interest" and a simpler model for lower-value cases.

"Blocks of interest" are those blocks for which interpolation is required for NHGIS time series tables--i.e., only those that share land with 2 or more "larger" 2010 census areas AND have > 0 population or housing units in 2000. "Larger" 2010 census areas are the areas for which NHGIS plans to release standardized data: block groups, places, county subdivisions, school districts, ZCTA's, urban areas, congressional districts (111th and 113th), and any units that can be constructed from these (e.g., census tracts, counties, etc.). The complete set also includes some neighboring blocks in order to complete an assessment of the interpolation by disaggregating from block pairs to single blocks, and in order to execute dasymetrically refined target-density weighting (TDW), which requires dasymetric zone areas for all parts of each populated 2010 block intersecting a 2000 block of interest.

For the blocks of interest, we use a hybrid of dasymetric and TDW interpolation models (see https://www.nhgis.org/documentation/time-series/2000-blocks-to-2010-geog) to allocate 2000 counts among 2010 blocks.

For blocks that "aren't of interest," we use unrefined TDW to compute weights, resulting in estimated densities that are proportional to the land-area densities of 2010 population + housing units in each intersecting 2010 block.


--------------------------------------------------------------------------------
References
--------------------------------------------------------------------------------

Research article explaining and assessing model used to generate hybrid interpolation weights:

	Schroeder, J. P. 2017. "Hybrid areal interpolation of census counts from 2000 blocks to 2010 geographies." Computers, Environment and Urban Systems 62, 53–63. http://dx.doi.org/10.1016/j.compenvurbsys.2016.10.001

 
--------------------------------------------------------------------------------
Citation and Use
--------------------------------------------------------------------------------
 
All persons are granted a limited license to use this documentation and the
accompanying data, subject to the following conditions:

* Publications and research reports employing NHGIS data must cite it appropriately. The citation should include the following:

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