
import cv2
import matplotlib.pyplot as plt

image = cv2.imread(r'C:\Users\Lenovo L380 A&I\OneDrive\Desktop\semester 4\sir rasikh\open\Image Segmentation and Thresholding\adaptive\car (1).jpg')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def show_image(img, title):
    plt.imshow(img, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

show_image(gray_image, "Original Grayscale Image")

thresh_gauss = cv2.adaptiveThreshold(
    gray_image, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    199, 5
)
show_image(thresh_gauss, "Adaptive Gaussian Thresholding")