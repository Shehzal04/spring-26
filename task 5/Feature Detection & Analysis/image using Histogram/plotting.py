import cv2
from matplotlib import pyplot as plt
img = cv2.imread(r'C:\Users\Lenovo L380 A&I\OneDrive\Desktop\semester 4\sir rasikh\open\Feature Detection & Analysis\image using Histogram\OIP.webp',0)
histr = cv2.calcHist([img],[0],None,[256],[0,256])
plt.plot(histr)
plt.show()