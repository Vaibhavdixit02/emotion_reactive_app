import os
import json
import re
import logging
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger("EmotionAPI")

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("🔴 ERROR: No API key found! Make sure GOOGLE_API_KEY is set in your .env file.")
else:
    print("✓ API key loaded from environment")

# Configure the Gemini API
try:
    genai.configure(api_key=api_key)
    print("✓ Gemini API configured")
except Exception as e:
    print(f"🔴 ERROR: Failed to configure Gemini API: {str(e)}")

def detect_emotion(image_path):
    """Detect emotion in facial image using Gemini API"""
    print(f"Starting emotion detection for image: {image_path}")
    
    try:
        # Verify the image exists
        if not os.path.exists(image_path):
            print(f"🔴 ERROR: Image file does not exist: {image_path}")
            return "neutral", 5
            
        # Load the image
        try:
            img = Image.open(image_path)
            print(f"✓ Image loaded successfully: size={img.size}, mode={img.mode}")
        except Exception as e:
            print(f"🔴 ERROR: Failed to load image: {str(e)}")
            return "neutral", 5
        
        # Initialize the model
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            print("✓ Gemini model initialized")
        except Exception as e:
            print(f"🔴 ERROR: Failed to initialize Gemini model: {str(e)}")
            return "neutral", 5
        
        # Create the prompt
        prompt = """
        Analyze this facial image and determine the primary emotion displayed.
        Return ONLY ONE of: 'happy', 'sad', 'angry', 'surprised', 'neutral', 'fearful', or 'disgusted'.
        Format your response as JSON with fields 'emotion' and 'confidence' (from 1-10).
        Example response: {"emotion": "happy", "confidence": 8}
        """
        
        # Get response from Gemini
        print("Sending request to Gemini API...")
        response = model.generate_content([prompt, img])
        
        # Log the raw response
        response_text = response.text
        print(f"Received response from Gemini API: {response_text}")
        
        # Parse the response
        try:
            # Try to find a JSON structure in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                print(f"Found JSON in response: {json_str}")
                
                data = json.loads(json_str)
                emotion = data.get('emotion', 'neutral')
                confidence = data.get('confidence', 5)
                
                print(f"✓ Successfully parsed JSON: emotion={emotion}, confidence={confidence}")
                return emotion, confidence
            else:
                print("⚠️ No JSON found in the response")
        except Exception as e:
            print(f"🔴 ERROR: Error parsing JSON response: {str(e)}")
        
        # Fallback - try to extract emotion directly from text
        print("Trying fallback: direct text extraction")
        for emotion in ['happy', 'sad', 'angry', 'surprised', 'neutral', 'fearful', 'disgusted']:
            if emotion in response_text.lower():
                print(f"✓ Found emotion in text: {emotion}")
                return emotion, 5
        
        print("⚠️ Could not extract emotion from text, using default")
    
    except Exception as e:
        print(f"🔴 ERROR: Unexpected error in emotion detection: {str(e)}")
    
    # Default fallback
    print("Returning default emotion: neutral")
    return "neutral", 5