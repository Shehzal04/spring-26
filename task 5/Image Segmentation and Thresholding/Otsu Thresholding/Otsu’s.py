import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread(r'C:\Users\Lenovo L380 A&I\OneDrive\Desktop\semester 4\sir rasikh\open\Image Segmentation and Thresholding\Otsu Thresholding\car.jpg')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
def show_image(img, title):
    plt.imshow(img, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()
show_image(gray_image, "Original Grayscale Image")

ret, otsu_thresh = cv2.threshold(
    gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print("Calculated Otsu threshold value:", ret)
show_image(otsu_thresh, "Otsu’s Thresholding")