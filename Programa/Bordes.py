import cv2

#Importar un video
#cap = cv2.VideoCapture('video3.mp4')

#Usar camara principal
cap = cv2.VideoCapture(0)

#Medidas de la Region de Interes
x_roi = 100
y_roi = 100	
hight_roi = 380
width_roi = 540

#Colores
color_roi = (0,0,255)
color_contours = (0,255,255)
color_hull = (255,0,0)

#Area minima de los contornos
areaMin = 2000


while True:
	#Leer cuadros de video
	ret, frame = cap.read()
	if ret == False: break

	#Recortamos la region de interes
	ROI = frame[x_roi:hight_roi, y_roi:width_roi]
	#Marcamos la ROI con un rectnagulo 
	cv2.rectangle(frame,(x_roi-2,y_roi-2),(width_roi+2, hight_roi+2),color_roi,3)
	
	#Convertimos la ROI a escala de grises
	grayROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
	
	#Ajustamos el umbral a un valor de 60
	_,th = cv2.threshold(grayROI,60,255, cv2.THRESH_BINARY_INV)

	#Se suaviza la imagen
	th = cv2.medianBlur(th,9)

	#Se muestra la imagen ubralizada
	cv2.imshow('th',th)
	
	#Detectamos los bordes
	imgCanny = cv2.Canny(th,100,100)

	#Se aumenta el ancho de los bordes
	imgDil = cv2.dilate(imgCanny, None, iterations=2)
	
	#Se muestran las imagenes
	#cv2.imshow('canny',imgCanny)
	#cv2.imshow('dilate',imgDil)

	#Encontramos los contornos en la imagen
	contornos,_ = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	for c in contornos:
		area = cv2.contourArea(c)
		if area > areaMin:
			#Dibujamos el contorno si el area es mayor al area minima
			cv2.drawContours(ROI, c,-1,color_contours,3)
			#"""
			#Aplicamos convexHull a cada contorno.
			##Cada contorno es una matriz de puntos de [n][1][3]
			hull1 = cv2.convexHull(c)
			cv2.drawContours(ROI,[hull1],0,color_hull,3)
			#"""
	
	#Mostramos el video
	cv2.imshow('Frame', frame)

	#Cerramos el programa con 'esc'	
	k = cv2.waitKey(20)
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()