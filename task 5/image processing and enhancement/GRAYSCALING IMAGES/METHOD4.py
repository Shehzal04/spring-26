import cv2

img = cv2.imread(r"C:\Users\Lenovo L380 A&I\OneDrive\Desktop\open\GRAYSCALING IMAGES\Screenshot-2741-300x213.png")
rows, cols = img.shape[:2]

for i in range(rows):
    for j in range(cols):
        gray = (img[i, j, 0] + img[i, j, 1] + img[i, j, 2]) / 3
        img[i, j] = [gray, gray, gray]

cv2.imshow('Grayscale Image (Average)', img)
cv2.waitKey(0)
cv2.destroyAllWindows()