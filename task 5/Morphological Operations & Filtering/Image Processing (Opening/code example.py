import cv2  
import numpy as np  

# Start capturing from webcam
screenRead = cv2.VideoCapture(0)

while True:
    # Capture a single frame from the webcam
    _, image = screenRead.read()
    
    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define blue color range
    blue1 = np.array([110, 50, 50])
    blue2 = np.array([130, 255, 255])
    
    # Create binary mask for blue color
    mask = cv2.inRange(hsv, blue1, blue2)

    # Define 5x5 structuring element (kernel)
    kernel = np.ones((5, 5), np.uint8)
    
    # Apply Opening to remove small white noise
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Show both original mask and cleaned version
    cv2.imshow('Original Blue Mask', mask)
    cv2.imshow('After Opening (Noise Removed)', opening)
    
    # Press 'a' key to stop
    if cv2.waitKey(1) & 0xFF == ord('a'):
        break

# Clean up
cv2.destroyAllWindows()
screenRead.release()