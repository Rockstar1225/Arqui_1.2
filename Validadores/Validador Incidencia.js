db.createCollection('Incidencia')

db.Incidencia.createIndex( {"id":1}, {unique:1} )
db.Incidencia.createIndex( {"usuarios.NIF":1}, {unique:1, sparse: true})

SCHEME={
   "bsonType": "object",
   "description": "Agregado de gestión del estado del juego, historial de mantenimiento y seguimiento de incidencias.",
   "required": ["id","tipo","fechaReporte","estado","tiempoResolucion","nivelEscalamiento","usuarios"],
   "properties": {
            "id": {
                "bsonType": "string", // Clave primaria
                "description": "id de la incidencia"
            },
            "tipo": {
                "bsonType": "string",
                "description": "tipo de incidencia al juego",
                "enum": ["Desgaste","Mal funcionamiento","Rotura","Vandalismo"]
            },
            "fechaReporte": {
                "bsonType": "date",
                "description": "fecha de reporte de la incidencia"
            },
            "estado": {
                "bsonType": "string",
                "description": "estado de la inicidencia",
                "enum": ["Abierta","Cerrada"]
            },
            "tiempoResolucion": {
               "bsonType": "double",
               "description": "tiempo en el que se resolverá la incidencia",
            },
            "nivelEscalamiento": {
               "bsonType": "number",
               "minimum": 1,
               "maximum": 10,
               "description": "Nivel de urgencia"
            },
            "usuarios": {
               "bsonType": "array",
               "description": "array de referencias a usuarios vinculados con esta incidencia",
               "minItems": 1,
               "items": {
                    "bsonType": "object",
                    "description": "objeto embedido del usuario",
                    "required": ["NIF","nombre","email","telefono"],
                    "properties": {
                        "NIF": {
                            "bsonType": "string",
                            "description": "Identificador de tipo string",
                        },
                        "nombre": {
                            "bsonType": "string",
                            "description": "nombre del usuario"
                        },
                        "email": {
                            "bsonType": "string",
                            "description": "email del usuario"
                        },
                        "telefono": {
                            "bsonType": "string",
                            "description": "telefono de los usuarios"
                        }
                   }
               } 
            },
    },
}

db.runCommand({ "collMod": "Incidencia", "validator": { $jsonSchema: SCHEME } })