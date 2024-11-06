import pandas as pd
import load
import change
import numpy as np
import random


def check_list(elemento: str, codes) -> list | None:
    if "_" not in elemento:
        return None
    data = elemento.split("_")
    if len(data) != 3:
        return None
    if not data[0].isdigit() or not data[1].isdigit():
        return None
    if data[0] not in codes.keys() or data[1] not in ["81", "83", "89"]:
        return None
    return data


def same_line(fecha: str, distrito: str, list_f: list, list_d: list) -> int:
    if fecha not in list_f or distrito not in list_d:
        return -1
    for n in range(0, len(list_f)):
        if list_f[n] == fecha and list_d[n] == distrito:
            return n
    return -1


def post_code(db: pd.DataFrame, codigo: int):
    code_id = db["Codigo"]["CÓDIGO"]
    for n in range(len(code_id)):
        if str(code_id[n]) == str(codigo):
            print(n)
            return n
    return -1


def new_meteo(db: pd.DataFrame):
    meteo = db["meteo24"]
    m_postal = db["Codigo"]
    col_postal = m_postal["CodigoPostal"]
    print(col_postal)
    codes = {
        "28079102": "MORATALAZ",
        "28079103": "VILLAVERDE",
        "28079104": "PUENTE DE VALLECAS",
        "28079106": "MONCLOA-ARAVACA",
        "28079107": "HORTALEZA",
        "28079108": "FUENCARRAL-EL PARDO",
        "28079109": "CHAMBERI",
        "28079110": "CENTRO",
        "28079111": "CHAMARTIN",
        "28079112": "VILLA DE VALLECAS",
        "28079113": "VILLA DE VALLECAS",
        "28079114": "ARGANZUELA",
        "28079115": "ARGANZUELA",
        "28079004": "MONCLOA-ARAVACA",
        "28079008": "SALAMANCA",
        "28079016": "CIUDAD LINEAL",
        "28079018": "CARABANCHEL",
        "28079024": "MONCLOA-ARAVACA",
        "28079035": "CENTRO",
        "28079036": "MORATALAZ",
        "28079038": "TETUAN",
        "28079039": "FUENCARRAL-EL PARDO",
        "28079054": "VILLA DE VALLECAS",
        "28079056": "CARABANCHEL",
        "28079058": "FUENCARRAL-EL PARDO",
        "28079059": "BARAJAS",
    }
    meses = {
        "1": 31,
        "2": 28,
        "3": 31,
        "4": 30,
        "5": 31,
        "6": 30,
        "7": 31,
        "8": 31,
        "9": 30,
        "10": 31,
        "11": 30,
        "12": 31,
    }
    ids = []
    codigo_postal = []
    distritos = []
    temperaturas = []
    precipitaciones = []
    viento = []
    fechas = []
    id = 1
    for i in range(len(meteo["PUNTO_MUESTREO"])):
        elemento = meteo["PUNTO_MUESTREO"][i]
        data = check_list(elemento, codes)
        if data is not None and str(meteo["MES"][i]) in meses.keys():
            for j in range(meteo["MES"][i]):
                dia = str(j + 1)
                mes = str(meteo["MES"][i])
                if j < 9:
                    dia = "0" + dia
                if int(mes) < 10:
                    mes = "0" + mes
                fecha = str(meteo["ANO"][i]) + "-" + mes + "-" + dia
                n_code = post_code(db, data[0])
                if n_code != -1:
                    linea = same_line(fecha, codes[data[0]], fechas, distritos)
                    if linea == -1:
                        ids.append(id)
                        id += 1
                        print(codigo_postal)
                        pcode = col_postal[n_code]
                        codigo_postal.append(int(pcode))
                        distritos.append(codes[data[0]])
                        fechas.append(fecha)
                        temperaturas.append(float("NaN"))
                        precipitaciones.append(float("NaN"))
                        viento.append(float("NaN"))
                        linea = len(distritos) - 1
                        if data[0] == "28079004":
                            ids.append(id)
                            id += 1
                            distritos.append(codes[data[0]])
                            pcode = col_postal[n_code + 1]
                            codigo_postal.append(int(pcode))
                            fechas.append(fecha)
                            temperaturas.append(float("NaN"))
                            precipitaciones.append(float("NaN"))
                            viento.append(float("NaN"))
                    booleano = "V" + dia
                    valor = "D" + dia
                    if data[1] == "81":
                        if meteo[booleano][i] == "V" and int(meteo[valor][i]) >= 20:
                            viento[linea] = True
                            if data[0] == "28079004":
                                viento[linea + 1] = True
                        else:
                            viento[linea] = False
                            if data[0] == "28079004":
                                viento[linea + 1] = False
                    elif data[1] == "83":
                        if meteo[booleano][i] == "V":
                            temperaturas[linea] = meteo[valor][i]
                            if data[0] == "28079004":
                                temperaturas[linea + 1] = meteo[valor][i]
                    else:
                        if meteo[booleano][i] == "V":
                            precipitaciones[linea] = meteo[valor][i]
                            if data[0] == "28079004":
                                precipitaciones[linea + 1] = meteo[valor][i]

    nuevo = pd.DataFrame()
    nuevo.loc[:, "ID"] = ids
    nuevo.loc[:, "CODIGO_POSTAL"] = codigo_postal
    nuevo.loc[:, "FECHA"] = fechas
    nuevo.loc[:, "TEMPERATURA"] = temperaturas
    nuevo.loc[:, "PRECIPITACION"] = precipitaciones
    nuevo.loc[:, "VIENTO"] = viento
    nuevo.loc[:, "DISTRITO"] = distritos
    db["meteo24"] = nuevo


def area_new_atribute(df: pd.DataFrame):
    """Method used for adding the atribute capacidadMax in Areas."""
    df["Juegos"]["AreaRecreativaID"] = 0
    index = 0
    # calculate number of games per area using lat and long
    # create column
    for area in df["Areas"].to_numpy():
        # number of games
        games = 0
        # serch by GPS
        lat_area = area[10]
        long_area = area[11]
        index_juego = 0
        for juego in df["Juegos"].to_numpy():
            lat_juego = juego[10]
            long_juego = juego[11]
            # match area, juego
            if lat_area == lat_juego and long_area == long_juego:
                # add games
                games += 1
                # insert areaID to Juegos
                df["Juegos"].loc[index_juego, "AreaRecreativaID"] = area[0]
            index_juego += 1
        # create columns
        df["Areas"].loc[index, "capacidadMax"] = games
        index += 1
    # give values to all games without a reference to an area
    index_juego = 0
    for juego in df["Juegos"].to_numpy():
        ref_area = juego[24]
        # there is no reference to an area
        if ref_area == 0:
            in_column = True
            while in_column:
                # insert a random reference to juegos
                rand_id = random.randint(1000000, 100000000)
                if rand_id not in df["Juegos"]["AreaRecreativaID"]:
                    df["Juegos"].loc[index_juego, "AreaRecreativaID"] = rand_id
                    in_column = False
        index_juego += 1

    print("New atribute Areas completed")


def juegos_new_atributes(df: pd.DataFrame):
    """This function will add indicadorExposicion and desgasteAcumulado to juegos"""
    # insert indicador exposicion value
    indicador_options = {"BAJO": 100, "MEDIO": 200, "ALTO": 300}
    for i in range(len(df["Juegos"])):
        selected_option = random.randint(0, 2)
        df["Juegos"].loc[i, "indicadorExposicion"] = list(indicador_options.keys())[
            selected_option
        ]
    # calculate desgasteAcumulado value
    index = 0
    wear_values = []
    for juego in df["Juegos"].to_numpy():
        # number of maintenance to game
        num_mant_juego = 0
        # random usage time between 1 and 15 years
        use_time = random.randint(1, 15)
        for maintenance in df["Mantenimiento"].to_numpy():
            if juego[0] == maintenance[5]:
                num_mant_juego += 1
        # adding wear value to a list to change its range
        wear_value = (
            use_time * indicador_options[df["Juegos"]["indicadorExposicion"][index]]
        ) - (num_mant_juego * 100)
        wear_values.append(wear_value)
        index += 1
    # insert desgasteAcumulado value
    for i in range(len(df["Juegos"])):
        df["Juegos"].loc[i, "desgasteAcumulado"] = adjust_range(
            wear_values, 0, 100, i
        )  # changing the range of values
    print("New atributes Juegos completed")


def adjust_range(values: list, new_min: int, new_max: int, index: int) -> int:
    old_min = min(values)
    old_max = max(values)
    new_value = int(
        (((values[index] - old_min) * (new_max - new_min)) / (old_max - old_min))
        + new_min
    )
    return new_value


def takeTimebyID(base: pd.DataFrame, id: str):
    numero = int(id[1:-4])
    lista = base["Mantenimiento"]["ID"]
    if numero < len(lista):
        return base["Mantenimiento"]["FECHA_INTERVENCION"][numero]
    return None


def tiempoResolucion(base: pd.DataFrame):
    col_index = base["Incidencias"]["MantenimientoID"]
    tiempos = []
    for n in range(len(col_index)):
        elemento = col_index[n]
        conjunto = elemento[1:-1]
        conjunto = conjunto.split(", ")
        tiempo = float(0)
        fecha_incidencia = base["Incidencias"]["FECHA_REPORTE"][n]
        for valor in conjunto:
            fecha_mat = takeTimebyID(base, valor)
            if fecha_mat != None and fecha_mat > fecha_incidencia:
                sub_t = fecha_mat - fecha_incidencia

                # Convertir sub_t a segundos para poder compararlo con el valor float 'tiempo'
                sub_t_seconds = sub_t.total_seconds()
                if sub_t_seconds > tiempo:
                    tiempo = sub_t_seconds
        if tiempo != 0:
            tiempo = tiempo // (60 * 60 * 24)
        tiempos.append(tiempo)
    base["Incidencias"].loc[:, "TIEMPO_RESOLUCION"] = tiempos


def lastFecha(db: pd.DataFrame):
    # Seleccionamos el último mantenimiento para cada juego en la tabla de mantenimiento
    max_mant = (
        db["Mantenimiento"]
        .groupby("JuegoID")["FECHA_INTERVENCION"]
        .max()
        .reset_index()
        .rename(columns={"FECHA_INTERVENCION": "ULTIMA_FECHA_MANTENIMIENTO"})
    )

    # Fusionamos las fechas de mantenimiento con la tabla de juegos
    db["Juegos"] = db["Juegos"].merge(
        max_mant, left_on="ID", right_on="JuegoID", how="left"
    )

    # Rellenamos con FECHA_INSTALACION en caso de que no haya mantenimientos
    db["Juegos"]["ULTIMA_FECHA_MANTENIMIENTO"].fillna(
        db["Juegos"]["FECHA_INSTALACION"], inplace=True
    )


def area_meteo(db: pd.DataFrame):
    lista_meteo = []
    tabla_area = db["Areas"]
    tabla_meteo = db["meteo24"]
    columna_cod_postal = tabla_area["COD_POSTAL"]
    columna_cod_meteo = tabla_meteo["CODIGO_POSTAL"]
    for n in range(len(columna_cod_postal)):
        valor = int(columna_cod_postal[n])
        estacion = 00000  # Valor predeterminado
        for m in range(len(columna_cod_meteo)):
            valor2 = int(columna_cod_postal[m])
            if valor == valor2:
                estacion = db["meteo24"]["ID"]
        lista_meteo.append(estacion)
    db["Areas"].loc[:, "ID_METEO"] = lista_meteo


# prueabs
"""base = load.load_db()
# new_meteo(base)
# for i in range(len(base["meteo24"]["FECHA"])):
#     print(base["meteo24"]["FECHA"][i], " ", base["meteo24"]["TEMPERATURA"][i], " ", base["meteo24"]["PRECIPITACION"][i],
#            " ", base["meteo24"]["VIENTO"][i], " ", base["meteo24"]["DISTRITO"][i])
change.adjust_gps(base) 
area_new_atribute(base)
# juegos_new_atributes(base)
# print(base)"""
