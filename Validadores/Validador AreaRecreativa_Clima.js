db.createCollection('AreaRecreativa_Clima')

db.AreaRecreativa_Clima.createIndex( {"nombre":1}, {unique:1} )
db.AreaRecreativa_Clima.createIndex( {"registrosClima.id":1}, {unique:1, sparse: true})
db.AreaRecreativa_Clima.createIndex( {"encuestas.id":1}, {unique:1, sparse: true} )
db.AreaRecreativa_Clima.createIndex( {"incidentesSeguridad.id":1}, {unique:1, sparse: true} )
db.AreaRecreativa_Clima.createIndex( {"juegos.id":1}, {unique:1, sparse: true} )
db.AreaRecreativa_Clima.createIndex( {"CantidadJuegosTipo.tipo":1}, {unique:1, sparse: true} )

SCHEME={
   "bsonType": "object",
   "description": "Agregado de gestión del estado de las áreas recreativas, juegos, incidentes de seguridad y datos climáticos.",
   "required": ["nombre", "coordenadasGPS", "barrio", "distrito", "fechaInstalacion", "estadoGlobalArea","capacidadMax","CantidadJuegosTipo", "juegos", "incidentesSeguridad", "registrosClima", "encuestas"],
   "properties": {
           "nombre": {
               "bsonType": "string",
               "description": "Tipo String. Clave Primaria"
           },
           "coordenadasGPS": {
               "bsonType": "array",
               "description": "Array que representa la latitud y la longitud",
               "minItems": 2,
               "maxItems": 3,
               "items": {
                  "bsonType": "float"
               }
           },
           "barrio": {
               "bsonType": "string",
               "description": "Barrio al que pertenece el area recreativa"
           },
           "distrito": {
               "bsonType": "string",
               "description": "Distrito al que pertenece el area recreativa"
           },
           "fechaInstalacion": {
               "bsonType": "date",
               "description": "Fecha de instalacion del area recreativa"
           },
           "estadoGlobalArea": {
               "bsonType": "string",
               "description": "Estado global del area recreativa",
               "enum": ["Operativa","Cerrada","Indispuesta"]
           },
           "capacidadMax": {
               "bsonType": "number",
               "description": "Numero máximo de juegos que incluye el área",
           },
           "CantidadJuegosTipo": {
               "bsonType": "array",
               "description": "Conteo de cuantos juegos hay de cada tipo en el area actual",
               "minItems": 0,
               "items": {
                  "bsonType": "object",
                  "description": "objeto resumen de conteo de un tipo de juegos",
                  "required": ["tipo","valor"],
                  "properties": {
                     "tipo": {
                        "bsonType": "string",
                        "description": "tipo de juegos a contar",
                        "enum": ["deportivas","infantiles","mayores"]
                     },
                     "valor": {
                        "bsonType": "number",
                        "minimum": 0
                     }
                  }
               } 
           },
           "juegos" : {
               "bsonType": "array",
               "description": "array de referencia a juegos incluidos en el area",
               "minItems": 0,
               "items": {
                  "bsonType": "object",
                  "description": "objeto de referencia al juego de un area",
                  "required": ["id"],
                  "properties": {
                     "id": {
                        "bsonType": "string"
                     }
                  }
               }
           },
           "incidentesSeguridad": {
               "bsonType": "array",
               "description": "array de referencias a los incidentes de seguridad",
               "minItems": 0,
               "items": {
                  "bsonType": "object",
                  "description": "objeto de representacion de incidencias de seguridad",
                  "required": ["id","tipo","gravedad","fechaDeReporte"],
                  "properties": {
                     "id": {
                        "bsonType": "string",
                        "description": "id del incidente de seguridad"
                     },
                     "fechaDeReporte": {
                        "bsonType": "date",
                        "description": "fecha de reporte de la incidencia de seguridad"
                     }
                  }
               }
           },
           "registrosClima": {
               "bsonType": "array",
               "description": "Array de referencias a los registros de clima para esta zona",
               "minItems": 0,
               "items": {
                  "bsonType": "object",
                  "description": "objeto referencia de un registro de clima",
                  "required": ["id"],
                  "properties": {
                     "id": {
                        "bsonType": "string",
                        "description": "id del registro de clima"
                     }
                  }
               }
           },
           "encuestas": {
               "bsonType": "array",
               "description": "Array de referencias a las encuestas de satisfacción de una zona",
               "minItems": 0,
               "items": {
                  "bsonType": "object",
                  "description": "objeto referencia de una encuesta de satisfacción",
                  "required": ["id"],
                  "properties": {
                     "id": {
                        "bsonType": "string",
                        "description": "id de la encuesta"
                     }
                  }
               }
           },
    },
}

db.runCommand({ "collMod": "AreaRecreativa_Clima", "validator": { $jsonSchema: SCHEME } })
