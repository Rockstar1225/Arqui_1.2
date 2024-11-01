import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn', de StackOverflow
import load


def remove_columns(df: pd.DataFrame, col: list, df_name: str) -> None:
    """This function will remove the columns passed as argument from the dataframe also passed as argument. """
    if df_name not in df.keys():
        print("Error: Table not in dataframe")
        return
    df[df_name].drop(columns=col, axis=1, inplace=True)
    
    



    
    