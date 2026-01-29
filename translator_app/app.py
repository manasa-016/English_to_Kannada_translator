from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import io
from pathlib import Path
import json

# Import translation and speech libraries
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import base64

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

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

# Try to initialize Google Cloud clients
try:
    translate_client = translate_v2.Client()
    tts_client = texttospeech.TextToSpeechClient()
    google_available = True
except:
    google_available = False
    print("Warning: Google Cloud credentials not found. Using fallback methods.")

# Speech recognizer
recognizer = sr.Recognizer()

@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """Translate text from source to target language"""
    try:
        data = request.json
        source_text = data.get('text', '')
        source_lang = data.get('source_lang', 'en')
        target_lang = data.get('target_lang', 'kn')
        
        if not source_text:
            return jsonify({'error': 'No text provided'}), 400
        
        if google_available:
            result = translate_client.translate_text(
                source_language=source_lang,
                target_language=target_lang,
                values=[source_text]
            )
            translated_text = result['translations'][0]['translatedText']
        else:
            # Fallback: Use a simple translation API (MyMemory API)
            import requests
            api_url = f"https://api.mymemory.translated.net/get?q={source_text}&langpair={source_lang}|{target_lang}"
            response = requests.get(api_url)
            if response.status_code == 200:
                translated_text = response.json()['responseData']['translatedText']
            else:
                translated_text = "[Translation Service Unavailable]"
        
        return jsonify({
            'translated_text': translated_text,
            'source_lang': source_lang,
            'target_lang': target_lang
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    """Convert text to speech"""
    try:
        data = request.json
        text = data.get('text', '')
        language = data.get('language', 'en')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if google_available:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code=language,
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            response = tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
            return jsonify({
                'audio': audio_base64,
                'format': 'mp3'
            })
        else:
            # Fallback: Use gTTS
            try:
                from gtts import gTTS
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
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    """Convert speech to text"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', 'en')
        
        if audio_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save the audio file temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_audio.wav')
        audio_file.save(temp_path)
        
        try:
            with sr.AudioFile(temp_path) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language=language)
                return jsonify({'text': text, 'language': language})
        except sr.UnknownValueError:
            return jsonify({'error': 'Could not understand audio'}), 400
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
        if google_available:
            result = translate_client.translate_text(
                source_language=source_lang,
                target_language=target_lang,
                values=[text]
            )
            translated_text = result['translations'][0]['translatedText']
        else:
            import requests
            api_url = f"https://api.mymemory.translated.net/get?q={text}&langpair={source_lang}|{target_lang}"
            response = requests.get(api_url)
            if response.status_code == 200:
                translated_text = response.json()['responseData']['translatedText']
            else:
                translated_text = text
        
        # Step 3: Text to Speech
        try:
            from gtts import gTTS
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

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
