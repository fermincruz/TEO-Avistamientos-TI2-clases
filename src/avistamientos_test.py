import avistamientos
from datetime import datetime, date
from coordenadas import *


def test_lee_avistamientos(datos):
    print("Test de lee_avistamientos")
    print(f"Se han leido {len(datos)}  avistamientos")
    print("Los cinco avistamientos primeros son: ")
    for a in datos[:5]:
        print("\t", a)
    print("Los cinco avistamientos últimos son: ")
    for a in datos[-5:]:
        print("\t", a)
    print("=======================================================\n")


def test_numero_avistamientos_fecha(datos):
    print("Test de numero_avistamientos_fecha")
    res = avistamientos.numero_avistamientos_fecha(datos, date(2005, 5, 1))
    print(f"El día 5 de enero de 2005 se produjeron {res} avistamientos")
    print("=======================================================\n")


def test_formas_estados(datos):
    print("Test de formas_estados")
    res = avistamientos.formas_estados(datos, {"in", "nm", "pa", "wa"})
    print(
        f"Número de formas distintas observadas en los estados in, nm, pa o wa: {res}"
    )
    print("=======================================================\n")


def test_duracion_total(datos):
    print("Test de duracion_total")
    res = avistamientos.duracion_total(datos, {"in", "nm", "pa", "wa"})
    print(
        f"Duración total de los avistamientos en in, nm, pa o wa: {res} segundos."
    )
    print("=======================================================\n")


def test_avistamientos_cercanos_ubicacion(datos):
    print("Test de avistamientos_cercanos_ubicacion")
    res = avistamientos.avistamientos_cercanos_ubicacion(
        datos, Coordenadas(40.1933333, -85.3863889), 0.1
    )
    print("Avistamientos cercanos a (40.1933333, -85.3863889):")
    for a in res:
        print("\t", a)
    print("=======================================================\n")


def test_avistamiento_mayor_duracion(datos):
    print("Test de avistamiento_mayor_duracion")
    res = avistamientos.avistamiento_mayor_duracion(datos, "circle")
    print(f"Avistamiento de forma 'circle' de mayor duración: {res}")
    print("=======================================================\n")


def test_avistamiento_cercano_mayor_duracion(datos):
    print("Test de avistamiento_cercano_mayor_duracion")
    duracion, comentario = avistamientos.avistamiento_cercano_mayor_duracion(
        datos, Coordenadas(40.1933333, -85.3863889), 0.5
    )
    print(
        f"Duración del avistamiento más largo en un entorno de radio 0.5 sobre\
             las coordenadas (40.1933333, -85.3863889): {duracion}"
    )
    print(f"Comentario: {comentario}")
    print("=======================================================\n")


def test_avistamientos_fechas_1(datos):
    print("Test de avistamientos_fechas (1 de 3)")
    avistamientos_fec = avistamientos.avistamientos_fechas(
        datos, date(2005, 5, 1), date(2005, 5, 1)
    )
    print("Mostrando los avistamientos del 1 de mayo de 2005:")
    for a in avistamientos_fec:
        print("\t", a)
    print("=======================================================\n")


def test_avistamientos_fechas_2(datos):
    print("Test de avistamientos_fechas (2 de 3))")
    avistamientos_fec = avistamientos.avistamientos_fechas(
        datos, fecha_final=date(2005, 5, 1)
    )
    print("Avistamientos hasta el 1 de mayo de 2005:", len(avistamientos_fec))
    print("=======================================================\n")


def test_avistamientos_fechas_3(datos):
    print("Test de avistamientos_fechas (3 de 3))")
    avistamientos_fec = avistamientos.avistamientos_fechas(
        datos, fecha_inicial=date(2005, 5, 1)
    )
    print("Avistamientos desde el 1 de mayo de 2005:", len(avistamientos_fec))
    print("=======================================================\n")


def test_comentario_mas_largo(datos):
    print("Test de comentario_mas_largo")
    print(
        f'El avistamiento con el comentario más largo de 2005 incluyendo la palabra "ufo" es:'
    )
    print(avistamientos.comentario_mas_largo(datos, 2005, "ufo"))
    print("=======================================================\n")


def test_media_dias_entre_avistamientos_1(datos):
    print("Test de media_dias_entre_avistamientos (1 de 2)")
    media = avistamientos.media_dias_entre_avistamientos(datos)
    print("La media entre dos avistamientos consecutivos es", media)
    print("=======================================================\n")


def test_media_dias_entre_avistamientos_2(datos):
    print("Test de media_dias_entre_avistamientos (2 de 2)")
    media = avistamientos.media_dias_entre_avistamientos(datos, 1979)
    print("La media entre dos avistamientos consecutivos en 1979 es", media)
    print("=======================================================\n")


def test_avistamientos_por_fecha(datos):
    print("Test de avistamientos_por_fecha")
    indice = avistamientos.avistamientos_por_fecha(datos)
    print(
        "Avistamientos por fecha  (solo se muestran 3 fechas aleatorias y 3 avistamientos de cada una máximo):"
    )
    for clave, valores in list(indice.items())[:3]:
        print(clave)
        for v in list(valores)[:3]:
            print("\t", v)
    print("=======================================================\n")


def test_formas_por_mes(datos):
    print("Test de formas_por_mes")
    indice = avistamientos.formas_por_mes(datos)
    for mes, formas in indice.items():
        print(f"{mes} ==> {sorted(formas)}")
    print("=======================================================\n")


def test_numero_avistamientos_por_año(datos):
    print("Test de numero_avistamientos_por_año")
    d = avistamientos.numero_avistamientos_por_año(datos)
    print("Número de avistamientos por año:")
    for año, numero in d.items():
        print(f"{año}: {numero}")
    print("=======================================================\n")


def test_num_avistamientos_por_mes(datos):
    print("Test de num_avistamientos_por_mes")
    d = avistamientos.num_avistamientos_por_mes(datos)
    print("Número de avistamientos por mes")
    for mes, numero in d.items():
        print(f"{mes}: {numero}")
    print("=======================================================\n")


def test_coordenadas_mas_avistamientos(datos):
    print("Test de coordenadas_mas_avistamientos")
    res = avistamientos.coordenadas_mas_avistamientos(datos)
    print(
        f"Coordenadas redondeadas de la región en la que se observaron más avistamientos: ({res.latitud}, {res.longitud})"
    )
    print("=======================================================\n")


def test_hora_mas_avistamientos(datos):
    print("Test de hora_mas_avistamientos")
    res = avistamientos.hora_mas_avistamientos(datos)
    print(f"Hora en la que se han observado más avistamientos: {res}")
    print("=======================================================\n")


def test_longitud_media_comentarios_por_estado(datos):
    print("Test de longitud_media_comentarios_por_estado")
    d = avistamientos.longitud_media_comentarios_por_estado(datos)
    print(
        "Mostrando la media de la longitud de los comentarios de los avistamientos de los estados:"
    )
    for estado, longitud in d.items():
        print(f"{estado}: {longitud}")
    print("=======================================================\n")


def test_porc_avistamientos_por_forma(datos):
    print("Test de porc_avistamientos_por_forma")
    d = avistamientos.porc_avistamientos_por_forma(datos)
    print("Porcentajes de avistamientos de las distintas formas")
    for forma, porcentaje in d.items():
        print(f"{forma}: {porcentaje}")
    print("=======================================================\n")


def test_avistamientos_mayor_duracion_por_estado(datos):
    print("Test de avistamientos_mayor_duracion_por_estado")
    d = avistamientos.avistamientos_mayor_duracion_por_estado(datos)
    print(f"Mostrando los 3 avistamientos de mayor duración por estado")
    for estado, av in d.items():
        print(estado)
        for a in av:
            print("\t", av)
    print("=======================================================\n")


def test_año_mas_avistamientos_forma(datos):
    print("Test de año_mas_avistamientos_forma")
    año = avistamientos.año_mas_avistamientos_forma(datos, "circle")
    print(f"Año con más avistamientos de tipo 'circle': {año}")
    print("=======================================================\n")


def test_estados_mas_avistamientos(datos):
    print("Test de estados_mas_avistamientos")
    estados = avistamientos.estados_mas_avistamientos(datos)
    print(
        f"Estados con más avistamientos, de mayor a menor nº de avistamientos: {estados}"
    )
    print("=======================================================\n")


def test_duracion_total_avistamientos_año(datos):
    print("Test de duracion_total_avistamientos_año")
    d = avistamientos.duracion_total_avistamientos_año(datos, "ca")
    print(
        f"Mostrando la duración total de los avistamientos por año en el estado 'ca'"
    )
    for año, duracion in d.items():
        print(f"{año}: {duracion}")
    print("=======================================================\n")


def test_avistamiento_mas_reciente_por_estado(datos):
    print("Test de avistamiento_mas_reciente_por_estado")
    d = avistamientos.avistamiento_mas_reciente_por_estado(datos)
    print("Mostrando la fecha del último avistamiento por estado")
    for estado, fecha in d.items():
        print(f"{estado}: {fecha}")
    print("=======================================================\n")


if __name__ == "__main__":
    datos = avistamientos.lee_avistamientos("data/ovnis.csv")
    #test_lee_avistamientos(datos)
    #test_numero_avistamientos_fecha(datos)
    # test_formas_estados(datos)
    # test_duracion_total(datos)
    # test_avistamientos_cercanos_ubicacion(datos)
    # test_avistamiento_mayor_duracion(datos)
    test_avistamiento_cercano_mayor_duracion(datos)
    # test_avistamientos_fechas_1(datos)
    # test_avistamientos_fechas_2(datos)
    # test_avistamientos_fechas_3(datos)
    # test_comentario_mas_largo(datos)
    # test_media_dias_entre_avistamientos_1(datos)
    # test_media_dias_entre_avistamientos_2(datos)
    # test_avistamientos_por_fecha(datos)
    # test_formas_por_mes(datos)
    # test_numero_avistamientos_por_año(datos)
    # test_num_avistamientos_por_mes(datos)
    # test_coordenadas_mas_avistamientos(datos)
    # test_hora_mas_avistamientos(datos)
    # test_longitud_media_comentarios_por_estado(datos)
    # test_porc_avistamientos_por_forma(datos)
    # test_avistamientos_mayor_duracion_por_estado(datos)
    # test_año_mas_avistamientos_forma(datos)
    # test_estados_mas_avistamientos(datos)
    # test_duracion_total_avistamientos_año(datos)
    # test_avistamiento_mas_reciente_por_estado(datos)
