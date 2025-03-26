import os
import json
import time
import cv2
import base64
import numpy as np
from PIL import Image
from io import BytesIO
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from gemini_emotion import detect_emotion
from utils import save_frame, calculate_emotion_confidence, ensure_directory

# Load environment variables
load_dotenv()

# Create necessary directories
ensure_directory("temp")
ensure_directory("static")

# Initialize Flask app
app = Flask(__name__)

# Store emotion history
emotion_history = ["neutral"]
confidence_history = [5]
current_emotion = "neutral"
current_confidence = 5

# Color schemes for different emotions
emotion_colors = {
    "happy": {
        "background": "#FFF9E0",
        "text": "#FF8C00",
        "border": "#FFDB58"
    },
    "sad": {
        "background": "#F0F8FF",
        "text": "#4169E1",
        "border": "#A7C7E7"
    },
    "angry": {
        "background": "#FFF0F0",
        "text": "#B22222",
        "border": "#FFCCCB"
    },
    "surprised": {
        "background": "#F0FFFF",
        "text": "#9932CC",
        "border": "#E0FFFF"
    },
    "neutral": {
        "background": "#FFFFFF",
        "text": "#2F4F4F",
        "border": "#E0E0E0"
    },
    "fearful": {
        "background": "#F8F6FF",
        "text": "#4B0082",
        "border": "#E6E6FA"
    },
    "disgusted": {
        "background": "#F0FFF0",
        "text": "#228B22",
        "border": "#E0FFC2"
    }
}

# Content recommendations for each emotion
emotion_content = {
    "happy": {
        "message": "You seem happy today! Here's some content to match your bright mood...",
        "recommendations": [
            "Share your joy with friends",
            "Take on a creative project",
            "Enjoy the bright atmosphere"
        ]
    },
    "sad": {
        "message": "Feeling blue? Here are some things that might cheer you up...",
        "recommendations": [
            "Practice self-care activities",
            "Reach out to a friend",
            "Listen to uplifting music"
        ]
    },
    "angry": {
        "message": "The subtle red tones help create a calming effect. Take a deep breath...",
        "recommendations": [
            "Take deep breaths",
            "Go for a short walk",
            "Try a quick meditation"
        ]
    },
    "surprised": {
        "message": "Surprise! Here's something interesting for you...",
        "recommendations": [
            "Interesting facts",
            "New discoveries",
            "Unexpected connections"
        ]
    },
    "neutral": {
        "message": "Welcome to the emotion-reactive interface!",
        "recommendations": [
            "Explore different emotions",
            "Watch how the interface changes",
            "Experience personalized content"
        ]
    },
    "fearful": {
        "message": "Everything's okay! Here's a calming environment for you...",
        "recommendations": [
            "Positive affirmations",
            "Calming visualizations",
            "Supportive resources"
        ]
    },
    "disgusted": {
        "message": "Let's refresh your perspective with something pleasant...",
        "recommendations": [
            "Beautiful nature scenes",
            "Pleasant visual experiences",
            "Fresh perspectives"
        ]
    }
}

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', 
                          emotion=current_emotion,
                          colors=emotion_colors[current_emotion],
                          content=emotion_content[current_emotion],
                          confidence=current_confidence)

@app.route('/analyze_emotion', methods=['POST'])
def analyze_emotion():
    """Analyze emotion from webcam image"""
    global current_emotion, current_confidence
    
    try:
        # Get image data from request
        image_data = request.json.get('image')
        
        if not image_data:
            return jsonify({'error': 'No image data received'}), 400
        
        # Remove the data:image/jpeg;base64, prefix
        image_data = image_data.split(',')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        
        # Convert to numpy array for OpenCV
        image_np = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        
        # Save frame temporarily
        temp_file_path = save_frame(frame)
        
        # Detect emotion
        print("Analyzing emotion...")
        emotion, confidence = detect_emotion(temp_file_path)
        print(f"Detected: {emotion}, confidence: {confidence}")
        
        # Smooth emotion detection
        smooth_emotion, smooth_confidence = calculate_emotion_confidence(
            confidence_history, 
            emotion_history, 
            emotion, 
            confidence
        )
        
        # Update current emotion and confidence
        current_emotion = smooth_emotion
        current_confidence = smooth_confidence
        
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        # Return the result
        return jsonify({
            'emotion': current_emotion,
            'confidence': current_confidence,
            'colors': emotion_colors[current_emotion],
            'content': emotion_content[current_emotion]
        })
        
    except Exception as e:
        print(f"Error in emotion analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)