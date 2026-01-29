"""
Simplified Flask app - Python 3.14 compatible version
This version works without Google Cloud credentials
No SpeechRecognition import to avoid compatibility issues with Python 3.14
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import io
import requests
import base64
from pathlib import Path

try:
    from gtts import gTTS
except ImportError:
    gTTS = None

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

@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/favicon.ico')
def favicon():
    """Return favicon (prevents 404 errors)"""
    return '', 204

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get list of available languages"""
    try:
        return jsonify(list(LANGUAGES.keys()))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/translate', methods=['POST'])
def translate():
    """Translate text using MyMemory API (free, no key required)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
            
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'English')
        target_lang = data.get('target_lang', 'Kannada')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Get language codes - support both language names and codes
        source_code = LANGUAGES.get(source_lang, source_lang).lower()
        target_code = LANGUAGES.get(target_lang, target_lang).lower()
        
        print(f"Translation request: {source_lang} ({source_code}) -> {target_lang} ({target_code})")
        print(f"Text: {text}")
        
        # Use MyMemory API (free translation service)
        api_url = "https://api.mymemory.translated.net/get"
        params = {
            'q': text,
            'langpair': f'{source_code}|{target_code}'
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        result = response.json()
        
        print(f"MyMemory Response: {result}")
        
        if result.get('responseStatus') == 200:
            translated_text = result.get('responseData', {}).get('translatedText', '').strip()
            
            print(f"Initial translated_text: '{translated_text}'")
            print(f"Has matches: {bool(result.get('matches'))}")
            
            # If translatedText is empty, try to use first match
            if not translated_text and result.get('matches'):
                matches = result.get('matches', [])
                print(f"Number of matches: {len(matches)}")
                if matches:
                    translated_text = matches[0].get('translation', '').strip()
                    print(f"Using match: '{translated_text}'")
            
            # If still empty, use the original text as fallback
            if not translated_text:
                print("No translation found, returning original text")
                translated_text = text
            
            print(f"Final translated text: '{translated_text}'")
            return jsonify({
                'original': text,
                'translated_text': translated_text,
                'source_lang': source_lang,
                'target_lang': target_lang
            })
        else:
            error_msg = result.get('responseDetails', 'Translation service error')
            print(f"Translation failed: {error_msg}")
            return jsonify({'error': error_msg}), 500
            
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Translation service timeout - try again'}), 504
    except Exception as e:
        print(f"Translation error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    """Convert text to speech using gTTS"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        lang = data.get('language', 'English')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Get language code - support both language names and codes
        lang_code = LANGUAGES.get(lang, lang).lower()
        
        # Use gTTS (Google Text-to-Speech)
        tts = gTTS(text=text, lang=lang_code, slow=False)
        
        # Save to bytes
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        
        # Convert to base64
        audio_base64 = base64.b64encode(audio_fp.getvalue()).decode()
        
        return jsonify({
            'audio': audio_base64,
            'format': 'mp3'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    """Convert speech to text (simplified - browser-side implementation)"""
    try:
        # Note: Actual speech recognition should be done client-side using Web Speech API
        # This endpoint is a placeholder for server-side processing if needed
        
        if 'file' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['file']
        lang = request.form.get('lang', 'en')
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # For now, return a placeholder
        # In production, you would use a speech-to-text API
        return jsonify({
            'text': 'Speech recognition placeholder',
            'lang': lang
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice-to-voice', methods=['POST'])
def voice_to_voice():
    """Full voice-to-voice translation pipeline"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        source_lang = request.form.get('source_lang', 'en')
        target_lang = request.form.get('target_lang', 'kn')
        
        # Step 1: Speech-to-text (placeholder - use browser's Web Speech API instead)
        recognized_text = "Sample text"  # Would come from audio file
        
        # Step 2: Translate
        source_code = LANGUAGES.get(source_lang, 'en')
        target_code = LANGUAGES.get(target_lang, 'en')
        
        api_url = f"https://api.mymemory.translated.net/get"
        params = {
            'q': recognized_text,
            'langpair': f'{source_code}|{target_code}'
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        result = response.json()
        
        if result.get('responseStatus') != 200:
            return jsonify({'error': 'Translation failed'}), 500
        
        translated_text = result.get('responseData', {}).get('translatedText', '')
        
        # Step 3: Text-to-speech
        tts = gTTS(text=translated_text, lang=target_code, slow=False)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        audio_base64 = base64.b64encode(audio_fp.getvalue()).decode()
        
        return jsonify({
            'original_text': recognized_text,
            'translated_text': translated_text,
            'audio': audio_base64,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'format': 'mp3'
        })
        
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Service timeout'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Translator service is running'})

if __name__ == '__main__':
    print("=" * 60)
    print("[GLOBE] English to Kannada Translator (Multi-Language)")
    print("=" * 60)
    print("\n[OK] Flask application starting...")
    print("[PIN] Server: http://localhost:5000")
    print("[PIN] Upload limit: 16 MB")
    print("\n[WORLD] Supported Languages:")
    for lang in LANGUAGES.keys():
        print(f"   * {lang}")
    print("\n" + "=" * 60)
    print("[STAR] Server is running! Open http://localhost:5000 in your browser")
    print("=" * 60 + "\n")
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=False
    )
