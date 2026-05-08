import cv2

img = cv2.imread(r"C:\Users\Lenovo L380 A&I\OneDrive\Desktop\open\GRAYSCALING IMAGES\Screenshot-2741-300x213.png", 0)

cv2.imshow('Grayscale Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()