--------------------------------------------------------------------------------
Documentation for nhgis_blk1990_blk2010_ge.csv
NHGIS crosswalk from 1990 to 2010 census blocks with GEOID identifiers
--------------------------------------------------------------------------------
 
Contents
    - Data Summary
    - Notes
    - Version History
    - Citation and Use
 
Additional documentation on NHGIS crosswalks is available at:
    https://www.nhgis.org/user-resources/geographic-crosswalks


--------------------------------------------------------------------------------
Data Summary
--------------------------------------------------------------------------------
 
File name:  nhgis_blk1990_blk2010_ge.csv
Content:
	- The top row is a header row
	- Each subsequent row represents a potential intersection between a 1990 block and 2010 block
	- The GEOID90 and GEOID10 fields contain standard census block identifiers
		- A block GEOID is a concatenation of:
			- State FIPS code: 2 digits
			- County FIPS code: 3 digits
			- Census tract code: 6 digits (1990 tract codes that were originally 4 digits, as in NHGIS files, are extended to 6 with an appended "00")
			- Census block code: 3 or 4 digits in 1990; 4 digits in 2010
		- The GEOID90 field contains numerous blank values. These represent cases where the only 1990 blocks intersecting the corresponding 2010 block are offshore, lying in coastal or Great Lakes waters, which are excluded from NHGIS's block boundary files. None of the missing 1990 blocks had any reported population or housing units. The blank values are included here to ensure that all 2010 blocks are represented in the file.
	- The WEIGHT field contains the interpolation weights NHGIS uses to allocate portions of 1990 block counts to 2010 blocks for geographically standardized time series tables
	- The PAREA_VIA_BLK00 field contains the approximate portion of the 1990 block's land* area lying in the 2010 block, based on intersections that the 1990 and 2010 block have with 2000 blocks in 2000 and 2010 TIGER/Line files (i.e. indirect overlay via 2000 blocks).
		* If a 1990 block's area is entirely water, then this value is based on the block's total area including water
		- NHGIS uses these values to compute lower and upper bounds on 1990 estimates: for any record with a value greater than 0 and less than 1, it is assumed that either all or none of the 1990 block's characteristics could be located in the corresponding 2010 block.


--------------------------------------------------------------------------------
Notes
--------------------------------------------------------------------------------

NHGIS uses this crosswalk to generate 1990 data standardized to 2010 census units for NHGIS time series tables. Complete documentation on the interpolation model used to generate the weights in the crosswalk is provided at https://www.nhgis.org/documentation/time-series/1990-blocks-to-2010-geog.

In short, the model is based on "cascading density weighting", as introduced in Chapter 3 of Jonathan Schroeder's dissertation (_Visualizing Patterns in U.S. Urban Population Trends_, University of Minnesota) available here: http://hdl.handle.net/11299/48076.

The general sequence of operations:
1. Estimate 2000 population and housing unit counts for each intersection between 2000 and 2010 blocks.
	- Our basic "cascading density weighting" model does this by allocating 2000 counts among 2010 blocks in proportion to 2010 block population and housing densities (population and housing summed together).
	- We use this basic approach only for 2000 blocks that are _not_ split by the boundaries of a 2010 target unit, where "target units" are the areas for which NHGIS plans to release standardized data: block groups, places, county subdivisions, school districts, ZCTA's, urban areas, congressional districts (111th and 113th), and any units that can be constructed from these (e.g., census tracts, counties, etc.).
	- For 2000 blocks that _are_ split by the boundaries of a 2010 target unit, we use NHGIS's more advanced hybrid interpolation model (see https://www.nhgis.org/documentation/time-series/2000-blocks-to-2010-geog) to allocate 2000 counts among 2010 blocks.
2. Use the estimated 2000 population and housing unit densities from step 1 to guide the allocation of 1990 counts among 1990-2000-2010 block intersections.

The procedure also combines two types of overlay to model intersections between 1990, 2000, and 2010 blocks:
1. "Direct overlay" of 1990 & 2000 block polygons from 2000 TIGER/Line files with 2000 & 2010 block polygons from 2010 TIGER/Line files (with a preliminary step to georectify Hawaii's 2000 TIGER polygons to 2010 TIGER features in order to accommodate a systematic change in the coordinate system used to represent Hawaii features between the two TIGER versions)
2. "Indirect overlay":
	a. Overlay 1990 & 2000 block polygons using the 2000 TIGER/Line basis
	b. Overlay 2000 & 2010 block polygons using the 2010 TIGER/Line basis
	c. Multiply 1990-2000 intersection proportions from step 2a with 2000-2010 proportions from step 2b to compute estimated proportions of each 1990 block within each 2010 block. (This is how the crosswalk's "PAREA_VIA_BLK00" values are derived.)

The direct overlay weights are _constrained_ to eliminate any 1990-2010 intersections that are not valid in the indirect overlay. This prevents most "slivers" (invalid intersections caused by changes in TIGER feature representations) from being assigned any weight.

The final weighting blends weights from constrained direct overlay (CDO) and indirect overlay (IO) through a weighted average, giving high weight to CDO (and low weight to IO) in cases where the two TIGER/Line representations of a 2000 block align well _and_ where the 1990-2000 block intersection and the 2000-2010 block intersection both comprise less than the entirety of the 2000 block. In cases where the block intersections cover the entirety of a 2000 block _or_ the block intersection from one TIGER/Line version has _no_ valid intersection with a the corresponding 2000 block in the other TIGER/Line version, then the weighting is based on IO alone.

 
--------------------------------------------------------------------------------
Version History
--------------------------------------------------------------------------------

* v001 (2017-08-16)
	For the preliminary version of this crosswalk, in the first step of the estimation model (estimating 2000 counts for intersections between 2000 and 2010 blocks), simple density weighting was used for _all_ cases (allocating 2000 block counts among intersections to yield a density distribution that matches the density ratios among the corresponding 2010 blocks in 2010). The readme file, however, erroneously described the v002 method instead.

* v002 (2017-09-07)
	The weights in the crosswalk were updated to use the v002 model (as had been described in the original documentation), such that in the first step of the estimation, simple density weighting is used only for 2000 blocks that are _not_ split by the boundaries of a 2010 target unit, and elsewhere, the more advanced hybrid interpolation model is used.


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
