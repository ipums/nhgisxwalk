# This file is part of the Minnesota Population Center's NHGISXWALK.
# For copyright and licensing information, see the NOTICE and LICENSE files
# in this project's top-level directory, and also on-line at:
#   https://github.com/ipums/nhgisxwalk

"""IDs and ID components of geographic code descriptions in a pandas.DataFrame.
"""


from io import StringIO

import numpy
import pandas

from .__code_components import *


def code_cols(geog, year):
    """Geography ID coded columns.

    Parameters
    ----------

    geog : str
         The specified census geography. This will support
         ["blk", "bgp", "bg", "tr", "co",...] in the future.

    year : str
        The specified census year. This will support
        ["1990", "2000", "2010", "2020"] in the future.

    Returns
    -------

    cols : list
        The correct ordering of columns to create the geography ID.

    """
    # ensure `year` is a str
    year = str(year)

    if geog == "bgp":
        if year == "1990":
            """
            # Geographic level (598_103):
            #       Block Group by:
            #                   State--
            #                   County--
            #                   County Subdivision--
            #                   Place/Remainder--
            #                   Census Tract--
            #                   Congressional District (101st) Code--
            #                   American Indian/Alaska Native Area/Remainder--
            #                   Reservation/Trust Lands/Remainder--
            #                   Alaska Native Regional Corporation/Remainder--
            #                   Urbanized Area/Remainder--
            #                   Urban/Rural
            """
            cols = [
                "STATEA",
                "COUNTYA",
                "CTY_SUBA",
                "PLACEA",
                "TRACTA",
                "CD101A",
                "AIANHHA",
                "RES_TRSTA",
                "ANRCA",
                "URB_AREAA",
                "URBRURALA",
                "BLCK_GRPA",
            ]
        if year == "2000":
            """
            # Geographic level (_90):
            #       Block Group by:
            #                   State--
            #                   County--
            #                   County Subdivision--
            #                   Place/Remainder--
            #                   Census Tract--
            #                   Urban/Rural
            """
            cols = [
                "STATEA",
                "COUNTYA",
                "CTY_SUBA",
                "PLACEA",
                "TRACTA",
                "URBRURALA",
                "BLCK_GRPA",
            ]

    if geog == "bg":
        if year == "1990":
            cols = ["STATEA", "COUNTYA", "TRACTA", "BLCK_GRPA"]

    return cols


def generate_atom_id(df, c1, c2, cname):
    """Generate a single "atom ID" to perform a set difference."""
    df[cname] = df[c1] + df[c2]
    return df


def generate_geoid(in_id):
    """Convert a GISJOIN ID to a GEOID ID.
    Note: NOT functional for Block Group Parts (only NHGIS).

    Parameters
    ----------

    in_id : str
        Input ID from particular year.

    Returns
    -------

    out_id : str or numpy.nan
        Converted ID.

    """

    if str(in_id) == "nan":
        out_id = in_id
    elif str(in_id).replace(".", "").isdigit():
        if not str(in_id).replace(".", "", 1).isdigit():
            raise ValueError("'in_id' has too many decimals to be a float: %s." % in_id)
        raise TypeError("Check the data type of '%s'." % in_id)
    elif not in_id.startswith("G"):
        raise ValueError("Check the NHGIS prefix of '%s'." % in_id)
    else:
        components = [in_id[1:3], in_id[4:7], in_id[8:12], in_id[12:]]
        out_id = "".join(components)

    return out_id


def gisjoin_id(record, component_order, trailing_zeros):
    """GISJOIN ID generator. Add 'G' and trailing zeros.
    See GISJOIN identifiers
    [https://www.nhgis.org/user-resources/geographic-crosswalks>].

    Parameters
    ----------

    record : namedtuple
        A single record instance of a ``pandas.DataFrame``.

    component_order : list
         The correct ordering of columns to create the ID.

    trailing_zeros : list
        The specific columns to add a trailing zero.

    Returns
    -------

    _id : str, numpy.nan
        The GISJOIN version of a census geography ID if the geography
        exists, otherwise ``numpy.nan``.

    """

    endex = -1
    vend = getattr(record, component_order[endex])
    # if the block ID isn't in the summary data
    if str(vend) == "nan":
        _id = vend
    else:
        # G prefix for GISJOIN
        join_id_vals = ["G"]
        for co in component_order[:endex]:
            v = getattr(record, co)
            # add trailing zero for NHGIS
            if co in trailing_zeros:
                v += "0"
            # append ID component to ID list
            join_id_vals.append(v)
        # concatenate ID components
        _id = "".join(join_id_vals + [vend])

    return _id


def blk_gj(df, order, cname="GISJOIN", tzero=["STATE", "COUNTY"]):
    """Recreate BLK GISJOIN ---- Used to extract 2000 block UR codes.

    Parameters
    ----------

    df : pandas.DataFrame
        The input dataframe.

    order : list-like
        The correct ordering of columns.

    cname : str
        The name for the new column. Default is 'GISJOIN'.

    tzeros : list
        The columns to add trailing zero. Default is ['STATE', 'COUNTY'].

    Returns
    -------

    df : pandas.DataFrame
        The input ``df`` with new column.

    """

    df[cname] = [gisjoin_id(record, order, tzero) for record in df.itertuples()]
    return df


def bgp_gj(df, order, cname="_GJOIN", tzero=["STATEA", "COUNTYA"]):
    """Recreate BGPs GISJOIN ID.

    Parameters
    ----------

    df : pandas.DataFrame
        The input dataframe.

    order : list-like
        The correct ordering of columns.

    cname : str
        The name for the new column. Default is '_GJOIN'.

    tzeros : list
        The columns to add trailing zero. Default is ['STATEA', 'COUNTYA'].

    Returns
    -------

    df : pandas.DataFrame
        The input ``df`` with new column.

    """

    # recreate GISJOIN ID (_GJOIN, [or other])
    df[cname] = [gisjoin_id(record, order, tzero) for record in df.itertuples()]
    return df


def bg_gj(year, _id, df=None, order=None, cname="GISJOIN", tzero=["STATEA", "COUNTYA"]):
    """Extract the block group ID from the block ID.
    See GISJOIN identifiers
    [https://www.nhgis.org/user-resources/geographic-crosswalks].

    The 1990 block group ID is the first character of the block ID, so
    the GISJOIN ID for a block group is G+state+0+county+0+tract+block[0].

    Parameters
    ----------

    year : str
        The census collection year.

    _id : str
        The block GISJOIN/GEOID.

    df : pandas.DataFrame
        The input dataframe.

    order : list-like
        The correct ordering of columns.

    cname : str
        The name for the new column. Default is 'GISJOIN'.

    tzeros : list
        The columns to add trailing zero. Default is ['STATEA', 'COUNTYA'].

    Returns
    -------

    block_group_id : str
        The block group GISJOIN.

    df : pandas.DataFrame
        The input ``df`` with new column.

    """

    # scenario 1: map function to each row of dataframe to extract ID
    if _id:
        # 1990 -- Block Group (by State--County--Census Tract)
        if year == "1990":
            len_id = len(_id)
            if len_id % 2 == 0:
                indexer = 3
            else:
                indexer = 2
        if year == "2010":
            indexer = 3

        block_group_id = _id[:-indexer]

        return block_group_id

    else:
        # scenario 2: build ID from summary file (whole dataframe)
        df[cname] = [gisjoin_id(record, order, tzero) for record in df.itertuples()]
        return df


def tr_gj(year, _id):
    """Extract the tract ID from the block ID.
    See GISJOIN identifiers
    [https://www.nhgis.org/user-resources/geographic-crosswalks].

    Parameters
    ----------

    year : str
        The census collection year.

    _id : str
        The block GISJOIN.

    Returns
    -------

    tract_id : str
        The tract GISJOIN.

    """

    if not _id.startswith("G"):
        raise ValueError("Check the NHGIS prefix of '%s'." % _id)

    if year == "2010":
        indexer = 14
        # slice out tract ID
        tract_id = _id[:indexer]
    else:
        msg = "Census year %s is not currently supported." % year
        raise ValueError(msg)

    return tract_id


def co_gj(year, _id):
    """Extract the county ID from the block ID.
    See GISJOIN identifiers
    [https://www.nhgis.org/user-resources/geographic-crosswalks].

    Parameters
    ----------

    year : str
        The census collection year.

    _id : str
        The block GISJOIN.

    Returns
    -------

    county_id : str
        The county GISJOIN.

    """

    if not _id.startswith("G"):
        raise ValueError("Check the NHGIS prefix of '%s'." % _id)

    if year == "2010":
        indexer = 8
        # slice out county ID
        county_id = _id[:indexer]
    else:
        msg = "Census year %s is not currently supported." % year
        raise ValueError(msg)

    return county_id


def id_from(target_func, target_year, source, vectorized):
    """Create target IDs from source IDs.

    Parameters
    ----------

    target_func : function or method
        The function or method for generating requested target IDs.

    target_year : str
        The original target ID year.

    source : iterable
        The original source IDs.

    vectorized : bool
        Potential speedup when set to ``True``. Default is ``True``.

    Returns
    -------

    result : iterable
        The generated target IDs.

    """

    # generate IDs from source geographies to target geographies
    if vectorized:
        result = numpy.vectorize(target_func)(target_year, source)
    else:
        result = [target_func(target_year, rec) for rec in source]

    return result


def gj_code_components(year, geo):
    """Fetch the raw-string of the components used to create the specified
    year+geography ID, and return in a dataframe.

    Parameters
    ----------

    year : str
        The specified census year.

    geo : str
        The specified census geography.

    Returns
    -------

    df : pandas.DataFrame
        A dataframe of two columns: "Variable", "Description". The
        "Variable" column is tabular name of the component that is
        explained in "Description".

    """

    if year == "1990":
        if geo == "blk":
            components = blk1990
        if geo == "bgp":
            components = bgp1990
        if geo == "bg":
            raise AttributeError()
            # components
        if geo == "tr":
            raise AttributeError()
            # components
        if geo == "co":
            raise AttributeError()
            # components

    if year == "2000":
        if geo == "blk":
            components = blk2000
        if geo == "bgp":
            components = bgp2000
            # components
        if geo == "bg":
            raise AttributeError()
            # components
        if geo == "tr":
            raise AttributeError()
            # components
        if geo == "co":
            raise AttributeError()
            # components

    if year == "2010":
        if geo == "blk":
            raise AttributeError()
            # components
        if geo == "bgp":
            raise AttributeError()
            # components
        if geo == "bg":
            components = bg2010
        if geo == "tr":
            components = tr2010
        if geo == "co":
            components = co2010
            # components

    # create ID components dataframe
    df = pandas.read_csv(StringIO(components), header=None)
    df.index.name = geo + year
    df.columns = ["Variable", "Description"]

    return df
