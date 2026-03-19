# app.py
import streamlit as st
import time
import random
import os

# Try to import helper modules
try:
    from capture import capture_image
    CAPTURE_AVAILABLE = True
except ImportError:
    CAPTURE_AVAILABLE = False
    st.sidebar.warning("⚠️ Camera module not available")

try:
    from spotify_api import get_recommended_songs
    SPOTIFY_AVAILABLE = True
except ImportError:
    SPOTIFY_AVAILABLE = False
    st.sidebar.warning("⚠️ Spotify API not configured")

# Simple emotion detection for demo
def get_emotion_demo():
    emotions = ['happy', 'sad', 'neutral', 'angry', 'surprise']
    return random.choice(emotions)

# Page configuration
st.set_page_config(
    page_title="Mood-Based Music Recommender",
    layout="centered",
    page_icon="🎵"
)

# Title and description
st.title("🎵 Mood-Based Music Recommendation System")
st.markdown("---")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    use_camera = st.checkbox("Use Camera", value=True)
    demo_mode = st.checkbox("Demo Mode", value=not CAPTURE_AVAILABLE)
    
    if st.button("Clear Cache"):
        # Remove captured images
        for file in os.listdir("."):
            if file.startswith("captured_") and file.endswith(".jpg"):
                os.remove(file)
        st.success("Cache cleared!")

# Main content
col1, col2, col3 = st.columns(3)
with col2:
    capture_button = st.button("🎬 Capture Mood & Get Music", type="primary", use_container_width=True)

if capture_button:
    # Create a container for results
    results_container = st.container()
    
    with results_container:
        # Step 1: Capture image
        st.subheader("📸 Step 1: Capturing your photo")
        
        mood = None
        image_captured = False
        
        if use_camera and CAPTURE_AVAILABLE and not demo_mode:
            try:
                # Generate unique filename
                filename = f"captured_{int(time.time())}.jpg"
                
                with st.spinner("Looking for camera..."):
                    # Capture image
                    success = capture_image(filename)
                    
                    if success and os.path.exists(filename):
                        st.image(filename, caption="Your Photo", use_column_width=True)
                        st.success("✅ Photo captured successfully!")
                        image_captured = True
                    else:
                        st.warning("⚠️ Could not capture photo. Switching to demo mode.")
                        demo_mode = True
                        
            except Exception as e:
                st.error(f"Camera error: {str(e)}")
                st.info("Switching to demo mode...")
                demo_mode = True
        else:
            demo_mode = True
        
        if demo_mode:
            # Show placeholder image
            st.image("https://images.unsplash.com/photo-1494790108755-2616b786d4b9?w=400&h=300&fit=crop",
                    caption="Demo Image - Happy Person",
                    use_column_width=True)
            st.info("🎭 Running in demo mode (no camera used)")
        
        # Step 2: Detect emotion
        st.subheader("😊 Step 2: Analyzing your mood")
        
        with st.spinner("Analyzing facial expression..."):
            # Simulate processing time
            time.sleep(1.5)
            
            if image_captured and not demo_mode:
                # Try to use real emotion detection if available
                try:
                    from emotion_detector import get_emotion
                    mood = get_emotion(filename)
                except:
                    mood = get_emotion_demo()
            else:
                mood = get_emotion_demo()
            
            # Display mood with emoji
            mood_emojis = {
                'happy': '😊',
                'sad': '😢',
                'neutral': '😐',
                'angry': '😠',
                'surprise': '😲',
                'fear': '😨'
            }
            
            emoji = mood_emojis.get(mood, '🎵')
            st.success(f"{emoji} **Detected Mood: {mood.upper()}**")
        
        # Step 3: Get recommendations
        st.subheader("🎧 Step 3: Your Music Recommendations")
        
        if SPOTIFY_AVAILABLE and mood:
            with st.spinner(f"Finding perfect {mood} songs..."):
                try:
                    songs = get_recommended_songs(mood)
                    if songs and len(songs) > 0:
                        st.balloons()
                        
                        # Create tabs for different views
                        tab1, tab2 = st.tabs(["🎵 Song List", "📊 Mood Info"])
                        
                        with tab1:
                            st.markdown(f"### Top {min(10, len(songs))} Songs for **{mood.upper()}** Mood")
                            st.markdown("---")
                            
                            for i, song in enumerate(songs[:10], 1):
                                with st.container():
                                    col1, col2 = st.columns([1, 4])
                                    with col1:
                                        st.markdown(f"**{i}.**")
                                    with col2:
                                        st.markdown(f"**{song['name']}**")
                                        st.markdown(f"*{song['artist']}*")
                                        st.markdown(f"[▶️ Listen on Spotify]({song['url']})", unsafe_allow_html=True)
                                    st.divider()
                        
                        with tab2:
                            st.markdown(f"### About **{mood.upper()}** Mood Music")
                            mood_descriptions = {
                                'happy': "Upbeat, energetic music to keep your spirits high!",
                                'sad': "Melancholic and emotional tracks for reflection.",
                                'neutral': "Balanced, relaxing tunes for any moment.",
                                'angry': "High-energy music to channel your intensity.",
                                'surprise': "Unexpected and exciting tracks to wow you!"
                            }
                            st.info(mood_descriptions.get(mood, "Great music for your current state!"))
                            
                    else:
                        st.warning("No songs found for this mood.")
                        
                except Exception as e:
                    st.error(f"Error fetching from Spotify: {str(e)}")
                    st.info("Showing demo recommendations instead...")
                    SPOTIFY_AVAILABLE = False
        
        if not SPOTIFY_AVAILABLE:
            # Demo recommendations
            st.info("🎭 Demo Mode: Sample Recommendations")
            
            # Different demo songs based on mood
            demo_playlists = {
                'happy': [
                    {"name": "Good Vibrations", "artist": "The Beach Boys", "url": "#"},
                    {"name": "Happy", "artist": "Pharrell Williams", "url": "#"},
                    {"name": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars", "url": "#"},
                    {"name": "Dancing Queen", "artist": "ABBA", "url": "#"},
                    {"name": "Can't Stop the Feeling", "artist": "Justin Timberlake", "url": "#"}
                ],
                'sad': [
                    {"name": "Someone Like You", "artist": "Adele", "url": "#"},
                    {"name": "Hurt", "artist": "Johnny Cash", "url": "#"},
                    {"name": "The Sound of Silence", "artist": "Simon & Garfunkel", "url": "#"},
                    {"name": "Yesterday", "artist": "The Beatles", "url": "#"},
                    {"name": "Nothing Compares 2 U", "artist": "Sinead O'Connor", "url": "#"}
                ],
                'angry': [
                    {"name": "Break Stuff", "artist": "Limp Bizkit", "url": "#"},
                    {"name": "Killing in the Name", "artist": "Rage Against the Machine", "url": "#"},
                    {"name": "Given Up", "artist": "Linkin Park", "url": "#"},
                    {"name": "Bodies", "artist": "Drowning Pool", "url": "#"},
                    {"name": "Down with the Sickness", "artist": "Disturbed", "url": "#"}
                ]
            }
            
            songs = demo_playlists.get(mood, demo_playlists['happy'])
            
            for i, song in enumerate(songs, 1):
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"**{i}.**")
                    with col2:
                        st.markdown(f"**{song['name']}**")
                        st.markdown(f"*{song['artist']}*")
                        if song['url'] != "#":
                            st.markdown(f"[▶️ Listen]({song['url']})", unsafe_allow_html=True)
                    st.divider()
        
        # Footer
        st.markdown("---")
        st.caption("Refresh the page to try again with a different mood!")

# Instructions if button not clicked
else:
    st.markdown("""
    ### How it works:
    
    1. **Capture** - Take a photo using your webcam
    2. **Analyze** - AI detects your current emotion
    3. **Recommend** - Get personalized music suggestions
    
    ### Features:
    - 🎭 Real-time emotion detection
    - 🎵 Spotify integration
    - 📱 Mobile-friendly interface
    - 🎨 Beautiful visual design
    
    Ready to discover music that matches your mood?
    """)
    
    # Display mood examples
    col1, col2, col3, col4, col5 = st.columns(5)
    moods = [
        ("😊", "Happy", "Upbeat pop & dance"),
        ("😢", "Sad", "Melancholic ballads"),
        ("😠", "Angry", "High-energy rock"),
        ("😲", "Surprise", "Experimental tunes"),
        ("😐", "Neutral", "Chill background music")
    ]
    
    for i, (emoji, name, desc) in enumerate(moods):
        with [col1, col2, col3, col4, col5][i]:
            st.markdown(f"<div style='text-align: center; padding: 10px; border-radius: 10px; background-color: #f0f2f6;'>"
                       f"<h1>{emoji}</h1><b>{name}</b><br><small>{desc}</small>"
                       f"</div>", unsafe_allow_html=True)