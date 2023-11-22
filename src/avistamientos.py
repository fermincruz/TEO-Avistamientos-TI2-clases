'''
Módulo avistamientos
Adaptación del notebook a proyecto: Toñi Reina
'''
import csv
from datetime import datetime
import math
from collections import namedtuple, Counter, defaultdict
from coordenadas import Coordenadas, distancia_haversine, redondear
from parsers import parse_datetime
import statistics
import locale

## Definición de tipos
Avistamiento = namedtuple('Avistamiento',
    'fechahora, ciudad, estado, forma, duracion, comentarios, coordenadas')

## 1. Operaciones de carga de datos
### 1.1 Función de lectura de datos
# Función de lectura que crea una lista de avistamientos
def lee_avistamientos(fichero):
    '''
    Lee un fichero de entrada y devuelve una lista de tuplas. 
    Para convertir la cadena con la fecha y la hora al tipo datetime, usar
        datetime.strptime(fecha_hora,'%m/%d/%Y %H:%M')    
    
    @param fichero: ruta del fichero csv que contiene los datos en codificación utf-8 
    @type fichero: str
    @return: lista de tuplas con la información de los avistamientos 
    @rtype: [Avistamiento(datetime, str, str, str, str, int, str, Coordenadas(float, float))]   
    '''
    avistamientos = []
    with open(fichero, encoding='utf-8') as f:       
        lector = csv.reader(f)
        next(lector)
        for cadena_fecha, city, state, shape, duration, comments, latitude, longitude \
                in lector:
            fecha = parse_datetime(cadena_fecha,'%m/%d/%Y %H:%M')
            duration = int(duration)
            coordenadas=Coordenadas(float(latitude), float(longitude))
            avistamientos.append(Avistamiento(fecha, city, state, shape, duration, \
                                comments, coordenadas))
    return avistamientos  

### 2.1 Número de avistamientos producidos en una fecha
def numero_avistamientos_fecha(avistamientos, fecha):
    ''' Avistamientos que se han producido en una fecha
    
    Toma como entrada una lista de avistamientos y una fecha.
    Devuelve el número de avistamientos que se han producido en esa fecha.

    @param avistamientos: lista de avistamientos
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param fecha: fecha del avistamiento 
    @type fecha: datetime.date
    @return:  Número de avistamientos producidos en la fecha 
    @rtype: int
    
    '''
    cont = 0
    for av in avistamientos:
        if av.fechahora.date() == fecha:
            cont += 1
    return cont      


# Por comprensión
def numero_avistamientos_fecha2(avistamientos, fecha):
    return sum(1 for av in avistamientos if av.fechahora.date() == fecha)

### 2.2 Número de formas observadas en un conjunto de estados
def formas_estados(avistamientos, estados):
    ''' 
    Devuelve el número de formas distintas observadas en avistamientos 
    producidos en alguno de los estados especificados.
    @param avistamientos: lista de tuplas con la información de los avistamientos
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float)))]
    @param estados: conjunto de estados para los que se quiere hacer el cálculo 
    @type estados: {str}
    @return: Número de formas distintas observadas en los avistamientos producidos
         en alguno de los estados indicados por el parámetro "estados"
    @rtype: int
    '''
    conjunto_formas = set()
    for a in avistamientos:
        if a.estado in estados:
            conjunto_formas.add(a.forma)
    return len(conjunto_formas)

def formas_estados2(avistamientos, estados):
    # Por comprensión
    return len({a.forma for a in avistamientos if a.estado in estados})
    
### 2.3 Duración total de los avistamientos en un estado
def duracion_total(avistamientos, estado):
    ''' 
    Devuelve la duración total de los avistamientos de un estado. 
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float)))]
    @param estado: estado para el que se quiere hacer el cálculo
    @type estado: str
    @return: duración total en segundos de todos los avistamientos del estado 
    @rtype: int
    '''
    duracion = 0
    for a in avistamientos:
        if a.estado == estado:
            duracion += a.duracion
    return duracion

def duracion_total2(avistamientos, estado):
    ## Por compresión
    return sum(a.duracion for a in avistamientos if a.estado == estado)


### 2.4 Avistamientos cercanos a una ubicación
def avistamientos_cercanos_ubicacion(avistamientos, ubicacion, radio):
    ''' 
    Devuelve el conjunto de avistamientos cercanos a una ubicación.
    @param avistamientos: lista de tuplas con la información de los avistamientos
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float)))]
    @param ubicacion: coordenadas de la ubicación para la cual queremos encontrar avistamientos cercanos 
    @type ubicacion: Coordenadas (float, float)
    @param radio: radio de distancia
    @param radio: float
    @return:Conjunto de avistamientos que se encuentran a una distancia
         inferior al valor "radio" de la ubicación dada por el parámetro "ubicacion" 
    @rtype: {Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))}
    '''
    conjunto_avistamientos = set()
    for a in avistamientos:
        if distancia_haversine(a.coordenadas, ubicacion) < radio:
            conjunto_avistamientos.add(a)
    return conjunto_avistamientos

def avistamientos_cercanos_ubicacion2(avistamientos, ubicacion, radio):
    ## Por compresión
    # TODO: Para casa
    pass


## Operaciones con máximos y mínimos
### 3.1 Avistamiento de una forma con mayor duración

def avistamiento_mayor_duracion(avistamientos, forma):
    '''
    Devuelve el avistamiento de mayor duración de entre todos los
    avistamientos de una forma dada.
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param forma: forma del avistamiento 
    @type forma: str
    @return:  avistamiento más largo de la forma dada
    @rtype: Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))
    '''
    lista_av_forma = []
    for a in avistamientos:
        if a.forma == forma:
            lista_av_forma.append(a)
    return max(lista_av_forma, key = lambda av:av.duracion) 
    

def avistamiento_mayor_duracion2(avistamientos, forma):
    # Por comprension
    # Si uso una expresión por comprensión como primer parámetro de una función
    # a la que voy a pasar más parámetros, tengo que poner entre paréntesis
    # la expresión por comprensión
    return max((a for a in avistamientos if a.forma == forma), 
               key = lambda av:av.duracion)

### 3.2 Avistamiento cercano a un punto con mayor duración
def avistamiento_cercano_mayor_duracion(avistamientos, coordenadas, radio=0.5):
    '''
    Devuelve la duración y los comentarios del avistamiento que más 
    tiempo ha durado de aquellos situados en el entorno de las
    coordenadas que se pasan como parámetro de entrada.
    El resultado debe ser una tupla de la forma (duración, comentarios)
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param coordenadas: tupla con latitud y longitud
    @type coordenadas: Coordenadas (float, float)
    @param radio: radio de búsqueda
    @type radio: float
    @return: duración y comentarios del avistamiento más largo en el entorno de las coordenadas comentarios del avistamiento más largo
    @rtype: int, str
    '''
    avistamientos_cercanos = []
    for a in avistamientos:
        if distancia_haversine(a.coordenadas, coordenadas) < radio:
            avistamientos_cercanos.append((a.duracion, a.comentarios))

    return max(avistamientos_cercanos)

    # Ya había una función que hacía lo anterior... o parecido:
    # avistamientos_cercanos = avistamientos_cercanos_ubicacion(avistamientos, coordenadas, radio)
    # avistamiento_mas_largo = max(avistamientos_cercanos, key= lambda a:a.duracion)
    # return (avistamiento_mas_largo.duracion, avistamiento_mas_largo.comentario)

def avistamiento_cercano_mayor_duracion2(avistamientos, coordenadas, radio=0.5):
    # Por comprensión
    return max((a.duracion, a.comentarios) 
               for a in avistamientos
               if distancia_haversine(a.coordenadas, coordenadas) < radio)


### 3.3 Avistamientos producidos entre dos fechas

def avistamientos_fechas(avistamientos, fecha_inicial=None, fecha_final=None):
    '''
    Devuelve una lista con los avistamientos que han tenido lugar
    entre fecha_inicial y fecha_final (ambas inclusive). La lista devuelta
    estará ordenada de los avistamientos más recientes a los más antiguos.
    
    Si fecha_inicial es None se devolverán todos los avistamientos
    hasta fecha_final.
    Si fecha_final es None se devolverán todos los avistamientos desde
    fecha_inicial.
    Si ambas fechas son None se devolverá la lista de 
    avistamientos completa. 
    
    Usar el método date() para obtener la fecha de un objeto datetime.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param fecha_inicial: fecha a partir de la cual se devuelven los avistamientos
    @type fecha_inicial:datetime.date
    @param fecha_final: fecha hasta la cual se devuelven los avistamientos
    @type fecha_final: datetime.date
    @return: lista de tuplas con la información de los avistamientos en el rango de fechas
    @rtype: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    '''
    # Vamos a hacerlo directamente por comprensión
    filtrado = [a  for a in avistamientos
                if (fecha_inicial == None or a.fechahora.date() >= fecha_inicial) and 
                   (fecha_final == None or a.fechahora.date() <= fecha_final)
    ]
    
    filtrado.sort(reverse=True)
    return filtrado
    
### 3.4 Avistamiento de un año con el comentario más largo
def comentario_mas_largo(avistamientos, anyo, palabra):
    ''' 
    Devuelve el avistamiento cuyo comentario es el más largo, de entre
    los avistamientos observados en el año dado por el parámetro "anyo"
    y cuyo comentario incluya la palabra recibida en el parámetro "palabra".
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param anyo: año para el que se hará la búsqueda 
    @type anyo: int
    @param palabra: palabra que debe incluir el comentario del avistamiento buscado 
    @type palabra: str
    @return: avistamiento con el comentario más largo
    @rtype: Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))
    '''    
    filtrado = [a for a in avistamientos 
                if a.fechahora.year == anyo and palabra in a.comentarios]
    return max(filtrado, key = lambda a:len(a.comentarios))
    
def comentario_mas_largo2(avistamientos, anyo, palabra):
    # Por comprensión
    return max(
        (a for a in avistamientos if a.fechahora.year == anyo and palabra in a.comentarios),
        key = lambda a:len(a.comentarios)
    )


### 3.5 Media de días entre avistamientos consecutivos
def media_dias_entre_avistamientos(avistamientos, anyo=None):
    ''' 
    Devuelve la media de días transcurridos entre dos avistamientos consecutivos.
    Si año es distinto de None, solo se contemplarán los avistamientos del año
    especificado para hacer el cálculo.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param anyo: año para el que se hará la búsqueda 
    @type anyo: int
    @return: media de días transcurridos entre avistamientos. Si no se puede realizar el
    cálculo, devuelve None 
    @rtype:-float
    '''    
    # Intenta primero dividir el problema en subproblemas
    # Para calcular los días entre dos fechas, abre un terminal,
    # prueba a restar dos fechas de tipo date y observa el tipo
    # que obtienes.
    
    if anyo != None:
        avistamientos = [a for a in avistamientos if a.fechahora.year == anyo]

    dias = calcula_dias_entre_avistamientos(avistamientos)

    if len(dias) == 0:
        return None
    return sum(dias)/len(dias)

def calcula_dias_entre_avistamientos(avistamientos):
    '''Devuelve una lista de enteros con los días que transcurren
    entre cada dos avistamientos consecutivos en el tiempo.'''
    avistamientos = sorted(avistamientos)

    res = []
    for a1, a2 in zip(avistamientos, avistamientos[1:]):
        res.append(
            (a2.fechahora.date() - a1.fechahora.date()).days
        )
    return res
        
## 4 Operaciones con diccionarios

### 4.1 Avistamientos por fecha
def avistamientos_por_fecha(avistamientos):
    ''' 
    Devuelve un diccionario que indexa los avistamientos por fechas
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return diccionario en el que las claves son las fechas de los avistamientos 
         y los valores son conjuntos con los avistamientos observados en esa fecha
    @rtype {datetime.date: {Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))}}
    '''
    res = defaultdict(set)
    for a in avistamientos:
        res[a.fechahora.date()].add(a)
    return res


### 4.2 Formas de avistamientos por mes
def formas_por_mes(avistamientos):
    ''' 
    Devuelve un diccionario que indexa las distintas formas de avistamientos
    por los nombres de los meses en que se observan.
    Por ejemplo, para el mes "Enero" se asociará un conjunto con todas las
    formas distintas observadas en dicho mes.
    
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return: diccionario en el que las claves son los nombres de los meses 
         y los valores son conjuntos con las formas observadas en cada mes
    @rtype {str: {str}}
    '''
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre",
             "Octubre", "Noviembre", "Diciembre"]
    res = defaultdict(set)
    for a in avistamientos:
        mes = meses[a.fechahora.month - 1]
        res[mes].add(a.forma)
    return res


### 4.3 Número de avistamientos por año
def numero_avistamientos_por_año(avistamientos):
    '''
    Devuelve el número de avistamientos observados en cada año.
             
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return: diccionario en el que las claves son los años
         y los valores son el número de avistamientos observados en ese año
    @rtype: {int: int}
    '''
    return Counter(a.fechahora.year for a in avistamientos)


### 4.4 Número de avistamientos por mes del año
def num_avistamientos_por_mes(avistamientos):
    '''
    Devuelve el número de avistamientos observados en cada mes del año.
    Usar como claves los nombres de los doce meses con la inicial en mayúsculas.

    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return:diccionario en el que las claves son los nombres de los meses y 
         los valores son el número de avistamientos observados en ese mes
    @rtype: {str: int}
    '''
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre",
             "Octubre", "Noviembre", "Diciembre"]
    return Counter(meses[a.fechahora.month-1] for a in avistamientos)


### 4.5 Coordenadas con mayor número de avistamientos

def coordenadas_mas_avistamientos(avistamientos): 
    '''
    Devuelve las coordenadas enteras que se corresponden con 
    la zona donde más avistamientos se han observado.

    Usa la función de coordenadas.py "redondear" para obtener
    la parte entera de las coordenadas.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]

    @return: Coordenadas (sin decimales) que acumulan más avistamientos
    @rtype: Coordenadas(float, float)
    '''   
    avistamientos_por_coordenadas = Counter(redondear(a.coordenadas) for a in avistamientos)
    # most_common devuelve una LISTA de las tuplas (clave, valor), por lo que para quedarnos
    # con la clave (el elemento más frecuente), debemos acceder primero al primer elemento
    # de esa lista, y después al primer elemento de la tupla (la clave)
    return avistamientos_por_coordenadas.most_common(1)[0][0]

    # Como Counter es un diccionario, también podemos buscar el máximo de los items
    # pidiéndole a max que se fije en los conteos (Segundo elemento de los items)
    return max(avistamientos_por_coordenadas.items(), key = lambda t:t[1])[0]


### 4.6 Hora del día con mayor número de avistamientos
def hora_mas_avistamientos(avistamientos):
    ''' 
    Devuelve la hora del día (de 0 a 23) con mayor número de avistamientos
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return: hora del día en la que se producen más avistamientos
    @rtype: int
       
    En primer lugar construiremos un diccionario cuyas claves sean las horas del
    día en las que se han observado avistamientos, y cuyos valores sean el número
    de avistamientos observados en esa hora.
    Después obtendremos el máximo de los elementos del diccionario según el valor
    del elemento.
    '''
    #  TODO: Para casa
    pass



### 4.7 Longitud media de los comentarios por estado

def longitud_media_comentarios_por_estado(avistamientos):
    '''
    Devuelve un diccionario en el que las claves son los estados donde se
    producen los avistamientos y los valores son la longitud media de los
    comentarios de los avistamientos en cada estado.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return: diccionario que almacena la longitud media de los comentarios (valores)
         por estado (claves)
    @rtype: {str: float}
    '''
    # Intenta primero descomponer el problema en subproblemas
    pass



### 4.8 Porcentaje de avistamientos por forma
def porc_avistamientos_por_forma(avistamientos):  
    '''
    Devuelve un diccionario en el que las claves son las formas de los
    avistamientos, y los valores los porcentajes de avistamientos con cada forma.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return:  diccionario que almacena los porcentajes de avistamientos (valores)
         por forma (claves)
    @rtype: {str: float}
            
    En primer lugar crearemos un diccionario cuyas claves sean las formas
    y cuyos valores sean el número de avistamientos de esa forma.
    Después crearemos un segundo diccionario con las mismas claves y cuyos valores
    resulten de dividir los valores del diccionario anterior por el número
    total de avistamientos, para obtener los porcentajes.
    '''  
    pass



### 4.9 Avistamientos de mayor duración por estado
def avistamientos_mayor_duracion_por_estado(avistamientos, n=3):
    '''
    Devuelve un diccionario que almacena los n avistamientos de mayor duración 
    en cada estado, ordenados de mayor a menor duración.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param n: número de avistamientos a almacenar por cada estado 
    @type n: int
    @return: diccionario en el que las claves son los estados y los valores son listas 
         con los "n" avistamientos de mayor duración de cada estado,
         ordenados de mayor a menor duración
            -> {str: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]}
    '''
    # Intenta primero descomponer el problema en subproblemas
    # (y si los pasos se implementan en funciones auxiliares, puedes reutilizarlos...)
    pass

### 4.10 Año con más avistamientos de una forma
def año_mas_avistamientos_forma(avistamientos, forma):
    '''
    Devuelve el año en el que se han observado más avistamientos
    de una forma dada.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param forma: forma del avistamiento 
    @type: str
    @return: año con mayor número de avistamientos de la forma dada
    @rtype: int
            
    
    En primer lugar se crea un diccionario con filtro cuyas claves sean los años
    y cuyos valores sean el número de avistamientos observados en ese año,
    utilizando la función ya definida numero_avistamientos_por_año.
    Luego, se calcula el máximo del diccionario según los valores.
    '''
    #  TODO: Para casa
    pass


### 4.11 Estados con mayor número de avistamientos
def estados_mas_avistamientos(avistamientos, n=5):
    '''
    Devuelve una lista con los estados en los que se han observado
    más avistamientos, junto con el número de avistamientos,
    ordenados de mayor a menor número de avistamientos.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param n: número de estados a devolver 
    @type n: int  
    @return: lista con los estados donde se han observado más avistamientos,
         junto con el número de avistamientos, en orden decreciente
         del número de avistamientos y con un máximo de "limite" estados.
    @rtype: [(str, int)]
    '''
    pass

      
### 4.12 Duración total de los avistamientos de cada año en un estado dado
def duracion_total_avistamientos_año(avistamientos, estado):
    '''
    Devuelve un diccionario que almacena la duración total de los avistamientos 
    en cada año, para un estado dado.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @param estado: nombre del estado
    @type estado: str
    @return: diccionario en el que las claves son los años y los valores son números 
         con la suma de las duraciones de los avistamientos observados ese año
         en el estado dado
    @rtype: {int: int}

    Se crea un diccionario con filtro cuyas claves sean los años
    y cuyos valores sean la suma de las duraciones de todos los avistamientos
    observados en ese año.
    '''
    pass


### 4.13 Fecha del avistamiento más reciente de cada estado
def avistamiento_mas_reciente_por_estado(avistamientos):
    '''
    Devuelve un diccionario que almacena la fecha del último avistamiento
    observado en cada estado.
    
    @param avistamientos: lista de tuplas con la información de los avistamientos 
    @type avistamientos: [Avistamiento(datetime, str, str, str, int, str, Coordenadas(float, float))]
    @return:  diccionario en el que las claves son los estados y los valores son 
         las fechas del último avistamientos observado en ese estado.
    @rtype: {str: datetime.datetime}
            
    En primer lugar crearemos un diccionario cuyas claves sean los estados
    y cuyos valores sean listas con los avistamientos observados en ese estado.
    Para ello usamos la función auxiliar  definida en el apartado 4.7
    Después crearemos un segundo diccionario cuyas claves sean los estados y
    cuyos valores sean los valores máximos de las listas, según el campo fechahora.
    '''
    pass
