import pandas as pd
import load
import change
import numpy as np

def check_list(elemento: str, codes) -> list:
    if "_" not in elemento:
        return None
    data = elemento.split("_")
    if len(data) !=3:
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



def new_meteo(db:pd.DataFrame):
    meteo = db["meteo24"]
    codes = {"28079102": "MORATALAZ", "28079103": "VILLAVERDE", "28079104": "PUENTE DE VALLECAS", "28079106": "MONCLOA-ARAVACA",
             "28079107": "HORTALEZA", "28079108": "FUENCARRAL-EL PARDO", "28079109": "CHAMBERI", "28079110": "CENTRO", 
             "28079111": "CHAMARTIN", "28079112": "VILLA DE VALLECAS", "28079113": "VILLA DE VALLECAS", "28079114": "ARGANZUELA",
             "28079115": "ARGANZUELA", "28079004": "MONCLOA-ARAVACA", "28079008": "SALAMANCA", "28079016": "CIUDAD LINEAL", 
             "28079018": "CARABANCHEL", "28079024": "MONCLOA-ARAVACA", "28079035": "CENTRO", "28079036": "MORATALAZ", "28079038": "TETUAN",
             "28079039":"FUENCARRAL-EL PARDO","28079054": "VILLA DE VALLECAS", "28079056": "CARABANCHEL", "28079058": "FUENCARRAL-EL PARDO",
             "28079059": "BARAJAS"}
    meses = {"1": 31, "2": 28, "3": 31, "4": 30, "5": 31, "6": 30, "7": 31, "8": 31, "9": 30, "10": 31, "11": 30, "12": 31}
    distritos = []
    temperaturas = []
    precipitaciones = []
    viento = []
    fechas = []
    for i in range(len(meteo["PUNTO_MUESTREO"])):
        elemento = meteo["PUNTO_MUESTREO"][i]
        data = check_list(elemento, codes)
        if data is not None and str(meteo["MES"][i]) in meses.keys():
            for j in range(meteo["MES"][i]):
                dia =str(j+1)
                if j < 9:
                    dia = "0" + dia
                fecha = str(meteo["ANO"][i]) + "-" + str(meteo["MES"][i]) + "-" + dia
                linea = same_line(fecha, codes[data[0]], fechas, distritos)
                if linea == -1:
                    distritos.append(codes[data[0]])
                    fechas.append(fecha)
                    temperaturas.append(float("NaN"))
                    precipitaciones.append(float("NaN"))
                    viento.append(float("NaN"))
                    linea = len(distritos) -1
                booleano = "V" + dia
                valor = "D" + dia
                if data[1] == "81":
                    if meteo[booleano][i] == "V" and int(meteo[valor][i]) >= 20:
                        viento[linea] = True
                    else:
                        viento[linea] = False
                elif data[1] == "83":
                    if meteo[booleano][i] == "V":
                        temperaturas[linea] = meteo[valor][i]
                else:
                    if meteo[booleano][i] == "V":
                        precipitaciones[linea] = meteo[valor][i]
            
    nuevo = pd.DataFrame()
    nuevo.loc[:, "FECHA"] = fechas
    nuevo.loc[:, "TEMPERATURA"] = temperaturas
    nuevo.loc[:, "PRECIPITACION"] = precipitaciones
    nuevo.loc[:, "VIENTO"] = viento
    nuevo.loc[:, "DISTRITO"] = distritos
    db["meteo24"] = nuevo
    
def area_new_atributes(df: pd.DataFrame)-> None:
    """Method used for adding the atribute capacidadMax in Areas."""
    # Add column with capacidadMax atribute
    df["Areas"]["capacidadMax"] = None
    """ for lat_area in df["Areas"]["LATITUD"]:
        index = 0
        games = 0
        for long_area in df["Areas"]["LONGITUD"]:
            for lat_juego in df["Juegos"]["LATITUD"]:
                for long_juego in df["Juegos"]["LONGITUD"]:
                    if lat_area == lat_juego and long_area == long_juego:
                        games += 1
        # add atribute to row
        df["Areas"].insert(index, "capacidadMax", games)
        index += 1 """
        
    index = 0
    for area in df["Areas"].to_numpy():
        games = 0
        lat_area = area[10]
        long_area = area[11]
        for juego in df["Juegos"].to_numpy():
            lat_juego = juego[10]
            long_juego = juego[11]
            if lat_area == lat_juego and long_area == long_juego:
                print("Juego in Area!")
                games += 1
        df["Areas"].loc[index, "capacidadMax"] = games
        index += 1
    # for item in df["Areas"]["capacidadMax"]:
    #     print(item)
    print(df["Areas"]["capacidadMax"].mean())
    print("added new atribute completed")
                    
             

# prueabs
base = load.load_db()
# new_meteo(base)
# for i in range(len(base["meteo24"]["FECHA"])):
#     print(base["meteo24"]["FECHA"][i], " ", base["meteo24"]["TEMPERATURA"][i], " ", base["meteo24"]["PRECIPITACION"][i],
#            " ", base["meteo24"]["VIENTO"][i], " ", base["meteo24"]["DISTRITO"][i])
change.adjust_gps(base) # run this so that the GPS are adjusted
area_new_atributes(base)
# print(base)