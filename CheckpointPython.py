%matplotlib inline
import cv2
from matplotlib import pyplot as plt
import numpy as np
import math


img = cv2.imread('circulo.PNG')
img_rgb = circulo_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
circulo_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

min = np.array([0, 10, 0])
max = np.array([180, 255, 255])

# cria mascara que define o que o circulo, e o que não é
mascara_hsv = cv2.inRange(circulo_hsv, min, max)
# procura o contorno
contornos, _ = cv2.findContours(mascara_hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# ordena areas de contorno
contours = sorted(contornos, key=cv2.contourArea, reverse=True)
# define as duas maiores areas
largest_contours = contours[:2]
# desenha os contornos
contour_image = cv2.drawContours(img_rgb.copy(), largest_contours, -1, (0, 255, 0), 2)


for i, contour in enumerate(largest_contours):
    # Calcular a área do contorno
    area = cv2.contourArea(contour)

    # Calcular os momentos do contorno
    M = cv2.moments(contour)

    # Calcular o centro de massa (centroide) do contorno
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0

    # Desenhar o centro de massa no contorno
    # Se for para desenhar o + é assim, tive que corrigir o lugar do + por que ele fica torto
    # cv2.putText(contour_image, '+', (cX-10, cY+10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.circle(contour_image, (cX, cY), 5, (0, 0, 255), -1)


    # Exibir a área e o centro de massa na imagem
    print(f'Contorno {i+1}: Area={area}, Centro de Massa=({cX},{cY})', (20, 40+i*60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # armazena os dois centros de massa em uma variavel
    # entender por que foi necessario um if aqui
    if i == 0:
        c1 = (cX, cY)
    elif i == 1:
        c2 = (cX, cY)

    # desenha a linha entre os dois centros de massa
    cv2.line(contour_image, c1, c2, (0, 0, 0), 2)

# Calcular a diferença entre as coordenadas x e y
delta_y = c2[1] - c1[1]
delta_x = c2[0] - c1[0]

# Calcular o ângulo em radianos
angle_rad = math.atan2(delta_y, delta_x)

# Converter o ângulo de radianos para graus
angle_deg = math.degrees(angle_rad)

print("O ângulo da reta é: ", angle_deg)

plt.imshow(contour_image)
plt.show()



