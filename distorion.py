import cv2
import numpy as np

# Leemos la imagen y la matriz de calibración de la cámara previamente obtenida
img = cv2.imread('imagen_distorsionada.jpg')
K = np.load('matriz_calibracion.npy')

# Obtenemos los coeficientes de distorsión de la matriz de calibración
dist_coef = K[:, -1]
K = K[:, :-1]

# Obtenemos los tamaños de la imagen
height, width = img.shape[:2]

# Creamos la nueva matriz de calibración para la corrección de distorsión
new_K, roi = cv2.getOptimalNewCameraMatrix(K, dist_coef, (width, height), 1, (width, height))

# Corregimos la distorsión de la imagen
img_undistorted = cv2.undistort(img, K, dist_coef, None, new_K)

# Mostramos la imagen original y la imagen corregida
cv2.imshow('Imagen Original', img)
cv2.imshow('Imagen Corregida', img_undistorted)
cv2.waitKey(0)
cv2.destroyAllWindows()