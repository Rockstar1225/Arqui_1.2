import pandas as pd
import itertools
import load
import change
import imputation
import numpy as np
import random


class Creator:
	def __init__ (self,bd: pd.DataFrame):
		
		# Base de datos en el estado requerido
		self.state = bd

		# Correspondencias entre columna a añadir y tablas que la requieren
		self.col_table = {
			"AreaRecreativaID": "meteo24",
			"JueID": "Incidencias",
		}

		# relaciones entre sí
		self.juego_incidencias = {} # extraida
		self.area_clima = {} 
		self.area_encuesta = {}
		self.area_incidente = {}
		self.area_juegos = {}
		self.juego_mantenimientos = {} # extraida
		self.mantenimiento_incidencias = {} # extraida


	def crear_area_clima(self):
		print(len(self.state["Juegos"]["AreaRecreativaID"]))

	def crear_area_juegos(self):

		tabla_juegos = self.state["Juegos"]

		# Extraer las areas de la tabla de juegos
		for i in range(len(tabla_juegos["AreaRecreativaID"])):
			valor_area = tabla_juegos.loc[i,"AreaRecreativaID"]	
			valor_juego = tabla_juegos.loc[i,"ID"]
			if valor_area not in self.area_juegos:
				self.area_juegos[valor_area] = [valor_juego]
			else:
				self.area_juegos[valor_area].append(valor_juego)

	def crear_juego_incidencias(self):

		# Tablas a utilizar
		tabla_juegos = self.state["Juegos"]
		tabla_incidencias = self.state["Incidencias"]
		tabla_mantenimiento = self.state["Mantenimiento"]
		
		# Operación de transformación de nombre de atributos. FIXME
		transform = lambda x: f"{x.split(" ")[1]}-{int(x.split(" ")[0][1:])}"

		# Extraer los mantenimientos de las incidencias. Mapa "MantenimientoID -> IncidenciaID"
		for i in range(len(tabla_incidencias["mantenimientoID"])):

			valor_manten = tabla_incidencias.loc[i,"MantenimientoID"]
			valor_id = tabla_incidencias.loc[i,"ID"]

			if valor_manten not in self.mantenimientos_incidencias:
				self.mantenimiento_incidencias[valor_manten] = [valor_id]
			else:
				self.mantenimiento_incidencias[valor_manten].append(valor_id)

		# Extraer los mantenimientos de los juegos. Mapa "JuegoID -> MantenimientoID"
		for i in range(len(tabla_mantenimiento["JuegoID"])):

			valor_manten = tabla_incidencias.loc[i,"ID"]
			valor_id = tabla_incidencias.loc[i,"JuegoID"]

			if valor_manten not in self.juego_mantenimientos:
				self.juego_mantenimientos[valor_id] = [transform(valor_manten)]
			else:
				self.juego_mantenimientos[valor_id].append(valor_manten)

		# Deducir las relaciones de juegos e incidencias. Mapa "JuegoID -> IncidenciasID"
		for juego in self.juego_mantenimientos.keys():
			for incidencia in self.mantenimiento_incidencias.values():
				if self.mantenimiento_incidencias[self.juego_mantenimientos[juego]] == incidencia:
					if juego not in self.juego_incidencias:
						self.juego_incidencias[juego] = [incidencia]
					else:
						self.juego_incidencias[juego].append(incidencia)



db = load.load_db()

c = Creator(db)
c.crear_area_clima()
