import cv2
import os
import numpy as np
import time
from datetime import datetime

def ensure_directory(directory):
    """Ensure a directory exists"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_frame(frame, directory="temp"):
    """Save a frame to a temporary file and return the file path"""
    # Ensure the temp directory exists
    ensure_directory(directory)
    
    # Generate a unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    file_path = os.path.join(directory, f"frame_{timestamp}.jpg")
    
    # Save the frame
    cv2.imwrite(file_path, frame)
    
    return file_path

def cleanup_temp_files(directory="temp", max_age_seconds=300):
    """Clean up temporary files older than max_age_seconds"""
    try:
        # Ensure the temp directory exists
        if not os.path.exists(directory):
            return
        
        current_time = time.time()
        
        # List all files in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # Check if the file is a regular file (not a directory)
            if os.path.isfile(file_path):
                # Get the file's last modification time
                file_mod_time = os.path.getmtime(file_path)
                
                # Delete if older than max_age_seconds
                if current_time - file_mod_time > max_age_seconds:
                    os.remove(file_path)
    except Exception as e:
        print(f"Error cleaning up temp files: {e}")

def calculate_emotion_confidence(confidence_history, emotion_history, current_emotion, current_confidence):
    """Calculate smoothed emotion confidence based on history"""
    # Add current values to history
    emotion_history.append(current_emotion)
    confidence_history.append(current_confidence)
    
    # Keep only the last 5 values
    if len(emotion_history) > 5:
        emotion_history.pop(0)
        confidence_history.pop(0)
    
    # Count occurrences of each emotion in history
    emotion_counts = {}
    for emotion in emotion_history:
        if emotion in emotion_counts:
            emotion_counts[emotion] += 1
        else:
            emotion_counts[emotion] = 1
    
    # Find the most common emotion
    most_common_emotion = max(emotion_counts, key=emotion_counts.get)
    
    # Calculate average confidence for this emotion
    total_confidence = 0
    count = 0
    
    for i, emotion in enumerate(emotion_history):
        if emotion == most_common_emotion:
            total_confidence += confidence_history[i]
            count += 1
    
    avg_confidence = total_confidence / count if count > 0 else 5
    
    return most_common_emotion, avg_confidence