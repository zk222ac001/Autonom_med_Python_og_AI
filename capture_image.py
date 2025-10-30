''' 
✅ Preview the camera feed using OpenCV (cv2)
🕒 Capture and save the image with a timestamped filename
💾 Optionally store it in a custom folder (e.g. /home/pi/Desktop/captured_images/)
'''
# Step no 1: libraries setup
from picamera2 import Picamera2, Preview
import cv2
import time
import os

# step no 2: Settings -------------------------------- 
SAVE_DIR = "/home/pi/Desktop/captured_images"  # folder to save images
os.makedirs(SAVE_DIR, exist_ok=True)  # create folder if it doesn’t exist

# step no 3 : Initialize camera ------------------------
picam2 = Picamera2()

# step no 4: Configure the camera stream (BGR for OpenCV) --------------------
config = picam2.create_preview_configuration(main={"format": "BGR888"})
picam2.configure(config)
picam2.start()

print("Camera started. Press 'c' to capture an image, 'q' to quit.")

while True:
    frame = picam2.capture_array()  # get frame
    cv2.imshow("Live Preview (Press 'c' to capture, 'q' to quit)", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        # Generate timestamped filename
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(SAVE_DIR, f"capture_{timestamp}.jpg")

        # Save the frame
        cv2.imwrite(filename, frame)
        print(f"✅ Image saved as: {filename}")

    elif key == ord('q'):
        print("Exiting...")
        break

# step no 5: Cleanup ---
cv2.destroyAllWindows()
picam2.stop()
