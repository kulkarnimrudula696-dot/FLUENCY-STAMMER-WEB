/**
 * FLUENCY 1-on-1 Face-to-Face Video Call Conversation Mode
 * Immersive video call experience with central speaking mascot companion,
 * real-time voice synthesis (TTS), live microphone turn-taking, PiP camera mirror,
 * and comprehensive speech analysis upon call completion.
 */

const ConversationPractice = {
  scenarios: [],
  activeScenario: null,
  conversationHistory: [],
  userSpokenSegments: [],
  currentUserTranscript: '',
  lastAiMessage: '',
  totalDurationSeconds: 0,
  isUserSpeaking: false,
  isCameraActive: false,
  cameraStream: null,
  recognition: null,
  synth: window.speechSynthesis,
  timerInterval: null,
  isInitialized: false,
  scenariosCache: {},
  audioEngine: null,
  recordedAudioUrl: null,

  getAudioEngine() {
    if (!this.audioEngine) {
      if (typeof FluencyAudioEngine !== 'undefined') {
        this.audioEngine = new FluencyAudioEngine();
      } else if (window.FluencyAudioEngine) {
        this.audioEngine = new window.FluencyAudioEngine();
      }
      if (this.audioEngine) {
        this.audioEngine.onAudioReady = (dataUrl) => {
          this.recordedAudioUrl = dataUrl;
        };
      }
    }
    return this.audioEngine;
  },

  init() {
    if (!this.isInitialized) {
      this.bindEvents();
      this.initSpeechRec();
      this.isInitialized = true;
    }
    this.updateUserIdentity();
    this.loadScenarios();
  },

  updateUserIdentity() {
    const user = (window.AppState && AppState.user) ? AppState.user : null;
    const rawName = (user && user.name) 
      ? user.name.trim() 
      : (localStorage.getItem('fluency_user_name') || 'You');
    const shortName = rawName.split(' ')[0] || 'You';
    const avatarId = (user && user.selected_avatar) 
      ? user.selected_avatar 
      : (localStorage.getItem('fluency_selected_avatar') || 'avatar-sunny');

    const avatarEl = document.getElementById('convo-pip-avatar');
    if (avatarEl && window.AvatarEngine) {
      avatarEl.innerHTML = AvatarEngine.render(avatarId, 48);
    }

    const nameLabel = document.getElementById('convo-pip-username-label');
    if (nameLabel) {
      nameLabel.innerText = shortName;
    }

    const badgeName = document.getElementById('convo-pip-badge-name');
    if (badgeName) {
      badgeName.innerText = shortName;
    }
  },

  cleanup() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
    if (this.synth) {
      try { this.synth.cancel(); } catch (e) {}
    }
    if (this.recognition && this.isUserSpeaking) {
      try { this.recognition.stop(); } catch (e) {}
      this.isUserSpeaking = false;
    }
    if (this.audioEngine) {
      this.audioEngine.stopRecording();
    }
    if (this.cameraStream && this.isCameraActive) {
      this.cameraStream.getTracks().forEach(t => t.stop());
      this.isCameraActive = false;
      const video = document.getElementById('convo-camera-video');
      const placeholder = document.getElementById('convo-pip-placeholder');
      const camText = document.getElementById('convo-cam-btn-text');
      if (video) video.style.display = 'none';
      if (placeholder) placeholder.style.display = 'flex';
      if (camText) camText.innerText = window.FluencyI18n ? FluencyI18n.t('btn_cam_on', 'Camera On') : 'Camera On';
    }
  },

  initSpeechRec() {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRec) {
      this.recognition = new SpeechRec();
      this.recognition.continuous = true;
      this.recognition.interimResults = true;
      
      // Sync recognition language with preferred language
      const langMap = {
        'English': 'en-US',
        'Hindi': 'hi-IN',
        'Marathi': 'mr-IN',
        'Spanish': 'es-ES',
        'French': 'fr-FR',
        'German': 'de-DE'
      };
      const currentLang = window.FluencyI18n ? FluencyI18n.currentLang : 'English';
      this.recognition.lang = langMap[currentLang] || 'en-US';

      this.recognition.onresult = (event) => {
        let interim = '';
        let final = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            final += event.results[i][0].transcript;
          } else {
            interim += event.results[i][0].transcript;
          }
        }

        const spoken = (final || interim).trim();
        if (spoken) {
          this.currentUserTranscript = spoken;
          const captionText = document.getElementById('convo-caption-text');
          const captionSpeaker = document.getElementById('convo-caption-speaker-name');
          if (captionSpeaker) {
            captionSpeaker.innerText = AppState.user ? AppState.user.name.split(' ')[0] : 'You';
          }
          if (captionText) {
            captionText.innerText = `"${spoken}"`;
          }
        }
      };

      this.recognition.onerror = (e) => {
        console.warn('Convo speech recognition event:', e.error);
      };

      this.recognition.onend = () => {
        if (this.isUserSpeaking) {
          try { this.recognition.start(); } catch (e) {}
        }
      };
    }
  },

  bindEvents() {
    // Scenario selection change
    document.getElementById('convo-scenario-select')?.addEventListener('change', (e) => {
      this.selectScenario(e.target.value);
    });

    // Primary Microphone button (Tap to Speak / Done Speaking)
    document.getElementById('btn-convo-mic-main')?.addEventListener('click', () => {
      this.toggleUserSpeaking();
    });

    // Replay Voice button
    document.getElementById('btn-convo-replay')?.addEventListener('click', () => {
      this.replayVoice();
    });

    // Camera toggle
    document.getElementById('btn-convo-camera-toggle')?.addEventListener('click', () => {
      this.toggleCamera();
    });

    // End & Analyze session
    document.getElementById('btn-convo-end-analyze')?.addEventListener('click', () => {
      this.endAndAnalyze();
    });
  },

  async loadScenarios() {
    const ageGroup = (AppState.user && AppState.user.age_group) || '18-23';
    const age = AppState.user ? (AppState.user.practice_age || 21) : 21;
    const cacheKey = ageGroup;
    if (this.scenariosCache[cacheKey] && this.scenariosCache[cacheKey].length > 0) {
      this.scenarios = this.scenariosCache[cacheKey];
      this.renderScenariosSelect();
      return;
    }

    try {
      const res = await fetch(`/api/content/scenarios?age_group=${encodeURIComponent(ageGroup)}&age=${age}`);
      const data = await res.json();
      this.scenarios = data.items || [];
      this.scenariosCache[cacheKey] = this.scenarios;
      this.renderScenariosSelect();
    } catch (err) {
      console.error("Failed to load conversation scenarios:", err);
    }
  },

  renderScenariosSelect() {
    const select = document.getElementById('convo-scenario-select');
    if (select && this.scenarios.length > 0) {
      select.innerHTML = this.scenarios.map(s => `<option value="${s.id}">${s.icon} ${s.title}</option>`).join('');
      this.selectScenario(this.scenarios[0].id);
    }
  },

  selectScenario(scenarioId) {
    this.activeScenario = this.scenarios.find(s => s.id === scenarioId) || this.scenarios[0];
    this.conversationHistory = [];
    this.userSpokenSegments = [];
    this.currentUserTranscript = '';
    this.totalDurationSeconds = 0;
    this.isUserSpeaking = false;

    // Update partner nametag & scenario context
    const mascotName = this.getMascotDisplayName();
    const partnerNameEl = document.getElementById('convo-partner-name');
    const scenarioDescEl = document.getElementById('convo-scenario-desc');
    if (partnerNameEl) partnerNameEl.innerText = `${mascotName} (Practice Partner)`;
    if (scenarioDescEl && this.activeScenario) scenarioDescEl.innerText = this.activeScenario.context;

    // Sync user avatar & name in PiP mirror
    this.updateUserIdentity();

    // Render large mascot
    this.renderMascot('smiling');

    // Start call timer
    this.startSessionTimer();

    // Trigger AI greeting voice
    if (this.activeScenario && this.activeScenario.ai_initial_message) {
      this.lastAiMessage = this.activeScenario.ai_initial_message;
      this.conversationHistory.push({ sender: 'ai', text: this.lastAiMessage });
      // Short delay for natural call connection feel
      setTimeout(() => {
        this.speakText(this.lastAiMessage);
      }, 400);
    }
  },

  getMascotId() {
    return AppState.user ? AppState.user.selected_mascot || 'otter' : 'otter';
  },

  getMascotDisplayName() {
    const mascotNames = {
      otter: 'Sammy',
      koala: 'Koby',
      capybara: 'Cappy',
      red_panda: 'Pip',
      hamster: 'Boba',
      duck: 'Ducky',
      seal: 'Snooze',
      axolotl: 'Lottie'
    };
    const id = this.getMascotId();
    return mascotNames[id] || 'Sammy';
  },

  renderMascot(state = 'smiling') {
    const container = document.getElementById('convo-mascot-partner');
    if (!container) return;
    const mascot = this.getMascotId();
    container.innerHTML = MascotEngine.render(mascot, state, 270);
  },

  setCallState(state, customMessage = null) {
    const pill = document.getElementById('convo-turn-pill');
    const turnText = document.getElementById('convo-turn-text');
    const ripples = document.getElementById('convo-voice-ripples');
    const mascotContainer = document.getElementById('convo-mascot-partner');
    const micBtn = document.getElementById('btn-convo-mic-main');
    const micLabel = document.getElementById('convo-mic-label');
    const micIcon = document.getElementById('convo-mic-icon');

    const t = (k, def) => (window.FluencyI18n ? FluencyI18n.t(k, def) : def);
    const mascotName = this.getMascotDisplayName();

    if (pill) {
      pill.className = `convo-turn-pill ${state}`;
    }

    if (state === 'ai-speaking') {
      if (turnText) turnText.innerText = customMessage || `${mascotName} is speaking...`;
      if (ripples) ripples.classList.add('active');
      if (mascotContainer) mascotContainer.classList.add('mascot-speaking-active');
      this.renderMascot('waving');
      if (micBtn) micBtn.classList.remove('active');
      if (micLabel) micLabel.innerText = t('btn_tap_to_speak', 'Tap to Speak');
      if (micIcon) micIcon.className = 'fa-solid fa-microphone';
    } 
    else if (state === 'user-turn') {
      if (turnText) turnText.innerText = customMessage || t('convo_your_turn', 'Your Turn to Speak — Tap Microphone');
      if (ripples) ripples.classList.remove('active');
      if (mascotContainer) mascotContainer.classList.remove('mascot-speaking-active');
      this.renderMascot('smiling');
      if (micBtn) micBtn.classList.remove('active');
      if (micLabel) micLabel.innerText = t('btn_tap_to_speak', 'Tap to Speak');
      if (micIcon) micIcon.className = 'fa-solid fa-microphone';
    } 
    else if (state === 'user-speaking') {
      if (turnText) turnText.innerText = customMessage || t('convo_listening_user', 'Listening to you... Speak freely');
      if (ripples) ripples.classList.add('active');
      if (mascotContainer) mascotContainer.classList.remove('mascot-speaking-active');
      this.renderMascot('listening');
      if (micBtn) micBtn.classList.add('active');
      if (micLabel) micLabel.innerText = t('btn_done_speaking', 'Done Speaking');
      if (micIcon) micIcon.className = 'fa-solid fa-microphone-lines fa-bounce';
    } 
    else if (state === 'thinking') {
      if (turnText) turnText.innerText = customMessage || t('convo_thinking', 'Thinking...');
      if (ripples) ripples.classList.remove('active');
      if (mascotContainer) mascotContainer.classList.remove('mascot-speaking-active');
      this.renderMascot('smiling');
      if (micBtn) micBtn.classList.remove('active');
      if (micLabel) micLabel.innerText = t('convo_thinking', 'Thinking...');
      if (micIcon) micIcon.className = 'fa-solid fa-circle-notch fa-spin';
    }
  },

  startSessionTimer() {
    if (this.timerInterval) clearInterval(this.timerInterval);
    const start = Date.now();
    this.timerInterval = setInterval(() => {
      this.totalDurationSeconds = Math.floor((Date.now() - start) / 1000);
      const timerDisp = document.getElementById('convo-session-timer');
      if (timerDisp) {
        const m = Math.floor(this.totalDurationSeconds / 60);
        const s = this.totalDurationSeconds % 60;
        timerDisp.innerText = `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
      }
    }, 1000);
  },

  speakText(text) {
    if (!this.synth) return;
    this.synth.cancel();

    this.lastAiMessage = text;
    this.setCallState('ai-speaking');

    // Update subtitle caption
    const captionSpeaker = document.getElementById('convo-caption-speaker-name');
    const captionText = document.getElementById('convo-caption-text');
    if (captionSpeaker) captionSpeaker.innerText = `${this.getMascotDisplayName()} (Partner)`;
    if (captionText) captionText.innerText = `"${text}"`;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.94; // Friendly, calm, steady pace
    utterance.pitch = 1.05;

    // Pick warm natural voice
    const voices = this.synth.getVoices();
    const currentLang = window.FluencyI18n ? FluencyI18n.currentLang : 'English';
    const langPrefixMap = {
      'English': 'en',
      'Hindi': 'hi',
      'Marathi': 'mr',
      'Spanish': 'es',
      'French': 'fr',
      'German': 'de'
    };
    const prefix = langPrefixMap[currentLang] || 'en';

    const matchVoice = voices.find(v => v.lang.startsWith(prefix) && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Samantha') || v.name.includes('Premium')));
    if (matchVoice) {
      utterance.voice = matchVoice;
    } else {
      const fallbackLangVoice = voices.find(v => v.lang.startsWith(prefix));
      if (fallbackLangVoice) utterance.voice = fallbackLangVoice;
    }

    utterance.onend = () => {
      this.setCallState('user-turn');
    };

    utterance.onerror = () => {
      this.setCallState('user-turn');
    };

    this.synth.speak(utterance);
  },

  replayVoice() {
    if (this.lastAiMessage) {
      this.speakText(this.lastAiMessage);
    }
  },

  async toggleUserSpeaking() {
    if (!this.isUserSpeaking) {
      // START USER SPEAKING
      if (this.synth) this.synth.cancel();
      this.isUserSpeaking = true;
      this.currentUserTranscript = '';

      const captionSpeaker = document.getElementById('convo-caption-speaker-name');
      const captionText = document.getElementById('convo-caption-text');
      if (captionSpeaker) captionSpeaker.innerText = AppState.user ? AppState.user.name.split(' ')[0] : 'You';
      if (captionText) captionText.innerText = "Listening to you...";

      this.setCallState('user-speaking');

      // Start Audio Engine Recording
      const engine = this.getAudioEngine();
      if (engine) {
        try {
          await engine.startRecording();
        } catch (e) {
          console.warn("AudioEngine start note:", e);
        }
      }

      if (this.recognition) {
        try {
          this.recognition.start();
        } catch (e) {
          console.warn("SpeechRec start note:", e);
        }
      }
    } else {
      // USER CLICKED "DONE SPEAKING"
      this.isUserSpeaking = false;
      
      // Stop Audio Engine Recording
      const engine = this.getAudioEngine();
      if (engine) {
        try {
          engine.stopRecording();
        } catch (e) {}
      }

      if (this.recognition) {
        try { this.recognition.stop(); } catch (e) {}
      }

      const spoken = this.currentUserTranscript.trim();
      if (!spoken) {
        showToast("Didn't catch any words. Try tapping Speak again.", "info");
        this.setCallState('user-turn');
        return;
      }

      this.userSpokenSegments.push(spoken);
      this.conversationHistory.push({ sender: 'user', text: spoken });
      this.currentUserTranscript = '';

      this.setCallState('thinking');

      try {
        const response = await fetch('/api/conversation/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            scenario_id: this.activeScenario ? this.activeScenario.id : 'scen_cafe',
            user_message: spoken,
            history: this.conversationHistory,
            persona: 'buddy_mascot'
          })
        });

        const data = await response.json();
        if (data.reply) {
          this.conversationHistory.push({ sender: 'ai', text: data.reply });
          this.speakText(data.reply);
        } else {
          this.setCallState('user-turn');
        }
      } catch (err) {
        console.error("Conversation AI response failed:", err);
        this.setCallState('user-turn');
      }
    }
  },

  async toggleCamera() {
    const video = document.getElementById('convo-camera-video');
    const placeholder = document.getElementById('convo-pip-placeholder');
    const camText = document.getElementById('convo-cam-btn-text');

    const t = (k, def) => (window.FluencyI18n ? FluencyI18n.t(k, def) : def);

    if (this.isCameraActive) {
      if (this.cameraStream) {
        this.cameraStream.getTracks().forEach(t => t.stop());
      }
      if (video) video.style.display = 'none';
      if (placeholder) placeholder.style.display = 'flex';
      this.isCameraActive = false;
      if (camText) camText.innerText = t('btn_cam_on', 'Camera On');
    } else {
      try {
        this.cameraStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        if (video) {
          video.srcObject = this.cameraStream;
          video.style.display = 'block';
        }
        if (placeholder) placeholder.style.display = 'none';
        this.isCameraActive = true;
        if (camText) camText.innerText = t('btn_cam_off', 'Camera Off');
      } catch (e) {
        showToast("Camera permission not granted.", "warning");
      }
    }
  },

  async endAndAnalyze() {
    if (this.userSpokenSegments.length === 0) {
      showToast("Please speak at least once during the call before viewing speech analysis.", "warning");
      return;
    }

    if (this.timerInterval) clearInterval(this.timerInterval);
    if (this.synth) this.synth.cancel();
    if (this.recognition) {
      try { this.recognition.stop(); } catch (e) {}
    }
    if (this.cameraStream) {
      this.cameraStream.getTracks().forEach(t => t.stop());
    }

    const fullTranscript = this.userSpokenSegments.join(" ");

    showToast("Analyzing your face-to-face conversation...", "info");

    try {
      const response = await fetch('/api/practice/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mode: 'conversation',
          title: `Conversation: ${this.activeScenario ? this.activeScenario.title : 'Live Practice'}`,
          duration_seconds: Math.max(this.totalDurationSeconds, 15),
          transcript: fullTranscript,
          prompt_text: this.activeScenario ? this.activeScenario.context : "1-on-1 Practice",
          audio_data_url: this.recordedAudioUrl
        })
      });

      const data = await response.json();
      if (data.feedback) {
        showFeedbackScreen(data.feedback, data.session);
      }
    } catch (err) {
      console.error("Conversation analysis error:", err);
      showToast("Error analyzing conversation session.", "error");
    }
  }
};

window.ConversationPractice = ConversationPractice;
