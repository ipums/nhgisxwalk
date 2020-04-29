"""
"""

from io import StringIO
import pandas

__all__ = ["calculate_atoms"]

toy_data = r"""
id_bgp90,id_bk90,id_bk10,id_tract10,wt,pop_bk90
A,A.1,X.1,X,1.0,60
A,A.2,X.2,X,0.3,100
A,A.2,Y.1,Y,0.7,100
B,B.1,X.3,X,1.0,50
B,B.2,Y.2,Y,1.0,80
"""


def calculate_atoms(
    df, weight=None, input_var=None, sum_var=None, groupby_cols=None
):
    """ Calculate the atoms (intersecting parts) of census geographies.
    
    Parameters
    ----------
    
    df : pandas.DataFrame
        input data
    
    weight : str
        weight colum name
    
    input_var : str
        input variable column name
    
    sum_var : str
        groupby and summed variable column name
    
    groupby_cols : list
        dataframe columns to perform groupby
    
    Returns
    -------
    
    atoms : pandas.DataFrame
        output data
    
    """
    
    df[sum_var] = df[weight] * df[input_var]
    
    atoms = df.groupby(groupby_cols)[sum_var].sum().to_frame()
    
    atoms.reset_index(inplace=True)
    
    return atoms


if __name__ == "__main__":
    toy_data = pandas.read_csv(StringIO(toy_data))
    print(toy_data)
    atom_df = calculate_atoms(
        toy_data,
        weight="wt",
        input_var="pop_bk90",
        sum_var="bgp90tract10",
        groupby_cols=["id_bgp90", "id_tract10"]
    )
    print(atom_df)
