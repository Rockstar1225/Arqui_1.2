import pandas as pd
import random


def check_list(elemento: str, codes) -> list | None:
    # verifica si el punto muestreo es correcto
    if "_" not in elemento:
        return None
    data = elemento.split("_")
    if len(data) != 3:
        return None
    if not data[0].isdigit() or not data[1].isdigit():
        return None
    #Sólo se sacan vientos (81), temperaturas (83) y precipitaciones (89)
    if data[0] not in codes.keys() or data[1] not in ["81", "83", "89"]:
        return None
    return data


def same_line(fecha: str, distrito: str, list_f: list, list_d: list) -> int:
    #Identifica una linea donde fecha sea su FECHA y distrito su DISTRITO.
    if fecha not in list_f or distrito not in list_d:
        return -1
    for n in range(0, len(list_f)):
        if list_f[n] == fecha and list_d[n] == distrito:
            return n
    return -1 #Si no hay, devuelve -1


def post_code(db: pd.DataFrame, codigo: int):
    #Identifica si el código postal pasado es igual al de una estación meteorológica.
    code_id = db["Codigo"]["CÓDIGO"]
    for n in range(len(code_id)):
        if str(code_id[n]) == str(codigo):
            return n #Posición dentro de Código
    return -1 #No existe


def new_meteo(db: pd.DataFrame):
    # Modifica totalmente la tabla de meteo24 para que muestre lo que pide el enunciado
    meteo = db["meteo24"]
    m_postal = db["Codigo"] #Lista de códigos postales para la relación área-meteo
    col_postal = m_postal["CodigoPostal"]
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
    } #Diccionario de distritos
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
    } #Diccionario de meses (como la fecha es por día, se necesita saber qué días hay que coger)
    ids = [] #Cada id representa la posición de la fila de forma ordenada
    codigo_postal = [] 
    distritos = [] 
    temperaturas = []
    precipitaciones = []
    viento = []
    fechas = []
    id = 1
    for i in range(len(meteo["PUNTO_MUESTREO"])):
        elemento = meteo["PUNTO_MUESTREO"][i]
        data = check_list(elemento, codes) #Verifica el PUNTO MUESTREO y el MES
        if data is not None and str(meteo["MES"][i]) in meses.keys():
            for j in range(meteo["MES"][i]): #Por cada fecha y distrito, una fila distinta
                dia = str(j + 1)
                mes = str(meteo["MES"][i])
                if j < 9:
                    dia = "0" + dia
                if int(mes) < 10:
                    mes = "0" + mes
                fecha = str(meteo["ANO"][i]) + "-" + mes + "-" + dia
                n_code = post_code(db, data[0]) #Verifica el código postal
                if n_code != -1:
                    # Si no existe una fila con dicha fecha y distrito, se crea una nueva
                    linea = same_line(fecha, codes[data[0]], fechas, distritos)
                    if linea == -1:
                        ids.append(id)
                        id += 1
                        pcode = col_postal[n_code]
                        codigo_postal.append(int(pcode))
                        distritos.append(codes[data[0]])
                        fechas.append(fecha)
                        temperaturas.append("-")
                        precipitaciones.append("-")
                        viento.append(False)
                        linea = len(distritos) - 1
                        if data[0] == "28079004": 
                            #Como Plaza de España tiene dos códigos postales, hay doble inserción
                            ids.append(id)
                            id += 1
                            distritos.append(codes[data[0]])
                            pcode = col_postal[n_code + 1]
                            codigo_postal.append(int(pcode))
                            fechas.append(fecha)
                            temperaturas.append("-")
                            precipitaciones.append("-")
                            viento.append(False)
                            #Aquí se tiene en cuenta la línea anterior
                    booleano = "V" + dia #Para modificar el valor, el booleano debe ser igual a V
                    valor = "D" + dia #Datos a insertar
                    if data[1] == "81":
                        if meteo[booleano][i] == "V" and int(meteo[valor][i]) >= 20:
                            viento[linea] = True
                            if data[0] == "28079004": #Plaza de España -> Doble inserción
                                viento[linea + 1] = True
                        else:
                            viento[linea] = False
                            if data[0] == "28079004": #Plaza de España -> Doble inserción
                                viento[linea + 1] = False
                    elif data[1] == "83":
                        if meteo[booleano][i] == "V":
                            temperaturas[linea] = meteo[valor][i]
                            if data[0] == "28079004": #Plaza de España -> Doble inserción
                                temperaturas[linea + 1] = meteo[valor][i]
                    else:
                        if meteo[booleano][i] == "V":
                            precipitaciones[linea] = meteo[valor][i]
                            if data[0] == "28079004": #Plaza de España -> Doble inserción
                                precipitaciones[linea + 1] = meteo[valor][i]

    nuevo = pd.DataFrame() #Se crea la nueva tabla
    nuevo.loc[:, "ID"] = ids
    nuevo.loc[:, "CODIGO_POSTAL"] = codigo_postal
    nuevo.loc[:, "FECHA"] = fechas
    pd.to_datetime(nuevo['FECHA']).apply(lambda x: x.date())
    nuevo.loc[:, "TEMPERATURA"] = temperaturas
    nuevo.loc[:, "PRECIPITACION"] = precipitaciones
    nuevo.loc[:, "VIENTO"] = viento
    nuevo.loc[:, "DISTRITO"] = distritos
    db["meteo24"] = nuevo


def area_new_atribute(df: pd.DataFrame):
    """Añade el atributo capacidadMax a Areas."""
    df["Juegos"]["AreaRecreativaID"] = 0
    index = 0
    # Calcula el número de juegos por area con lat y long
    for area in df["Areas"].to_numpy(): 
        games = 0 # Número de juegos
         # Buscar por GPS
        lat_area = area[10]
        long_area = area[11]
        index_juego = 0
        for juego in df["Juegos"].to_numpy():
            lat_juego = juego[10]
            long_juego = juego[11]
            # Si coinciden, se suma el núemrod e juegos y se añade el areaID a Juegos
            if lat_area == lat_juego and long_area == long_juego:
                games += 1
                df["Juegos"].loc[index_juego, "AreaRecreativaID"] = area[0]
            index_juego += 1
       # Aquí crea la columna
        df["Areas"].loc[index, "capacidadMax"] = games
        index += 1
    # Añadir valor a los juegos sin áreas
    index_juego = 0
    for juego in df["Juegos"].to_numpy():
        ref_area = juego[24]
        # Si no hay referencia del juego en área
        if ref_area == 0:
            in_column = True
            while in_column:
                # Inserta un valor random no repetido
                rand_id = random.randint(1000000, 100000000)
                if rand_id not in df["Juegos"]["AreaRecreativaID"]:
                    df["Juegos"].loc[index_juego, "AreaRecreativaID"] = rand_id
                    in_column = False
        index_juego += 1


def juegos_new_atributes(df: pd.DataFrame):
    """Añade las columnas indicadorExposicion y desgasteAcumulado a Juegos"""
    # Inserta el valor de indicador exposicion
    indicador_options = {"BAJO": 100, "MEDIO": 200, "ALTO": 300}
    for i in range(len(df["Juegos"])):
        selected_option = random.randint(0, 2)
        df["Juegos"].loc[i, "indicadorExposicion"] = list(indicador_options.keys())[
            selected_option
        ]
    # Calcula el valor de desgasteAcumulado
    index = 0
    wear_values = []
    for juego in df["Juegos"].to_numpy():
        # Número del mantenimiento al juego
        num_mant_juego = 0
        # Uso aleatorio puede ser un entero del 1 al 15
        use_time = random.randint(1, 15)
        for maintenance in df["Mantenimiento"].to_numpy():
            if juego[0] == maintenance[5]:
                num_mant_juego += 1
        # Añadir el wear value a una lista para cambiar su rango
        wear_value = (
            use_time * indicador_options[df["Juegos"]["indicadorExposicion"][index]]
        ) - (num_mant_juego * 100)
        wear_values.append(wear_value)
        index += 1
    # Inserta desgasteAcumulado
    for i in range(len(df["Juegos"])):
        df["Juegos"].loc[i, "desgasteAcumulado"] = adjust_range(
            wear_values, 0, 100, i
        )  # Cambia el rango de sus valores


def adjust_range(values: list, new_min: int, new_max: int, index: int) -> int:
    #Fórmula para ajustar un valor dentro de una lista a unos nuevos límites
    old_min = min(values)
    old_max = max(values)
    new_value = int(
        (((values[index] - old_min) * (new_max - new_min)) / (old_max - old_min))
        + new_min
    )
    return new_value


def takeTimebyID(base: pd.DataFrame, id: str):
    #Coge una fecha de mantenimiento desde su id
    numero = int(id[1:-4])
    lista = base["Mantenimiento"]["ID"]
    if numero < len(lista):
        return base["Mantenimiento"]["FECHA_INTERVENCION"][numero]
    return None


def tiempoResolucion(base: pd.DataFrame):
    #Calcula el tiempo entre la incidencia y el mantenimiento
    col_index = base["Incidencias"]["MantenimientoID"] 
    #Importante: La incidencia debe contener el id de dicho mantenimiento
    tiempos = []
    for n in range(len(col_index)):
        elemento = col_index[n]
        conjunto = elemento[1:-1]
        conjunto = conjunto.split(", ")
        tiempo = float(0) #Tiempo predeterminado
        fecha_incidencia = base["Incidencias"]["FECHA_REPORTE"][n]
        for valor in conjunto:
            fecha_mat = takeTimebyID(base, valor)
            # Al tener ambas fechas, se hace la resta si la de mantenimiento es más tardía que la de la incidencia
            if fecha_mat != None and fecha_mat > fecha_incidencia:
                sub_t = fecha_mat - fecha_incidencia

                # Convertir sub_t a segundos para poder compararlo con el valor float 'tiempo'
                sub_t_seconds = sub_t.total_seconds()
                if sub_t_seconds > tiempo:
                    tiempo = sub_t_seconds
        if tiempo != 0:
            tiempo = tiempo // (60 * 60 * 24)#Pasar a días
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
    #Inserta en Áreas el id de la meteo24 que pertenece
    lista_meteo = [] #Columna de los id de meteo
    tabla_area = db["Areas"] 
    tabla_meteo = db["meteo24"]
    columna_cod_postal = tabla_area["COD_POSTAL"]
    columna_cod_meteo = tabla_meteo["CODIGO_POSTAL"]

    # Crear un diccionario para el mapeo de códigos postales a ID
    codigo_to_id = {
        columna_cod_meteo[i]: tabla_meteo["ID"][i]
        for i in range(len(columna_cod_meteo))
    }

    for valor in columna_cod_postal:
        estacion = 0  # Valor predeterminado

        # Asegurarse de que ambos valores son enteros
        if pd.notnull(valor) and type(valor) is not str:  # Evita valores nulos
            valor = int(valor) if not isinstance(valor, int) else valor
            estacion = codigo_to_id.get(
                valor, estacion
            )  # Obtener el valor o usar predeterminado

        lista_meteo.append(estacion)

    # Asignar la lista resultante a una nueva columna "MeteoID" en db["Areas"]
    db["Areas"]["MeteoID"] = lista_meteo

def nivelEscalamiento(db:pd.DataFrame):
    #Inserta el nivel de escalamiento. Si es abierto -> aleatorio del 1 al 10. Si no, es 1.
    incidencias = db["Incidencias"]
    lista_rec = []
    for n in range(len(incidencias["ESTADO"])):
        if incidencias["ESTADO"][n] == "ABIERTO":
            numero = random.randint(1, 10)
            lista_rec.append(numero)
        else:
            lista_rec.append(1)

    incidencias.loc[:, "NIVEL_RECONOCIMIENTO"] = lista_rec
