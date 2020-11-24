[<img align="middle" src="figs/nhgis_logo_black.png" height="100">](https://www.nhgis.org)

# NHGISXWALK
## Spatio-temporal [NHGIS Crosswalks](https://www.nhgis.org/user-resources/geographic-crosswalks)

[![Documentation](https://img.shields.io/static/v1.svg?label=docs&message=current&color=4ca)](https://ipums.github.io/nhgisxwalk/) [![GitHub release](https://img.shields.io/github/v/tag/ipums/nhgisxwalk?include_prereleases&logo=GitHub)](https://img.shields.io/github/v/tag/ipums/nhgisxwalk?include_prereleases&logo=GitHub) [![unittests](https://github.com/ipums/nhgisxwalk/workflows/.github/workflows/unittests.yml/badge.svg)](https://github.com/ipums/nhgisxwalk/actions?query=workflow%3A.github%2Fworkflows%2Funittests.yml) [![codecov](https://codecov.io/gh/ipums/nhgisxwalk/branch/main/graph/badge.svg)](https://codecov.io/gh/ipums/nhgisxwalk) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ipums/nhgisxwalk/main)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

This pacakge allows for the generation of temporal crosswalks of census geographic data built from the smallest intersecting units (atoms). Each row in a crosswalk represents a single atom and is comprised of a source ID (`geo+year+gj`), a target ID (`geo+year+gj`), and at least one column of weights. An example of a source ID is `bgp1990gj` (block group parts from 1990) and an example of a target ID is `tr1990gj` (tracts from 2010) — see [`notebooks/data-subset-sample-workflow-bgp1990tr2010.ipynb`](https://github.com/ipums/nhgisxwalk/blob/main/notebooks/data-subset-sample-workflow-bgp1990tr2010.ipynb) for the `nhgis_bgp1990gj_to_tr1990gj` crosswalk extract of Delaware. The weights are the interpolated proportions of source attributes that are are calculated as being within the target units. For a description of the algorithmic workflow see the [General Crosswalk Construction Framework](https://github.com/ipums/nhgisxwalk/blob/main/resources/frameworks/general-crosswalk-construction-framework.pdf). Data from 1990 poses a specific problem due to the US Census Bureau not explicitly including blocks with no population/housing units in the summary files (SF1). For a description of the algorithmic workflow in the 1990 "no data" scenarios see [Handling 1990 No-Data Blocks in Crosswalks](https://github.com/ipums/nhgisxwalk/blob/main/resources/frameworks/handling-1990-no-data-blocks-in-crosswalks.pdf). For more information of the base crosswalks see their [technical details](https://www.nhgis.org/user-resources/geographic-crosswalks#details). For further description see Schroeder (2007). 

#### Currently supported crosswalks include:

| source | target |
|--------|-------|
|1990 block group parts | 2010 counties|
|2000 block group parts | 2010 counties|
|1990 block group parts | 2010 tracts|
|2000 block group parts | 2010 tracts|
|1990 block group parts | 2010 block groups|
|2000 block group parts | 2010 block groups|

#### Planned supported crosswalks include:

| source | target |
|--------|-------|
|1990 block group parts | 2012 tracts|
|2000 block group parts | 2012 tracts|
|1990 block group parts | 2012 block groups|
|2000 block group parts | 2012 block groups|

* **Schroeder, J. P**. 2007. *Target-density weighting interpolation and uncertainty evaluation for temporal analysis of census data*. Geographical Analysis 39 (3):311–335.

## Examples

* [Proportionally-weighted Synthetic Atoms](https://github.com/ipums/nhgisxwalk/blob/main/notebooks/weighted-portion-synthetic-atoms.ipynb)
* [Synthetic Example](https://github.com/ipums/nhgisxwalk/blob/main/notebooks/synthetic-example.ipynb)
* Sample Workflow (see all [here](https://github.com/ipums/nhgisxwalk/blob/master/notebooks)):
  * [1990 block group parts to 2010 tracts](https://github.com/ipums/nhgisxwalk/blob/main/notebooks/data-subset-sample-workflow-bgp1990tr2010.ipynb)

## Resources

* [Frequently Asked Questions](https://github.com/ipums/nhgisxwalk/wiki/FAQ-&-Resources)
    * [What are "block group parts" and how can I download them?](https://github.com/ipums/nhgisxwalk/wiki/FAQ-&-Resources#what-are-block-group-parts-and-how-can-i-download-them)
    * [How are the crosswalks sorted?](https://github.com/ipums/nhgisxwalk/wiki/FAQ-&-Resources#how-are-the-crosswalks-sorted)

## Installation

Currently `nhgisxwalk` officially supports Python [3.6](https://docs.python.org/3.6/), [3.7](https://docs.python.org/3.7/), [3.8](https://docs.python.org/3.8/), and [3.9](https://docs.python.org/3.9/). Please make sure that you are operating in a Python >= 3.6 environment. Install the most current development version of `nhgisxwalk` by running:

```
$ pip install git+https://github.com/ipums/nhgisxwalk
```

##  Contribute

NHGISXWALK is under active development and contributors are welcome. If you have any suggestions, feature requests, or bug reports, please open new [issues](https://github.com/ipums/nhgisxwalk/issues) on GitHub. To submit patches, please review the `nhgisxwalk` [contributing guidelines](https://github.com/ipums/nhgisxwalk/blob/master/.github/CONTRIBUTING.md) before opening a [pull request](https://github.com/ipums/nhgisxwalk/pulls).

## Support

If you are having issues, please [create an issue](https://github.com/ipums/nhgisxwalk/issues).

## Citations
If you use `nhgisxwalk` in a scientific publication, we would appreciate using the following citations:
* **Steven Manson, Jonathan Schroeder, David Van Riper, and Steven Ruggles**. *IPUMS National Historical Geographic Information System: Version 14.0* [Database]. Minneapolis, MN: IPUMS. 2019. http://doi.org/10.18128/D050.V14.0
* **James Gaboardi**. *[ipums/nhgisxwalk](https://github.com/ipums/nhgisxwalk)*. Zenodo. 2020. [![DOI](https://zenodo.org/badge/259962549.svg)](https://zenodo.org/badge/latestdoi/259962549)


## License
The package is licensed under the [MPL-2.0 License](https://github.com/ipums/nhgisxwalk/blob/master/LICENSE).



## Funding
This project is funded through:

[<img align="middle" src="figs/nsf_logo.png" width="100">](https://www.nsf.gov/index.jsp) National Science Foundation Award #1825768: [National Historical Geographic Information System](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1825768&HistoricalAwards=false)

