db.createCollection('Juego')
db.Juego.createIndex({ "id": 1 }, { unique: 1 })

SCHEME = {
  "bsonType": "object",
  "description": "Agregado de gestión del estado del juego, historial de mantenimiento y seguimiento de incidencias.",
  "required": ["id", "modelo", "estadoOperativo", "accesibilidad", "fechaInstalacion", "tipo", "desgasteAcumulado", "indicadorExposicion", "ultimaFechaMantenimiento", "mantenimientos", "incidencias"],
  "properties": {
    "id": {
      "bsonType": "string",
      "description": "Tipo String. Clave Primaria"
    },
    "modelo": {
      "bsonType": "string",
      "description": "Modelo de fabricacion del juego"
    },
    "estadoOperativo": {
      "bsonType": "string",
      "description": "Estado del juego",
      "enum": ["OPERATIVO", "INDISPUESTO"]
    },
    "accesibilidad": {
      "bsonType": "bool",
      "description": "Si el juego es accesible por la gente o no"
    },
    "fechaInstalacion": {
      "bsonType": "string",
      "description": "Fecha de instalacion del juego"
    },
    "tipo": {
      "bsonType": "string",
      "description": "Tipo de juego",
      "enum": ["DEPORTIVAS", "INFANTILES", "MAYORES"]
    },
    "desgasteAcumulado": {
      "bsonType": "number",
      "description": "porcentaje de desgaste que tiene un juego",
      "minimum": 0,
      "maximum": 100,
    },
    "indicadorExposicion": {
      "bsonType": "string",
      "description": "Indicador de exposición a temperaturas aridas",
      "enum": ["INTACTO", "BAJO", "MEDIO", "ALTO"]
    },
    "ultimaFechaMantenimiento": {
      "bsonType": "string",
      "description": "ultima fecha de mantenimiento del juego"
    },
    "mantenimientos": {
      "bsonType": "array",
      "description": "array de referencias a registros de mantenimiento del juego",
      "minItems": 0,
      "items": {
        "bsonType": "string",
        "description": "objeto de referencia de mantenimiento realizado"
      }
    },
    "incidencias": {
      "bsonType": "array",
      "description": "array de referencias a las incidencias reportadas para este juego",
      "minItems": 0,
      "items": {
        "bsonType": "string",
        "description": "objeto de referencia a la incidencia del juego"
      }
    },
  },
}

db.runCommand({ "collMod": "Juego", "validator": { $jsonSchema: SCHEME } })
