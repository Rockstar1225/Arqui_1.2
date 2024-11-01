import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn', de StackOverflow
import load
import unicodedata
from dateutil import parser


# capitalizar una columna entera
def capitalize_column(df: pd.DataFrame, colname: str) -> pd.DataFrame:
    df[colname] =  df[colname].apply(lambda x: x.upper())

# Encontrar un dato en una tabla
def take_atribute(df: pd.DataFrame, tabla: str,  columna: str, id: int) -> str:
    archivo = df[tabla]
    fila = None
    for i in range(len(archivo["ID"])):
        valor = archivo["ID"][i]
        if id == valor:
            fila = i
            return archivo[columna][fila]
    return None

# Encuentra una tabla sin contar las tachadas que contenga una columna con el mismo nombre que la pasada por argumento
def find_table_by_column(df: pd.DataFrame, tablas_tachadas: list, column:str)-> str:
    for tabla in df:
        if tabla not in tablas_tachadas:
            t_analizar = df[tabla]
            if column in t_analizar:
                return tabla
    return None

def find_id(df: pd.DataFrame, tabla: str, fila: int):
    archivo = df[tabla]
    if tabla == "Usuarios":
        return archivo["NIF"][fila]
    elif tabla == "meteo24":
        return archivo["PROVINCIA"][fila]
    elif tabla == "Codigo":
        return archivo["CÓDIGO"][fila]
    else:
        return archivo["ID"][fila]



#Rellenar filas vacias
def empty_data(df: pd.DataFrame):
    for tabla_name in df:
        tabla = base[tabla_name]
        for columna in tabla:
            tabla[columna] = tabla[columna].astype(object)
            lista = tabla[columna]
            for i in range(len(lista)):
                if pd.isna(lista[i]): #Función para detectar los nan. Me la ha dado Chat gpt
                    whilebreaker = False
                    tachadas = [tabla_name]
                    while not whilebreaker:
                        id = find_id(df, tabla_name, i)
                        new_tab = find_table_by_column(df, tachadas, columna)
                        if new_tab is None:
                            tabla.loc[i, columna] =  f"{id}-{columna}-ausente"
                            whilebreaker = True
                        else:
                            valor = take_atribute(df, new_tab, columna, id)
                            if valor is None:
                                tachadas.append(new_tab)
                            else:
                                lista[i] = valor
                                whilebreaker = True
    print("Emp terminado")



def reformatear_fecha(df: pd.DataFrame, table_name: str, column_name: str): #ChatGPT
    archivo = df[table_name]
    fechas_nuevas = []
    for fecha in archivo[column_name]:
        try:
            f_adapt = parser.parse(fecha)
            f_formt = f_adapt.strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            f_formt = pd.NaT
        fechas_nuevas.append(f_formt)
    archivo[column_name] = fechas_nuevas
    empty_data(df)

def delete_special(df: pd.DataFrame):
    lista_tildes = ["DESC_CLASIFICACION", "BARRIO", "DISTRITO", "NOMBRE", "TIPO_INCIDENTE"]
    for tabla_n in df:
        tabla = df[tabla_n]
        for columna in tabla:
            if columna in lista_tildes:
                for n in range(len(tabla[columna])):
                    elemento = tabla[columna][n]
                    elemento = ''.join(c for c in unicodedata.normalize('NFD', elemento) if unicodedata.category(c) != 'Mn') #Tildes
                    elemento = "".join(char for char in elemento if char.isalnum() or char == " ") # Caracter especial
                    tabla.loc[n, columna] = str(elemento)
    print("Sp terminado")


def formato_tlf(df:pd.DataFrame):
    columna = df["Usuarios"]["TELEFONO"]
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


def no_duplicates(df: pd.DataFrame):
    for tabla_n in df:
        if tabla_n == "meteo24":
            continue
        else:
            columnas_sin_primary = list(df[tabla_n].columns)
            primary_key = columnas_sin_primary.pop(0)
            # quitar las filas que repitan todo menos la primary key
            df[tabla_n] = df[tabla_n].drop_duplicates(subset=columnas_sin_primary, keep="first")
            # quitar las filas que repitan la primary key
            df[tabla_n] = df[tabla_n].drop_duplicates(subset=[primary_key], keep="first")
        
def adjust_gps(df: pd.DataFrame)-> None:
    """ Function that cleans GPS data."""
    # check if lat in [-90, 90] and long in [-180, 180]
    lat_area = df["Areas"]["LATITUD"]
    long_area = df["Areas"]["LONGITUD"]
    lat_juego = df["Juegos"]["LATITUD"]
    long_juego = df["Juegos"]["LONGITUD"]
    # if value is wrong the value chosen is the median
    for i in range(len(lat_area)):
        if abs(lat_area[i]) > 90:
            lat_area[i] = lat_area.median() 
    for i in range(len(long_area)):
        if abs(long_area[i]) > 180:
            long_area[i] = long_area.median()
    for i in range(len(lat_juego)):
        if abs(lat_juego[i]) > 90:
            lat_juego[i] = lat_juego.median()
    for i in range(len(long_area)):
        if abs(long_juego[i]) > 180:
            long_juego[i] = long_juego.median()            
    # adjust areas
    lat_area = lat_area.apply(lambda x: "{:3.6f}".format(x))
    long_area = long_area.apply(lambda x: "{:3.6f}".format(x))
    # adjust Juegos
    lat_juego = lat_juego.apply(lambda x: "{:3.6f}".format(x))
    long_juego = long_juego.apply(lambda x: "{:3.6f}".format(x))

def adjust_ETRS89(df: pd.DataFrame)-> None:
        """This function converts the ETRS89 data to GPS coordinates. """
        x_coord_area = df["Areas"]["COORD_GIS_X"]
        y_coord_area = df ["Areas"]["COORD_GIS_Y"]
        x_coord_juegos = df["Juegos"]["COORD_GIS_X"]
        y_coord_juegos= df ["Juegos"]["COORD_GIS_Y"]
        
        # adjust area
        x_coord_area = x_coord_area.apply(lambda x: "{:3.3f}".format(x % 180))
        y_coord_area = y_coord_area.apply(lambda x: "{:3.3f}".format(x % 90))
        
        #adjust juegos
        x_coord_juegos = x_coord_juegos.apply(lambda x: "{:3.3f}".format(x % 180))
        y_coord_juegos = y_coord_juegos.apply(lambda x: "{:3.3f}".format(x % 90))
        
        for item in y_coord_juegos:
            print(item)

def enum_checker(db: pd.DataFrame):
    posiciones_borrar = []
    for n_tabla in db:
        tabla = db[n_tabla]
        for n_columna in tabla:
            if n_tabla == "Juegos" and n_columna == "ESTADO":
                columna = tabla[n_columna]
                for i in range (len(columna)):
                    if tabla[columna[i]] != "OPERATIVO":
                        posiciones_borrar.append[i]
            elif n_tabla == "Areas" and n_columna == "ESTADO":
                columna = tabla[n_columna]
                for i in range (len(columna)):
                    if tabla[columna[i]] != "OPERATIVO":
                        posiciones_borrar.append[i]
        
    
# Pruebas
base = load.load_db()
print(base)

empty_data(base)
# delete_special(base)
# formato_tlf(base)
# reformatear_fecha(base, "Mantenimiento", "FECHA_INTERVENCION")
# adjust_gps(base)
# adjust_ETRS89(base)
# print(base)