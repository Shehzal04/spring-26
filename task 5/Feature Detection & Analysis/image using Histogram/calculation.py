import cv2, matplotlib.pyplot as plt
import cv2


img = cv2.imread(r'C:\Users\Lenovo L380 A&I\OneDrive\Desktop\semester 4\sir rasikh\open\Feature Detection & Analysis\image using Histogram\OIP.webp', 0)
histg = cv2.calcHist([img], [0], None, [256], [0, 256])

# Plot histogram
plt.plot(histg)
plt.title("Histogram using OpenCV calcHist()")
plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")
plt.show()