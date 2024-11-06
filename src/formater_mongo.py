import load
import change
import numpy as np
import random


class Creator:
    def __init__(self, bd: dict):

        # Base de datos en el estado requerido
        self.state = bd

        # Correspondencias entre columna a añadir y tablas que la requieren
        self.col_table = {
            "AreaRecreativaID": "meteo24",
            "JueID": "Incidencias",
        }

        # relaciones entre sí
        self.juego_incidencias = {}  # extraida
        self.area_clima = {}
        self.area_encuesta = {}  # extraida
        self.area_incidente = {}
        self.area_juegos = {}
        self.juego_mantenimientos = {}  # extraida
        self.mantenimiento_incidencias = {}  # extraida

    def crear_area_clima(self):
        print(len(self.state["Juegos"]["AreaRecreativaID"]))

    def crear_area_juegos(self):

        tabla_juegos = self.state["Juegos"]

        # Extraer las areas de la tabla de juegos
        for i in range(len(tabla_juegos["AreaRecreativaID"])):
            valor_area = tabla_juegos.loc[i, "AreaRecreativaID"]
            valor_juego = tabla_juegos.loc[i, "ID"]
            if valor_area is not None and valor_area not in self.area_juegos:
                self.area_juegos[valor_area] = [valor_juego]
            else:
                self.area_juegos[valor_area].append(valor_juego)

    def crear_area_encuestas(self):
        tabla_encuestas = self.state["Encuestas"]

        # Extraer los mantenimientos de las incidencias. Mapa "AreaRecreativaID -> EncuestasID"
        for i in range(len(tabla_encuestas["AreaRecreativaID"])):

            valor_area = tabla_encuestas.loc[i, "AreaRecreativaID"]
            valor_id = tabla_encuestas.loc[i, "ID"]

            if valor_area not in self.area_encuesta:
                self.area_encuesta[valor_area] = [valor_id]
            else:
                self.area_encuesta[valor_area].append(valor_id)

    def crear_juego_incidencias(self):

        # Tablas a utilizar
        tabla_incidencias = self.state["Incidencias"]
        tabla_mantenimiento = self.state["Mantenimiento"]

        # Operación de transformación de nombre de atributos. FIXME
        transform = lambda x: f"{x.split(" ")[1]}-{int(x.split(" ")[0][1:])}"

        # Extraer los mantenimientos de las incidencias. Mapa "MantenimientoID -> IncidenciaID"
        for i in range(len(tabla_incidencias["MantenimientoID"])):

            valor_manten = tabla_incidencias.loc[i, "MantenimientoID"]
            valor_id = tabla_incidencias.loc[i, "ID"]

            if valor_manten not in self.mantenimiento_incidencias:
                self.mantenimiento_incidencias[valor_manten] = [valor_id]
            else:
                self.mantenimiento_incidencias[valor_manten].append(valor_id)

        # Extraer los mantenimientos de los juegos. Mapa "JuegoID -> MantenimientoID"
        for i in range(len(tabla_mantenimiento["JuegoID"])):

            valor_id = tabla_mantenimiento.loc[i, "JuegoID"]
            valor_manten = tabla_mantenimiento.loc[i, "ID"]

            if valor_id not in self.juego_mantenimientos:
                # print("Tipo de valor de mantenimiento: ", type(valor_manten))
                print("Valor a insertar", transform(valor_manten))
                self.juego_mantenimientos[valor_id] = [transform(valor_manten)]
            else:
                self.juego_mantenimientos[valor_id].append(valor_manten)

        # Deducir las relaciones de juegos e incidencias. Mapa "JuegoID -> IncidenciasID"
        for juego in self.juego_mantenimientos.keys():
            for incidencia in self.mantenimiento_incidencias.values():
                # extraer todos los mantenimientos
                for mantenimiento in self.juego_mantenimientos[juego]:
                    if mantenimiento not in self.mantenimiento_incidencias:
                        continue
                    if self.mantenimiento_incidencias[mantenimiento] == incidencia:
                        if juego not in self.juego_incidencias:
                            self.juego_incidencias[juego] = [incidencia]
                        else:
                            self.juego_incidencias[juego].append(incidencia)

        print(
            "Relaciones de juego_mantenimientos, mantenimiento_incdencias, juego_incidencias terminadas"
        )
    def crear_areas_incidentes(self) ->None:
        """Creating reference for Areas-Incidentes"""
        tabla_incidentes_seg = self.state["Incidentes"]     
        for i in range(len(tabla_incidentes_seg["AreaRecreativaID"])):
            id_area = tabla_incidentes_seg.loc[i, "AreaRecreativaID"]
            id_incidendes_seg = tabla_incidentes_seg.loc[i, "ID"]
            if id_area is not None and id_area not in self.area_incidente:
                self.area_incidente[id_area] = [id_incidendes_seg]
            else:
                self.area_incidente[id_area].append(id_incidendes_seg)
        
