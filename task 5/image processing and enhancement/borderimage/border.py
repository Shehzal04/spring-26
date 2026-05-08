import cv2

image = cv2.imread(r"C:\\Users\\Lenovo L380 A&I\\OneDrive\\Desktop\\semester 4\\sir rasikh\\open\\borderimage\\logo.png")

border_reflect = cv2.copyMakeBorder(image, 50, 50, 50, 50, cv2.BORDER_REFLECT)
border_reflect_101 = cv2.copyMakeBorder(image, 50, 50, 50, 50, cv2.BORDER_REFLECT_101)
border_replicate = cv2.copyMakeBorder(image, 50, 50, 50, 50, cv2.BORDER_REPLICATE)

cv2.imshow("Border Reflect", border_reflect)
cv2.imshow("Border Reflect 101", border_reflect_101)
cv2.imshow("Border Replicate", border_replicate)

cv2.waitKey(0)
cv2.destroyAllWindows()