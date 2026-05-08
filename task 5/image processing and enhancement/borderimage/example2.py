import cv2

image = cv2.imread(r"C:\Users\Lenovo L380 A&I\OneDrive\Desktop\semester 4\sir rasikh\open\borderimage\logo.png")
bordered_image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0, 0, 255))

cv2.imshow("Red Border Image", bordered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()