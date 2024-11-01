db.createCollection('IncidenteSeguridad')

db.IncidenteSeguridad.createIndex( {"id":1}, {unique:1} )

SCHEME={
   "bsonType": "object",
   "description": "Objeto que representa un incidente de seguridad",
   "required": ["id","fechaReporte","tipoIncidente","gravedad"],
   "properties": {
        "id": {
            "bsonType": "string",
            "description": "id del incidente de seguridad"
        },
        "tipoIncidente": {
            "bsonType": "string",
            "description": "tipo de incidencia de seguridad",
            "enum": ["Robo", "Caida","Accidente","Vandalismo","Daño estructural" ]
        },
        "gravedad": {
            "bsonType": "string",
            "description": "gravedad del incidente",
            "enum": [ "Baja","Media","Alta","Crítica" ]
        },
        "fechaDeReporte": {
            "bsonType": "date",
            "description": "fecha de reporte de la incidencia de seguridad"
        }
    },
}

db.runCommand({ "collMod": "IncidenteSeguridad", "validator": { $jsonSchema: SCHEME } })
