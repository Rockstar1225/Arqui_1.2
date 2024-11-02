import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn', de StackOverflow
import load
from datetime import datetime
from dateutil import parser


# capitalizar una columna entera
def capitalize_column(df: pd.DataFrame, table_name:str, colname: str) -> pd.DataFrame:
    df[table_name][colname] =  df[table_name][colname].apply(lambda x: x.upper())

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



import pandas as pd

# Optimización para rellenar filas vacías
def empty_data(df_dict):
    for tabla_name, tabla in df_dict.items():
        # Convertir a tipo 'object' una vez
        tabla = tabla.astype(object)

        # Identificar posiciones NaN
        nan_positions = tabla.isna()

        # Diccionario para almacenar asignaciones
        assignment_dict = {}

        for columna in nan_positions.columns:
            nan_indices = nan_positions.index[nan_positions[columna]]

            for i in nan_indices:
                tachadas = [tabla_name]
                id_val = find_id(df_dict, tabla_name, i)  # Obtener una vez el id
                valor = None
                
                while True:
                    new_tab = find_table_by_column(df_dict, tachadas, columna)
                    if new_tab is None:
                        valor = f"{id_val}-{columna}-ausente"
                        break
                    valor = take_atribute(df_dict, new_tab, columna, id_val)
                    if valor is not None:
                        break
                    tachadas.append(new_tab)

                # Añadir al diccionario de asignación
                if columna not in assignment_dict:
                    assignment_dict[columna] = {}
                assignment_dict[columna][i] = valor

        # Realizar las asignaciones en bloque usando el diccionario de asignación
        for columna, valores in assignment_dict.items():
            tabla.loc[valores.keys(), columna] = list(valores.values())

        # Actualizar la tabla en el diccionario original (si no es una copia)
        df_dict[tabla_name] = tabla

    print("Emp terminado")




def reformatear_fecha(df: pd.DataFrame, table_name: str, column_name: str): #ChatGPT
    archivo = df[table_name]
    fechas_nuevas = []
    for fecha in archivo[column_name]:
        try:
            f_formt = parser.parse(fecha)
        except (ValueError, TypeError):
            f_formt = pd.NaT
        fechas_nuevas.append(f_formt)
    archivo[column_name] = fechas_nuevas

def delete_special(df: pd.DataFrame):
    lista_tildes = ["DESC_CLASIFICACION", "BARRIO", "DISTRITO", "NOMBRE", "TIPO_INCIDENTE", "GRAVEDAD", "TIPO_INTERVENCION"]
    # Diccionario para reemplazar letras con tildes
    replacements = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}
    for tabla_n in df:
        tabla = df[tabla_n]
        for columna in tabla:
            if columna in lista_tildes:
                for accented_char, unaccented_char in replacements.items():
                    tabla[columna] = tabla[columna].str.replace(accented_char, unaccented_char)
                tabla[columna] = tabla[columna].str.replace(r'[^a-zA-Z0-9 ñÑ-]', '', regex=True)
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
    # with too much precisions games can never belong to an area
    df["Areas"]["LATITUD"] = df["Areas"]["LATITUD"].apply(lambda x: "{:3.3f}".format(x))
    df["Areas"]["LONGITUD"] = df["Areas"]["LONGITUD"].apply(lambda x: "{:3.3f}".format(x))
    # adjust Juegos
    df["Juegos"]["LATITUD"] = df["Juegos"]["LATITUD"].apply(lambda x: "{:3.3f}".format(x))
    df["Juegos"]["LONGITUD"] = df["Juegos"]["LONGITUD"].apply(lambda x: "{:3.3f}".format(x))
    
    print("Adjust GPS completed")

def adjust_ETRS89(df: pd.DataFrame)-> None:
        """This function converts the ETRS89 data to GPS coordinates. """
        
        # adjust area
        df["Areas"]["COORD_GIS_X"] = df["Areas"]["COORD_GIS_X"].apply(lambda x: "{:3.3f}".format(x % 180))
        df["Areas"]["COORD_GIS_Y"] = df["Areas"]["COORD_GIS_Y"].apply(lambda x: "{:3.3f}".format(x % 90))
        
        #adjust juegos
        df["Juegos"]["COORD_GIS_X"] = df["Juegos"]["COORD_GIS_X"].apply(lambda x: "{:3.3f}".format(x % 180))
        df["Juegos"]["COORD_GIS_Y"] = df["Juegos"]["COORD_GIS_Y"].apply(lambda x: "{:3.3f}".format(x % 90))
        

def enum_checker(db: pd.DataFrame):
    for n_tabla in db:
        tabla = db[n_tabla]
        for n_columna in tabla:
            posiciones_borrar = []
            if n_tabla == "Areas" and n_columna == "ESTADO":
                columna = tabla[n_columna]
                for i in range (len(columna)):
                    if tabla[n_columna][i] != "OPERATIVO":
                        posiciones_borrar.append(i)
            elif n_tabla == "Juegos" and n_columna == "ESTADO":
                columna = tabla[n_columna]
                for i in range (len(columna)):
                    if tabla[n_columna][i] != "OPERATIVO" and tabla[n_columna][i] != "REPARACION":
                        posiciones_borrar.append(i)
            elif n_tabla == "Incidencias" and n_columna == "TIPO_INCIDENCIA":
                columna = tabla[n_columna]
                for i in range (len(columna)):
                    if tabla[n_columna][i] != "DESGASTE" and tabla[n_columna][i] != "ROTURA" and tabla[n_columna][i] != "VANDALISMO" and tabla[n_columna][i] != "MAL FUNCIONAMIENTO":
                        posiciones_borrar.append(i)
            elif n_tabla == "Incidencias" and n_columna == "ESTADO":
                columna = tabla[n_columna]
                for i in range (len(columna)):
                    if tabla[n_columna][i] != "ABIERTA" and tabla[n_columna][i] != "CERRADA":
                        posiciones_borrar.append(i)
            elif n_tabla == "Mantenimiento" and n_columna == "TIPO_INTERVENCION":
                columna = tabla[n_columna]
                for i in range (len(columna)):
                    if tabla[n_columna][i] != "CORRECTIVO" and tabla[n_columna][i] != "EMERGENCIA"  and tabla[n_columna][i] != "PREVENTIVO" :
                        posiciones_borrar.append(i)
            elif n_tabla == "Mantenimiento" and n_columna in ["ESTADO_PREVIO", "ESTADO_POSTERIOR"]:
                columna = tabla[n_columna]
                for i in range (len(columna)):
                    if tabla[n_columna][i] != "MALO" and tabla[n_columna][i] != "REGULAR"  and tabla[n_columna][i] != "BUENO" :
                        print("f")
                        posiciones_borrar.append(i)
            elif n_tabla == "Incidentes" and n_columna == "TIPO_INCIDENTE":
                columna = tabla[n_columna]
                for i in range (len(columna)):
                    if tabla[n_columna][i] != "ROBO" and tabla[n_columna][i] != "CAIDA" and tabla[n_columna][i] != "VANDALISMO" and tabla[n_columna][i] != "ACCIDENTE" and tabla[n_columna][i] != "DAÑO ESTRUCTURAL":
                        posiciones_borrar.append(i)
            elif n_tabla == "Incidentes" and n_columna == "GRAVEDAD":
                columna = tabla[n_columna]
                for i in range (len(columna)):
                    if tabla[n_columna][i] != "ALTA" and tabla[n_columna][i] != "BAJA" and tabla[n_columna][i] != "MEDIA" and tabla[n_columna][i] != "CRITICA":
                        posiciones_borrar.append(i)
            tabla.drop(posiciones_borrar)

def nif_status(db:pd.DataFrame):
    columna = db["Usuarios"]["NIF"]
    posiciones_borrar = []
    for i in range(len(columna)):
        elemento = columna[i]
        if "-" not in elemento:
            posiciones_borrar.append(i)
        else:
            lista = elemento.split("-")
            if len(lista) != 3:
                posiciones_borrar.append(i)
            else:
                if not lista[0].isdigit() or lista[1].isdigit() or lista[2].isdigit():
                    posiciones_borrar.append(i)
    db["Usuarios"].drop(posiciones_borrar)

def check_id(db: pd.DataFrame):
    lista = ["Areas", "Juegos", "Encuestas", "Incidencias", "Incidentes", "Mantenimiento"]
    for nombre in lista:
        columna = db[nombre]["ID"]
        posiciones_borrar = []
        if nombre == "Mantenimiento":
            for n in range(len(columna)):
                expected = '"-' + str(n+1) + ',00 MNT"'
                if expected != columna[n]:
                    posiciones_borrar.append(n)
        else:
            for n in range(len(columna)):
                if not isinstance(columna[n], int):
                    posiciones_borrar.append(n)
        db[nombre].drop(posiciones_borrar)
 
    
# Pruebas
base = load.load_db()
capitalize_column(base, "Areas", "ESTADO")
capitalize_column(base, "Juegos", "ESTADO")
capitalize_column(base, "Incidencias", "TIPO_INCIDENCIA")
capitalize_column(base, "Incidencias", "ESTADO")
capitalize_column(base, "Mantenimiento", "TIPO_INTERVENCION")
capitalize_column(base, "Mantenimiento", "ESTADO_PREVIO")
capitalize_column(base, "Mantenimiento", "ESTADO_POSTERIOR")
capitalize_column(base, "Incidentes", "TIPO_INCIDENTE")
capitalize_column(base, "Incidentes", "GRAVEDAD")
empty_data(base)
delete_special(base)
enum_checker(base)
formato_tlf(base)
check_id(base)
nif_status(base)
reformatear_fecha(base, "Mantenimiento", "FECHA_INTERVENCION")
# adjust_gps(base)
# adjust_ETRS89(base)
print(base)