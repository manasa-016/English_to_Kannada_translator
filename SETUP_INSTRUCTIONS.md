# Multilingual Translator - Setup & Installation Guide

A full-stack web application that translates text and speech across multiple languages with a beautiful, responsive UI.

## Features

✨ **Translation Modes:**
- **Text-to-Text**: Translate written text between languages
- **Text-to-Voice**: Convert translated text to speech
- **Voice-to-Text**: Convert speech to text and translate
- **Voice-to-Voice**: Translate spoken input to spoken output in target language

📱 **Supported Languages:**
- English, Kannada, Hindi, Tamil, Telugu
- Spanish, French, German, Chinese, Japanese
- Arabic, Portuguese, Russian, Italian

🎨 **Beautiful UI:**
- Modern gradient design
- Responsive layout (desktop, tablet, mobile)
- Real-time translation with loading indicators
- Translation history
- Keyboard shortcuts (Ctrl+Enter to translate)

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 2GB
- **Microphone**: Required for voice input features
- **Internet**: Required for speech recognition and translation APIs

## Installation Steps

### Step 1: Install Python

**Windows:**
1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"

**macOS:**
```bash
# Using Homebrew
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

### Step 2: Clone or Extract the Project

If you have a zip file:
```bash
# Extract to your desired location
# For this guide, we'll use the default path
```

Navigate to the project folder:
```bash
cd "c:\Users\student\Desktop\Manasa M(078)\English_to_Kannada_translator\translator_app"
```

### Step 3: Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

After activation, your terminal should show `(venv)` at the beginning of the line.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This may take 2-5 minutes depending on your internet speed.

### Step 5: Install FFmpeg (Required for Audio Processing)

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract it to a folder (e.g., C:\ffmpeg)
3. Add FFmpeg to PATH:
   - Open Environment Variables: Press Windows+X, search "Environment Variables"
   - Click "Edit the system environment variables"
   - Click "Environment Variables..." button
   - Under "System variables", click "Path" then "Edit"
   - Click "New" and add: `C:\ffmpeg\bin` (or your FFmpeg path)
   - Click OK and restart your computer

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

### Step 6: Setup Translation API (Optional but Recommended)

By default, the app uses free translation APIs. For better translation quality:

**Option A: Use Google Cloud (Recommended)**
1. Go to https://cloud.google.com/
2. Create a new project
3. Enable Translation API and Text-to-Speech API
4. Create a service account and download JSON credentials
5. Set environment variable:
   ```bash
   # Windows
   set GOOGLE_APPLICATION_CREDENTIALS="path\to\your\credentials.json"
   
   # macOS/Linux
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
   ```

**Option B: Use Free APIs (Fallback)**
The app automatically uses free translation APIs if Google Cloud is not configured.

## Running the Application

### Method 1: Using Command Prompt/Terminal

1. Navigate to the project directory:
```bash
cd "c:\Users\student\Desktop\Manasa M(078)\English_to_Kannada_translator\translator_app"
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Run the Flask app:
```bash
python app.py
```

4. Open your web browser and go to:
```
http://localhost:5000
```

### Method 2: Using Run Script (Windows)

Create a file named `run.bat` in the translator_app folder:

```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
python app.py
pause
```

Then double-click `run.bat` to run the app.

### Method 3: Using Run Script (macOS/Linux)

Create a file named `run.sh` in the translator_app folder:

```bash
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python app.py
```

Then run:
```bash
chmod +x run.sh
./run.sh
```

## Using the Application

### Text-to-Text Translation

1. Select "Text to Text" mode
2. Choose source and target languages
3. Enter text in the left panel
4. Click the "Translate" button
5. View translation in the right panel
6. Use "Copy" to copy text or "Listen" to hear it

### Voice Input Features

**Prerequisites for Voice Features:**
- Allow microphone access when prompted
- Speak clearly and at normal volume
- Use a quiet environment for better recognition

**Voice-to-Text:**
1. Select "Voice to Text" mode
2. Click "Start Recording"
3. Speak clearly into the microphone
4. Click "Stop Recording" when done
5. Click "Translate"
6. Translated text appears in the right panel

**Text-to-Voice:**
1. Select "Text to Voice" mode
2. Enter text in the left panel
3. Click "Translate"
4. Audio will be generated and ready to play

**Voice-to-Voice:**
1. Select "Voice to Voice" mode
2. Record your speech
3. Click "Translate"
4. Listen to the translated speech

### History

- All translations are automatically saved
- Last 20 translations shown in the history section
- Click any history item to load it

### Keyboard Shortcuts

- **Ctrl + Enter**: Translate immediately
- **Swap button**: Exchange source and target languages

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
# Make sure virtual environment is activated
# Windows
venv\Scripts\activate

# Then reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
**Solution 1:** Close other applications using port 5000
**Solution 2:** Change the port in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Changed from 5000 to 5001
```

### Issue: Microphone not detected
**Solutions:**
1. Check Windows Settings > Sound > Input devices
2. Ensure the app has microphone permissions
3. Restart your browser
4. Try a different browser (Chrome works best)

### Issue: Speech recognition not working
**Solutions:**
1. Check internet connection (required for Google Speech Recognition)
2. Speak clearly and loudly
3. Reduce background noise
4. Check that your microphone is working

### Issue: Translation not working
**Solutions:**
1. Check internet connection
2. Verify language codes are correct
3. Try using fallback translation API (automatic if Google Cloud not configured)
4. Check Flask console for error messages

### Issue: Audio playback not working
**Solutions:**
1. Check that speakers/headphones are working
2. Ensure volume is not muted
3. Check browser permissions for audio
4. Try a different browser

## Project Structure

```
translator_app/
├── app.py                 # Flask application & API endpoints
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Beautiful styling
│   └── js/
│       └── app.js        # Frontend logic
└── uploads/              # Temporary audio files (auto-created)
```

## API Endpoints

All endpoints expect JSON requests and return JSON responses.

### GET /
- Returns the main HTML page

### POST /api/translate
**Request:**
```json
{
    "text": "Hello",
    "source_lang": "en",
    "target_lang": "kn"
}
```
**Response:**
```json
{
    "translated_text": "ಹಲೋ",
    "source_lang": "en",
    "target_lang": "kn"
}
```

### POST /api/text-to-speech
**Request:**
```json
{
    "text": "Hello",
    "language": "en"
}
```
**Response:**
```json
{
    "audio": "base64_encoded_audio",
    "format": "mp3"
}
```

### POST /api/speech-to-text
**Request:** (multipart form-data)
- `audio`: WAV audio file
- `language`: language code

**Response:**
```json
{
    "text": "Hello",
    "language": "en"
}
```

### POST /api/voice-to-voice
**Request:** (multipart form-data)
- `audio`: WAV audio file
- `source_lang`: source language code
- `target_lang`: target language code

**Response:**
```json
{
    "audio": "base64_encoded_audio",
    "text": "translated_text",
    "source_text": "original_text",
    "format": "mp3"
}
```

## Performance Tips

1. **Speed up translations**: Use text-to-text instead of voice-to-voice
2. **Better speech recognition**: Speak clearly and avoid background noise
3. **Faster loading**: Clear browser cache occasionally
4. **Save bandwidth**: Use shorter text inputs

## Security Notes

⚠️ **For Production:**
1. Set `debug=False` in `app.py`
2. Add authentication if deploying online
3. Validate all user inputs
4. Use HTTPS instead of HTTP
5. Implement rate limiting
6. Secure API credentials with environment variables

## Frequently Asked Questions

**Q: Why is translation slow?**
A: Network speed affects API response times. Also, voice features require processing time.

**Q: Can I deploy this online?**
A: Yes, use platforms like Heroku, PythonAnywhere, or AWS. You'll need to handle larger file uploads and concurrent users.

**Q: Which translation engine is best?**
A: Google Cloud provides the best quality but requires setup. Free APIs work well for most cases.

**Q: Can I add more languages?**
A: Yes, modify the LANGUAGES dictionary in `app.py` and the language select dropdowns in `index.html`.

**Q: Is my data stored?**
A: Only translation history is stored locally in your browser. Audio files are temporarily stored server-side and automatically deleted.

## Support & Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Google Cloud Translation**: https://cloud.google.com/translate/
- **Web Speech API**: https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API

## License

This project is free to use and modify for educational purposes.

## Troubleshooting Checklist

Before contacting support:
- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] All requirements installed (`pip list` shows Flask, etc.)
- [ ] FFmpeg installed and in PATH
- [ ] Port 5000 not in use
- [ ] Internet connection active
- [ ] No antivirus blocking the app
- [ ] Using latest browser version

## Contact & Issues

If you encounter any issues:
1. Check the troubleshooting section above
2. Check Flask console output for error messages
3. Verify all installation steps were completed
4. Try restarting the application

---

**Version**: 1.0.0
**Last Updated**: January 2026
**Author**: Your Name

Enjoy translating! 🌍
