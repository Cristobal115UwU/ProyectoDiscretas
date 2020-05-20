import cv2
from ConvexHull import GrahamScan
from tkinter import *
from tkinter import messagebox
#Ventana emergente que indica las requerimientos para el funcionamiento del programa.
window = Tk()
window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
window.withdraw()
messagebox.showinfo(message="Antes de iniciar el programa, asegurese de tener una camara web, estar en una habitacion oscura y tener una lampara de escritorio a la mano :)", title="Bienvenido")
window.deiconify()
window.destroy()
window.quit()

#Usar camara principal
cap = cv2.VideoCapture(0)

#Medidas de la Region de Interes
x_roi = 100
y_roi = 100	
hight_roi = 380
width_roi = 540

#Colores
color_roi = (255,0,0)
color_contours = (0,255,255)
color_hull = (0,255,0)

#Area minima de los contornos
areaMin = 2000

#Limites
rightLim = width_roi - 2
leftLim = x_roi + 2
upLim = y_roi + 2
downLim = hight_roi - 2

while True:
	#Leer cuadros de video
	ret, frame = cap.read()
	if ret == False: break

	#Recortamos la region de interes ROI
	ROI = frame[x_roi:hight_roi, y_roi:width_roi]

	#Marcamos la ROI con un rectangulo 
	cv2.rectangle(frame,(x_roi-2,y_roi-2),(width_roi+2, hight_roi+2),color_roi,2)
	
	#Convertimos la ROI a escala de grises
	grayROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
	
	#Ajustamos el umbral a un valor de 60
	_,th = cv2.threshold(grayROI,60,255, cv2.THRESH_BINARY_INV)

	#Se suaviza la imagen
	th = cv2.medianBlur(th,9)

	#Se muestra la imagen umbralizada
	#cv2.imshow('Vision Umbral',th)
	
	#Detectamos los bordes
	imgCanny = cv2.Canny(th,100,100)

	#Se aumenta el ancho de los bordes
	imgDil = cv2.dilate(imgCanny, None, iterations=10)
	
	#Se muestran las imagenes
	cv2.imshow('canny',imgCanny)
	cv2.imshow('dilate',imgDil)

	#Encontramos los contornos en la imagen
	contornos,_ = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	for c in contornos:
		area = cv2.contourArea(c)
		if area > areaMin:
			#Hacemos comvex hull mediante graham scan a cada contorno.
			hull1,xMin,yMin,xMax,yMax = GrahamScan(c)
			
			#Dibujamos el casco
			cv2.drawContours(ROI,[hull1],0,color_hull,3)
			
			#Verificamos las colisiones
			if xMax[0] + x_roi >= rightLim:
				cv2.putText(frame,"Colision", (550,230), 1, 1.3, (0,0,255), thickness=2)

			if xMin[0] + x_roi <= leftLim:
				cv2.putText(frame,"Colision", (10,230), 1, 1.3, (0,0,255), thickness=2)

			if yMin[1] + y_roi <= upLim:
				cv2.putText(frame,"Colision", (300,50), 1, 1.3, (0,0,255), thickness=2)

			if yMax[1] + y_roi >= downLim:
				cv2.putText(frame,"Colision", (300,440), 1, 1.3, (0,0,255), thickness=2)
	
	#Mostramos el video
	cv2.imshow('Vision normal', frame)

	#Cerramos el programa con 'esc'	
	k = cv2.waitKey(20)
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()