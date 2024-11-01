db.createCollection('Juego')
db.Juego.createIndex( {"id":1}, {unique:1} )
db.Juego.createIndex( {"mantenimientos.id":1}, {unique:1, sparse: true})
db.Juego.createIndex( {"incidencias.id":1}, {unique:1, sparse: true})

SCHEME={
   "bsonType": "object",
   "description": "Agregado de gestión del estado del juego, historial de mantenimiento y seguimiento de incidencias.",
   "required": ["id","nombre","modelo","estadoOperativo","accesibilidad","fechaInstalacion","tipo","desgasteAcumulado","indicadorExposicion","ultimaFechaMantenimiento","mantenimientos","incidencias"],
   "properties": {
           "id": {
               "bsonType": "string",
               "description": "Tipo String. Clave Primaria"
           },
           "nombre": {
               "bsonType": "string",
               "description": "nombre del juego"
           }
           "modelo": {
               "bsonType": "string",
               "description": "Modelo de fabricacion del juego"
           },
           "estadoOperativo": {
               "bsonType": "string",
               "description": "Estado del juego",
               "enum": ["Operativo","Indispuesto"]
           },
           "accesibilidad": {
               "bsonType": "bool",
               "description": "Si el juego es accesible por la gente o no"
           },
           "fechaInstalacion": {
               "bsonType": "date",
               "description": "Fecha de instalacion del juego"
           },
           "tipo": {
               "bsonType": "string",
               "description": "Tipo de juego",
               "enum": ["deportivas","infantiles","mayores"]
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
               "enum": ["intacto","bajo","medio","alto"]
           },
           "ultimaFechaMantenimiento": {
               "bsonType": "date",
               "description": "ultima fecha de mantenimiento del juego"
           }

           "mantenimientos": {
               "bsonType": "array",
               "description": "array de referencias a registros de mantenimiento del juego",
               "minItems": 0,
               "items": {
                  "bsonType": "object",
                  "description": "objeto de referencia de mantenimiento realizado",
                  "required": ["id"],
                  "properties": {
                     "id": {
                        "bsonType": "string",
                        "description": "id del mantenimiento realizado al juego",
                     },
                  }
               } 
           },
           "incidencias" : {
               "bsonType": "array",
               "description": "array de referencias a las incidencias reportadas para este juego",
               "minItems": 0,
               "items": {
                  "bsonType": "object",
                  "description": "objeto de referencia a la incidencia del juego",
                  "required": ["id", "tipo","fechaReporte","estado"],
                  "properties": {
                     "id": {
                        "bsonType": "string", // Clave primaria
                        "description": "id de la incidencia"
                     }, 
                     "estado": {
                        "bsonType": "string",
                        "description": "estado de la inicidencia",
                        "enum": [ "Abierta","Cerrada" ]
                     }
                  }
               }
           },
    },
}

db.runCommand({ "collMod": "Juego", "validator": { $jsonSchema: SCHEME } })