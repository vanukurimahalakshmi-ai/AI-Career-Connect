/**
 * AI CAREER CONNECT - Live Voice Interview Studio Controller
 */

let currentTranscriptId = null;
let currentSessionId = null;

document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('startSessionBtn');
    const micBtn = document.getElementById('micRecordBtn');
    const submitBtn = document.getElementById('submitAnswerBtn');

    if (startBtn) {
        startBtn.addEventListener('click', startNewInterviewSession);
    }

    if (micBtn) {
        micBtn.addEventListener('click', toggleSpeechRecording);
    }

    if (submitBtn) {
        submitBtn.addEventListener('click', submitVoiceResponse);
    }
});

function startNewInterviewSession() {
    const roleSelect = document.getElementById('targetRoleSelect');
    const topicSelect = document.getElementById('topicSelect');
    
    const targetRole = roleSelect ? roleSelect.value : 'Senior AI Engineer';
    const topic = topicSelect ? topicSelect.value : 'Technical Behavioral & Architecture';

    document.getElementById('sessionSetupBox').style.display = 'none';
    document.getElementById('activeInterviewStudio').style.display = 'block';
    
    // Update Question Box Loading State
    document.getElementById('aiQuestionText').innerText = "AI Interviewer is generating your tailored question...";

    fetch('/api/interview/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_role: targetRole, topic: topic })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            currentSessionId = data.session.id;
            currentTranscriptId = data.current_question.transcript_id;
            
            const qText = data.current_question.question;
            document.getElementById('aiQuestionText').innerText = qText;
            
            // Speak question using TTS
            speakAIResponse(qText, data.current_question.audio_url);
            
            // Render Hints
            const hintsBox = document.getElementById('questionHints');
            if (hintsBox && data.current_question.hints) {
                hintsBox.innerHTML = data.current_question.hints.map(h => `<span class="badge-ai" style="margin-right: 6px;">💡 ${h}</span>`).join('');
            }
        }
    })
    .catch(err => {
        console.error("Start session error:", err);
        document.getElementById('aiQuestionText').innerText = "Unable to connect to AI server. Please refresh.";
    });
}

function toggleSpeechRecording() {
    const micBtn = document.getElementById('micRecordBtn');
    const waveAnim = document.getElementById('voiceWaveAnim');
    const speechBox = document.getElementById('userSpeechInput');

    if (!window.voiceEngine) return;

    if (!window.voiceEngine.isRecording) {
        // Start STT
        micBtn.classList.add('recording');
        if (waveAnim) waveAnim.classList.add('active');
        document.getElementById('speechStatusText').innerText = "🎙️ Listening... Speak into your microphone.";

        window.voiceEngine.startListening(
            (finalText, interimText) => {
                speechBox.value = finalText + (interimText ? ` [${interimText}]` : '');
            },
            (err) => {
                document.getElementById('speechStatusText').innerText = `⚠️ STT Note: ${err}`;
            }
        );
    } else {
        // Stop STT
        const finalRecordedText = window.voiceEngine.stopListening();
        micBtn.classList.remove('recording');
        if (waveAnim) waveAnim.classList.remove('active');
        document.getElementById('speechStatusText').innerText = "✅ Audio captured. Click Submit Answer for AI Feedback.";
        
        if (finalRecordedText) {
            speechBox.value = finalRecordedText;
        }
    }
}

function submitVoiceResponse() {
    const responseText = document.getElementById('userSpeechInput').value;

    if (!responseText || responseText.trim().length === 0) {
        alert("Please speak your response or enter text into the box before submitting.");
        return;
    }

    if (!currentTranscriptId) {
        alert("No active question session. Please start a new session.");
        return;
    }

    document.getElementById('aiFeedbackBox').style.display = 'block';
    document.getElementById('feedbackContent').innerHTML = `
        <div style="text-align: center; padding: 20px;">
            <div class="badge-ai"><span class="badge-dot"></span> Analyzing answer structure and speech metrics with Mistral AI...</div>
        </div>
    `;

    fetch('/api/interview/submit_answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            transcript_id: currentTranscriptId,
            user_speech_text: responseText
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            const evalData = data.evaluation;

            document.getElementById('feedbackContent').innerHTML = `
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                    <h4 style="font-size: 20px;">Overall Answer Score</h4>
                    <span style="font-size: 28px; font-weight: 800; color: ${evalData.score >= 80 ? '#10B981' : '#F59E0B'}">${evalData.score}/100</span>
                </div>
                <p style="color: #CBD5E1; line-height: 1.6; margin-bottom: 16px;">${evalData.feedback}</p>
                <div>
                    <h5 style="color: #9CA3AF; margin-bottom: 8px;">Key Recommendations:</h5>
                    <ul style="padding-left: 20px; color: #94A3B8;">
                        ${(evalData.key_takeaways || []).map(t => `<li style="margin-bottom: 6px;">${t}</li>`).join('')}
                    </ul>
                </div>
            `;

            // Speak AI Feedback via TTS
            speakAIResponse(evalData.feedback, evalData.audio_url);
        }
    })
    .catch(err => {
        console.error("Evaluation error:", err);
    });
}

function speakAIResponse(text, audioUrl) {
    const avatar = document.getElementById('aiAvatarBox');
    if (avatar) avatar.classList.add('speaking');

    const onSpeechFinished = () => {
        if (avatar) avatar.classList.remove('speaking');
    };

    if (audioUrl) {
        window.voiceEngine.playAudioUrl(audioUrl, onSpeechFinished);
    } else {
        window.voiceEngine.speak(text, onSpeechFinished);
    }
}
