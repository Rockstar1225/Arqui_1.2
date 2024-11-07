import load
import change
import numpy as np
import random
import json


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
        self.juego_tipo = {}  # extraida
        self.juego_incidencias = {}  # extraida
        self.area_meteo = {}  # extraida
        self.area_encuesta = {}  # extraida
        self.area_incidente = {}  # extraida
        self.area_juegos = {}  # extraida mas o menos
        self.juego_mantenimientos = {}  # extraida
        self.mantenimiento_incidencias = {}  # extraida
        self.incidencia_usuario = {}  # extraida

        # objetos_extraidos
        self.areas = []
        self.encuestas = []  # generadoas
        self.registrosClima = []
        self.incidentesSeguridad = []  # generados
        self.juegos = []
        self.incidencias = []
        self.usuarios = []  # generados
        self.mantenimientos = []

    def generar_usuarios(self):

        # extraer columnas de datos usuarios
        nifs = self.extraer_columna("Usuarios", "NIF")
        nombre = self.extraer_columna("Usuarios", "NOMBRE")
        email = self.extraer_columna("Usuarios", "EMAIL")
        tlf = self.extraer_columna("Usuarios", "TELEFONO")

        for i in range(len(nifs)):
            self.usuarios.append(
                {
                    "NIF": nifs[i],
                    "nombre": nombre[i],
                    "email": email[i],
                    "telefono": tlf[i],
                }
            )
        print("Usuarios Generados")

    def generar_encuestas(self):

        id = self.extraer_columna("Encuestas", "ID")
        fecha = self.extraer_columna("Encuestas", "FECHA")
        accesibilidad = self.extraer_columna("Encuestas", "PUNTUACION_ACCESIBILIDAD")
        calidad = self.extraer_columna("Encuestas", "PUNTUACION_CALIDAD")
        comantarios = self.extraer_columna("Encuestas", "COMENTARIOS")

        for i in range(len(id)):
            self.encuestas.append(
                {
                    "id": int(id[i]),
                    "fechaEncuesta": str(fecha[i]),
                    "puntuacionAccesibilidad": accesibilidad[i],
                    "puntuacionCalidad": calidad[i],
                    "comentaraios": comantarios[i],
                }
            )
        print("Encuestas generadas!!")

    def generar_incidentes(self):

        id = self.extraer_columna("Incidentes", "ID")
        fecha = self.extraer_columna("Incidentes", "FECHA_REPORTE")
        tipo = self.extraer_columna("Incidentes", "TIPO_INCIDENTE")
        gravedad = self.extraer_columna("Incidentes", "GRAVEDAD")

        for i in range(len(id)):
            self.incidentesSeguridad.append(
                {
                    "id": int(id[i]),
                    "fechaDeReporte": str(fecha[i]),
                    "tipoIncidente": tipo[i],
                    "gravedad": gravedad[i],
                }
            )
        print("Incidentes generados!!")

    def generar_incidencias(self):

        id = self.extraer_columna("Incidencias", "ID")
        fecha = self.extraer_columna("Incidencias", "TIPO_INCIDENCIA")
        tipo = self.extraer_columna("Incidencias", "FECHA_REPORTE")
        estado = self.extraer_columna("Incidencias", "ESTADO")
        tiempo = self.extraer_columna("Incidencias", "TIEMPO_RESOLUCION")
        escala = self.extraer_columna("Incidencias", "NIVEL_RECONOCIMIENTO")
        # nivel escalamiento

        for i in range(len(id)):
            if id[i] in self.incidencia_usuario:

                usuarios = self.incidencia_usuario[int(id[i])]

                # encontrar usuarios en la relación incidencia-usuario
                res_users = []
                for user in self.usuarios:
                    for usuarioID in usuarios:
                        if user["NIF"] == usuarioID:
                            res_users.append(user)

                self.incidencias.append(
                    {
                        "id": int(id[i]),
                        "fechaReporte": str(fecha[i]),
                        "tipo": tipo[i],
                        "estado": estado[i],
                        "tiempoResolucion": float(tiempo[i]),
                        "nivel de escalamiento": int(escala[i]),
                        "usuarios": res_users,
                    }
                )
        print("Incidecias generadas!!")

    def extraer_columna(self, table: str, column: str) -> list:
        result = []
        for i in range(len(self.state[table][column])):
            result.append(self.state[table].loc[i, column])
        return result

    def crear_area_clima(self):
        tabla_areas = self.state["Areas"]

        # Extraer las areas de la tabla de juegos
        for i in range(len(tabla_areas["MeteoID"])):
            valor_meteo = int(tabla_areas.loc[i, "MeteoID"])
            valor_id = int(tabla_areas.loc[i, "ID"])

            if valor_meteo == 0:
                continue

            if valor_meteo not in self.area_meteo:
                self.area_meteo[valor_id] = [valor_meteo]
            else:
                self.area_meteo[valor_id].append(valor_meteo)
        print("Area-Meteo Completado")

    def crear_area_juegos(self):

        tabla_juegos = self.state["Juegos"]

        # Extraer las areas de la tabla de juegos
        for i in range(len(tabla_juegos["AreaRecreativaID"])):
            valor_area = tabla_juegos.loc[i, "AreaRecreativaID"]
            valor_juego = tabla_juegos.loc[i, "ID"]

            if valor_area > 1000000:
                continue

            if valor_area not in self.area_juegos:
                self.area_juegos[valor_area] = [valor_juego]
            else:
                self.area_juegos[valor_area].append(valor_juego)
        print("Area-Juegos Completado")

    def crear_juegos_tipo(self):

        tabla_juegos = self.state["Juegos"]

        # Extraer los tipos de la tabla de juegos
        for i in range(len(tabla_juegos["tipo_juego"])):
            valor_tipo = tabla_juegos.loc[i, "tipo_juego"]
            if valor_tipo not in self.juego_tipo:
                self.juego_tipo[valor_tipo] = 1
            else:
                self.juego_tipo[valor_tipo] += 1
        print("Juegos Tipo Completado")

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
        print("Area-Encuestas Completado")

    def crear_juego_incidencias(self):

        # Tablas a utilizar
        tabla_incidencias = self.state["Incidencias"]
        tabla_mantenimiento = self.state["Mantenimiento"]

        # Operación de transformación de nombre de atributos.
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
                # print("Valor a insertar", transform(valor_manten))
                self.juego_mantenimientos[valor_id] = [transform(valor_manten)]
            else:
                self.juego_mantenimientos[valor_id].append(valor_manten)

        # Deducir las relaciones de juegos e incidencias. Mapa "JuegoID -> IncidenciasID"
        for juego in self.juego_mantenimientos.keys():
            for incidencia in self.mantenimiento_incidencias.values():
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

    def crear_areas_incidentes(self) -> None:
        """Creating reference for Areas-Incidentes"""
        tabla_incidentes_seg = self.state["Incidentes"]
        for i in range(len(tabla_incidentes_seg["AreaRecreativaID"])):
            id_area = tabla_incidentes_seg.loc[i, "AreaRecreativaID"]
            id_incidendes_seg = tabla_incidentes_seg.loc[i, "ID"]
            if id_area is not None and id_area not in self.area_incidente:
                self.area_incidente[id_area] = [id_incidendes_seg]
            else:
                self.area_incidente[id_area].append(id_incidendes_seg)
        print("Area-incidente Completado")

    def crear_incidencia_usuario(self) -> None:
        """Creating a reference for Usuario-Incidencias"""
        tabla_incidencias = self.state["Incidencias"]
        for i in range(len(tabla_incidencias["UsuarioID"])):
            id_usuarios_str = tabla_incidencias.loc[i, "UsuarioID"].replace("'", '"')
            id_usuarios_list = json.loads(id_usuarios_str)
            id_incidencias = tabla_incidencias.loc[i, "ID"]
            for id_usuarios in id_usuarios_list:
                if (
                    id_usuarios is not None
                    and id_usuarios not in self.incidencia_usuario
                ):
                    self.incidencia_usuario[int(id_incidencias)] = [id_usuarios]
                else:
                    self.incidencia_usuario[int(id_incidencias)].append(id_usuarios)
        print("Incidencia-Usuario Completado")
