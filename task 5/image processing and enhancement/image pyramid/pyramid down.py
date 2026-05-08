import cv2
import numpy as np
from matplotlib import pyplot as plt

# image same folder mein rakho
image = cv2.imread(r"C:\Users\Lenovo L380 A&I\OneDrive\Desktop\open\image pyramid\img.webp")

if image is None:
    print(" Image load nahi hui, path ya naam check karo")
else:
    downsampled_image = cv2.pyrDown(image)

    # BGR → RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    down_rgb = cv2.cvtColor(downsampled_image, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.imshow(image_rgb)
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(down_rgb)
    plt.title("Pyramid Downsampled Image")
    plt.axis("off")

    plt.show()
