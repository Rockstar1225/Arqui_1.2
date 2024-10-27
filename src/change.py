import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn', de StackOverflow
import load

# capitalizar una columna entera
def capitalize_column(db: pd.DataFrame, colname: str) -> pd.DataFrame:
    db[colname] =  db[colname].apply(lambda x: x.upper())

# Encontrar un dato en una tabla
def take_atribute(db: pd.DataFrame, tabla: str,  columna: str, id: int) -> str:
    archivo = db[tabla]
    fila = None
    for i in range(len(archivo["ID"])):
        valor = archivo["ID"][i]
        if id == valor:
            fila = i
            return archivo[columna][fila]
    return None

# Encuentra una tabla sin contar las tachadas que contenga una columna con el mismo nombre que la pasada por argumento
def find_table_by_column(db: pd.DataFrame, tablas_tachadas: list, column:str)-> str:
    for tabla in db:
        if tabla not in tablas_tachadas:
            t_analizar = db[tabla]
            if column in t_analizar:
                return tabla
    return None

def find_id(db: pd.DataFrame, tabla: str, fila: int):
    archivo = db[tabla]
    if tabla == "Usuarios":
        return archivo["NIF"][fila]
    elif tabla == "meteo24":
        return archivo["PROVINCIA"][fila]
    else:
        return archivo["ID"][fila]

#Rellenar filas vacias
def empty_data(db: pd.DataFrame):
    for tabla_name in db:
        tabla = base[tabla_name]
        for columna in tabla:
            lista = tabla[columna]
            for i in range(len(columna)):
                if pd.isna(lista[i]): #Función para detectar los nan. Me la ha dado Chat gpt
                    print("None encontrado")
                    whilebreaker = False
                    tachadas = [tabla_name]
                    new_tab = None
                    while not whilebreaker:
                        id = find_id(db, tabla_name, i)
                        new_tab = find_table_by_column(db, tachadas, columna)
                        if new_tab is None:
                            lista[i] = str(id) + "-" + columna + "-desconocido"
                            whilebreaker = True
                        else:
                            valor = take_atribute(db, tabla_name, columna, id)
                            if valor is None:
                                tachadas.append(new_tab)
                            else:
                                lista[i] = valor
                                whilebreaker = True
            



# Pruebas
base = load.load_db()
print(find_table_by_column(base, ["Areas"], "DISTRITO"))
print(take_atribute(base, "Areas", "DISTRITO", 3573005))
empty_data(base)