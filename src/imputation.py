import pandas as pd
import load

def column_district(db:pd.DataFrame):
    meteo = db["meteo24"]
    dict = {"28079102": "MORATALAZ", "28079103": "VILLAVERDE", "28079104": "PUENTE DE VALLECAS", "28079106": "MONCLOA-ARAVACA",
             "28079107": "HORTALEZA", "28079108": "FUENCARRAL-EL PARDO", "28079109": "CHAMBERI", "28079110": "CENTRO", 
             "28079111": "CHAMARTIN", "28079112": "VILLA DE VALLECAS", "28079113": "VILLA DE VALLECAS", "28079114": "ARGANZUELA",
             "28079115": "ARGANZUELA", "28079004": "MONCLOA-ARAVACA", "28079008": "SALAMANCA", "28079016": "CIUDAD LINEAL", 
             "28079018": "CARABANCHEL", "28079024": "MONCLOA-ARAVACA", "28079035": "CENTRO", "28079036": "MORATALAZ", "28079038": "TETUAN",
             "28079039":"FUENCARRAL-EL PARDO","28079054": "VILLA DE VALLECAS", "28079056": "CARABANCHEL", "28079058": "FUENCARRAL-EL PARDO",
             "28079059": "BARAJAS"}
    distritos = []
    eliminar = []
    for i in range(len(meteo["PUNTO_MUESTREO"])):
        elemento = meteo["PUNTO_MUESTREO"][i]
        if "_" not in elemento:
            eliminar.append(i)
        else:
            data = elemento.split("_")
            if len(data) !=3:
                eliminar.append(i)
            else:
                if not data[0].isdigit() or not data[1].isdigit() or not data[2].isdigit():
                    eliminar.append(i)
                else:
                    try:
                        distritos.append(dict[data[0]])
                    except:
                        eliminar.append(i)
    total_falsas = len(eliminar)
    for j in range(total_falsas):
        fila_actual = total_falsas -j -1
        meteo.drop(fila_actual)
    meteo.loc[:, "DISTRITOS"] = distritos


base = load.load_db()
column_district(base)
print(base["meteo24"])