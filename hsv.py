# This program detects the red color in an image using OpenCV and HSV color space.
'''
Load image	Read the input image from disk.
2️⃣ Convert to HSV	Prepare image for color detection.
3️⃣ Define color range	Specify which HSV values represent “red.”
4️⃣ Create mask	Highlight only the red areas (white = red).
5️⃣ Apply mask	Show only red regions in the final image.
6️⃣ Display results	View original, mask, and detected color side by side.
'''
'''
Imports the OpenCV library (short for Open Source Computer Vision).
This library allows Python to handle image processing, object detection, video streaming, etc.
The module name is cv2.
'''
import cv2
'''
Imports NumPy, a powerful library for handling numerical data and arrays.
OpenCV represents images as NumPy arrays, so NumPy is used for defining color 
ranges and pixel-level operations.
'''
import numpy as np
'''
Reads an image from your computer (in this case, 'zuh1.jpg').
cv2.imread() loads the image into a NumPy array called frame.
Each pixel in the image now has BGR (Blue, Green, Red) values — 
OpenCV uses BGR instead of RGB by default.
If the image is not found, frame will be None. 
Always check that 'zuh1.jpg' is in the same folder as your script.
'''
frame = cv2.imread('zuh1.jpg')
'''
Converts the image from BGR color space to HSV (Hue, Saturation, Value).
This step is crucial because HSV makes color detection more accurate and less sensitive to lighting changes.
What happens here:
OpenCV goes through every pixel and transforms its BGR values into corresponding HSV values.
This gives us a version of the image where each pixel is represented by:
H (Hue): Type of color (0–180)
S (Saturation): Intensity (0–255)
V (Value): Brightness (0–255)
'''
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Red color range in HSV
# Defines the lower limit of the red color in the HSV space.
# Any pixel with Hue ≥ 0, Saturation ≥ 120, and Value ≥ 70 can be considered “red-ish”.
lower_red = np.array([0, 120, 70])
'''
Defines the upper limit of the red color.
Together with the lower limit, this forms a range of HSV values that represent red shades.
Think of it like telling OpenCV:
“Everything between this low range and this high range in HSV should be considered red.”'''
upper_red = np.array([10, 255, 255])
'''
Creates a binary mask from the HSV image.
Each pixel in hsv is checked:
If it falls within the red range → that pixel becomes white (255) in the mask.
Otherwise → that pixel becomes black (0).
This produces a black-and-white image (mask) where white = detected color region.
'''
mask = cv2.inRange(hsv, lower_red, upper_red)
'''
This applies the mask to the original image.
cv2.bitwise_and() keeps only the pixels where the mask is white (255).
All other pixels are turned black (0).
The resulting image (result) shows only the red areas of the original photo — everything else is hidden.
'''
result = cv2.bitwise_and(frame, frame, mask=mask)

# Displays the original image in a window named “Original”.
cv2.imshow('Original', frame)
# Displays the mask image (black and white).
# The white regions correspond to the detected red color in the image.
cv2.imshow('Mask', mask)
# Displays the final result, where only the red parts of the image are visible.
cv2.imshow('Detected Color', result)
'''
Waits indefinitely for a key press.
The image windows remain open until you press any key.
If you use cv2.waitKey(1), the window refreshes continuously —
used for video or real-time detection.
'''
cv2.waitKey(0)

'''Closes all OpenCV windows after a key is pressed.
It’s good practice to add:
'''
cv2.destroyAllWindows()

# Visual Flow :
# 📷 Original Image → 🎨 Convert to HSV → 🧱 Create Mask → 🎯 Extract Red Areas

'''
............................Why Masking Is Important.............................
It helps the robot “see” only the color of interest (e.g., red ball).
The rest of the scene (background, floor, lighting) is ignored.
The mask can now be processed to find the object’s shape, position, and size.
'''

'''
Color masking is like giving the robot ‘blinders’ — it only sees the specific color we want,
which makes detection simpler and faster. Once the color mask is ready, we can use contours to 
identify the shape and position of the object.”
'''
