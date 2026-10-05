/**
 * FLUENCY Audio Recorder & Real-Time Speech Recognition Engine
 * Integrates:
 * - MediaRecorder for client-side audio recording
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

    this.initSpeechRecognition();
  }

  initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = true;
      this.recognition.interimResults = true;
      this.recognition.lang = 'en-US';

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

        if (this.onTranscriptUpdate) {
          this.onTranscriptUpdate(this.transcript.trim(), interim.trim());
        }
      };

      this.recognition.onerror = (event) => {
        console.warn('Speech recognition status/error:', event.error);
      };

      this.recognition.onend = () => {
        if (this.isRecognizing) {
          try {
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
      console.log("Start Recording clicked");
      console.log("mediaDevices:", navigator.mediaDevices);
      console.log("isSecureContext:", window.isSecureContext);
      console.log("Requesting microphone...");

      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.stream = stream;
        console.log("Microphone stream received:", stream);
      } catch (error) {
        console.error("Microphone error:", error);
        throw error;
      }
    }

    // Set up MediaRecorder
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
      this.mediaRecorder = new MediaRecorder(this.stream);
    }

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

    this.mediaRecorder.start(250); // Slice chunks every 250ms

    // Start Speech Recognition (non-blocking)
    if (this.recognition) {
      try {
        this.isRecognizing = true;
        this.recognition.start();
      } catch (e) {
        console.warn("Speech recognition status:", e);
      }
    }

    // Start Real-Time Waveform Visualizer (non-blocking)
    if (canvasElement) {
      try {
        this.startWaveformVisualizer(canvasElement);
      } catch (vizErr) {
        console.warn("Waveform visualizer status:", vizErr);
      }
    }

    // Start Timer
    this.startTime = Date.now();
    this.timerInterval = setInterval(() => {
      this.elapsedSeconds = Math.floor((Date.now() - this.startTime) / 1000);
      if (this.onTimerTick) {
        this.onTimerTick(this.elapsedSeconds);
      }
    }, 1000);
  }

  stopRecording() {
    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      this.mediaRecorder.stop();
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

    if (this.timerInterval) {
      clearInterval(this.timerInterval);
    }

    if (this.animFrameId) {
      cancelAnimationFrame(this.animFrameId);
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
    if (this.animFrameId) {
      cancelAnimationFrame(this.animFrameId);
    }
    if (this.audioCtx && this.audioCtx.state !== 'closed') {
      try { this.audioCtx.close(); } catch (e) {}
    }

    const ctx = canvas.getContext('2d');
    this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
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
  }

  formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  getRecordingStats() {
    const words = (this.transcript.trim().match(/\S+/g) || []).length;
    return {
      duration_seconds: Math.max(1, this.elapsedSeconds),
      words_spoken: words,
      transcript: this.transcript.trim()
    };
  }
}

// Window exposure and global attachment
window.FluencyAudioEngine = FluencyAudioEngine;
if (typeof globalThis !== 'undefined') {
  globalThis.FluencyAudioEngine = FluencyAudioEngine;
}
