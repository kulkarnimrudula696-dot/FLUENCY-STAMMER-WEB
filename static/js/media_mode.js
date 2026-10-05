/**
 * FLUENCY Image & Video Description Mode Practice Engine
 * Practice spontaneous speech, vocabulary structuring, and visual articulation.
 */

const MediaPractice = {
  currentTab: 'image', // 'image' or 'video'
  activeItem: null,
  audioEngine: null,
  isRecording: false,
  hasRecorded: false,
  recordedAudioUrl: null,
  recordedTranscript: "",

  init() {
    this.audioEngine = new FluencyAudioEngine();
    this.bindEvents();
    this.loadMediaContent();
  },

  bindEvents() {
    // Switch between Image & Video tabs
    document.getElementById('btn-tab-image')?.addEventListener('click', () => {
      this.switchTab('image');
    });
    document.getElementById('btn-tab-video')?.addEventListener('click', () => {
      this.switchTab('video');
    });

    // Next item button
    document.getElementById('btn-next-media')?.addEventListener('click', () => {
      this.loadMediaContent(true);
    });

    // Record toggle
    document.getElementById('btn-media-record-toggle')?.addEventListener('click', () => {
      if (!this.isRecording) {
        this.startPractice();
      } else {
        this.stopPractice();
      }
    });

    // Submit for analysis
    document.getElementById('btn-media-submit')?.addEventListener('click', () => {
      this.submitAnalysis();
    });

    // Audio Engine callbacks
    this.audioEngine.onTranscriptUpdate = (finalTranscript, interim) => {
      this.recordedTranscript = finalTranscript;
      const transcriptDisp = document.getElementById('media-live-transcript');
      if (transcriptDisp) {
        transcriptDisp.innerHTML = `<strong>Live Transcript:</strong> ${finalTranscript} <span style="color:#D9A6A0;">${interim}</span>`;
      }
    };

    this.audioEngine.onTimerTick = (seconds) => {
      const timerDisp = document.getElementById('media-record-timer');
      if (timerDisp) {
        timerDisp.innerText = this.audioEngine.formatTime(seconds);
      }
    };

    this.audioEngine.onAudioReady = (dataUrl) => {
      this.recordedAudioUrl = dataUrl;
      const playerBox = document.getElementById('media-audio-player-box');
      const audioEl = document.getElementById('media-audio-playback');
      if (playerBox && audioEl) {
        audioEl.src = dataUrl;
        playerBox.style.display = 'flex';
      }
    };
  },

  switchTab(tab) {
    this.currentTab = tab;
    document.getElementById('btn-tab-image').classList.toggle('active', tab === 'image');
    document.getElementById('btn-tab-video').classList.toggle('active', tab === 'video');
    this.loadMediaContent();
  },

  async loadMediaContent(randomize = false) {
    const age = AppState.user ? AppState.user.practice_age : 21;
    const url = this.currentTab === 'image' 
      ? `/api/content/images?age=${age}` 
      : `/api/content/videos?type=all`;

    try {
      const res = await fetch(url);
      const data = await res.json();
      if (data.items && data.items.length > 0) {
        const idx = randomize ? Math.floor(Math.random() * data.items.length) : 0;
        this.activeItem = data.items[idx];
        this.renderMediaDisplay();
      }
    } catch (err) {
      console.error("Error loading media items:", err);
    }
  },

  renderMediaDisplay() {
    if (!this.activeItem) return;

    document.getElementById('media-item-title').innerText = this.activeItem.title;
    document.getElementById('media-category-badge').innerText = this.activeItem.category || 'Visual Observation';

    const viewerFrame = document.getElementById('media-viewer-frame');
    if (this.currentTab === 'image') {
      viewerFrame.innerHTML = `<img src="${this.activeItem.image_url}" alt="${this.activeItem.title}" style="max-height: 100%; border-radius: var(--radius-lg);" />`;
    } else {
      viewerFrame.innerHTML = `
        <video controls autoplay muted loop style="max-height: 100%; width: 100%; border-radius: var(--radius-lg);">
          <source src="${this.activeItem.video_src}" type="video/mp4">
          Your browser does not support the video tag.
        </video>
      `;
    }

    document.getElementById('media-prompt-text').innerText = this.activeItem.description_prompt;

    // Guiding questions
    const qList = document.getElementById('media-guiding-questions');
    if (qList && this.activeItem.guiding_questions) {
      qList.innerHTML = this.activeItem.guiding_questions.map(q => `<li><i class="fa-solid fa-circle-question" style="color:#7A4E4A;"></i> ${q}</li>`).join('');
    }

    // Suggested vocabulary keywords
    const kwCloud = document.getElementById('media-keywords-cloud');
    if (kwCloud && this.activeItem.suggested_keywords) {
      kwCloud.innerHTML = this.activeItem.suggested_keywords.map(kw => `<span class="keyword-chip">${kw}</span>`).join('');
    }

    this.resetRecordingUI();
  },

  resetRecordingUI() {
    this.isRecording = false;
    this.hasRecorded = false;
    this.recordedAudioUrl = null;
    this.recordedTranscript = "";

    const recBtn = document.getElementById('btn-media-record-toggle');
    if (recBtn) {
      recBtn.className = 'btn btn-primary btn-lg';
      recBtn.innerHTML = `<i class="fa-solid fa-microphone"></i> Start Explaining`;
    }

    const micIndicator = document.getElementById('media-mic-indicator');
    if (micIndicator) micIndicator.classList.remove('recording');

    const submitBtn = document.getElementById('btn-media-submit');
    if (submitBtn) submitBtn.disabled = true;

    const timerDisp = document.getElementById('media-record-timer');
    if (timerDisp) timerDisp.innerText = "00:00";

    const playerBox = document.getElementById('media-audio-player-box');
    if (playerBox) playerBox.style.display = 'none';

    const transcriptDisp = document.getElementById('media-live-transcript');
    if (transcriptDisp) transcriptDisp.innerHTML = "";
  },

  async startPractice() {
    const canvas = document.getElementById('media-waveform-canvas');
    try {
      await this.audioEngine.startRecording(canvas);
      this.isRecording = true;

      const recBtn = document.getElementById('btn-media-record-toggle');
      recBtn.className = 'btn btn-accent btn-lg';
      recBtn.innerHTML = `<i class="fa-solid fa-stop"></i> Stop Explaining`;

      const micIndicator = document.getElementById('media-mic-indicator');
      if (micIndicator) micIndicator.classList.add('recording');

      showToast("Recording started. Describe what you observe with relaxed phrasing.", "info");
    } catch (err) {
      showToast(err.message, "error");
    }
  },

  stopPractice() {
    if (!this.isRecording) return;
    this.audioEngine.stopRecording();
    this.isRecording = false;
    this.hasRecorded = true;

    const recBtn = document.getElementById('btn-media-record-toggle');
    recBtn.className = 'btn btn-secondary btn-lg';
    recBtn.innerHTML = `<i class="fa-solid fa-rotate-left"></i> Re-record`;

    const micIndicator = document.getElementById('media-mic-indicator');
    if (micIndicator) micIndicator.classList.remove('recording');

    const submitBtn = document.getElementById('btn-media-submit');
    if (submitBtn) submitBtn.disabled = false;

    showToast("Recorded! Submit to receive speech fluency feedback.", "success");
  },

  async submitAnalysis() {
    const submitBtn = document.getElementById('btn-media-submit');
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Speech...`;

    try {
      const finalTranscript = this.recordedTranscript.trim() || "Observed and described the scene in detail.";

      const response = await fetch('/api/practice/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mode: 'media',
          title: `Describe: ${this.activeItem.title}`,
          duration_seconds: Math.max(this.audioEngine.elapsedSeconds, 3),
          transcript: finalTranscript,
          prompt_text: this.activeItem.description_prompt,
          audio_data_url: this.recordedAudioUrl
        })
      });

      const data = await response.json();
      if (data.feedback) {
        showFeedbackScreen(data.feedback, data.session);
      } else {
        showToast("Error processing feedback.", "error");
      }
    } catch (err) {
      console.error("Media analysis error:", err);
      showToast("Network error while analyzing speech.", "error");
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Submit for Analysis`;
    }
  }
};
