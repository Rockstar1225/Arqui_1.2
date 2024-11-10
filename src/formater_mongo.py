import json
import os


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
        self.juego_tipo = {}
        self.juego_incidencias = {}
        self.area_meteo = {}
        self.area_encuesta = {}
        self.area_incidente = {}
        self.area_juegos = {}
        self.juego_mantenimientos = {}
        self.mantenimiento_incidencias = {}
        self.incidencia_usuario = {}

        # objetos_extraidos
        self.areas = []
        self.encuestas = []  # generadoas
        self.registrosClima = []
        self.incidentesSeguridad = []  # generados
        self.juegos = []
        self.incidencias = []
        self.usuarios = []  # generados
        self.mantenimientos = []

    def get_json_data(self, objs: list, collection_name: str):

        # Dar formato ISO 8601 a fechas
        for obj in objs:
            for key in obj:
                if "fecha" in key:
                    obj[key] = (
                        f"{str(obj[key]).split(" ")[0]}T{str(obj[key]).split(" ")[1]}Z"
                    )

        # abrir fiechero y escribir datos
        with open(f"DatasetsNuevos/{collection_name}.js", "w") as file:
            file.write(
                f"""db.{collection_name}.insertMany(
                    { json.dumps(objs,indent=4) }
                )"""
            )
        print(f"JSON creado para {collection_name}")

    def generar_usuarios(self):

        # extraer columnas de datos usuarios
        nifs = self.extraer_columna("Usuarios", "NIF")
        nombre = self.extraer_columna("Usuarios", "NOMBRE")
        email = self.extraer_columna("Usuarios", "EMAIL")
        tlf = self.extraer_columna("Usuarios", "TELEFONO")

        for i in range(len(nifs)):
            self.usuarios.append(
                {
                    "NIF": str(nifs[i]),
                    "nombre": str(nombre[i]),
                    "email": str(email[i]),
                    "telefono": str(tlf[i]),
                }
            )
        print("Generar Usuarios")

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
        tipo = self.extraer_columna("Incidencias", "TIPO_INCIDENCIA")
        fecha = self.extraer_columna("Incidencias", "FECHA_REPORTE")
        estado = self.extraer_columna("Incidencias", "ESTADO")
        tiempo = self.extraer_columna("Incidencias", "TIEMPO_RESOLUCION")
        escala = self.extraer_columna("Incidencias", "NIVEL_RECONOCIMIENTO")

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
                        "nivelEscalamiento": int(escala[i]),
                        "usuarios": res_users,
                    }
                )
        print("Incidecias generadas!!")

    def generar_juegos(self):
        id = self.extraer_columna("Juegos", "ID")
        modelo = self.extraer_columna("Juegos", "MODELO")
        estado_op = self.extraer_columna("Juegos", "ESTADO")
        accesibilidad = self.extraer_columna("Juegos", "ACCESIBLE")
        fecha_instalacion = self.extraer_columna("Juegos", "FECHA_INSTALACION")
        tipo = self.extraer_columna("Juegos", "tipo_juego")
        desgaste = self.extraer_columna("Juegos", "desgasteAcumulado")
        indicador_exposicion = self.extraer_columna("Juegos", "indicadorExposicion")
        ultima_fecha_mant = self.extraer_columna("Juegos", "ULTIMA_FECHA_MANTENIMIENTO")

        for i in range(len(id)):
            # si el juego no tiene incidencias
            if id[i] not in list(self.juego_incidencias.keys()):
                incidencia = [""]
            else:
                incidencia = self.juego_incidencias[id[i]]
            # si el juego no tiene mantenimientos
            if id[i] not in list(self.juego_mantenimientos.keys()):
                mantenimiento = [""]
            else:
                mantenimiento = self.juego_mantenimientos[id[i]]
            self.juegos.append(
                {
                    "id": str(id[i]),
                    "modelo": str(modelo[i]),
                    "estadoOperativo": str(estado_op[i]),
                    "accesibilidad": bool(accesibilidad[i]),
                    "fechaInstalacion": str(fecha_instalacion[i]),
                    "tipo": str(tipo[i]),
                    "desgasteAcumulado": int(desgaste[i]),
                    "indicadorExposicion": str(indicador_exposicion[i]),
                    "ultimaFechaMantenimiento": str(ultima_fecha_mant[i]),
                    "mantenimientos": mantenimiento,
                    "incidencias": incidencia,
                }
            )

        print("Juegos generados!!")

    def generar_clima(self):
        id = self.extraer_columna("meteo24", "ID")
        fecha = self.extraer_columna("meteo24", "FECHA")
        temp = self.extraer_columna("meteo24", "TEMPERATURA")
        vent = self.extraer_columna("meteo24", "VIENTO")
        prec = self.extraer_columna("meteo24", "PRECIPITACION")
        for i in range(len(id)):
            # Solo pasa a entero los valores numéricos, no los -
            if temp[i] != "-":
                temp[i] = int(temp[i])
            else:
                temp[i] = 0
            if prec[i] != "-":
                prec[i] = int(prec[i])
            else:
                prec[i] = 0

            self.registrosClima.append(
                {
                    "id": int(id[i]),
                    "fecha": fecha[i],
                    "temperatura": temp[i],
                    "vientosFuertes": bool(vent[i]),
                    "precipitacion": prec[i],
                }
            )
        print("Climas generados!!")

    def generar_area(self):
        id = self.extraer_columna("Areas", "ID")
        barrio = self.extraer_columna("Areas", "BARRIO")
        distr = self.extraer_columna("Areas", "DISTRITO")
        estado = self.extraer_columna("Areas", "ESTADO")
        lat = self.extraer_columna("Areas", "LATITUD")
        long = self.extraer_columna("Areas", "LONGITUD")
        fecha = self.extraer_columna("Areas", "FECHA_INSTALACION")
        capmax = self.extraer_columna("Areas", "capacidadMax")

        for i in range(len(id)):
            # Solo pasa a entero los valores numéricos, no los -

            # extraer incidentes de seguridad de la relación
            res_incidentes = []
            if int(id[i]) in self.area_incidente:
                incidentes = self.area_incidente[int(id[i])]
                for inci in self.incidentesSeguridad:
                    for incidentesID in incidentes:
                        if inci["id"] == incidentesID:
                            res_incidentes.append(int(incidentesID))

            # extraer encuestas de la relación
            res_encuestas = []
            if int(id[i]) in self.area_encuesta:
                encuestas = self.area_encuesta[int(id[i])]
                for enc in self.encuestas:
                    for encuestaID in encuestas:
                        if enc["id"] == encuestaID:
                            res_encuestas.append(int(encuestaID))

            # extraer climas de la relación
            res_climas = []
            if int(id[i]) in self.area_meteo:
                climas = self.area_meteo[int(id[i])]
                for clima in self.registrosClima:
                    for climaID in climas:
                        if clima["id"] == climaID:
                            res_climas.append(int(climaID))

            # extraer juegos de la relación
            res_juegos = []
            print("Area Juego: ", int(id[i]) in self.area_juegos)
            if int(id[i]) in self.area_juegos:
                juegos = self.area_juegos[int(id[i])]
                for juegoID in juegos:
                    res_juegos.append(int(juegoID))

            # extraer atributo juego_tipo
            res_juegos_tipo_valor = []
            for tipo in self.juego_tipo:
                objeto = {"tipo": str(tipo), "valor": int(self.juego_tipo[tipo])}
                res_juegos_tipo_valor.append(objeto)

            self.areas.append(
                {
                    "id": int(id[i]),
                    "barrio": barrio[i],
                    "distrito": distr[i],
                    "estadoOperativo": estado[i],
                    "coordenadasGPS": [lat[i], long[i]],
                    "fecha": fecha[i],
                    "capacidadMaxima": float(capmax[i]),
                    "incidentesSeguridad": res_incidentes,
                    "encuestas": res_encuestas,
                    "registrosClima": res_climas,
                    "juegos": res_juegos,
                    "cantidadJuegosTipo": res_juegos_tipo_valor,
                }
            )

    def generar_mantenimientos(self):

        id = self.extraer_columna("Mantenimiento", "ID")
        tipo = self.extraer_columna("Mantenimiento", "TIPO_INTERVENCION")
        estado_previo = self.extraer_columna("Mantenimiento", "ESTADO_PREVIO")
        estado_posterior = self.extraer_columna("Mantenimiento", "ESTADO_POSTERIOR")
        fecha = self.extraer_columna("Mantenimiento", "FECHA_INTERVENCION")

        transform = lambda x: f"{x.split(" ")[1]}-{int(x.split(" ")[0][1:])}"
        for i in range(len(id)):

            if transform(id[i]) in self.mantenimiento_incidencias:
                incidencias = self.mantenimiento_incidencias[transform(id[i])]

                # encontrar incidencias en la relación mantenimiento-incidencias
                res_incidencias = []
                for inci in self.incidencias:
                    for incidenciasID in incidencias:
                        if inci["id"] == incidenciasID:
                            res_incidencias.append(int(incidenciasID))

                self.mantenimientos.append(
                    {
                        "id": transform(id[i]),
                        "tipoIntervencion": str(tipo[i]),
                        "estadoPrevio": estado_previo[i],
                        "estadoPosterior": estado_posterior[i],
                        "fechaIntervencion": fecha[i],
                        "incidencias": res_incidencias,
                    }
                )
        print("Mantenimientos generadas!!")

    def extraer_columna(self, table: str, column: str) -> list:
        # Extrae las tablas definitivas completas, iterando por sus columnas
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

            if valor_area not in self.area_juegos:
                self.area_juegos[int(valor_area)] = [int(valor_juego)]
            else:
                self.area_juegos[int(valor_area)].append(int(valor_juego))
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

            id_manten_str = tabla_incidencias.loc[i, "MantenimientoID"]
            id_manten_list = id_manten_str[1:-1].split(", ")
            valor_id = tabla_incidencias.loc[i, "ID"]

            for manten_id in id_manten_list:
                if manten_id not in self.mantenimiento_incidencias:
                    self.mantenimiento_incidencias[transform(manten_id)] = [valor_id]
                else:
                    self.mantenimiento_incidencias[transform(manten_id)].append(
                        valor_id
                    )

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
                        for inc in incidencia:
                            if juego not in self.juego_incidencias:
                                self.juego_incidencias[juego] = [str(int(inc))]
                            else:
                                self.juego_incidencias[juego].append(str(int(inc)))

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
