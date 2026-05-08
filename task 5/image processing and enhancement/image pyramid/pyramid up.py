import cv2
from matplotlib import pyplot as plt

# Image same folder mein rakho
image = cv2.imread(r"C:\Users\Lenovo L380 A&I\OneDrive\Desktop\open\image pyramid\img.webp")

if image is None:
    print(" Image load nahi hui, path ya filename check karo")
else:
    # Upsampling
    upsampled_image = cv2.pyrUp(image)

    # Convert BGR -> RGB for correct colors in matplotlib
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    upsampled_rgb = cv2.cvtColor(upsampled_image, cv2.COLOR_BGR2RGB)

    # Display using matplotlib
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(image_rgb)
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(upsampled_rgb)
    plt.title("Upsampled Image")
    plt.axis("off")

    plt.show()
