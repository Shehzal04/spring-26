import cv2
from matplotlib import pyplot as plt
image_path = r"C:\Users\Lenovo L380 A&I\OneDrive\Desktop\open\original.webp"
image = cv2.imread(image_path)
resized_image = cv2.resize(image, (1900, 800))

bilateral = cv2.bilateralFilter(resized_image, 15, 150, 150)  
bilateral_rgb = cv2.cvtColor(bilateral, cv2.COLOR_BGR2RGB)  

plt.imshow(bilateral_rgb)
plt.title('Bilateral Blurred Image')
plt.axis('off')
plt.show()