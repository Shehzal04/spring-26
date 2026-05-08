import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread(r'C:\Users\Lenovo L380 A&I\OneDrive\Desktop\semester 4\sir rasikh\open\simple\car.jpg')

if image is None:
    raise FileNotFoundError("Image not loaded. Check the path!")

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def show_image(img, title):
    plt.imshow(img, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()
    
show_image(gray_image, 'Original Grayscale Image')
_, thresh_binary = cv2.threshold(gray_image, 120, 255, cv2.THRESH_BINARY)
show_image(thresh_binary, 'Binary Threshold ')