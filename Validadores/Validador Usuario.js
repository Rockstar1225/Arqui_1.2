db.createCollection('Usuario')

db.Usuario.createIndex( {"NIF":1}, {unique:1} )

SCHEME={
   "bsonType": "object",
   "description": "Objeto que representa un usuario de la zona recreativa",
   "required": ["NIF","nombre","email","telefono"],
   "properties": {
        "NIF": {
            "bsonType": "string",
            "description": "Identificador del usuario"
        },
        "nombre": {
            "bsonType": "string",
            "description": "nombre de usuario de la zona",
        },
        "email": {
            "bsonType": "string",
            "description": "email del usuario",
        },
        "telefono": {
            "bsonType": "string",
            "description": "telefono del usuario",
        } 
    },
}

db.runCommand({ "collMod": "Usuario", "validator": { $jsonSchema: SCHEME } })