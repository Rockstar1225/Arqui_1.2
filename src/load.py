import pandas as pd
import os
import re


def load_db():
    # paths usados
    pwd = os.getcwd()
    dataset_dir = f"{pwd}/DatasetsArquiViejos"

    # leer datasets y guardarlos en un diccionario
    df = {} 
    for item in os.listdir(dataset_dir):
        try:
            file_name = re.findall("[A-Z][^A-Z]*", item)[0]
            temp_db = pd.read_csv(f"{dataset_dir}/{item}")
            df[file_name] = temp_db
        except IndexError:
            file_name = item.split('.')[0]
            temp_db = pd.read_csv(f"{dataset_dir}/{item}")
            df[file_name] = temp_db       
    return df