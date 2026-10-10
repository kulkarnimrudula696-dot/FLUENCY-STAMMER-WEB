/**
 * FLUENCY Reading Mode Practice Engine
 * Read aloud with teleprompter, audio recording, real-time waveform,
 * audio playback review, and data-driven speech analysis.
 * Features instant Level & Length switching across all 9 combinations,
 * sequential passage cycling on "New Passage", and robust state reset.
 */

const ReadingPractice = {
  activeContent: null,
  audioEngine: null,
  isRecording: false,
  hasRecorded: false,
  recordedAudioUrl: null,
  recordedTranscript: "",
  isInitialized: false,
  contentCache: {},
  passageIndexMap: {},

  init() {
    if (!this.audioEngine) {
      this.audioEngine = new FluencyAudioEngine();
    }
    if (!this.isInitialized) {
      this.bindEvents();
      this.isInitialized = true;
    }
    this.loadContent();
  },

  cleanup() {
    if (this.isRecording && this.audioEngine) {
      this.audioEngine.stopRecording();
      this.isRecording = false;
    }
  },

  bindEvents() {
    // Length & Difficulty filter changes -> Immediate reload
    document.getElementById('reading-filter-length')?.addEventListener('change', () => this.loadContent(false));
    document.getElementById('reading-filter-diff')?.addEventListener('change', () => this.loadContent(false));

    // Switch passage button ("New Passage") -> Cycles to next passage
    document.getElementById('btn-next-reading')?.addEventListener('click', () => this.loadContent(true));

    // Custom Text Toggle
    document.getElementById('btn-custom-reading-toggle')?.addEventListener('click', () => {
      const customBox = document.getElementById('custom-reading-input-box');
      if (customBox) {
        const isHidden = customBox.style.display === 'none';
        customBox.style.display = isHidden ? 'block' : 'none';
      }
    });

    document.getElementById('btn-apply-custom-reading')?.addEventListener('click', () => {
      const customTxt = document.getElementById('custom-reading-textarea')?.value.trim();
      if (customTxt) {
        this.activeContent = {
          id: "custom_" + Date.now(),
          title: "Custom Reading Practice",
          category: "User Custom",
          word_count: customTxt.split(/\s+/).filter(Boolean).length,
          text: customTxt,
          target_wpm: "115-150 WPM",
          focus_sound: "Natural phrasing and diaphragmatic pacing"
        };
        this.renderPassage();
        const customBox = document.getElementById('custom-reading-input-box');
        if (customBox) customBox.style.display = 'none';
        showToast("Custom text loaded to teleprompter.", "success");
      }
    });

    // Record toggle button
    document.getElementById('btn-reading-record-toggle')?.addEventListener('click', () => {
      if (!this.isRecording) {
        this.startPractice();
      } else {
        this.stopPractice();
      }
    });

    // Submit for analysis button
    document.getElementById('btn-reading-submit')?.addEventListener('click', () => {
      this.submitAnalysis();
    });

    // Audio Engine callbacks
    this.audioEngine.onTranscriptUpdate = (finalTranscript, interim) => {
      this.recordedTranscript = finalTranscript;
      const transcriptDisp = document.getElementById('reading-live-transcript');
      if (transcriptDisp) {
        const curLang = this.getCurrentLanguage();
        const livePrefixes = {
          'Hindi': 'सजीव प्रतिलेख (Live):',
          'Marathi': 'थेट प्रतिलेख (Live):',
          'Spanish': 'Transcripción en vivo:',
          'French': 'Transcription en direct :',
          'German': 'Live-Transkription:',
          'Japanese': 'リアルタイム文字起こし:',
          'Chinese': '实时转录:',
          'English': 'Live Transcript:'
        };
        const prefix = livePrefixes[curLang] || 'Live Transcript:';
        transcriptDisp.innerHTML = `<strong>${prefix}</strong> ${finalTranscript} <span style="color:#C58B5C;">${interim}</span>`;
      }
    };

    this.audioEngine.onTimerTick = (seconds) => {
      const timerDisp = document.getElementById('reading-record-timer');
      if (timerDisp) {
        timerDisp.innerText = this.audioEngine.formatTime(seconds);
      }
    };

    this.audioEngine.onAudioReady = (dataUrl) => {
      this.recordedAudioUrl = dataUrl;
      const playerBox = document.getElementById('reading-audio-player-box');
      const audioEl = document.getElementById('reading-audio-playback');
      if (playerBox && audioEl) {
        audioEl.src = dataUrl;
        playerBox.style.display = 'flex';
      }
    };
  },

  getCurrentLanguage() {
    if (window.FluencyI18n && typeof window.FluencyI18n.getLanguage === 'function') {
      return window.FluencyI18n.getLanguage();
    }
    if (window.AppState && window.AppState.user && window.AppState.user.preferred_language) {
      return window.AppState.user.preferred_language;
    }
    try {
      return localStorage.getItem('fluency_app_lang') || localStorage.getItem('fluency_language') || 'English';
    } catch (e) {
      return 'English';
    }
  },

  async loadContent(cyclePassage = false) {
    if (this.isRecording && this.audioEngine) {
      this.audioEngine.stopRecording();
      this.isRecording = false;
    }

    const lengthType = document.getElementById('reading-filter-length')?.value || 'all';
    const difficulty = document.getElementById('reading-filter-diff')?.value || 'all';
    const ageGroup = (window.AppState && AppState.user && AppState.user.age_group) ? AppState.user.age_group : '18-23';
    const currentLang = this.getCurrentLanguage();

    const engine = this.getAudioEngine();
    if (engine && typeof engine.setLanguage === 'function') {
      engine.setLanguage(currentLang);
    }

    const cacheKey = `${currentLang}_${ageGroup}_${lengthType}_${difficulty}`;

    const applyPassage = (items) => {
      if (!items || items.length === 0) return;
      if (cyclePassage) {
        let curIdx = this.passageIndexMap[cacheKey] || 0;
        let nextIdx = (curIdx + 1) % items.length;
        this.passageIndexMap[cacheKey] = nextIdx;
        this.activeContent = items[nextIdx];
      } else {
        this.passageIndexMap[cacheKey] = 0;
        this.activeContent = items[0];
      }
      this.renderPassage();
    };

    if (this.contentCache[cacheKey] && this.contentCache[cacheKey].length > 0) {
      applyPassage(this.contentCache[cacheKey]);
      return;
    }

    try {
      const res = await fetch(`/api/content/reading?length_type=${encodeURIComponent(lengthType)}&difficulty=${encodeURIComponent(difficulty)}&age_group=${encodeURIComponent(ageGroup)}&language=${encodeURIComponent(currentLang)}`);
      const data = await res.json();
      if (data.items && data.items.length > 0) {
        this.contentCache[cacheKey] = data.items;
        applyPassage(data.items);
      }
    } catch (err) {
      console.error("Failed to load reading passages:", err);
    }
  },

  renderPassage() {
    if (!this.activeContent) return;

    const currentLang = this.getCurrentLanguage();

    const titleEl = document.getElementById('reading-title');
    const catEl = document.getElementById('reading-category-badge');
    const wordsEl = document.getElementById('reading-word-count-badge');
    const targetWpmEl = document.getElementById('reading-target-wpm');
    const focusEl = document.getElementById('reading-focus-sound');
    const bodyEl = document.getElementById('reading-text-body');
    const instTextEl = document.getElementById('reading-instruction-text');
    const instLabelEl = document.getElementById('reading-instruction-label');

    if (titleEl) titleEl.innerText = this.activeContent.title;
    if (catEl) catEl.innerText = this.activeContent.category || 'Reading Practice';

    // Localized word unit
    const wordLabels = {
      'Hindi': 'शब्द',
      'Marathi': 'शब्द',
      'Spanish': 'palabras',
      'French': 'mots',
      'German': 'Wörter',
      'Japanese': '文字',
      'Chinese': '字',
      'English': 'words'
    };
    const wordUnit = wordLabels[currentLang] || 'words';
    if (wordsEl) wordsEl.innerText = `${this.activeContent.word_count} ${wordUnit}`;

    if (targetWpmEl) targetWpmEl.innerText = this.activeContent.target_wpm || '115-145 WPM';
    if (focusEl) focusEl.innerText = this.activeContent.focus_sound || 'Diaphragmatic pauses & relaxed flow';

    // Localized Instruction
    const instructionLabels = {
      'Hindi': 'मार्गदर्शन / सुझाव:',
      'Marathi': 'मार्गदर्शन / सूचना:',
      'Spanish': 'Instrucción:',
      'French': 'Conseil de lecture :',
      'German': 'Lesehinweis:',
      'Japanese': 'アドバイス:',
      'Chinese': '朗读提示:',
      'English': 'Reading Instruction:'
    };
    if (instLabelEl) {
      instLabelEl.innerText = instructionLabels[currentLang] || 'Reading Instruction:';
    }
    if (instTextEl) {
      instTextEl.innerText = this.activeContent.instruction || (currentLang === 'Hindi' ? 'शांत गति से पढ़ें और प्रत्येक शब्द पर ध्यान दें।' : 'Read aloud at a calm, comfortable pace.');
    }

    // Render text with word spans
    const words = (this.activeContent.text || '').split(/\s+/).filter(Boolean);
    const wrapped = words.map((w, idx) => `<span class="word-span" id="rword-${idx}">${w}</span>`).join(' ');
    if (bodyEl) bodyEl.innerHTML = wrapped;

    // Reset recording state cleanly
    this.resetRecordingUI();
  },

  resetRecordingUI() {
    this.isRecording = false;
    this.hasRecorded = false;
    this.recordedAudioUrl = null;
    this.recordedTranscript = "";

    const startText = (window.FluencyI18n && typeof window.FluencyI18n.t === 'function') ? window.FluencyI18n.t('btn_start_recording') : 'Start Recording';
    const recBtn = document.getElementById('btn-reading-record-toggle');
    if (recBtn) {
      recBtn.className = 'btn btn-primary btn-lg';
      recBtn.innerHTML = `<i class="fa-solid fa-microphone"></i> <span>${startText}</span>`;
    }

    const micIndicator = document.getElementById('reading-mic-indicator');
    if (micIndicator) micIndicator.classList.remove('recording');

    const submitText = (window.FluencyI18n && typeof window.FluencyI18n.t === 'function') ? window.FluencyI18n.t('btn_submit_analysis') : 'Submit for Analysis';
    const submitBtn = document.getElementById('btn-reading-submit');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> <span>${submitText}</span>`;
    }

    const timerDisp = document.getElementById('reading-record-timer');
    if (timerDisp) timerDisp.innerText = "00:00";

    const playerBox = document.getElementById('reading-audio-player-box');
    if (playerBox) playerBox.style.display = 'none';

    const transcriptDisp = document.getElementById('reading-live-transcript');
    if (transcriptDisp) transcriptDisp.innerHTML = "";
  },

  getAudioEngine() {
    if (!this.audioEngine) {
      if (typeof FluencyAudioEngine !== 'undefined') {
        this.audioEngine = new FluencyAudioEngine();
      } else if (window.FluencyAudioEngine) {
        this.audioEngine = new window.FluencyAudioEngine();
      }
      if (this.audioEngine) {
        this.bindEvents();
      }
    }
    return this.audioEngine;
  },

  async startPractice() {
    const engine = this.getAudioEngine();
    if (!engine) {
      showToast("Recording engine failed to initialize. Please refresh.", "error");
      return;
    }

    const currentLang = this.getCurrentLanguage();
    if (typeof engine.setLanguage === 'function') {
      engine.setLanguage(currentLang);
    }

    const canvas = document.getElementById('reading-waveform-canvas');
    try {
      await engine.startRecording(canvas);
      this.isRecording = true;

      const stopText = (window.FluencyI18n && typeof window.FluencyI18n.t === 'function') ? (window.FluencyI18n.t('btn_stop_recording') || 'Stop Recording') : 'Stop Recording';
      const recBtn = document.getElementById('btn-reading-record-toggle');
      if (recBtn) {
        recBtn.className = 'btn btn-accent btn-lg';
        recBtn.innerHTML = `<i class="fa-solid fa-stop"></i> <span>${stopText}</span>`;
      }

      const micIndicator = document.getElementById('reading-mic-indicator');
      if (micIndicator) micIndicator.classList.add('recording');

      showToast("Recording started. Read aloud at a calm, comfortable pace.", "info");
    } catch (err) {
      console.error("Microphone error in Reading Mode:", err);
      const errMsg = (err && err.message) ? err.message : "Microphone access failed. Please check browser permissions.";
      showToast(errMsg, "error");
      this.resetRecordingUI();
    }
  },

  stopPractice() {
    if (!this.isRecording) return;
    const engine = this.getAudioEngine();
    if (engine) {
      engine.stopRecording();
      if (typeof engine.getFullTranscript === 'function') {
        const fullT = engine.getFullTranscript();
        if (fullT) {
          this.recordedTranscript = fullT;
        }
      }
    }
    this.isRecording = false;
    this.hasRecorded = true;

    const rerecordText = (window.FluencyI18n && typeof window.FluencyI18n.t === 'function') ? (window.FluencyI18n.t('btn_try_again') || 'Re-record') : 'Re-record';
    const recBtn = document.getElementById('btn-reading-record-toggle');
    if (recBtn) {
      recBtn.className = 'btn btn-secondary btn-lg';
      recBtn.innerHTML = `<i class="fa-solid fa-rotate-left"></i> <span>${rerecordText}</span>`;
    }

    const micIndicator = document.getElementById('reading-mic-indicator');
    if (micIndicator) micIndicator.classList.remove('recording');

    const submitBtn = document.getElementById('btn-reading-submit');
    if (submitBtn) submitBtn.disabled = false;

    showToast("Recording complete! You can preview audio or submit for analysis.", "success");
  },

  async submitAnalysis() {
    if (!this.hasRecorded && this.audioEngine.elapsedSeconds < 2) {
      showToast("Please record your reading before submitting.", "warning");
      return;
    }

    const submitBtn = document.getElementById('btn-reading-submit');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Speech...`;
    }

    try {
      let finalTranscript = (this.recordedTranscript || "").trim();
      if (!finalTranscript && this.audioEngine && typeof this.audioEngine.getFullTranscript === 'function') {
        finalTranscript = this.audioEngine.getFullTranscript().trim();
      }

      const response = await fetch('/api/practice/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mode: 'reading',
          title: this.activeContent ? this.activeContent.title : "Reading Practice",
          duration_seconds: Math.max(this.audioEngine.elapsedSeconds, 3),
          transcript: finalTranscript,
          prompt_text: this.activeContent ? this.activeContent.text : "",
          audio_data_url: this.recordedAudioUrl,
          language: this.getCurrentLanguage()
        })
      });

      const data = await response.json();
      if (data.feedback) {
        if (window.AppState) AppState.invalidateStatsCache();
        showFeedbackScreen(data.feedback, data.session);
      } else {
        showToast("Error processing speech feedback.", "error");
      }
    } catch (err) {
      console.error("Submission error:", err);
      showToast("Network error while analyzing speech.", "error");
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Submit for Analysis`;
      }
    }
  }
};
