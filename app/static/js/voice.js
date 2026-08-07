/**
 * AI CAREER CONNECT - Voice Studio STT & TTS Engine
 * Handles client-side Speech-to-Text (STT) and Text-to-Speech (TTS) capabilities.
 */

class VoiceEngine {
    constructor() {
        // Speech Recognition Setup (STT)
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = SpeechRecognition ? new SpeechRecognition() : null;
        
        if (this.recognition) {
            this.recognition.continuous = true;
            this.recognition.interimResults = true;
            this.recognition.lang = 'en-US';
        }

        // Speech Synthesis Setup (TTS)
        this.synth = window.speechSynthesis;
        this.isRecording = false;
        this.finalTranscript = '';
    }

    /**
     * Start Speech-to-Text Recording
     */
    startListening(onResult, onError) {
        if (!this.recognition) {
            if (onError) onError("Browser STT not supported in this browser. Please use Chrome/Edge/Safari.");
            return;
        }

        this.finalTranscript = '';
        this.isRecording = true;

        this.recognition.onresult = (event) => {
            let interim = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    this.finalTranscript += event.results[i][0].transcript + ' ';
                } else {
                    interim += event.results[i][0].transcript;
                }
            }
            if (onResult) onResult(this.finalTranscript, interim);
        };

        this.recognition.onerror = (event) => {
            console.error("[VoiceEngine] STT Error:", event.error);
            if (onError) onError(event.error);
        };

        this.recognition.start();
    }

    /**
     * Stop Speech-to-Text Recording
     */
    stopListening() {
        if (this.recognition && this.isRecording) {
            this.recognition.stop();
            this.isRecording = false;
        }
        return this.finalTranscript.trim();
    }

    /**
     * Text-to-Speech (TTS) Voice Synthesis
     */
    speak(text, onEnd) {
        if (!this.synth) return;

        // Cancel existing speech
        this.synth.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.lang = 'en-US';

        // Select natural voice if available
        const voices = this.synth.getVoices();
        const preferredVoice = voices.find(v => v.lang.includes('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Samantha')));
        if (preferredVoice) {
            utterance.voice = preferredVoice;
        }

        if (onEnd) {
            utterance.onend = onEnd;
            utterance.onerror = onEnd;
        }

        this.synth.speak(utterance);
    }

    /**
     * Play server-generated audio file URL (Fallback TTS MP3)
     */
    playAudioUrl(audioUrl, onEnd) {
        if (!audioUrl) return;
        const audio = new Audio(audioUrl);
        if (onEnd) {
            audio.onended = onEnd;
            audio.onerror = onEnd;
        }
        audio.play().catch(e => {
            console.warn("[VoiceEngine] Fallback to browser Speech Synthesis:", e);
            if (onEnd) onEnd();
        });
    }
}

window.voiceEngine = new VoiceEngine();
