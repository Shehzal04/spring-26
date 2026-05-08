import cv2
import matplotlib.pyplot as plt
src = cv2.imread(r'C:\Users\Lenovo L380 A&I\OneDrive\Desktop\semester 4\sir rasikh\open\convert image\image.png')

if src is None:
    print("Image not loaded. Check path.")
else:
    rgb_image = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    plt.imshow(rgb_image)
    plt.title("RGB Image for Matplotlib")
    plt.axis('off')
    plt.show()