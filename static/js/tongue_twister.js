/**
 * FLUENCY Tongue Twister Practice Engine
 * Focused speech motor agility, phoneme coordination, and strict sequence-aligned word matching.
 * Built following the proven Reading Mode architecture with:
 * - Curated 30+ tongue twisters across Easy, Medium, and Hard difficulty
 * - Sequential cycling on "Next Tongue Twister" without immediate repeats
 * - Audio recording with FluencyAudioEngine and real-time waveform visualizer
 * - Live transcript capture via Web Speech API
 * - Audio playback preview & Try-Again reset
 * - Sequence-aligned speech comparison and deep AI speech analysis
 */

const TongueTwisterPractice = {
  items: [],
  filteredItems: [],
  currentIndex: 0,
  activeItem: null,
  currentDifficulty: 'all',
  contentCache: {},
  twisterIndexMap: {},
  audioEngine: null,
  isRecording: false,
  hasRecorded: false,
  recordedAudioUrl: null,
  recordedTranscript: "",
  isInitialized: false,

  init() {
    this.getAudioEngine();
    if (!this.isInitialized) {
      this.bindEvents();
      this.isInitialized = true;
    }
    this.loadContent(false);
  },

  cleanup() {
    if (this.isRecording && this.audioEngine) {
      this.audioEngine.stopRecording();
      this.isRecording = false;
    }
  },

  getAudioEngine() {
    if (!this.audioEngine) {
      if (typeof FluencyAudioEngine !== 'undefined') {
        this.audioEngine = new FluencyAudioEngine();
      } else if (window.FluencyAudioEngine) {
        this.audioEngine = new window.FluencyAudioEngine();
      }
      if (this.audioEngine) {
        this.bindAudioEngineCallbacks();
      }
    }
    return this.audioEngine;
  },

  bindAudioEngineCallbacks() {
    if (!this.audioEngine) return;

    this.audioEngine.onTranscriptUpdate = (finalTranscript, interim) => {
      this.recordedTranscript = finalTranscript;
      const transcriptDisp = document.getElementById('twister-live-transcript');
      if (transcriptDisp) {
        if (finalTranscript || interim) {
          transcriptDisp.innerHTML = `<strong>Live Transcript:</strong> "${finalTranscript} <span style="color:#D35400;">${interim}</span>"`;
        } else {
          transcriptDisp.innerHTML = "";
        }
      }
    };

    this.audioEngine.onTimerTick = (seconds) => {
      const timerDisp = document.getElementById('twister-record-timer');
      if (timerDisp) {
        timerDisp.innerText = this.audioEngine.formatTime(seconds);
      }
    };

    this.audioEngine.onAudioReady = (dataUrl) => {
      this.recordedAudioUrl = dataUrl;
      const playerBox = document.getElementById('twister-audio-player-box');
      const audioEl = document.getElementById('twister-audio-playback');
      if (playerBox && audioEl) {
        audioEl.src = dataUrl;
        playerBox.style.display = 'flex';
      }
    };
  },

  bindEvents() {
    // Next Tongue Twister button (matches Reading Mode's btn-next-reading)
    document.getElementById('btn-next-twister')?.addEventListener('click', () => this.loadContent(true));
    document.getElementById('btn-twister-next')?.addEventListener('click', () => this.loadContent(true));

    // Previous & Random buttons
    document.getElementById('btn-twister-prev')?.addEventListener('click', () => this.prevItem());
    document.getElementById('btn-twister-random')?.addEventListener('click', () => this.randomItem());

    // Record toggle button
    document.getElementById('btn-twister-record-toggle')?.addEventListener('click', () => {
      if (!this.isRecording) {
        this.startPractice();
      } else {
        this.stopPractice();
      }
    });

    // Submit for analysis button
    document.getElementById('btn-twister-submit')?.addEventListener('click', () => {
      this.submitAnalysis();
    });

    // Try Again button (resets current attempt)
    document.getElementById('btn-twister-try-again')?.addEventListener('click', () => {
      this.resetRecordingUI();
      showToast("Ready for a fresh attempt! Click Start Recording when you're ready.", "info");
    });
  },

  async loadContent(cycleTwister = false) {
    if (this.isRecording && this.audioEngine) {
      this.audioEngine.stopRecording();
      this.isRecording = false;
    }

    const diff = this.currentDifficulty || 'all';
    const cacheKey = `twister_${diff}`;

    const applyItem = (items) => {
      if (!items || items.length === 0) return;
      this.filteredItems = items;

      if (cycleTwister) {
        let curIdx = this.twisterIndexMap[cacheKey] || 0;
        let nextIdx = (curIdx + 1) % items.length;
        this.twisterIndexMap[cacheKey] = nextIdx;
        this.currentIndex = nextIdx;
      } else {
        if (this.twisterIndexMap[cacheKey] !== undefined && this.twisterIndexMap[cacheKey] < items.length) {
          this.currentIndex = this.twisterIndexMap[cacheKey];
        } else {
          this.twisterIndexMap[cacheKey] = 0;
          this.currentIndex = 0;
        }
      }

      this.renderCurrentItem();
    };

    if (this.contentCache[cacheKey] && this.contentCache[cacheKey].length > 0) {
      applyItem(this.contentCache[cacheKey]);
      return;
    }

    try {
      const res = await fetch(`/api/content/tongue-twisters?difficulty=${encodeURIComponent(diff)}`);
      const data = await res.json();
      const items = data.items || [];
      if (items.length > 0) {
        this.contentCache[cacheKey] = items;
        applyItem(items);
      } else {
        showToast("No tongue twisters found for this difficulty.", "warning");
      }
    } catch (err) {
      console.error("Failed to load tongue twisters:", err);
      showToast("Unable to load tongue twisters. Please check network connection.", "error");
    }
  },

  setDifficulty(diff) {
    this.currentDifficulty = diff;
    
    // Update active tab styles
    document.querySelectorAll('.twister-diff-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.diff === diff);
    });

    this.loadContent(false);
  },

  renderCurrentItem() {
    this.resetRecordingUI();

    if (!this.filteredItems || this.filteredItems.length === 0) {
      return;
    }

    if (this.currentIndex < 0) this.currentIndex = 0;
    if (this.currentIndex >= this.filteredItems.length) this.currentIndex = 0;

    const item = this.filteredItems[this.currentIndex];
    this.activeItem = item;

    // Badge Difficulty Styling
    const diffBadge = document.getElementById('twister-item-diff-tag');
    if (diffBadge) {
      const diffCapitalized = (item.difficulty || 'easy').toUpperCase();
      diffBadge.innerText = diffCapitalized;
      if (item.difficulty === 'easy') {
        diffBadge.style.background = "#EAF5EE";
        diffBadge.style.color = "#2E7D32";
        diffBadge.style.borderColor = "#C8E6C9";
      } else if (item.difficulty === 'medium') {
        diffBadge.style.background = "#FFF9E6";
        diffBadge.style.color = "#9A633F";
        diffBadge.style.borderColor = "#FFE082";
      } else {
        diffBadge.style.background = "#F3E8FF";
        diffBadge.style.color = "#7C3AED";
        diffBadge.style.borderColor = "#DDD6FE";
      }
    }

    // Item Metadata
    const titleEl = document.getElementById('twister-item-title');
    if (titleEl) titleEl.innerText = item.title || "Tongue Twister";

    const soundBadge = document.getElementById('twister-item-sound-tag');
    if (soundBadge) soundBadge.innerText = `🎯 Focus: ${item.focus_sound || 'Agile Articulation'}`;

    const repsTag = document.getElementById('twister-item-reps-tag');
    if (repsTag) repsTag.innerText = `🔁 Target: ${item.target_reps || '2-3 Reps'}`;

    const countTag = document.getElementById('twister-item-count-badge');
    const wordCount = item.word_count || (item.text || '').split(/\s+/).filter(Boolean).length;
    if (countTag) countTag.innerText = `${wordCount} words`;

    // Wrap words in individual spans for crisp teleprompter layout
    const prompterText = document.getElementById('twister-text-body');
    if (prompterText) {
      const words = (item.text || '').split(/\s+/).filter(Boolean);
      const wrapped = words.map((w, idx) => `<span class="word-span" id="tword-${idx}">${w}</span>`).join(' ');
      prompterText.innerHTML = `“${wrapped}”`;
    }

    const tipBox = document.getElementById('twister-item-tip');
    if (tipBox) {
      tipBox.innerHTML = `<strong>💡 Articulation Tip:</strong> ${item.tip || 'Start slowly, glide smoothly across consonants, and keep breath steady.'}`;
    }

    const indexBadge = document.getElementById('twister-counter-badge');
    if (indexBadge) {
      indexBadge.innerText = `Twister ${this.currentIndex + 1} of ${this.filteredItems.length}`;
    }
  },

  prevItem() {
    if (!this.filteredItems || this.filteredItems.length === 0) return;
    const cacheKey = `twister_${this.currentDifficulty || 'all'}`;
    this.currentIndex = (this.currentIndex - 1 + this.filteredItems.length) % this.filteredItems.length;
    this.twisterIndexMap[cacheKey] = this.currentIndex;
    this.renderCurrentItem();
  },

  randomItem() {
    if (!this.filteredItems || this.filteredItems.length <= 1) return;
    const cacheKey = `twister_${this.currentDifficulty || 'all'}`;
    let newIndex = this.currentIndex;
    while (newIndex === this.currentIndex) {
      newIndex = Math.floor(Math.random() * this.filteredItems.length);
    }
    this.currentIndex = newIndex;
    this.twisterIndexMap[cacheKey] = this.currentIndex;
    this.renderCurrentItem();
  },

  resetRecordingUI() {
    if (this.isRecording && this.audioEngine) {
      this.audioEngine.stopRecording();
    }
    this.isRecording = false;
    this.hasRecorded = false;
    this.recordedAudioUrl = null;
    this.recordedTranscript = "";

    const timerDisp = document.getElementById('twister-record-timer');
    if (timerDisp) timerDisp.innerText = "00:00";

    const transcriptDisp = document.getElementById('twister-live-transcript');
    if (transcriptDisp) transcriptDisp.innerHTML = "";

    const micIndicator = document.getElementById('twister-mic-indicator');
    if (micIndicator) micIndicator.classList.remove('recording');

    const recBtn = document.getElementById('btn-twister-record-toggle');
    if (recBtn) {
      recBtn.className = 'btn btn-primary btn-lg';
      recBtn.style.background = '#E65100';
      recBtn.style.borderColor = '#BF360C';
      recBtn.innerHTML = `<i class="fa-solid fa-microphone"></i> <span>Start Recording</span>`;
    }

    const submitBtn = document.getElementById('btn-twister-submit');
    if (submitBtn) submitBtn.disabled = true;

    const tryAgainBtn = document.getElementById('btn-twister-try-again');
    if (tryAgainBtn) tryAgainBtn.style.display = 'none';

    const playerBox = document.getElementById('twister-audio-player-box');
    if (playerBox) playerBox.style.display = 'none';

    const audioEl = document.getElementById('twister-audio-playback');
    if (audioEl) audioEl.src = "";
  },

  async startPractice() {
    this.resetRecordingUI();
    const engine = this.getAudioEngine();
    if (!engine) {
      showToast("Recording engine failed to initialize. Please refresh the page.", "error");
      return;
    }

    const canvas = document.getElementById('twister-waveform-canvas');
    try {
      await engine.startRecording(canvas);
      this.isRecording = true;
      this.hasRecorded = false;

      const recBtn = document.getElementById('btn-twister-record-toggle');
      if (recBtn) {
        recBtn.className = 'btn btn-accent btn-lg';
        recBtn.style.background = '#D32F2F';
        recBtn.style.borderColor = '#B71C1C';
        recBtn.innerHTML = `<i class="fa-solid fa-stop"></i> <span>Stop Recording</span>`;
      }

      const micIndicator = document.getElementById('twister-mic-indicator');
      if (micIndicator) micIndicator.classList.add('recording');

      showToast("Recording started! Read the tongue twister clearly aloud.", "info");
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

    const recBtn = document.getElementById('btn-twister-record-toggle');
    if (recBtn) {
      recBtn.className = 'btn btn-secondary btn-lg';
      recBtn.style.background = '';
      recBtn.style.borderColor = '';
      recBtn.innerHTML = `<i class="fa-solid fa-rotate-left"></i> <span>Re-record</span>`;
    }

    const micIndicator = document.getElementById('twister-mic-indicator');
    if (micIndicator) micIndicator.classList.remove('recording');

    const submitBtn = document.getElementById('btn-twister-submit');
    if (submitBtn) submitBtn.disabled = false;

    const tryAgainBtn = document.getElementById('btn-twister-try-again');
    if (tryAgainBtn) tryAgainBtn.style.display = 'inline-flex';

    showToast("Recording captured! Preview your audio or click Submit for Speech Analysis.", "success");
  },

  async submitAnalysis() {
    if (!this.hasRecorded && (!this.audioEngine || this.audioEngine.elapsedSeconds < 2)) {
      showToast("Please record the tongue twister before submitting.", "warning");
      return;
    }

    const submitBtn = document.getElementById('btn-twister-submit');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Speech...`;
    }

    try {
      const finalTranscript = (this.recordedTranscript || "").trim();
      const promptText = this.activeItem ? this.activeItem.text : "";
      const durationSecs = this.audioEngine ? Math.max(this.audioEngine.elapsedSeconds, 2) : 3;

      const response = await fetch('/api/practice/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mode: 'twister',
          title: this.activeItem ? this.activeItem.title : "Tongue Twister Practice",
          duration_seconds: durationSecs,
          transcript: finalTranscript,
          prompt_text: promptText,
          audio_data_url: this.recordedAudioUrl
        })
      });

      const data = await response.json();
      if (data.feedback) {
        if (window.AppState) AppState.invalidateStatsCache();
        showFeedbackScreen(data.feedback, data.session);
      } else {
        showToast("Error processing tongue twister feedback.", "error");
      }
    } catch (err) {
      console.error("Submission error:", err);
      showToast("Network error while analyzing tongue twister.", "error");
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> <span>Submit for Analysis</span>`;
      }
    }
  }
};

window.TongueTwisterPractice = TongueTwisterPractice;
