import pandas as pd

# capitalizar una columna entera
def capitalize_column(db: pd.DataFrame, colname: str) -> pd.DataFrame:
    db[colname] =  db[colname].apply(lambda x: x.upper())
    
    