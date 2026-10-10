/**
 * FLUENCY Audio Recorder & Real-Time Speech Recognition Engine
 * Integrates:
 * - Safe microphone acquisition with modern navigator.mediaDevices + legacy getUserMedia fallbacks
 * - MediaRecorder for client-side audio recording and data URL encoding
 * - AudioContext + AnalyserNode for live canvas audio waveform visualization
 * - Web Speech API (SpeechRecognition) for live speech-to-text
 */

class FluencyAudioEngine {
  constructor() {
    this.mediaRecorder = null;
    this.audioChunks = [];
    this.audioBlob = null;
    this.audioDataUrl = null;
    this.stream = null;
    
    // Audio Context & Analyzer
    this.audioCtx = null;
    this.analyser = null;
    this.animFrameId = null;
    
    // Speech Recognition
    this.recognition = null;
    this.transcript = "";
    this.interimTranscript = "";
    this.isRecognizing = false;
    
    // Timer
    this.startTime = 0;
    this.elapsedSeconds = 0;
    this.timerInterval = null;
    
    // Callbacks
    this.onTranscriptUpdate = null;
    this.onTimerTick = null;
    this.onAudioReady = null;

    this.currentLanguage = null;
    this.initSpeechRecognition();
  }

  static isSupported() {
    return !!(
      (navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === 'function') ||
      navigator.getUserMedia ||
      navigator.webkitGetUserMedia ||
      navigator.mozGetUserMedia ||
      navigator.msGetUserMedia
    );
  }

  normalizeMediaError(err) {
    if (!err) return new Error("Unknown microphone error occurred.");
    const name = err.name || "";
    if (name === "NotAllowedError" || name === "PermissionDeniedError") {
      const e = new Error("Microphone permission was denied. Please allow microphone access in your browser settings.");
      e.name = "NotAllowedError";
      return e;
    }
    if (name === "NotFoundError" || name === "DevicesNotFoundError") {
      const e = new Error("No microphone device was detected. Please plug in or enable a microphone.");
      e.name = "NotFoundError";
      return e;
    }
    if (name === "NotReadableError" || name === "TrackStartError") {
      const e = new Error("Microphone is currently occupied or in use by another application.");
      e.name = "NotReadableError";
      return e;
    }
    if (name === "OverconstrainedError" || name === "ConstraintNotSatisfiedError") {
      const e = new Error("Microphone does not satisfy the requested audio constraints.");
      e.name = "OverconstrainedError";
      return e;
    }
    if (name === "SecurityError") {
      const e = new Error("Microphone access blocked due to security restrictions. Please use localhost or HTTPS.");
      e.name = "SecurityError";
      return e;
    }
    return err;
  }

  async requestUserAudioStream() {
    // 1. Standard modern API: navigator.mediaDevices.getUserMedia
    if (navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === 'function') {
      try {
        return await navigator.mediaDevices.getUserMedia({ audio: true });
      } catch (err) {
        throw this.normalizeMediaError(err);
      }
    }

    // 2. Legacy getUserMedia fallbacks
    const legacyGUM = navigator.getUserMedia ||
      navigator.webkitGetUserMedia ||
      navigator.mozGetUserMedia ||
      navigator.msGetUserMedia;

    if (legacyGUM) {
      return new Promise((resolve, reject) => {
        legacyGUM.call(
          navigator,
          { audio: true },
          (stream) => resolve(stream),
          (err) => reject(this.normalizeMediaError(err))
        );
      });
    }

    // 3. Informative error if running in an insecure non-localhost context
    const isLocal = location.hostname === 'localhost' ||
      location.hostname === '127.0.0.1' ||
      location.hostname === '[::1]' ||
      location.protocol === 'https:';

    if (!isLocal && !window.isSecureContext) {
      const err = new Error("Microphone access requires a secure connection (HTTPS) or local server (http://localhost:5000 / http://127.0.0.1:5000). Please open the application via localhost or HTTPS.");
      err.name = "SecurityError";
      throw err;
    }

    // 4. Fallback for completely unsupported browser environment
    const err = new Error("Microphone recording (getUserMedia) is not available in this browser. Please use Chrome, Edge, Firefox, or Safari.");
    err.name = "NotSupportedError";
    throw err;
  }

  getRecognitionLanguage() {
    let lang = this.currentLanguage;
    if (!lang && window.FluencyI18n && typeof window.FluencyI18n.getLanguage === 'function') {
      lang = window.FluencyI18n.getLanguage();
    }
    if (!lang && window.AppState && window.AppState.user && window.AppState.user.preferred_language) {
      lang = window.AppState.user.preferred_language;
    }
    if (!lang) {
      try {
        lang = localStorage.getItem('fluency_app_lang') || localStorage.getItem('fluency_language');
      } catch (e) {}
    }

    const map = {
      'Hindi': 'hi-IN',
      'Marathi': 'mr-IN',
      'Spanish': 'es-ES',
      'French': 'fr-FR',
      'German': 'de-DE',
      'Japanese': 'ja-JP',
      'Chinese': 'zh-CN',
      'English': 'en-US'
    };

    return map[lang] || 'en-US';
  }

  setLanguage(langName) {
    this.currentLanguage = langName;
    if (this.recognition) {
      this.recognition.lang = this.getRecognitionLanguage();
    }
  }

  getFullTranscript() {
    const finalPart = (this.transcript || "").trim();
    const interimPart = (this.interimTranscript || "").trim();
    if (finalPart && interimPart) {
      return `${finalPart} ${interimPart}`;
    }
    return finalPart || interimPart || "";
  }

  initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = true;
      this.recognition.interimResults = true;
      this.recognition.lang = this.getRecognitionLanguage();

      this.recognition.onresult = (event) => {
        let interim = '';
        let final = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            final += event.results[i][0].transcript + ' ';
          } else {
            interim += event.results[i][0].transcript;
          }
        }

        if (final) {
          this.transcript += final;
        }
        this.interimTranscript = interim;

        const full = this.getFullTranscript();
        if (this.onTranscriptUpdate) {
          this.onTranscriptUpdate(full, interim.trim(), this.transcript.trim());
        }
      };

      this.recognition.onerror = (event) => {
        console.warn('Speech recognition status/error:', event.error);
      };

      this.recognition.onend = () => {
        if (this.isRecognizing) {
          try {
            this.recognition.lang = this.getRecognitionLanguage();
            this.recognition.start();
          } catch (e) {}
        }
      };
    } else {
      console.log('Web Speech API not supported natively in this browser; fallback mode active.');
    }
  }

  async startRecording(canvasElement = null) {
    this.audioChunks = [];
    this.transcript = "";
    this.interimTranscript = "";
    this.elapsedSeconds = 0;

    // Check if we already have an active, usable audio track
    const hasLiveStream = this.stream && this.stream.active && this.stream.getAudioTracks().some(t => t.readyState === 'live');

    if (hasLiveStream) {
      // Re-enable existing tracks if they were muted/disabled
      this.stream.getAudioTracks().forEach(track => {
        track.enabled = true;
      });
      console.log("Reusing existing granted microphone stream:", this.stream);
    } else {
      console.log("Requesting microphone stream...");
      try {
        const stream = await this.requestUserAudioStream();
        this.stream = stream;
        console.log("Microphone stream received successfully:", stream);
      } catch (error) {
        console.error("Microphone initialization error:", error);
        throw error;
      }
    }

    // Set up MediaRecorder if stream exists
    if (this.stream && typeof MediaRecorder !== 'undefined') {
      try {
        let options = {};
        if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
          options = { mimeType: 'audio/webm;codecs=opus' };
        } else if (MediaRecorder.isTypeSupported('audio/webm')) {
          options = { mimeType: 'audio/webm' };
        } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
          options = { mimeType: 'audio/mp4' };
        }
        this.mediaRecorder = new MediaRecorder(this.stream, options);
      } catch (mrErr) {
        try {
          this.mediaRecorder = new MediaRecorder(this.stream);
        } catch (e) {
          console.warn("MediaRecorder fallback note:", e);
        }
      }

      if (this.mediaRecorder) {
        this.mediaRecorder.ondataavailable = (e) => {
          if (e.data && e.data.size > 0) {
            this.audioChunks.push(e.data);
          }
        };

        this.mediaRecorder.onstop = async () => {
          const mimeType = (this.mediaRecorder && this.mediaRecorder.mimeType) || 'audio/webm';
          this.audioBlob = new Blob(this.audioChunks, { type: mimeType });
          // Convert to Base64 data URL for persistence and playback
          const reader = new FileReader();
          reader.readAsDataURL(this.audioBlob);
          reader.onloadend = () => {
            this.audioDataUrl = reader.result;
            if (this.onAudioReady) {
              this.onAudioReady(this.audioDataUrl, this.audioBlob);
            }
          };
        };

        try {
          this.mediaRecorder.start(250); // Slice chunks every 250ms
        } catch (mStartErr) {
          console.warn("MediaRecorder start note:", mStartErr);
        }
      }
    }

    // Start Speech Recognition (non-blocking)
    if (this.recognition) {
      try {
        this.recognition.abort();
      } catch (e) {}
      try {
        this.recognition.lang = this.getRecognitionLanguage();
        this.isRecognizing = true;
        this.recognition.start();
      } catch (e) {
        console.warn("Speech recognition start note:", e);
      }
    }

    // Start Real-Time Waveform Visualizer (non-blocking)
    if (canvasElement && this.stream) {
      try {
        this.startWaveformVisualizer(canvasElement);
      } catch (vizErr) {
        console.warn("Waveform visualizer note:", vizErr);
      }
    }

    // Start Timer
    this.startTime = Date.now();
    if (this.timerInterval) clearInterval(this.timerInterval);
    this.timerInterval = setInterval(() => {
      this.elapsedSeconds = Math.floor((Date.now() - this.startTime) / 1000);
      if (this.onTimerTick) {
        this.onTimerTick(this.elapsedSeconds);
      }
    }, 1000);
  }

  stopRecording() {
    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      try {
        this.mediaRecorder.stop();
      } catch (e) {}
    }

    // Keep stream active for instant reuse on subsequent recordings without prompting again
    if (this.stream) {
      this.stream.getAudioTracks().forEach(track => {
        track.enabled = false;
      });
    }

    this.isRecognizing = false;
    if (this.recognition) {
      try {
        this.recognition.stop();
      } catch (e) {}
    }

    // Commit any in-flight interim transcript so words spoken right before stopping are preserved
    if (this.interimTranscript && this.interimTranscript.trim()) {
      const interim = this.interimTranscript.trim();
      const current = (this.transcript || "").trim();
      if (!current.endsWith(interim)) {
        this.transcript = (current ? current + ' ' + interim : interim).trim();
      }
      this.interimTranscript = '';
    }

    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }

    if (this.animFrameId) {
      cancelAnimationFrame(this.animFrameId);
      this.animFrameId = null;
    }

    if (this.audioCtx && this.audioCtx.state !== 'closed') {
      try {
        this.audioCtx.close();
      } catch (e) {}
    }
  }

  releaseMicrophone() {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }
  }

  startWaveformVisualizer(canvas) {
    if (!canvas || !this.stream) return;

    if (this.animFrameId) {
      cancelAnimationFrame(this.animFrameId);
      this.animFrameId = null;
    }
    if (this.audioCtx && this.audioCtx.state !== 'closed') {
      try { this.audioCtx.close(); } catch (e) {}
    }

    try {
      const AudioCtxClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtxClass) return;

      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      this.audioCtx = new AudioCtxClass();
      if (this.audioCtx.state === 'suspended') {
        this.audioCtx.resume();
      }
      this.analyser = this.audioCtx.createAnalyser();
      this.analyser.fftSize = 256;

      const source = this.audioCtx.createMediaStreamSource(this.stream);
      source.connect(this.analyser);

      const bufferLength = this.analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const draw = () => {
        this.animFrameId = requestAnimationFrame(draw);
        this.analyser.getByteFrequencyData(dataArray);

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#FAF4EB';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const barWidth = (canvas.width / bufferLength) * 2.2;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
          const barHeight = (dataArray[i] / 255) * (canvas.height - 10);

          // Warm otter gradient for bars
          const grad = ctx.createLinearGradient(0, canvas.height, 0, 0);
          grad.addColorStop(0, '#9A633F');
          grad.addColorStop(1, '#FFC83D');

          ctx.fillStyle = grad;
          ctx.beginPath();
          ctx.roundRect(x, canvas.height - barHeight, barWidth - 2, barHeight, [4, 4, 0, 0]);
          ctx.fill();

          x += barWidth;
        }
      };

      draw();
    } catch (vizErr) {
      console.warn("Waveform visualizer note:", vizErr);
    }
  }

  formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  getRecordingStats() {
    const full = this.getFullTranscript();
    const words = (full.match(/\S+/g) || []).length;
    return {
      duration_seconds: Math.max(1, this.elapsedSeconds),
      words_spoken: words,
      transcript: full
    };
  }
}

// Window exposure and global attachment
window.FluencyAudioEngine = FluencyAudioEngine;
if (typeof globalThis !== 'undefined') {
  globalThis.FluencyAudioEngine = FluencyAudioEngine;
}
