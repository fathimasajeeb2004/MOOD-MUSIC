# capture.py
import cv2
import os

def capture_image(filename="captured.jpg"):
    """Capture image from webcam and save with given filename"""
    cam = cv2.VideoCapture(0)
    
    if not cam.isOpened():
        raise Exception("Could not open webcam")
    
    # Set camera properties for better quality
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    st_frame = None  # For Streamlit display
    
    # For Streamlit, we can't use cv2.imshow, so we'll capture once
    ret, frame = cam.read()
    
    if ret:
        # Save the image
        cv2.imwrite(filename, frame)
        cam.release()
        return True
    else:
        cam.release()
        raise Exception("Failed to capture image")