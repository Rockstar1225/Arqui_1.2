db.createCollection('IncidenteSeguridad')

db.IncidenteSeguridad.createIndex({ "id": 1 }, { unique: 1 })

SCHEME = {
  "bsonType": "object",
  "description": "Objeto que representa un incidente de seguridad",
  "required": ["id", "fechaDeReporte", "tipoIncidente", "gravedad"],
  "properties": {
    "id": {
      "bsonType": "number",
      "description": "id del incidente de seguridad"
    },
    "tipoIncidente": {
      "bsonType": "string",
      "description": "tipo de incidencia de seguridad",
      "enum": ["ROBO", "CAIDA", "ACCIDENTE", "VANDALISMO", "DAÑO ESTRUCTURAL"]
    },
    "gravedad": {
      "bsonType": "string",
      "description": "gravedad del incidente",
      "enum": ["BAJA", "MEDIA", "ALTA", "CRITICA"]
    },
    "fechaDeReporte": {
      "bsonType": "string",
      "description": "fecha de reporte de la incidencia de seguridad"
    }
  },
}

db.runCommand({ "collMod": "IncidenteSeguridad", "validator": { $jsonSchema: SCHEME } })
