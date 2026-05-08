import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread(r'C:\Users\Lenovo L380 A&I\OneDrive\Desktop\semester 4\sir rasikh\open\Morphological Operations & Filtering\eroison\cat.webp', 0)
plt.imshow(img, cmap='gray')
plt.title("Original Image")
plt.axis('off')
plt.show()
kernel = np.ones((5, 5), np.uint8)
img_dilation = cv2.dilate(img, kernel, iterations=1)

plt.imshow(img_dilation, cmap='gray')
plt.title("After Dilation")
plt.axis('off')
plt.show()