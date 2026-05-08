import cv2
from matplotlib import pyplot as plt
image_path = r"C:\Users\Lenovo L380 A&I\OneDrive\Desktop\open\original.webp"
image = cv2.imread(image_path)
resized_image = cv2.resize(image, (1900, 800))

median = cv2.medianBlur(resized_image, 11)  
median_rgb = cv2.cvtColor(median, cv2.COLOR_BGR2RGB)  

plt.imshow(median_rgb)
plt.title('Median Blurred Image')
plt.axis('off')
plt.show()