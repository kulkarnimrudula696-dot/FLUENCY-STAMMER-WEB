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
        transcriptDisp.innerHTML = `<strong>Live Transcript:</strong> ${finalTranscript} <span style="color:#C58B5C;">${interim}</span>`;
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

  async loadContent(cyclePassage = false) {
    if (this.isRecording && this.audioEngine) {
      this.audioEngine.stopRecording();
      this.isRecording = false;
    }

    const lengthType = document.getElementById('reading-filter-length')?.value || 'all';
    const difficulty = document.getElementById('reading-filter-diff')?.value || 'all';
    const ageGroup = (window.AppState && AppState.user && AppState.user.age_group) ? AppState.user.age_group : '18-23';
    const currentLang = window.FluencyI18n ? window.FluencyI18n.currentLang : 'English';
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
      const res = await fetch(`/api/content/reading?length_type=${encodeURIComponent(lengthType)}&difficulty=${encodeURIComponent(difficulty)}&age_group=${encodeURIComponent(ageGroup)}`);
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

    const titleEl = document.getElementById('reading-title');
    const catEl = document.getElementById('reading-category-badge');
    const wordsEl = document.getElementById('reading-word-count-badge');
    const targetWpmEl = document.getElementById('reading-target-wpm');
    const focusEl = document.getElementById('reading-focus-sound');
    const bodyEl = document.getElementById('reading-text-body');

    if (titleEl) titleEl.innerText = this.activeContent.title;
    if (catEl) catEl.innerText = this.activeContent.category || 'Reading Practice';
    if (wordsEl) wordsEl.innerText = `${this.activeContent.word_count} words`;
    if (targetWpmEl) targetWpmEl.innerText = this.activeContent.target_wpm || '115-145 WPM';
    if (focusEl) focusEl.innerText = this.activeContent.focus_sound || 'Diaphragmatic pauses & relaxed flow';

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

    const recBtn = document.getElementById('btn-reading-record-toggle');
    if (recBtn) {
      recBtn.className = 'btn btn-primary btn-lg';
      recBtn.innerHTML = `<i class="fa-solid fa-microphone"></i> Start Recording`;
    }

    const micIndicator = document.getElementById('reading-mic-indicator');
    if (micIndicator) micIndicator.classList.remove('recording');

    const submitBtn = document.getElementById('btn-reading-submit');
    if (submitBtn) submitBtn.disabled = true;

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

    const canvas = document.getElementById('reading-waveform-canvas');
    try {
      await engine.startRecording(canvas);
      this.isRecording = true;

      const recBtn = document.getElementById('btn-reading-record-toggle');
      if (recBtn) {
        recBtn.className = 'btn btn-accent btn-lg';
        recBtn.innerHTML = `<i class="fa-solid fa-stop"></i> Stop Recording`;
      }

      const micIndicator = document.getElementById('reading-mic-indicator');
      if (micIndicator) micIndicator.classList.add('recording');

      showToast("Recording started. Read aloud at a calm, comfortable pace.", "info");
    } catch (err) {
      console.error("Microphone error:", err);
      const errType = err && err.name ? err.name : 'MicrophoneError';
      const errDetails = err && err.message ? err.message : '';
      const displayMsg = errDetails ? `${errType}: ${errDetails}` : `${errType}: Failed to access microphone.`;
      showToast(displayMsg, "error");
    }
  },

  stopPractice() {
    if (!this.isRecording) return;
    const engine = this.getAudioEngine();
    if (engine) {
      engine.stopRecording();
    }
    this.isRecording = false;
    this.hasRecorded = true;

    const recBtn = document.getElementById('btn-reading-record-toggle');
    if (recBtn) {
      recBtn.className = 'btn btn-secondary btn-lg';
      recBtn.innerHTML = `<i class="fa-solid fa-rotate-left"></i> Re-record`;
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
      const finalTranscript = this.recordedTranscript.trim();

      const response = await fetch('/api/practice/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mode: 'reading',
          title: this.activeContent ? this.activeContent.title : "Reading Practice",
          duration_seconds: Math.max(this.audioEngine.elapsedSeconds, 3),
          transcript: finalTranscript,
          prompt_text: this.activeContent ? this.activeContent.text : "",
          audio_data_url: this.recordedAudioUrl
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
