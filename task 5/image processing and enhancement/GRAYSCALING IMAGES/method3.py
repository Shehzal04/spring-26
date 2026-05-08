import cv2

img_weighted = cv2.imread(r"C:\Users\Lenovo L380 A&I\OneDrive\Desktop\open\GRAYSCALING IMAGES\Screenshot-2741-300x213.png")
rows, cols = img_weighted.shape[:2]

for i in range(rows):
    for j in range(cols):
        gray = 0.2989 * img_weighted[i, j][2] + 0.5870 * img_weighted[i, j][1] + 0.1140 * img_weighted[i, j][0]
        img_weighted[i, j] = [gray, gray, gray]

cv2.imshow('Grayscale Image (Weighted)', img_weighted)
cv2.waitKey(0)
cv2.destroyAllWindows()