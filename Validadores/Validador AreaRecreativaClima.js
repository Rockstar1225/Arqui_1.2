db.createCollection('AreaRecreativaClima')

db.AreaRecreativaClima.createIndex({ "registrosClima.id": 1 }, { unique: 1, sparse: true })
db.AreaRecreativaClima.createIndex({ "encuestas.id": 1 }, { unique: 1, sparse: true })
db.AreaRecreativaClima.createIndex({ "incidentesSeguridad.id": 1 }, { unique: 1, sparse: true })
db.AreaRecreativaClima.createIndex({ "juegos.id": 1 }, { unique: 1, sparse: true })
db.AreaRecreativaClima.createIndex({ "CantidadJuegosTipo.tipo": 1 }, { unique: 1, sparse: true })

SCHEME = {
  "bsonType": "object",
  "description": "Agregado de gestión del estado de las áreas recreativas, juegos, incidentes de seguridad y datos climáticos.",
  "required": ["id", "coordenadasGPS", "barrio", "distrito", "fecha", "estadoOperativo", "capacidadMaxima", "cantidadJuegosTipo", "juegos", "incidentesSeguridad", "registrosClima", "encuestas"],
  "properties": {
    "id": {
      "bsonType": "number",
      "description": "Clave Primaria"
    },
    "coordenadasGPS": {
      "bsonType": "array",
      "description": "Array que representa la latitud y la longitud",
      "minItems": 2,
      "maxItems": 2,
      "items": {
        "bsonType": "string"
      }
    },
    "fecha": {
      "bsonType": "string",
      "description": "fecha de instalación del área"
    },
    "barrio": {
      "bsonType": "string",
      "description": "Barrio al que pertenece el area recreativa"
    },
    "distrito": {
      "bsonType": "string",
      "description": "Distrito al que pertenece el area recreativa"
    },
    "estadoOperativo": {
      "bsonType": "string",
      "description": "Estado global del area recreativa",
      "enum": ["OPERATIVO", "CERRADO", "INDISPUESTO"]
    },
    "capacidadMaxima": {
      "bsonType": "number",
      "description": "Numero máximo de juegos que incluye el área",
    },
    "cantidadJuegosTipo": {
      "bsonType": "array",
      "description": "Conteo de cuantos juegos hay de cada tipo en el area actual",
      "minItems": 0,
      "items": {
        "bsonType": "object",
        "description": "objeto resumen de conteo de un tipo de juegos",
        "required": ["tipo", "valor"],
        "properties": {
          "tipo": {
            "bsonType": "string",
            "description": "tipo de juegos a contar",
            "enum": ["DEPORTIVAS", "INFANTILES", "MAYORES"]
          },
          "valor": {
            "bsonType": "number",
            "minimum": 0
          }
        }
      }
    },
    "juegos": {
      "bsonType": "array",
      "description": "array de referencia a juegos incluidos en el area",
      "minItems": 0,
      "items": {
        "bsonType": "number",
	"description": "juegos en un area",
      }
    },
    "incidentesSeguridad": {
      "bsonType": "array",
      "description": "array de referencias a los incidentes de seguridad",
      "minItems": 0,
      "items": {
        "bsonType": "number",
        "description": "objeto de representacion de incidencias de seguridad"
      }
    },
    "registrosClima": {
      "bsonType": "array",
      "description": "Array de referencias a los registros de clima para esta zona",
      "minItems": 0,
      "items": {
        "bsonType": "number",
      }
    },
    "encuestas": {
      "bsonType": "array",
      "description": "Array de referencias a las encuestas de satisfacción de una zona",
      "minItems": 0,
      "items": {
        "bsonType": "number",
        "description": "objeto referencia de una encuesta de satisfacción"
      }
    },
  },
}

db.runCommand({ "collMod": "AreaRecreativaClima", "validator": { $jsonSchema: SCHEME } })
