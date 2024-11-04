import pandas as pd
import datetime 
import load as ld
import change as ch
import imputation as im

def main():
    base = ld.load_db()
    ch.adjust_gps(base)
    ch.adjust_ETRS89(base)
    ch.empty_data(base)
    im.area_new_atribute(base)
    im.juegos_new_atributes(base)
    im.new_meteo(base)
    ch.no_duplicates(base)
    for tab_name in base:
        for column_name in base[tab_name]:
            ch.reformatear_fecha(base, tab_name, column_name)
            if type(base[tab_name][column_name][0]) == str:
                ch.capitalize_column(base, tab_name, column_name)
    ch.delete_special(base)
    im.tiempoResolucion(base)
    ch.enum_checker(base)
    ch.formato_tlf(base)
    ch.check_id(base)
    ch.nif_status(base)
    ch.incidencias_status(base)
    print(base)
main()