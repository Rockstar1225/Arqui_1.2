db.createCollection('RegistroClima')

db.RegistroClima.createIndex( {"id":1}, {unique:1} )

SCHEME={
   "bsonType": "object",
   "description": "Objeto que representa los datos del clima en la zona de una area recreativa",
   "required": ["id","fecha","temperatura","precipitacion","vientosFuertes"],
   "properties": {
        "id": {
            "bsonType": "string",
            "description": "id del registro del clima"
        },
        "temperatura": {
            "bsonType": "double",
            "description": "temperatura tomada en la zona del area recreativa",
        },
        "precipitacion": {
            "bsonType": "double",
            "description": "precipitacion tomada en la zona del area recreativa",
        },
        "fecha": {
            "bsonType": "date",
            "description": "fecha de la toma de muestras del clima"
        },
        "vientosFuertes": {
            "bsonType": "bool",
            "description": "si hacen vientos fuertes o no"
        }
    },
}

db.runCommand({ "collMod": "RegistroClima", "validator": { $jsonSchema: SCHEME } })