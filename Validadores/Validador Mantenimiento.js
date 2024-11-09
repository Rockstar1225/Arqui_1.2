db.createCollection('Mantenimiento')

db.Mantenimiento.createIndex({ "id": 1 }, { unique: 1 })

SCHEME = {
  "bsonType": "object",
  "description": "Objeto que representa un incidente de seguridad",
  "required": ["id", "fechaIntervencion", "tipoIntervencion", "estadoPrevio", "estadoPosterior"],
  "properties": {
    "id": {
      "bsonType": "string",
      "description": "id del mantenimiento a realizar a un juego"
    },
    "tipoIntervencion": {
      "bsonType": "string",
      "description": "tipo de intervencion",
      "enum": ["CORRECTIVO", "EMERGENCIA", "PREVENTIVO"]
    },
    "estadoPrevio": {
      "bsonType": "string",
      "description": "estado previo a la intervencion",
    },
    "estadoPosterior": {
      "bsonType": "string",
      "description": "estado posterior a la intervencion",
    },
    "fechaIntervencion": {
      "bsonType": "string",
      "description": "fecha de intervencion de mantenimiento"
    },
    "incidencias": {
      "bsonType": "array",
      "description": "incidencias que referencia un mantenimiento",
      "minItems": 0,
      "items": {
        "bsonType": "number",
        "description": "objeto de referencia de incidencias realizadas"
      }
    }
  },
}

db.runCommand({ "collMod": "Mantenimiento", "validator": { $jsonSchema: SCHEME } })
