# Emotion-Reactive Web Interface

A web application that captures webcam input, analyzes facial expressions using Google's Gemini API, and dynamically adjusts the interface colors based on detected emotions.

## Features

- **Real-time emotion detection** using Google Gemini 1.5 flash model
- **Dynamic UI styling** based on detected emotions with color themes
- **Emotion-specific content** recommendations and suggestions
- **In-browser webcam integration** with manual and auto-capture options
- **Smooth transitions** between emotional states
- **Debug console** for troubleshooting

## Supported Emotions

The application detects and responds to the following emotions:
- Happy
- Sad
- Angry
- Surprised
- Neutral
- Fearful
- Disgusted

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Google API key for Gemini Pro Vision

### Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd emotion-reactive-app
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your Google API key:
   - Get a Google API key for Gemini from the [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Add your API key to the `.env` file:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

## Usage

1. Run the Flask application:
   ```
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Click the "Start Camera" button to begin capturing webcam input

4. Click "Analyze Emotion" or toggle "Auto-Capture" to detect emotions

5. Express different emotions to see the interface change in real-time

## How It Works

1. The application uses your browser's webcam API to capture video
2. When you click "Analyze Emotion" or enable auto-capture, it:
   - Captures a frame from the webcam
   - Sends the image to the server as a base64-encoded JPEG
   - Server processes the image with Google Gemini API to detect emotions
   - Results are sent back to update the UI colors and content

## Project Structure

```
emotion_reactive_app/
├── app.py                 # Main Flask application
├── gemini_emotion.py      # Gemini API integration
├── utils.py               # Helper functions
├── .env                   # API keys (gitignored)
├── README.md              # Documentation
├── templates/             # HTML templates
│   └── index.html         # Main application page
└── static/                # Static assets folder
```

## Key Features

- **Browser-based webcam capture**: Uses the HTML5 Webcam API for reliable camera access
- **Manual and automatic capture modes**: Analyze on-demand or set to auto-capture every few seconds
- **Real-time UI updates**: Changes colors, content, and recommendations based on detected emotions
- **Built-in debugging**: Visual debug console shows what's happening at each step
- **Smooth visual transitions**: Gradual color changes between emotional states

## Limitations

- Emotion detection requires good lighting conditions
- The application requires webcam access and an internet connection
- The Gemini API has rate limits and usage costs

## License

[MIT License](LICENSE)

## Acknowledgements

- Google Gemini API for emotion analysis
- Flask web framework
- HTML5 Webcam API for browser camera integration