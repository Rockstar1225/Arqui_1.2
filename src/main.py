import load as ld
import change as ch
import imputation as im
import formater_mongo as mongo_creator


def main():
    base = ld.load_db()
    ch.adjust_gps(base)
    ch.adjust_ETRS89(base)
    ch.empty_data(base)
    im.area_new_atribute(base)
    im.juegos_new_atributes(base)
    im.new_meteo(base)
    ch.no_duplicates(base)
    im.area_meteo(base)
    for tab_name in base:
        for column_name in base[tab_name]:
            ch.reformatear_fecha(base, tab_name, column_name)
            if type(base[tab_name][column_name][0]) is str:
                ch.capitalize_column(base, tab_name, column_name)
    ch.delete_special(base)
    ch.enum_checker(base)
    ch.check_id(base)
    ch.nif_status(base)
    ch.formato_tlf(base)
    ch.incidencias_status(base)
    im.tiempoResolucion(base)
    im.lastFecha(base)
    im.area_new_atribute(base)
    im.area_meteo(base)
    im.nivelEscalamiento(base)

    # Extracción de incidencias
    extractor = mongo_creator.Creator(base)
    # extractor.crear_area_clima()
    extractor.crear_juego_incidencias()
    extractor.crear_areas_incidentes()
    extractor.crear_area_encuestas()
    extractor.crear_area_juegos()
    extractor.crear_juegos_tipo()
    extractor.crear_area_clima()
    extractor.crear_incidencia_usuario()
    # Generar datos
    extractor.generar_usuarios()
    extractor.generar_encuestas()
    extractor.generar_incidentes()
    extractor.generar_incidencias()
    extractor.generar_clima()
    extractor.generar_area()
    extractor.generar_mantenimientos()
    extractor.generar_juegos()

    # Formatear datos
    extractor.get_json_data(extractor.incidentesSeguridad, "IncidenteSeguridad")
    extractor.get_json_data(extractor.areas, "AreaRecreativaClima")
    extractor.get_json_data(extractor.encuestas, "EncuestaSatisfaccion")
    extractor.get_json_data(extractor.incidencias, "Incidencia")
    extractor.get_json_data(extractor.juegos, "Juego")
    extractor.get_json_data(extractor.mantenimientos, "Mantenimiento")
    extractor.get_json_data(extractor.registrosClima, "RegistroClima")
    extractor.get_json_data(extractor.usuarios, "Usuario")
    # print(base)
    # print(base["Areas"]["MeteoID"])


if __name__ == "__main__":
    main()
