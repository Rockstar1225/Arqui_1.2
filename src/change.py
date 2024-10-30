import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn', de StackOverflow
import load
import unicodedata
from dateutil import parser

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
            tabla[columna] = tabla[columna].astype(object)
            lista = tabla[columna]
            for i in range(len(lista)):
                if pd.isna(lista[i]): #Función para detectar los nan. Me la ha dado Chat gpt
                    whilebreaker = False
                    tachadas = [tabla_name]
                    while not whilebreaker:
                        id = find_id(db, tabla_name, i)
                        new_tab = find_table_by_column(db, tachadas, columna)
                        if new_tab is None:
                            tabla.loc[i, columna] =  f"{id}-{columna}-ausente"
                            whilebreaker = True
                        else:
                            valor = take_atribute(db, new_tab, columna, id)
                            if valor is None:
                                tachadas.append(new_tab)
                            else:
                                lista[i] = valor
                                whilebreaker = True
    print("Emp terminado")



def reformatear_fecha(db: pd.DataFrame, table_name: str, column_name: str): #ChatGPT
    archivo = db[table_name]
    fechas_nuevas = []
    for fecha in archivo[column_name]:
        try:
            f_adapt = parser.parse(fecha)
            f_formt = f_adapt.strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            f_formt = pd.NaT
        fechas_nuevas.append(f_formt)
    archivo[column_name] = fechas_nuevas
    empty_data(db)

def delete_special(db: pd.DataFrame):
    lista_tildes = ["DESC_CLASIFICACION", "BARRIO", "DISTRITO", "NOMBRE", "TIPO_INCIDENTE"]
    for tabla_n in db:
        tabla = db[tabla_n]
        for columna in tabla:
            if columna in lista_tildes:
                for n in range(len(tabla[columna])):
                    elemento = tabla[columna][n]
                    elemento = ''.join(c for c in unicodedata.normalize('NFD', elemento) if unicodedata.category(c) != 'Mn') #Tildes
                    elemento = "".join(char for char in elemento if char.isalnum() or char == " ") # Caracter especial
                    tabla.loc[n, columna] = str(elemento)
    print("Sp terminado")


def formato_tlf(db:pd.DataFrame):
    columna = db["Usuarios"]["TELEFONO"]
    for i in range (len(columna)):
        valor = columna[i]
        if " " or "+" in valor:
            espacio = ""
            j = 0
            while "34" not in espacio:
                espacio += valor[j]
                j += 1
            numero = valor[j:]
            lista = numero.split(" ")
            new_tlf = "34"
            for x in lista:
                new_tlf += x
            columna[i] = new_tlf
    print("Tlf terminado")


def no_duplicates(db: pd.DataFrame, table_name: str, id_column: str):
    tabla = db[table_name]
    columna = tabla[id_column]
    fila_unicos = []
    fila_repetidos = []
    for i in range(len(columna)):
        valor = columna[i]
        if valor in fila_unicos:
            fila_repetidos.append(i)
        else:
            fila_unicos.append(valor)
    print(fila_repetidos)
    dominio = len(fila_repetidos)
    for j in range(dominio):
        db[table_name].drop(fila_repetidos[dominio-1-j])
# Pruebas
base = load.load_db()
empty_data(base)
delete_special(base)
formato_tlf(base)
reformatear_fecha(base, "Mantenimiento", "FECHA_INTERVENCION")
print(base)