import cv2

from simple.code import show_image
import numpy as np
import matplotlib.pyplot as plt
image = cv2.imread(r'C:\Users\Lenovo L380 A&I\OneDrive\Desktop\semester 4\sir rasikh\open\simple\car.jpg')
if image is None:
    raise FileNotFoundError("Image not loaded. Check the path!")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh_tozero_inv = cv2.threshold(
    gray_image, 120, 255, cv2.THRESH_TOZERO_INV)
show_image(thresh_tozero_inv, 'Set to 0 Inverted')
