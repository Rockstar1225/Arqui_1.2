db.createCollection('EncuestaSatisfaccion')

db.EncuestaSatisfaccion.createIndex( {"id":1}, {unique:1} )

SCHEME={
   "bsonType": "object",
   "description": "Objeto que representa una encuesta de satisfacción de los usuarios hacia un area recreativa",
   "required": ["id","fechaEncuesta","puntuacionAccesibilidad","puntuacionCalidad","comentarios"],
   "properties": {
           "id": {
               "bsonType": "string",
               "description": "Tipo String. Clave Primaria"
           },
           "fechaEncuesta": {
               "bsonType": "date",
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
               "bsonType": "array",
               "description": "Lista de comentarios en formato string",
               "minItems": 0,
               "items": {
                  "bsonType": "string",
                  "description": "comentario de un usuario hacia el area recreativa", 
               } 
           } 
    },
}

db.runCommand({ "collMod": "EncuestaSatisfaccion", "validator": { $jsonSchema: SCHEME } })
