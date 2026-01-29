# 🚀 Quick Start Guide - Multilingual Translator

## One-Minute Setup

### Windows
```bash
cd translator_app
run.bat
```
Then open: `http://localhost:5000`

### macOS/Linux
```bash
cd translator_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app_simple.py
```
Then open: `http://localhost:5000`

---

## ⏱️ 5-Minute Setup (If run.bat doesn't work)

### Step 1: Install Python (if needed)
- Download from https://python.org
- Check "Add to PATH" during installation

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Application
```bash
python app_simple.py
```

### Step 5: Open Browser
```
http://localhost:5000
```

---

## 🎯 Features Available Immediately

✅ Text-to-Text Translation (14 languages)
✅ Text-to-Voice (listen to translations)
✅ Voice-to-Text (record and transcribe)
✅ Voice-to-Voice (complete translation)
✅ Translation History (last 20)
✅ Copy-to-Clipboard
✅ Language Swap

---

## 🔥 Common Commands

| Command | Windows | macOS/Linux |
|---------|---------|------------|
| Activate venv | `venv\Scripts\activate` | `source venv/bin/activate` |
| Install deps | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Run app | `python app_simple.py` | `python3 app_simple.py` |
| Deactivate venv | `deactivate` | `deactivate` |

---

## 🐛 Quick Troubleshooting

### Error: "python command not found"
→ Python not installed. Download from python.org

### Error: "Port 5000 already in use"
→ Edit `app_simple.py`, change `port=5000` to `port=5001`

### Error: "ModuleNotFoundError: No module named 'flask'"
→ Activate virtual environment first, then install requirements

### Microphone not detected
→ Check Windows Sound Settings, restart browser, allow permissions

### Translation not working
→ Check internet connection is active

---

## 📁 Important Files

| File | What It Does |
|------|---|
| `run.bat` | Auto-start script for Windows |
| `app_simple.py` | Main app (uses free APIs) |
| `requirements.txt` | All dependencies to install |
| `templates/index.html` | The beautiful UI |
| `static/css/style.css` | Styling |
| `static/js/app.js` | Frontend logic |

---

## 🌐 Supported Languages

1. English
2. Kannada
3. Hindi
4. Tamil
5. Telugu
6. Spanish
7. French
8. German
9. Chinese
10. Japanese
11. Arabic
12. Portuguese
13. Russian
14. Italian

---

## 💡 Tips & Tricks

✨ **Faster translations**: Use text-to-text instead of voice modes
✨ **Better voice recognition**: Speak clearly in quiet environment
✨ **Copy translations**: Click the "Copy" button on right panel
✨ **Listen to results**: Click "Listen" button to hear pronunciation
✨ **Swap languages**: Click the swap button in the middle
✨ **Keyboard shortcut**: Press Ctrl+Enter to translate immediately
✨ **View history**: Scroll down to see recent translations
✨ **Use history**: Click any history item to reload it

---

## 🔗 Important Links

- **Full Setup Guide**: See SETUP_INSTRUCTIONS.md
- **Python Download**: https://python.org
- **FFmpeg (if needed)**: https://ffmpeg.org
- **Troubleshooting**: SETUP_INSTRUCTIONS.md

---

## ⚡ System Requirements

✅ Python 3.8+
✅ Internet connection
✅ Microphone (for voice features)
✅ Modern web browser
✅ 2GB RAM minimum

---

## 🎓 What You're Learning

This project demonstrates:
- Flask web framework
- REST APIs
- Frontend-backend communication
- Audio processing
- Responsive web design
- JavaScript event handling
- Web APIs

---

## 📞 Still Have Issues?

1. **Check SETUP_INSTRUCTIONS.md** - Has detailed help
2. **Look at Flask console** - Shows error messages
3. **Press F12 in browser** - Check for JavaScript errors
4. **Verify all files exist** - Check file structure
5. **Try app_simple.py** - Uses free APIs without credentials

---

## 🎉 Success Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] Flask running (python app_simple.py)
- [ ] Browser open to http://localhost:5000
- [ ] Can enter text
- [ ] Can translate
- [ ] Can hear results
- [ ] Can record voice

If all checked ✅, you're ready to translate!

---

## 🚀 Ready?

```
cd translator_app
python app_simple.py
# Open http://localhost:5000
```

**Happy translating!** 🌍

---

**Version: 1.0.0 | January 2026**
