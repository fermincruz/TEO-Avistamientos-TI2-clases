## Definición de tipos
# Creación de una tupla con nombre para las coordenadas
from collections import namedtuple
from math import radians, sin, cos, asin, sqrt
Coordenadas = namedtuple('Coordenadas', 'latitud, longitud')

def a_radianes(coordenadas):
    '''Convierte unas coordenadas en grados a radianes

    @param coordenadas: Coordenadas que se quieren convertir a radianes
    @type coordenadas: Coordenadas(float, float)
    @return: Las coordenadas convertidas a radianes
    @rtype: Coordenadas(float, float)
    '''
    return Coordenadas(radians(coordenadas.latitud), radians(coordenadas.longitud))


def distancia_haversine(coordenadas1, coordenadas2):
    '''Devuelve la distancia de harvesine entre dos coordenadas

    @param coordenadas1: Coordenadas del primer punto
    @type coordenadas1: Coordenadas(float, float)
    @param coordenadas2: Coordenadas del segundo punto
    @type coordenadas2: Coordenadas(float, float)
    @return: La distancia harvesine entre las dos coordenadas dadas como parámetro
    @rtype: float
    '''
    coordenadas1 = a_radianes(coordenadas1)
    coordenadas2 = a_radianes(coordenadas2)
    dlon = coordenadas2.longitud - coordenadas1.longitud 
    dlat = coordenadas1.latitud - coordenadas1.latitud 
    a = sin(dlat/2)**2 + cos(coordenadas1.latitud) * cos(coordenadas2.latitud) * sin(dlon/2)**2
    r = 6371 # Radio de la tierra en kilómetors
    d = 2 * r * asin(sqrt(a)) 
    return d

def redondear(coordenadas):
    '''Devuelve unas coordenadas cuya latitud y longitud son 
    el redondeo de la latitud y la longitud de las coordenadas originales

    @param coordenadas: Coordenadas que se quieren convertir a radianes
    @type coordenadas: Coordenadas(float, float)
    @return: Las coordenadas redondeadas
    @rtype: Coordenadas(float, float)

    '''
    return Coordenadas(round(coordenadas.latitud), round(coordenadas.longitud))