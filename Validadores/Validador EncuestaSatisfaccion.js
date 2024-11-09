db.createCollection('EncuestaSatisfaccion')

db.EncuestaSatisfaccion.createIndex({ "id": 1 }, { unique: 1 })

SCHEME = {
  "bsonType": "object",
  "description": "Objeto que representa una encuesta de satisfacción de los usuarios hacia un area recreativa",
  "required": ["id", "fechaEncuesta", "puntuacionAccesibilidad", "puntuacionCalidad", "comentarios"],
  "properties": {
    "id": {
      "bsonType": "number",
      "description": "Tipo String. Clave Primaria"
    },
    "fechaEncuesta": {
      "bsonType": "string",
      "description": "Fecha de realización de encuesta"
    },
    "puntuacionAccesibilidad": {
      "bsonType": "number",
      "minimum": 1,
      "maximum": 5,
      "description": "puntuaciones de los usuarios respecto a la accesibilidad",
    },
    "puntuacionCalidad": {
      "bsonType": "number",
      "minimum": 1,
      "maximum": 5,
      "description": "puntuaciones de los usuarios respecto a la calidad",
    },
    "comentarios": {
      "bsonType": "string",
      "description": "Lista de comentarios en formato string",
      "enum": ["ACEPTABLE", "DEFICIENTE", "EXCELENTE", "MUY BUENO", "REGULAR"]
    }
  },
}

db.runCommand({ "collMod": "EncuestaSatisfaccion", "validator": { $jsonSchema: SCHEME } })
