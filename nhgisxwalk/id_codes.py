"""IDs and ID components of geographic code descriptions in a pandas.DataFrame.
"""

from .__code_components import *
import numpy
import pandas
from io import StringIO


# To Do ----- v0.0.1
#
# ID generator: -- blk_id, bkg_id, cty_id...


def code_cols(geog, year):
    """Geography ID coded columns.
    
    Parameters
    ----------
    
    geog : str
        Will support ["blk", "bgp", "bgr", "trt", "cty",...].
    
    year : str
        Will support ["1990", "2000", "2010"].
        
    Returns
    -------
    
    cols : list
        Correct ordering of columns to create the geography ID.
    
    """
    # ensure `year` is a str
    year = str(year)

    if geog == "bgp" and year == "1990":
        cols = [
            "STATEA",
            "COUNTYA",
            "CTY_SUBA",
            "PLACEA",
            "TRACTA",
            "CDA",  ########################################### swap out "CD103A"
            "AIANHHA",
            "RES_TRSTA",
            "ANRCA",
            "URB_AREAA",
            "URBRURALA",
            "BLCK_GRPA",
        ]

    return cols


def blk_id():
    """
    """

    pass


def bgp_id(df, order, cname="_GJOIN", tzero=["STATEA", "COUNTYA"], nhgis=True):
    """recreate a the BGPs GISJOIN/GEOID
    
    Parameters
    ----------
    
    df : pandas.DataFrame
        Input dataframe.
    
    order : list-like
        Correct ordering of columns.
    
    cname : str
        Name for new column.
    
    tzeros : list
        Columns to add trailing zero. `nhgis` must be True.
    
    nhgis : bool
        Added 'G' and training zeros. See `GISJOIN identifiers` at
        https://www.nhgis.org/user-resources/geographic-crosswalks
    
    Returns
    -------
    
    df : pandas.DataFrame
        Dataframe with new column.
    
    """

    def _gjoin(x):
        """internal GISJOIN/GEOID generator"""

        # container for ID components
        join_id_vals = []
        for o in order:

            # if the val associated with `o` is a numpy.float
            v = getattr(x, o)

            try:
                # handle NaN values
                if not numpy.isnan(v):
                    _id_val = str(v)
                else:
                    _id_val = ""

            # if the val associated with `o` is a str
            except TypeError:
                _id_val = str(v)

            # trailing zero for NHGIS
            if nhgis and o in tzero:
                _id_val += "0"
            # append ID component to ID list
            join_id_vals.append(_id_val)

        id_str = "".join(join_id_vals)
        if nhgis:
            # G prefix for GISJOIN and concatentate ID components
            id_str = "G" + id_str

        return id_str

    # recreate GISJOIN ID (_GJOIN, [or other])
    df[cname] = [_gjoin(record) for record in df.itertuples()]

    return df


def bkg_id():
    """
    """

    pass


def trt_id(year, _id, nhgis=True):
    """Extract the tract ID from the block ID.
    
    Parameters
    ----------
    
    year : str
        Census collection year.
    
    _id : str
        Block GISJOIN/GEOID.
    
    nhgis : bool
        Added 'G' and training zeros. See `GISJOIN identifiers` at
        https://www.nhgis.org/user-resources/geographic-crosswalks
    
    Returns
    -------
    
    tract_id : str
        Tract GISJOIN/GEOID.
    
    """

    if year == "2010":
        indexer = 14
        if not nhgis:
            indexer = "?"
        # slice out tract ID
        tract_id = _id[:indexer]
    else:
        msg = "Census year %s is not currently supported." % year
        raise RuntimeError(msg)

    return tract_id


def cty_id():
    """
    """

    pass


def id_from(target_func, target_year, source, vectorized):
    """Create target IDs from source IDs.
    
    Parameters
    ----------
    
    target_func : function or method
        Function or method for generating requested target IDs.
    
    target_year : str
        Target ID year.
    
    source : iterable
        Original source IDs.
    
    vectorized : bool
        Potential speedup when (True).
    
    Returns
    -------
    
    result : iterable
        Generated target IDs.
    
    """

    # generate IDs from source geographies to target geographies
    if vectorized:
        result = numpy.vectorize(target_func)(target_year, source)
    else:
        result = [target_func(target_year, rec) for rec in source]

    return result


def id_code_components(year, geo):
    """Fetch the raw-string and create a dataframe.
    
    Parameters
    ----------
    
    year : str
        ...
    
    geo : str
        ...
    
    Returns
    -------
    
    df : pandas.DataFrame
        ...
    
    """

    if year == "1990":
        if geo == "blk":
            components = blk1990
        if geo == "bgp":
            components = bgp1990
        if geo == "bkg":
            pass
            # components
        if geo == "trt":
            pass
            # components
        if geo == "cty":
            pass
            # components

    if year == "2000":
        if geo == "blk":
            pass
            # components
        if geo == "bgp":
            pass
            # components
        if geo == "bkg":
            pass
            # components
        if geo == "trt":
            pass
            # components
        if geo == "cty":
            pass
            # components

    if year == "2010":
        if geo == "blk":
            pass
            # components
        if geo == "bgp":
            pass
            # components
        if geo == "bkg":
            pass
            # components
        if geo == "trt":
            components = trt2010
        if geo == "cty":
            pass
            # components

    # create ID components dataframe
    df = pandas.read_csv(StringIO(components), header=None)
    df.index.name = geo + year
    df.columns = ["Variable", "Description"]

    return df
