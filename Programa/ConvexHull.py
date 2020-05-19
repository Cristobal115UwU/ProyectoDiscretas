#import matplotlib.pyplot as plt 
import numpy as np 
#import random as rnd
import math
from operator import itemgetter

"""
def createPoints(n):
    arrayPoints = np.zeros((n,1,2))
    for i in range(n):
        for k in range(2):
            arrayPoints[i][0][k] =  rnd.randint(0,100)
    return arrayPoints
"""
def arrayToList(array):
    puntosList = []
    for i in range(len(array)):
        puntosList.append((array[i][0][0],array[i][0][1]))
    return puntosList

def polarAngle(p0, p1=None):
    if p1 == None: p1 = ancla
    yDif = p0[1] - p1[1]
    xDif = p0[0] - p1[0]
    return math.atan2(yDif,xDif)

def det(p1,p2,p3):
    return (p2[0]-p1[0])*(p3[1]-p1[1]) \
        -(p2[1]-p1[1])*(p3[0]-p1[0])

def sortAnglePoints( puntos ):
    aux = sorted(puntos, key = polarAngle )
    return aux

def GrahamScan( arrayPuntos ):
    global ancla
    pointsList = arrayToList(arrayPuntos)
    sortList = []
    sortList = sorted(pointsList, key=itemgetter(1,0) )
    ancla = sortList[0]
    sortedList = sortAnglePoints( sortList )
    del sortedList[sortedList.index(ancla)]

    hull = [ancla, sortedList[0] ]
    for s in sortedList[1:]:
        while det(hull[-2], hull[-1], s) <= 0:
            del hull[-1]
            if len(hull) < 2: break
        hull.append(s)
    
    hullArray = np.ndarray((len(hull),1,2),dtype=int)
    for i in range(len(hull)):
        hullArray[i][0] = hull[i]
    return hullArray

"""
#Programa para pruebas jaja

arrayPoints = createPoints(500)
hullPoints = GrahamScan(arrayPoints)

x = [arrayPoints[i][0][0] for i in range(len(arrayPoints))]
y = [arrayPoints[i][0][1] for i in range(len(arrayPoints))]

xHull = [hullPoints[i][0] for i in range(len(hullPoints))]
xHull.append(hullPoints[0][0])

yHull = [hullPoints[i][1] for i in range(len(hullPoints))]
yHull.append(hullPoints[0][1])

plt.plot(x,y,'g.')
plt.plot(xHull,yHull,'ro-')
plt.grid(True)
plt.show()
"""