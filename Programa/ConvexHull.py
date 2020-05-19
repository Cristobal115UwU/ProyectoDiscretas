import numpy as np 
import math
from operator import itemgetter

#Fucnion que convierte un arreglo de [n][1][2] a una lista [n][2]
def arrayToList(array):
    arr = np.resize(array,(len(array),2))
    arr.tolist()
    return arr

#Funcion que convierte una lista [n][2] a un arreglo [n][1][2]
def listToArray( lista ):
    hullArray = np.array(lista ,dtype=int)
    hullArray = np.resize(hullArray,(len(lista),1,2))
    return hullArray

#Funcion que devuelve el angulo polar de dos puntos
def polarAngle(p0, p1=None):
    if p1 == None: p1 = ancla
    yDif = p0[1] - p1[1]
    xDif = p0[0] - p1[0]
    return math.atan2(yDif,xDif)

#Funcion que devuelve el sentido de tres puntos
def det(p1,p2,p3):
    return (p2[0]-p1[0])*(p3[1]-p1[1]) \
        -(p2[1]-p1[1])*(p3[0]-p1[0])

#Funcion que ordena los puntos con respecto a su angulo polar
def sortAnglePoints( puntos ):
    aux = sorted(puntos, key = polarAngle )
    return aux

#Funcion Graham scan
def GrahamScan( arrayPuntos ):
    global ancla
    #Convertimos el arreglo a lista
    pointsList = arrayToList(arrayPuntos)
    #Ordenamos la lista respecto a las ordenadas
    sortList = sorted(pointsList, key=itemgetter(1,0) )
    #Definimos nuestro punto 0
    ancla = sortList[0]
    #Ordenamos los puntos respecto a su angulo con el punto 0
    sortedList = sortAnglePoints( sortList )
    #Eliminamos el punto 0 de la lista de puntos
    del sortedList[sortedList.index(ancla)]

    #Creamos una nueva lista y agregamos el punto 0 y el primer punto de la lista ordenada
    hull = [ancla, sortedList[0] ]
    #Para cada punto en la lista, se obtiene su sentido
    for s in sortedList[1:]:
        while det(hull[-2], hull[-1], s) <= 0:
            del hull[-1]
            if len(hull) < 2: break
        hull.append(s)
    #Ordenamos la lista de puntos del casco con respecto a la absisa y obtenemos el punto maximo y minimo
    limites = sorted(hull,key=itemgetter(0))
    xMin = limites[0]
    xMax = limites[-1]
    #Ordenamos la lista de puntos del casco con respecto a la ordenada y obtenemos el punto maximo y minimo
    limites = sorted(hull,key=itemgetter(1))
    yMin = limites[0]
    yMax = limites[-1]
    
    #Devolvemos el arreglo de puntos del casco convexo y los limites
    return (listToArray(hull), xMin, yMin, xMax, yMax)