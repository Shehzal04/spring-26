import cv2

src = cv2.imread(r'C:\Users\Lenovo L380 A&I\OneDrive\Desktop\semester 4\sir rasikh\open\convert image\image.png')

if src is None:
    print("Image not loaded. Check path.")
else:
    gray_image = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Gray", gray_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()