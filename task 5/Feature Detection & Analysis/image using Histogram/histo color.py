import cv2, matplotlib.pyplot as plt
img = cv2.imread(r"C:\Users\Lenovo L380 A&I\OneDrive\Desktop\semester 4\sir rasikh\open\Feature Detection & Analysis\image using Histogram\OIP.webp")

# colors for channels
colors = ('b', 'g', 'r')

for i, col in enumerate(colors):
    hist = cv2.calcHist([img], [i], None, [256], [0, 256])
    plt.plot(hist, color=col)
    plt.xlim([0, 256])

plt.title("RGB Color Histogram")
plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")
plt.show()