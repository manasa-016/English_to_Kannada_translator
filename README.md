# 🌍 Multilingual Translator - Full Stack Web Application

A feature-rich, beautifully designed web application that translates text and speech across 14 different languages with support for voice-to-voice, voice-to-text, text-to-voice, and text-to-text translation modes.

## ✨ Quick Start

### Windows Users (Easiest)
1. Navigate to the `translator_app` folder
2. Double-click `run.bat`
3. Open browser to `http://localhost:5000`

### macOS/Linux Users
```bash
cd translator_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app_simple.py
# Open http://localhost:5000
```

## 🎯 Key Features

✅ **4 Translation Modes**
- Text-to-Text: Translate written text
- Text-to-Voice: Convert text to speech
- Voice-to-Text: Transcribe and translate speech
- Voice-to-Voice: Real-time language conversion!

✅ **14 Languages Supported**
English, Kannada, Hindi, Tamil, Telugu, Spanish, French, German, Chinese, Japanese, Arabic, Portuguese, Russian, Italian

✅ **Beautiful, Responsive UI**
- Modern gradient design with smooth animations
- Works on desktop, tablet, and mobile
- Translation history (20 recent translations)
- Real-time processing with loading indicators
- Keyboard shortcuts (Ctrl+Enter to translate)

✅ **Zero Setup Hassle**
- Uses free APIs (no API keys needed)
- One-click installation for Windows
- Works out of the box

## 📁 Project Structure

```
translator_app/
├── app.py                 # Full Flask app
├── app_simple.py          # Flask app with free APIs (RECOMMENDED)
├── requirements.txt       # Python dependencies
├── run.bat               # Windows quick-start
├── templates/index.html  # Beautiful responsive UI
└── static/
    ├── css/style.css     # Modern styling
    └── js/app.js         # Frontend logic
```

## 📖 Full Documentation

See **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** for detailed:
- Step-by-step installation guide
- Complete troubleshooting
- API reference
- Performance optimization
- Production deployment

## 🔧 System Requirements

- Python 3.8 or higher
- Internet connection (required)
- Microphone (for voice features)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 💡 Quick Usage Examples

### Translate Text
1. Select "Text to Text"
2. Choose source and target languages
3. Enter text
4. Click Translate button
5. View result on the right

### Voice-to-Voice Translation
1. Select "Voice to Voice"
2. Click "Start Recording"
3. Speak clearly
4. Click "Stop Recording"
5. Click Translate
6. Hear your speech translated!

### Listen to Translation
1. After translating text
2. Click "Listen" button
3. Hear the pronunciation

## ⚙️ Main API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /` | Main interface |
| `POST /api/translate` | Text translation |
| `POST /api/text-to-speech` | Text to speech |
| `POST /api/speech-to-text` | Speech to text |
| `POST /api/voice-to-voice` | Voice translation |

## 🛠️ Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Python not found | Download from https://python.org |
| Port 5000 in use | Change port in app.py |
| Microphone not working | Check system permissions |
| Translation fails | Check internet connection |

See SETUP_INSTRUCTIONS.md for complete help.

## 🎨 Technology Stack

- **Backend**: Python 3.8+, Flask 2.3+
- **Frontend**: HTML5, CSS3, JavaScript
- **APIs**: MyMemory (translation), Google (speech & TTS)
- **Storage**: Browser LocalStorage

## 📱 Mobile Responsive

Works perfectly on:
- 💻 Desktop computers
- 📱 Tablets
- 📲 Smartphones
- Any modern browser

## 🔒 Privacy First

✅ History stored locally only
✅ Audio auto-deleted
✅ No data tracking
✅ No login required

## 🚀 How to Run

### For Windows (Easiest!)
```bash
cd translator_app
run.bat
```

### For macOS/Linux
```bash
cd translator_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app_simple.py
```

### Then Open
```
http://localhost:5000
```

## 🎓 Learning Resources

This project teaches:
- Flask web development
- RESTful APIs
- Frontend-backend communication
- Audio processing
- Responsive CSS design
- JavaScript ES6+
- Web Audio API

## 🌟 Why Use This?

✨ Complete translation solution
✨ No complex setup
✨ Completely free
✨ Beautiful modern UI
✨ Works everywhere
✨ Educational value

## 📞 Need Help?

1. Check SETUP_INSTRUCTIONS.md
2. Review Flask console output
3. Press F12 for browser errors
4. Verify internet connection
5. Try running `python app_simple.py`

## 🎉 Ready to Start?

**Windows:**
```bash
cd translator_app && run.bat
```

**macOS/Linux:**
```bash
cd translator_app && python3 app_simple.py
```

Open: `http://localhost:5000`

---

**Start translating across 14 languages! 🌍🗣️**