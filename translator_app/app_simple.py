"""
Simplified Flask app with fallback translation APIs
This version works without Google Cloud credentials
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import io
import requests
import base64
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Language codes
LANGUAGES = {
    'English': 'en',
    'Kannada': 'kn',
    'Hindi': 'hi',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Chinese': 'zh',
    'Japanese': 'ja',
    'Arabic': 'ar',
    'Portuguese': 'pt',
    'Russian': 'ru',
    'Italian': 'it',
    'Malayalam': 'ml'
}

# Try to import optional libraries
try:
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    SPEECH_RECOGNITION_AVAILABLE = True
except:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("Warning: SpeechRecognition not fully configured")

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except:
    GTTS_AVAILABLE = False
    print("Warning: gTTS not available")

@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """Translate text using free MyMemory API"""
    try:
        data = request.json
        source_text = data.get('text', '')
        source_lang = data.get('source_lang', 'en')
        target_lang = data.get('target_lang', 'kn')
        
        if not source_text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Use MyMemory API (free, no authentication required)
        api_url = f"https://api.mymemory.translated.net/get"
        params = {
            'q': source_text,
            'langpair': f'{source_lang}|{target_lang}'
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('responseStatus') == 200:
                translated_text = result['responseData']['translatedText']
                return jsonify({
                    'translated_text': translated_text,
                    'source_lang': source_lang,
                    'target_lang': target_lang
                })
        
        return jsonify({'error': 'Translation service unavailable'}), 500
    
    except requests.Timeout:
        return jsonify({'error': 'Translation service timeout'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    """Convert text to speech using gTTS"""
    try:
        data = request.json
        text = data.get('text', '')
        language = data.get('language', 'en')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if not GTTS_AVAILABLE:
            return jsonify({'error': 'Text-to-speech service not available'}), 500
        
        # Use gTTS (Google Text-to-Speech - free)
        tts = gTTS(text=text, lang=language, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
        return jsonify({
            'audio': audio_base64,
            'format': 'mp3'
        })
    
    except Exception as e:
        return jsonify({'error': f'Text-to-speech failed: {str(e)}'}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    """Convert speech to text using Google Speech Recognition"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', 'en')
        
        if audio_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not SPEECH_RECOGNITION_AVAILABLE:
            return jsonify({'error': 'Speech recognition not available'}), 500
        
        # Save the audio file temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_audio.wav')
        audio_file.save(temp_path)
        
        try:
            with sr.AudioFile(temp_path) as source:
                audio = recognizer.record(source)
                # Use Google's free speech recognition API
                text = recognizer.recognize_google(audio, language=language)
                return jsonify({'text': text, 'language': language})
        
        except sr.UnknownValueError:
            return jsonify({'error': 'Could not understand audio. Please try again.'}), 400
        except sr.RequestError as e:
            return jsonify({'error': f'Speech recognition error: {str(e)}'}), 500
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice-to-voice', methods=['POST'])
def voice_to_voice():
    """Convert voice from one language to another"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        source_lang = request.form.get('source_lang', 'en')
        target_lang = request.form.get('target_lang', 'kn')
        
        if not SPEECH_RECOGNITION_AVAILABLE:
            return jsonify({'error': 'Speech recognition not available'}), 500
        
        # Step 1: Speech to Text
        temp_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_voice.wav')
        audio_file.save(temp_audio_path)
        
        try:
            with sr.AudioFile(temp_audio_path) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language=source_lang)
        except Exception as e:
            return jsonify({'error': f'Speech recognition failed: {str(e)}'}), 500
        finally:
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
        
        # Step 2: Translate
        api_url = f"https://api.mymemory.translated.net/get"
        params = {
            'q': text,
            'langpair': f'{source_lang}|{target_lang}'
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('responseStatus') == 200:
                translated_text = result['responseData']['translatedText']
            else:
                translated_text = text
        else:
            translated_text = text
        
        # Step 3: Text to Speech
        if not GTTS_AVAILABLE:
            return jsonify({'error': 'Text-to-speech service not available'}), 500
        
        try:
            tts = gTTS(text=translated_text, lang=target_lang, slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
            return jsonify({
                'audio': audio_base64,
                'text': translated_text,
                'format': 'mp3',
                'source_text': text
            })
        except Exception as e:
            return jsonify({'error': f'Text-to-speech failed: {str(e)}'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get available languages"""
    return jsonify({'languages': LANGUAGES})

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'speech_recognition': SPEECH_RECOGNITION_AVAILABLE,
        'text_to_speech': GTTS_AVAILABLE
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("""
    ========================================
    Multilingual Translator
    ========================================
    
    Starting Flask server...
    
    Open your browser and go to:
    http://localhost:5000
    
    Features available:
    - Text-to-Text Translation: ✓
    - Text-to-Speech: {'✓' if GTTS_AVAILABLE else '✗'}
    - Speech-to-Text: {'✓' if SPEECH_RECOGNITION_AVAILABLE else '✗'}
    - Voice-to-Voice: {'✓' if (GTTS_AVAILABLE and SPEECH_RECOGNITION_AVAILABLE) else '✗'}
    
    Press Ctrl+C to stop the server
    ========================================
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True)
