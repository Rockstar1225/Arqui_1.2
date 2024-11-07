import pandas as pd
import datetime as dt
from dateutil import parser


# capitalizar una columna entera
def capitalize_column(df: dict, table_name: str, colname: str) -> None:
    df[table_name][colname] = df[table_name][colname].apply(lambda x: x.upper())


# Encontrar un dato en una tabla si su id es igual al pasado por argumento
def take_atribute(df: dict, tabla: str, columna: str, id: int) -> str | None:
    archivo = df[tabla]
    fila = None
    for i in range(len(archivo["ID"])):
        valor = archivo["ID"][i]
        if id == valor:
            fila = i
            return archivo[columna][fila]
    return None


# Encuentra una tabla sin contar las tachadas que contenga una columna con el mismo nombre que la pasada por argumento
def find_table_by_column(df: dict, tablas_tachadas: list, column: str) -> str | None:
    for tabla in df:
        if tabla not in tablas_tachadas:
            t_analizar = df[tabla]
            if column in t_analizar:
                return tabla
    return None


#Encuentra un id según que tabla (hay columnas ID que no se llaman ID) y que fila
def find_id(df: dict, tabla: str, fila: int):
    archivo = df[tabla]
    if tabla == "Usuarios": return archivo["NIF"][fila]
    elif tabla == "meteo24": return archivo["PROVINCIA"][fila]
    elif tabla == "Codigo": return archivo["CÓDIGO"][fila]
    else: return archivo["ID"][fila]


# Para rellenar filas vacías
def empty_data(df_dict):
    for tabla_name, tabla in df_dict.items():
        # Convertir a tipo 'object' para poder indicar los casos nulos que no se pueden modificar
        tabla = tabla.astype(object)
        nan_positions = tabla.isna() # Identificar posiciones NaN
        assignment_dict = {} # Diccionario para almacenar asignaciones

        for columna in nan_positions.columns:
            nan_indices = nan_positions.index[nan_positions[columna]]
            for i in nan_indices:
                valor = aux_dir(tabla_name, tabla, columna, i)
                if valor is None:
                    tachadas = [tabla_name]
                    id_val = find_id(df_dict, tabla_name, i)  # Obtener una vez el id
                    while True:
                        new_tab = find_table_by_column(df_dict, tachadas, columna)
                        if new_tab is None:
                            if columna in ["FECHA_INSTALACION", "FECHA", "FECHA_REPORTE", "FECHA_INTERVENCION"]:
                                valor = dt.datetime.strptime( "2018-12-31 00:00:00", "%Y-%m-%d %H:%M:%S")
                            else:
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


def aux_dir(tabla_name, tabla, columna, i):
    if tabla_name in ["Areas", "Juegos"] and columna in [
        "TIPO_VIA",
        "NOM_VIA",
        "NUM_VIA",
    ]:
        if not pd.isna(tabla["DIRECCION_AUX"][i]):
            lista = tabla["DIRECCION_AUX"][i].split(" ")
            via = None
            n = 0
            if "·" in lista:
                via = lista[2]
                n = 3
            else:
                via = lista[0]
            nombre, numero = "", ""
            while n < len(lista):
                if lista[n].isdigit():
                    numero = lista[n]
                    break
                if lista[n] == ",":
                    break
                nombre += lista[n]
                n += 1
            if columna == "TIPO_VIA":
                return via
            elif columna == "NOM_VIA":
                return nombre
            else:
                return numero
    return None


def reformatear_fecha(df: dict, table_name: str, column_name: str):
    tablas = [
        "Areas",
        "Encuestas",
        "Incidencias",
        "Incidentes",
        "Juegos",
        "Mantenimiento",
        "meteo24",
    ]
    columnas = ["FECHA_INSTALACION", "FECHA", "FECHA_REPORTE", "FECHA_INTERVENCION"]
    if table_name in tablas and column_name in columnas:
        archivo = df[table_name]
        fechas_nuevas = []
        for fecha in archivo[column_name]:
            try:
                f_formt = parser.parse(fecha)
                f_formt.strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                f_formt = dt.datetime.strptime(
                    "2018-12-31 00:00:00", "%Y-%m-%d %H:%M:%S"
                )
            fechas_nuevas.append(f_formt)
        archivo[column_name] = fechas_nuevas


def delete_special(df: dict):
    lista_tildes = [
        "DESC_CLASIFICACION",
        "BARRIO",
        "DISTRITO",
        "NOMBRE",
        "TIPO_INCIDENTE",
        "GRAVEDAD",
        "TIPO_INTERVENCION",
        "DIRECCION_AUX",
    ]
    # Diccionario para reemplazar letras con tildes
    replacements = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "Á": "A",
        "É": "E",
        "Í": "I",
        "Ó": "O",
        "Ú": "U",
    }
    for tabla_n in df:
        tabla = df[tabla_n]
        for columna in tabla:
            if columna in lista_tildes:
                for accented_char, unaccented_char in replacements.items():
                    tabla[columna] = tabla[columna].str.replace(
                        accented_char, unaccented_char
                    )
                tabla[columna] = tabla[columna].str.replace(
                    r"[^a-zA-Z0-9 ñÑ-]", "", regex=True
                )
    print("Sp terminado")


def formato_tlf(df: dict):
    columna = df["Usuarios"]["TELEFONO"]
    for i in range(len(columna)):
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


def no_duplicates(df: dict):
    for tabla_n in df:
        if tabla_n == "meteo24" or tabla_n == "Codigo":
            continue
        else:
            columnas_sin_primary = list(df[tabla_n].columns)
            primary_key = columnas_sin_primary.pop(0)
            # quitar las filas que repitan todo menos la primary key
            df[tabla_n] = df[tabla_n].drop_duplicates(
                subset=columnas_sin_primary, keep="first"
            )
            # quitar las filas que repitan la primary key
            df[tabla_n] = df[tabla_n].drop_duplicates(
                subset=[primary_key], keep="first"
            )


def adjust_gps(df: dict) -> None:
    """Function that cleans GPS data."""
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
    df["Areas"]["LONGITUD"] = df["Areas"]["LONGITUD"].apply(
        lambda x: "{:3.3f}".format(x)
    )
    # adjust Juegos
    df["Juegos"]["LATITUD"] = df["Juegos"]["LATITUD"].apply(
        lambda x: "{:3.3f}".format(x)
    )
    df["Juegos"]["LONGITUD"] = df["Juegos"]["LONGITUD"].apply(
        lambda x: "{:3.3f}".format(x)
    )

    print("Adjust GPS completed")


def adjust_ETRS89(df: dict) -> None:
    """This function converts the ETRS89 data to GPS coordinates."""

    # adjust area
    df["Areas"]["COORD_GIS_X"] = df["Areas"]["COORD_GIS_X"].apply(
        lambda x: "{:3.3f}".format(x % 180)
    )
    df["Areas"]["COORD_GIS_Y"] = df["Areas"]["COORD_GIS_Y"].apply(
        lambda x: "{:3.3f}".format(x % 90)
    )

    # adjust juegos
    df["Juegos"]["COORD_GIS_X"] = df["Juegos"]["COORD_GIS_X"].apply(
        lambda x: "{:3.3f}".format(x % 180)
    )
    df["Juegos"]["COORD_GIS_Y"] = df["Juegos"]["COORD_GIS_Y"].apply(
        lambda x: "{:3.3f}".format(x % 90)
    )


def enum_checker(db: dict):
    for n_tabla in db:
        tabla = db[n_tabla]
        for n_columna in tabla:
            new_columna = []
            columna = tabla[n_columna]

            if n_tabla == "Areas" and n_columna == "ESTADO":
                for valor in columna:
                    if valor != "OPERATIVO":
                        new_columna.append(None)
                    else:
                        new_columna.append(valor)

            elif n_tabla == "Juegos" and n_columna == "ESTADO":
                for valor in columna:
                    if valor not in ["OPERATIVO, REPARACION"]:
                        new_columna.append(None)
                    else:
                        new_columna.append(valor)

            elif n_tabla == "Incidencias" and n_columna == "TIPO_INCIDENCIA":
                for valor in columna:
                    if valor not in [
                        "DESGASTE",
                        "ROTURA",
                        "VANDALISMO",
                        "MAL FUNCIONAMIENTO",
                    ]:
                        new_columna.append(None)
                    else:
                        new_columna.append(valor)

            elif n_tabla == "Incidencias" and n_columna == "ESTADO":
                for valor in columna:
                    if valor not in ["ABIERTA", "CERRADA"]:
                        new_columna.append(None)
                    else:
                        new_columna.append(valor)

            elif n_tabla == "Mantenimiento" and n_columna == "TIPO_INTERVENCION":
                for valor in columna:
                    if valor not in ["CORRECTIVO", "EMERGENCIA", "PREVENTIVO"]:
                        new_columna.append(None)
                    else:
                        new_columna.append(valor)

            elif n_tabla == "Mantenimiento" and n_columna in [
                "ESTADO_PREVIO",
                "ESTADO_POSTERIOR",
            ]:
                for valor in columna:
                    if valor not in ["MALO", "REGULAR", "BUENO"]:
                        new_columna.append(None)
                    else:
                        new_columna.append(valor)

            elif n_tabla == "Incidentes" and n_columna == "TIPO_INCIDENTE":
                for valor in columna:
                    if valor not in [
                        "ROBO",
                        "CAIDA",
                        "VANDALISMO",
                        "ACCIDENTE",
                        "DAÑO ESTRUCTURAL",
                    ]:
                        new_columna.append(None)
                    else:
                        new_columna.append(valor)

            elif n_tabla == "Incidentes" and n_columna == "GRAVEDAD":
                for valor in columna:
                    if valor not in ["ALTA", "BAJA", "MEDIA", "CRITICA"]:
                        new_columna.append(None)
                    else:
                        new_columna.append(valor)

            if len(new_columna) > 0:
                tabla[n_columna] = new_columna
                tabla.dropna(subset=n_columna)


def nif_status(db: dict):
    columna = db["Usuarios"]["NIF"]
    new_columna = []
    for elemento in columna:
        if "-" not in elemento:
            new_columna.append(None)
        else:
            lista = elemento.split("-")
            if len(lista) != 3:
                new_columna.append(None)
            else:
                if (
                    not lista[0].isdigit()
                    or not lista[1].isdigit()
                    or not lista[2].isdigit()
                ):
                    new_columna.append(None)
                else:
                    new_columna.append(elemento)
    db["Usuarios"]["NIF"] = new_columna
    db["Usuarios"].dropna(subset=["NIF"])


def check_id(db: dict):
    lista = [
        "Areas",
        "Juegos",
        "Encuestas",
        "Incidencias",
        "Incidentes",
        "Mantenimiento",
    ]
    for nombre in lista:
        columna = db[nombre]["ID"]
        new_columna = []
        if nombre == "Mantenimiento":
            n = 1
            for valor in columna:
                expected = f"-{n},00\xa0MNT"
                if expected != valor:
                    new_columna.append(None)
                else:
                    valor = f"-{n} MNT"
                    new_columna.append(valor)
                n += 1
        else:
            for valor in columna:
                if not isinstance(valor, int):
                    new_columna.append(None)
                else:
                    new_columna.append(valor)
        db[nombre]["ID"] = new_columna
        db[nombre].dropna(subset=["ID"])


def incidencias_status(db: dict):
    # Crear copias de los conjuntos de búsqueda para optimizar el acceso
    ids = set(db["Mantenimiento"]["ID"])
    nifs = set(db["Usuarios"]["NIF"])

    # Crear una copia del DataFrame "Incidencias"
    tabla = db["Incidencias"].copy()

    # Procesar la columna "MantenimientoID"
    mantenimiento_ids = []
    for valor in tabla["MantenimientoID"]:
        if valor.startswith("[") and valor.endswith("]"):
            contenido = valor[1:-1]
            partes = contenido.split(", ")
            partes_filtradas = []
            for parte in partes:
                if (
                    parte.startswith("'MNT-")
                    and parte.endswith("'")
                    and parte[5:-1].isdigit()
                ):
                    numero = str(
                        int(parte[5:-1])
                    )  # Convertir a entero y luego a cadena para quitar ceros iniciales
                    expected = f"-{numero} MNT"
                    if expected in ids:
                        partes_filtradas.append(expected)
            if partes_filtradas:
                mantenimiento_ids.append(f"[{', '.join(partes_filtradas)}]")
            else:
                mantenimiento_ids.append(None)
        else:
            mantenimiento_ids.append(None)

    # Asignar los valores filtrados a la columna "MantenimientoID"
    tabla["MantenimientoID"] = mantenimiento_ids

    # Eliminar las filas con valores None en "MantenimientoID"
    tabla = tabla.dropna(subset=["MantenimientoID"])

    # Procesar la columna "UsuarioID"
    usuario_ids = []
    for valor in tabla["UsuarioID"]:
        if valor.startswith("[") and valor.endswith("]"):
            contenido = valor[1:-1]
            partes = contenido.split(", ")
            partes_filtradas = [parte for parte in partes if parte[1:-1] in nifs]
            if partes_filtradas:
                usuario_ids.append(f"[{', '.join(partes_filtradas)}]")
            else:
                usuario_ids.append(None)
        else:
            usuario_ids.append(None)

    # Asignar los valores filtrados a la columna "UsuarioID"
    tabla["UsuarioID"] = usuario_ids

    # Eliminar las filas con valores None en "UsuarioID"
    tabla = tabla.dropna(subset=["UsuarioID"])

    # Asignar el DataFrame modificado de nuevo en el DataFrame original
    db["Incidencias"] = tabla


# Pruebas
"""base = load.load_db()
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
incidencias_status(base)
# adjust_gps(base)
# adjust_ETRS89(base)
print(base)"""
