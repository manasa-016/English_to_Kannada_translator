// Global State
const state = {
    currentMode: 'text-to-text',
    sourceText: '',
    targetText: '',
    translationHistory: JSON.parse(localStorage.getItem('translationHistory')) || [],
    mediaRecorder: null,
    audioChunks: [],
    recordingStartTime: null,
    recordingTimer: null,
};

// DOM Elements
const sourceText = document.getElementById('sourceText');
const targetText = document.getElementById('targetText');
const sourceLang = document.getElementById('sourceLang');
const targetLang = document.getElementById('targetLang');
const translateBtn = document.getElementById('translateBtn');
const swapBtn = document.getElementById('swapBtn');
const recordBtn = document.getElementById('recordBtn');
const historyContainer = document.getElementById('historyContainer');
const toast = document.getElementById('toast');
const loadingIndicator = document.getElementById('loadingIndicator');
const modeBtns = document.querySelectorAll('.mode-btn');
const clearSourceText = document.getElementById('clearSourceText');
const copyTargetText = document.getElementById('copyTargetText');
const speakTargetText = document.getElementById('speakTargetText');

// Mode Management
modeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const mode = btn.dataset.mode;
        switchMode(mode);
    });
});

function switchMode(mode) {
    state.currentMode = mode;

    // Update active button
    modeBtns.forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-mode="${mode}"]`).classList.add('active');

    // Hide all sections
    document.querySelectorAll('.input-section').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.output-section').forEach(el => el.classList.remove('active'));

    // Show relevant sections based on mode
    switch (mode) {
        case 'text-to-text':
            document.getElementById('text-to-text-input').classList.add('active');
            document.getElementById('text-output-section').classList.add('active');
            break;
        case 'text-to-voice':
            document.getElementById('text-to-text-input').classList.add('active');
            document.getElementById('voice-output-section').classList.add('active');
            break;
        case 'voice-to-text':
            document.getElementById('voice-input-section').classList.add('active');
            document.getElementById('text-output-section').classList.add('active');
            break;
        case 'voice-to-voice':
            document.getElementById('voice-input-section').classList.add('active');
            document.getElementById('voice-output-section').classList.add('active');
            break;
    }

    // Reset recording
    if (state.mediaRecorder && state.mediaRecorder.state === 'recording') {
        stopRecording();
    }
}

// Translation
translateBtn.addEventListener('click', async () => {
    switch (state.currentMode) {
        case 'text-to-text':
            await translateTextToText();
            break;
        case 'text-to-voice':
            await translateTextToVoice();
            break;
        case 'voice-to-text':
            await translateVoiceToText();
            break;
        case 'voice-to-voice':
            await translateVoiceToVoice();
            break;
    }
});

async function translateTextToText() {
    const text = sourceText.value.trim();
    if (!text) {
        showToast('Please enter text to translate', 'warning');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text,
                source_lang: sourceLang.value,
                target_lang: targetLang.value
            })
        });

        const data = await response.json();
        console.log('Translation Response:', data);
        if (response.ok) {
            state.targetText = data.translated_text;
            console.log('Setting translated text:', data.translated_text);
            targetText.innerHTML = `<p>${escapeHtml(data.translated_text)}</p>`;
            console.log('targetText element after update:', targetText.innerHTML);
            addToHistory(text, data.translated_text, `${sourceLang.value} → ${targetLang.value}`);
            showToast('Translation successful!', 'success');
        } else {
            showToast(data.error || 'Translation failed', 'error');
        }
    } catch (error) {
        console.error('Translation error:', error);
        showToast('Error during translation', 'error');
    } finally {
        showLoading(false);
    }
}

async function translateTextToVoice() {
    const text = sourceText.value.trim();
    if (!text) {
        showToast('Please enter text to convert', 'warning');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/api/text-to-speech', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text,
                language: targetLang.value
            })
        });

        const data = await response.json();
        if (response.ok) {
            const audioData = `data:audio/${data.format};base64,${data.audio}`;
            const audioElement = document.getElementById('targetAudio');
            audioElement.src = audioData;
            document.getElementById('downloadAudio').style.display = 'block';
            showToast('Voice generation successful!', 'success');
        } else {
            showToast(data.error || 'Voice generation failed', 'error');
        }
    } catch (error) {
        console.error('TTS error:', error);
        showToast('Error during voice generation', 'error');
    } finally {
        showLoading(false);
    }
}

async function translateVoiceToText() {
    const audioBlob = await getAudioBlob();
    if (!audioBlob) {
        showToast('Please record audio first', 'warning');
        return;
    }

    showLoading(true);

    try {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'audio.wav');
        formData.append('language', sourceLang.value);

        const response = await fetch('/api/speech-to-text', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (response.ok) {
            // Now translate
            const translateResponse = await fetch('/api/translate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: data.text,
                    source_lang: sourceLang.value,
                    target_lang: targetLang.value
                })
            });

            const translateData = await translateResponse.json();
            if (translateResponse.ok) {
                state.targetText = translateData.translated_text;
                targetText.innerHTML = `<p>${escapeHtml(translateData.translated_text)}</p>`;
                addToHistory(data.text, translateData.translated_text, `${sourceLang.value} → ${targetLang.value}`);
                showToast('Voice to text translation successful!', 'success');
            }
        } else {
            showToast(data.error || 'Speech recognition failed', 'error');
        }
    } catch (error) {
        console.error('Voice to text error:', error);
        showToast('Error during voice to text conversion', 'error');
    } finally {
        showLoading(false);
    }
}

async function translateVoiceToVoice() {
    const audioBlob = await getAudioBlob();
    if (!audioBlob) {
        showToast('Please record audio first', 'warning');
        return;
    }

    showLoading(true);

    try {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'audio.wav');
        formData.append('source_lang', sourceLang.value);
        formData.append('target_lang', targetLang.value);

        const response = await fetch('/api/voice-to-voice', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (response.ok) {
            const audioData = `data:audio/${data.format};base64,${data.audio}`;
            const audioElement = document.getElementById('targetAudio');
            audioElement.src = audioData;
            document.getElementById('downloadAudio').style.display = 'block';
            addToHistory(data.source_text, data.text, `${sourceLang.value} → ${targetLang.value}`);
            showToast('Voice to voice translation successful!', 'success');
        } else {
            showToast(data.error || 'Translation failed', 'error');
        }
    } catch (error) {
        console.error('Voice to voice error:', error);
        showToast('Error during voice to voice translation', 'error');
    } finally {
        showLoading(false);
    }
}

// Audio Recording
recordBtn.addEventListener('click', async () => {
    if (!state.mediaRecorder || state.mediaRecorder.state === 'inactive') {
        startRecording();
    } else {
        stopRecording();
    }
});

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        state.mediaRecorder = new MediaRecorder(stream);
        state.audioChunks = [];

        state.mediaRecorder.ondataavailable = (event) => {
            state.audioChunks.push(event.data);
        };

        state.mediaRecorder.onstop = () => {
            const audioBlob = new Blob(state.audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            const audioElement = document.getElementById('sourceAudio');
            audioElement.src = audioUrl;

            // Store for later use
            window.recordedAudioBlob = audioBlob;

            document.getElementById('audioPlayback').style.display = 'block';
            document.getElementById('recordingStatus').style.display = 'none';
            clearInterval(state.recordingTimer);
        };

        state.mediaRecorder.start();
        state.recordingStartTime = Date.now();

        recordBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Recording';
        recordBtn.style.background = 'linear-gradient(135deg, #f56565, #e53e3e)';
        document.getElementById('recordingStatus').style.display = 'block';

        // Timer
        startRecordingTimer();
    } catch (error) {
        console.error('Recording error:', error);
        showToast('Microphone access denied', 'error');
    }
}

function stopRecording() {
    if (state.mediaRecorder) {
        state.mediaRecorder.stop();
        state.mediaRecorder.stream.getTracks().forEach(track => track.stop());

        recordBtn.innerHTML = '<i class="fas fa-microphone"></i> Start Recording';
        recordBtn.style.background = '';
    }
}

function startRecordingTimer() {
    const recordingTimeEl = document.getElementById('recordingTime');
    state.recordingTimer = setInterval(() => {
        const elapsed = Math.floor((Date.now() - state.recordingStartTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        recordingTimeEl.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }, 1000);
}

function getAudioBlob() {
    return new Promise((resolve) => {
        if (window.recordedAudioBlob) {
            resolve(window.recordedAudioBlob);
        } else {
            resolve(null);
        }
    });
}

// Swap Languages
swapBtn.addEventListener('click', () => {
    const temp = sourceLang.value;
    sourceLang.value = targetLang.value;
    targetLang.value = temp;

    // Swap text if in text-to-text mode
    if (state.currentMode === 'text-to-text') {
        const tempText = sourceText.value;
        sourceText.value = targetText.textContent || '';
        targetText.innerHTML = `<p>${escapeHtml(tempText)}</p>`;
    }
});

// Copy and Listen
copyTargetText.addEventListener('click', () => {
    const text = targetText.textContent;
    navigator.clipboard.writeText(text).then(() => {
        showToast('Text copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy text', 'error');
    });
});

speakTargetText.addEventListener('click', async () => {
    const text = targetText.textContent;
    if (!text) {
        showToast('No text to speak', 'warning');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/api/text-to-speech', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text,
                language: targetLang.value
            })
        });

        const data = await response.json();
        if (response.ok) {
            const audioData = `data:audio/${data.format};base64,${data.audio}`;
            const audio = new Audio(audioData);
            audio.play();
        } else {
            showToast(data.error || 'Speech synthesis failed', 'error');
        }
    } catch (error) {
        console.error('Speech synthesis error:', error);
        showToast('Error during speech synthesis', 'error');
    } finally {
        showLoading(false);
    }
});

// Clear Source Text
clearSourceText.addEventListener('click', () => {
    sourceText.value = '';
    sourceText.focus();
});

// History Management
function addToHistory(source, target, langs) {
    const item = {
        source: source.substring(0, 50),
        target: target.substring(0, 50),
        langs,
        timestamp: new Date().getTime()
    };

    state.translationHistory.unshift(item);
    if (state.translationHistory.length > 20) {
        state.translationHistory.pop();
    }

    localStorage.setItem('translationHistory', JSON.stringify(state.translationHistory));
    renderHistory();
}

function renderHistory() {
    if (state.translationHistory.length === 0) {
        historyContainer.innerHTML = '<p class="empty-message">No translations yet</p>';
        return;
    }

    historyContainer.innerHTML = state.translationHistory.map((item, index) => `
        <div class="history-item" onclick="useHistoryItem(${index})">
            <div class="history-item-source">From: ${escapeHtml(item.source)}</div>
            <div class="history-item-text">${escapeHtml(item.target)}</div>
            <div class="history-item-lang">${item.langs}</div>
        </div>
    `).join('');
}

function useHistoryItem(index) {
    const item = state.translationHistory[index];
    sourceText.value = item.source;
    showToast('History item loaded', 'success');
}

// Utility Functions
function showLoading(show) {
    if (show) {
        loadingIndicator.classList.add('active');
        translateBtn.disabled = true;
    } else {
        loadingIndicator.classList.remove('active');
        translateBtn.disabled = false;
    }
}

function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast ${type} active`;

    setTimeout(() => {
        toast.classList.remove('active');
    }, 3000);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Download Audio
document.getElementById('downloadAudio').addEventListener('click', () => {
    const audio = document.getElementById('targetAudio');
    if (audio.src) {
        const link = document.createElement('a');
        link.href = audio.src;
        link.download = `translation_${Date.now()}.mp3`;
        link.click();
    }
});

// Initialize
renderHistory();
switchMode('text-to-text');

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
        translateBtn.click();
    }
});

console.log('Translator app initialized');
