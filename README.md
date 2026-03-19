The Mood-Based Music Recommendation System is an intelligent web application that detects a user's emotion through facial expression analysis and recommends songs based on the detected mood. 
The system captures an image using a webcam, analyzes the emotion using a deep learning-based facial recognition model, and retrieves suitable music recommendations through the Spotify API. 
The application is built using Python and Streamlit, which provides an interactive interface for users to easily access the system.
This project demonstrates the integration of computer vision, machine learning, and API-based music recommendation in a single application.

System Workflow

The system follows a step-by-step pipeline:
The user opens the application through Streamlit.
The user clicks the button to capture their mood.
The system captures an image using the webcam.
The captured image is analyzed to detect the user's emotion.
The detected emotion is sent to the recommendation module.
Songs related to the detected mood are fetched from Spotify.
The recommended songs are displayed on the interface.
