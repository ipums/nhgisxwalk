"""
"""

import numpy
import pandas


def str_types(var_names):
    """String-type formatting for ID characters."""
    dtype = {c:str for c in var_names}
    return dtype


def get_context(geography, _file):
    """Get variable context for an NHGIS dataset"""
    df = pandas.read_csv(_file, header=None)
    df.index.name = geography
    df.columns = ["Variable", "Description"]
    return df


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
            "CDA", ################ swap out "CD103A"
            "AIANHHA",
            "RES_TRSTA",
            "ANRCA",
            "URB_AREAA",
            "URBRURALA",
            "BLCK_GRPA"
        ]
    
    return cols


def bgp_id(
    df, order, cname="_GJOIN", tzero=["STATEA", "COUNTYA"], nhgis=True
):
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
            id_str = "G"+id_str
        
        return id_str
    
    # recreate GISJOIN ID (_GJOIN, [or other])
    df[cname] = [_gjoin(record) for record in df.itertuples()]
    
    return df


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


def id_from(target_func, target_year, source, vectorized=True):
    """Create target IDs from source IDs.
    
    Parameters
    ----------
    
    target_func : function or method
        function or method for generating requested target IDs
    
    target_year : str
        target ID year
    
    source : iterable
        original source IDs
    
    vectorized : bool
        potential speedup when vectorized
    
    Returns
    -------
    
    result : iterable
        generated target IDs
    
    """
    
    # generate IDs from source geographies to target geographies
    if vectorized:
        result = numpy.vectorize(target_func)("2010", source)
    else:
        result = [target_func("2010", rec) for rec in source]
    
    return result
    
    