import cv2
import numpy as np
from matplotlib import pyplot as plt

# Image same folder mein rakho
image = cv2.imread(r"C:\Users\Lenovo L380 A&I\OneDrive\Desktop\open\image pyramid\img.webp")

if image is None:
    print(" Image load nahi hui, path ya filename check karo")
else:
    pyramid = [image]

    # Downsampling (3 levels)
    temp_image = image.copy()
    for i in range(3): 
        temp_image = cv2.pyrDown(temp_image)
        pyramid.append(temp_image)

    # Show pyramid using matplotlib
    for i in range(len(pyramid)-1, -1, -1):
        img_rgb = cv2.cvtColor(pyramid[i], cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(8, 5))
        plt.imshow(img_rgb)
        plt.title(f"Pyramid Level {i}")
        plt.axis("off")
        plt.show()
