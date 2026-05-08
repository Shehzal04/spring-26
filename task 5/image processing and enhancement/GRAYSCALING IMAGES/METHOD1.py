import cv2

image = cv2.imread(r"C:\Users\Lenovo L380 A&I\OneDrive\Desktop\open\GRAYSCALING IMAGES\Screenshot-2741-300x213.png")

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow('Grayscale', gray_image)
cv2.waitKey(0)  
cv2.destroyAllWindows()