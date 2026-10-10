/**
 * FLUENCY Breath & Relax Engine
 * Peaceful diaphragmatic breathing & relaxation practice.
 * Deep Olive (#4F5D3A) and Forest Olive (#34452B) peaceful atmosphere.
 */

const BreathingPractice = {
  activePattern: {
    name: "Box Breathing",
    inhale: 4,
    hold1: 4,
    exhale: 4,
    hold2: 4
  },
  
  targetDurationSeconds: 180, // Default 3 min
  remainingSeconds: 180,
  isRunning: false,
  isPaused: false,
  currentPhase: 'inhale', // inhale, hold1, exhale, hold2
  phaseTimer: 4,
  intervalId: null,
  cameraStream: null,
  isCameraOn: false,
  isInitialized: false,

  init() {
    if (!this.isInitialized) {
      this.bindEvents();
      this.isInitialized = true;
    }
    this.renderMascot();
  },

  cleanup() {
    if (this.isRunning) {
      this.pause();
    }
    if (this.isCameraOn && this.cameraStream) {
      this.cameraStream.getTracks().forEach(t => t.stop());
      this.isCameraOn = false;
      const container = document.getElementById('breath-cam-box');
      if (container) container.style.display = 'none';
      const btn = document.getElementById('btn-toggle-breath-cam');
      if (btn) btn.innerHTML = `<i class="fa-solid fa-video"></i> Camera On`;
    }
  },

  renderMascot() {
    const container = document.getElementById('breath-mascot-container');
    if (container) {
      const mascot = AppState.user ? AppState.user.selected_mascot : 'otter';
      container.innerHTML = MascotEngine.render(mascot, 'breathing', 110);
    }
  },

  bindEvents() {
    // Duration buttons
    document.querySelectorAll('.duration-pill-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        if (this.isRunning) return;
        document.querySelectorAll('.duration-pill-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const mins = parseInt(btn.dataset.mins || 3);
        this.targetDurationSeconds = mins * 60;
        this.remainingSeconds = this.targetDurationSeconds;
        this.updateTimeDisplay();
      });
    });

    // Technique selector
    const patternSelect = document.getElementById('breath-pattern-select');
    if (patternSelect) {
      patternSelect.addEventListener('change', (e) => {
        const val = e.target.value;
        if (val === '478') {
          this.activePattern = { name: "4-7-8 Relaxing", inhale: 4, hold1: 7, exhale: 8, hold2: 0 };
        } else if (val === '55') {
          this.activePattern = { name: "Coherent 5-5", inhale: 5, hold1: 0, exhale: 5, hold2: 0 };
        } else {
          this.activePattern = { name: "Box Breathing", inhale: 4, hold1: 4, exhale: 4, hold2: 4 };
        }
        this.reset();
      });
    }

    // Camera toggle
    const camBtn = document.getElementById('btn-toggle-breath-cam');
    if (camBtn) {
      camBtn.addEventListener('click', () => this.toggleCamera());
    }

    // Chimes toggle
    const chimeBtn = document.getElementById('btn-toggle-chimes');
    if (chimeBtn) {
      chimeBtn.addEventListener('click', () => {
        this.chimesEnabled = !this.chimesEnabled;
        chimeBtn.innerHTML = this.chimesEnabled ? `<i class="fa-solid fa-volume-high"></i> Sound On` : `<i class="fa-solid fa-volume-xmark"></i> Muted`;
      });
    }
  },

  start() {
    if (this.isRunning && !this.isPaused) return;

    this.isRunning = true;
    this.isPaused = false;
    this.currentPhase = 'inhale';
    this.phaseTimer = this.activePattern.inhale;

    document.getElementById('btn-breath-start').style.display = 'none';
    document.getElementById('btn-breath-pause').style.display = 'inline-flex';
    document.getElementById('btn-breath-stop').style.display = 'inline-flex';

    this.playChime(440); // Soft A4 chime
    this.updateCircleVisual();

    this.intervalId = setInterval(() => {
      this.tick();
    }, 1000);
  },

  pause() {
    if (!this.isRunning || this.isPaused) return;
    this.isPaused = true;
    clearInterval(this.intervalId);
    document.getElementById('btn-breath-pause').innerHTML = `<i class="fa-solid fa-play"></i> Resume`;
  },

  resume() {
    if (!this.isRunning || !this.isPaused) return;
    this.isPaused = false;
    document.getElementById('btn-breath-pause').innerHTML = `<i class="fa-solid fa-pause"></i> Pause`;
    this.intervalId = setInterval(() => {
      this.tick();
    }, 1000);
  },

  stop() {
    clearInterval(this.intervalId);
    const practicedSeconds = this.targetDurationSeconds - this.remainingSeconds;
    this.isRunning = false;
    this.isPaused = false;

    document.getElementById('btn-breath-start').style.display = 'inline-flex';
    document.getElementById('btn-breath-pause').style.display = 'none';
    document.getElementById('btn-breath-stop').style.display = 'none';
    document.getElementById('btn-breath-pause').innerHTML = `<i class="fa-solid fa-pause"></i> Pause`;

    // Reset visual
    const circle = document.getElementById('breath-circle');
    if (circle) {
      circle.className = 'breath-circle-main';
    }
    document.getElementById('breath-phase-text').innerText = "Ready to Breathe";
    document.getElementById('breath-phase-countdown').innerText = "4";

    if (practicedSeconds >= 30) {
      this.saveSession(practicedSeconds);
    }
    this.remainingSeconds = this.targetDurationSeconds;
    this.updateTimeDisplay();
  },

  reset() {
    this.stop();
    this.remainingSeconds = this.targetDurationSeconds;
    this.updateTimeDisplay();
  },

  tick() {
    this.remainingSeconds--;
    this.updateTimeDisplay();

    if (this.remainingSeconds <= 0) {
      this.stop();
      showToast("Beautiful practice! You completed your breathing cycle.", "success");
      return;
    }

    this.phaseTimer--;

    if (this.phaseTimer <= 0) {
      // Transition to next phase in pattern
      if (this.currentPhase === 'inhale') {
        if (this.activePattern.hold1 > 0) {
          this.currentPhase = 'hold1';
          this.phaseTimer = this.activePattern.hold1;
        } else {
          this.currentPhase = 'exhale';
          this.phaseTimer = this.activePattern.exhale;
        }
      } else if (this.currentPhase === 'hold1') {
        this.currentPhase = 'exhale';
        this.phaseTimer = this.activePattern.exhale;
      } else if (this.currentPhase === 'exhale') {
        if (this.activePattern.hold2 > 0) {
          this.currentPhase = 'hold2';
          this.phaseTimer = this.activePattern.hold2;
        } else {
          this.currentPhase = 'inhale';
          this.phaseTimer = this.activePattern.inhale;
        }
      } else if (this.currentPhase === 'hold2') {
        this.currentPhase = 'inhale';
        this.phaseTimer = this.activePattern.inhale;
      }

      this.updateCircleVisual();
    }

    document.getElementById('breath-phase-countdown').innerText = this.phaseTimer;
  },

  updateCircleVisual() {
    const circle = document.getElementById('breath-circle');
    const phaseText = document.getElementById('breath-phase-text');
    if (!circle || !phaseText) return;

    if (this.currentPhase === 'inhale') {
      circle.className = 'breath-circle-main inhale';
      circle.style.transitionDuration = `${this.activePattern.inhale}s`;
      phaseText.innerText = "Breathe In (Nose)";
      this.playChime(523.25); // C5
    } else if (this.currentPhase === 'hold1' || this.currentPhase === 'hold2') {
      circle.className = 'breath-circle-main hold';
      circle.style.transitionDuration = `0.5s`;
      phaseText.innerText = "Hold & Soften";
      this.playChime(659.25); // E5
    } else if (this.currentPhase === 'exhale') {
      circle.className = 'breath-circle-main exhale';
      circle.style.transitionDuration = `${this.activePattern.exhale}s`;
      phaseText.innerText = "Gently Exhale (Lips)";
      this.playChime(392.00); // G4
    }
  },

  updateTimeDisplay() {
    const mins = Math.floor(this.remainingSeconds / 60);
    const secs = this.remainingSeconds % 60;
    const disp = document.getElementById('breath-total-time');
    if (disp) {
      disp.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
  },

  async toggleCamera() {
    const container = document.getElementById('breath-cam-box');
    const video = document.getElementById('breath-cam-video');
    const btn = document.getElementById('btn-toggle-breath-cam');

    if (this.isCameraOn) {
      if (this.cameraStream) {
        this.cameraStream.getTracks().forEach(t => t.stop());
      }
      container.style.display = 'none';
      this.isCameraOn = false;
      btn.innerHTML = `<i class="fa-solid fa-video"></i> Camera On`;
    } else {
      if (!navigator.mediaDevices || typeof navigator.mediaDevices.getUserMedia !== 'function') {
        showToast("Camera access is not supported in this browser environment or requires HTTPS/localhost.", "warning");
        return;
      }
      try {
        this.cameraStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        video.srcObject = this.cameraStream;
        container.style.display = 'block';
        this.isCameraOn = true;
        btn.innerHTML = `<i class="fa-solid fa-video-slash"></i> Camera Off`;
      } catch (err) {
        showToast("Camera access was not granted.", "warning");
      }
    }
  },

  playChime(freq = 440) {
    if (!this.chimesEnabled) return;
    try {
      if (!this.audioCtx) {
        this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, this.audioCtx.currentTime);
      gain.gain.setValueAtTime(0.08, this.audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, this.audioCtx.currentTime + 1.2);
      osc.connect(gain);
      gain.connect(this.audioCtx.destination);
      osc.start();
      osc.stop(this.audioCtx.currentTime + 1.2);
    } catch (e) {}
  },

  async saveSession(seconds) {
    try {
      await fetch('/api/practice/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mode: 'breath',
          title: `${this.activePattern.name} (${Math.round(seconds / 60)} min)`,
          duration_seconds: seconds,
          transcript: "Completed diaphragmatic breath and relax session.",
          prompt_text: `Pattern: ${this.activePattern.name}`
        })
      });
      showToast(`Logged ${Math.round(seconds)}s of mindful breathing to your progress.`, "success");
    } catch (err) {}
  }
};
