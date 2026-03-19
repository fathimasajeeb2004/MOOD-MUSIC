# emotion_detector.py - Lightweight version without DeepFace
import random

def get_emotion(img_path=None):
    """
    Simulated emotion detection for demo purposes
    In a real app, replace with actual ML model
    """
    emotions = ['happy', 'sad', 'neutral', 'angry', 'surprise', 'fear']
    
    # For demo, return random emotion
    # You can replace this with a real model later
    return random.choice(emotions)

# Alternative: Use fer library (lighter than DeepFace)
# Uncomment below if you want to use fer instead

# from fer import FER
# import cv2
# 
# detector = FER()
# 
# def get_emotion(img_path="captured.jpg"):
#     try:
#         img = cv2.imread(img_path)
#         if img is None:
#             return "neutral"
#         
#         result = detector.top_emotion(img)
#         if result[0] is not None:
#             return result[0]
#         else:
#             return "neutral"
#     except:
#         return "neutral"