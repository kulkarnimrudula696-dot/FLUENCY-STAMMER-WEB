/**
 * FLUENCY My Progress & Recording History Engine
 * Visualizes longitudinal speech trends (Chart.js), practice streaks,
 * provides honest recording-to-recording comparisons,
 * and enables persistent audio recording playback directly from session history.
 */

const ProgressEngine = {
  charts: {},
  sessionsCache: [],
  statsCache: null,
  lastFetched: 0,
  isInitialized: false,
  currentlyPlayingId: null,

  init(forceRefresh = false) {
    if (!this.isInitialized) {
      this.bindEvents();
      this.isInitialized = true;
    }
    this.loadProgressData(forceRefresh);
    this.loadSessionsHistory(forceRefresh);
  },

  cleanup() {
    if (this.currentlyPlayingId) {
      this.pauseSessionAudio(this.currentlyPlayingId);
    }
  },

  invalidateCache() {
    this.statsCache = null;
    this.lastFetched = 0;
    this.sessionsCache = [];
  },

  bindEvents() {
    // Mode filter on history
    document.getElementById('history-filter-mode')?.addEventListener('change', (e) => {
      this.renderHistoryList(e.target.value);
    });

    // Recording comparison trigger
    document.getElementById('btn-run-comparison')?.addEventListener('click', () => {
      this.compareSelectedRecordings();
    });
  },

  async loadProgressData(forceRefresh = false) {
    const now = Date.now();
    if (!forceRefresh && this.statsCache && (now - this.lastFetched < 20000)) {
      this.populateStatsUI(this.statsCache);
      return;
    }

    try {
      const res = await fetch('/api/practice/progress-stats');
      const data = await res.json();
      this.statsCache = data;
      this.lastFetched = now;
      this.populateStatsUI(data);
    } catch (err) {
      console.error("Failed to load progress stats:", err);
    }
  },

  populateStatsUI(data) {
    // Update stat cards
    const streakEl = document.getElementById('prog-streak-val');
    const totalDaysEl = document.getElementById('prog-total-days-val');
    const weeklyMinsEl = document.getElementById('prog-weekly-mins-val');
    const totalSessionsEl = document.getElementById('prog-total-sessions-val');
    const improvEl = document.getElementById('prog-improvement-summary');

    if (streakEl) streakEl.innerText = `${data.streak} Days`;
    if (totalDaysEl) totalDaysEl.innerText = `${data.total_practice_days} Days`;
    if (weeklyMinsEl) weeklyMinsEl.innerText = `${data.weekly_minutes}m`;
    if (totalSessionsEl) totalSessionsEl.innerText = data.total_sessions;
    if (improvEl) improvEl.innerText = data.improvement_summary;

    if (data.charts) {
      this.renderCharts(data.charts);
    }
  },

  renderCharts(chartData) {
    if (!window.Chart) return;

    // Destroy existing instances to prevent canvas reuse errors
    if (this.charts.pace) this.charts.pace.destroy();
    if (this.charts.fillers) this.charts.fillers.destroy();
    if (this.charts.modes) this.charts.modes.destroy();

    const dates = chartData.dates && chartData.dates.length > 0 ? chartData.dates : ['Practice 1', 'Practice 2', 'Practice 3'];
    const wpmValues = chartData.wpm && chartData.wpm.length > 0 ? chartData.wpm : [110, 125, 138];
    const fillerValues = chartData.fillers && chartData.fillers.length > 0 ? chartData.fillers : [4, 2, 1];

    // 1. Your Speaking Speed Chart
    const paceCtx = document.getElementById('chart-pace-trend')?.getContext('2d');
    if (paceCtx) {
      this.charts.pace = new Chart(paceCtx, {
        type: 'line',
        data: {
          labels: dates,
          datasets: [
            {
              label: 'Speaking Speed (words/minute)',
              data: wpmValues,
              borderColor: '#9A633F',
              backgroundColor: 'rgba(154, 99, 63, 0.12)',
              borderWidth: 3,
              fill: true,
              tension: 0.35,
              pointBackgroundColor: '#9A633F',
              pointRadius: 5
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top' },
            tooltip: {
              callbacks: {
                label: (ctx) => {
                  const val = Math.round(ctx.raw || 0);
                  return `Speaking speed: ${val} words/minute`;
                },
                afterLabel: (ctx) => {
                  const val = ctx.raw || 0;
                  const t = (k, f) => (window.FluencyI18n ? window.FluencyI18n.t(k, f) : f);
                  if (val >= 110 && val <= 155) return t('speed_comfortable', 'Comfortable pace');
                  if (val >= 85 && val < 110) return t('speed_deliberate', 'Calm, deliberate pace');
                  if (val > 175) return t('speed_fast', 'Fast pace');
                  if (val > 155) return t('speed_brisk', 'Brisk pace');
                  if (val > 0 && val < 85) return t('speed_slow', 'Slow pace');
                  return '';
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              suggestedMin: 70,
              suggestedMax: 170,
              title: { display: true, text: 'Words spoken per minute' }
            }
          }
        }
      });
    }

    // 2. Filler Words Used Chart
    const fillersCtx = document.getElementById('chart-fillers-trend')?.getContext('2d');
    if (fillersCtx) {
      this.charts.fillers = new Chart(fillersCtx, {
        type: 'bar',
        data: {
          labels: dates,
          datasets: [
            {
              label: 'Filler Words Used',
              data: fillerValues,
              backgroundColor: '#D9A6A0',
              hoverBackgroundColor: '#7A4E4A',
              borderRadius: 8
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top' },
            tooltip: {
              callbacks: {
                label: (ctx) => {
                  const count = ctx.raw || 0;
                  return count === 1 ? '1 filler word' : `${count} filler words`;
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: { stepSize: 1 },
              title: { display: true, text: 'Number of filler words' }
            }
          }
        }
      });
    }

    // 3. Practice Modes Distribution Donut
    const modeCtx = document.getElementById('chart-mode-dist')?.getContext('2d');
    if (modeCtx) {
      const modeCounts = chartData.mode_distribution || { breath: 1, reading: 2, media: 1, conversation: 1, twister: 1 };
      this.charts.modes = new Chart(modeCtx, {
        type: 'doughnut',
        data: {
          labels: ['Breath & Relax', 'Reading Mode', 'Image/Video', 'Tongue Twister', 'Conversation'],
          datasets: [{
            data: [
              modeCounts.breath || 0,
              modeCounts.reading || 0,
              (modeCounts.media || 0) + (modeCounts.video || 0) + (modeCounts.image || 0),
              (modeCounts.twister || 0) + (modeCounts.tongue_twister || 0),
              modeCounts.conversation || 0
            ],
            backgroundColor: ['#4F5D3A', '#6B4632', '#9A633F', '#E65100', '#C65F32'],
            borderWidth: 2,
            borderColor: '#FFFFFF'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'right' }
          }
        }
      });
    }
  },

  async loadSessionsHistory(forceRefresh = false) {
    if (!forceRefresh && this.sessionsCache && this.sessionsCache.length > 0) {
      this.renderHistoryList('all');
      this.populateComparisonDropdowns();
      return;
    }

    try {
      const res = await fetch('/api/practice/sessions?mode=all');
      const data = await res.json();
      this.sessionsCache = data.sessions || [];
      this.renderHistoryList('all');
      this.populateComparisonDropdowns();
    } catch (err) {
      console.error("Failed to load sessions history:", err);
    }
  },

  renderHistoryList(filterMode = 'all') {
    const container = document.getElementById('practice-history-list');
    if (!container) return;

    let filtered = this.sessionsCache;
    if (filterMode !== 'all') {
      if (filterMode === 'media') {
        filtered = this.sessionsCache.filter(s => s.mode === 'media' || s.mode === 'video' || s.mode === 'image');
      } else if (filterMode === 'twister') {
        filtered = this.sessionsCache.filter(s => s.mode === 'twister' || s.mode === 'tongue_twister' || s.mode === 'tongue-twister');
      } else {
        filtered = this.sessionsCache.filter(s => s.mode === filterMode);
      }
    }

    if (filtered.length === 0) {
      container.innerHTML = `
        <div style="text-align:center; padding: 40px; color: var(--text-muted); background: var(--surface-cream); border-radius: var(--radius-md); border: 1.5px dashed var(--border-cream);">
          <i class="fa-solid fa-microphone-lines-slash" style="font-size: 32px; margin-bottom: 12px; color: var(--text-light);"></i>
          <p style="margin: 0; font-size: 1rem; font-weight: 700;">No practice sessions recorded in this mode yet.</p>
          <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: var(--text-light);">Complete any practice mode to build your audio history!</p>
        </div>
      `;
      return;
    }

    const modeBadges = {
      breath: { label: 'Breath & Relax', color: '#4F5D3A', bg: '#EBF0E1', icon: 'lungs' },
      reading: { label: 'Reading Mode', color: '#6B4632', bg: '#F4E8DC', icon: 'book-open' },
      media: { label: 'Image / Video', color: '#7A4E4A', bg: '#F9E7E5', icon: 'photo-film' },
      image: { label: 'Image Practice', color: '#7A4E4A', bg: '#F9E7E5', icon: 'image' },
      video: { label: 'Video Practice', color: '#9A633F', bg: '#FFF9E6', icon: 'film' },
      twister: { label: 'Tongue Twister', color: '#D35400', bg: '#FFE3D4', icon: 'wand-magic-sparkles' },
      tongue_twister: { label: 'Tongue Twister', color: '#D35400', bg: '#FFE3D4', icon: 'wand-magic-sparkles' },
      conversation: { label: 'Conversation', color: '#C65F32', bg: '#FFE8D1', icon: 'comments' }
    };

    container.innerHTML = filtered.map(s => {
      const b = modeBadges[s.mode] || { label: s.mode, color: '#9A633F', bg: '#FFF4DE', icon: 'microphone' };
      const hasAudio = Boolean(s.has_audio || s.audio_data_url);

      return `
        <div class="fluency-card session-history-card" id="session-card-${s.id}" style="padding: 18px 22px; margin-bottom: 14px; border: 1.5px solid var(--border-subtle); display: flex; flex-direction: column; gap: 10px;">
          
          <!-- Top Row: Session Info & Actions -->
          <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;">
            <div style="display: flex; align-items: center; gap: 14px; min-width: 240px; flex: 1;">
              <div style="background: ${b.bg}; color: ${b.color}; width: 44px; height: 44px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0;">
                <i class="fa-solid fa-${b.icon}"></i>
              </div>
              <div>
                <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                  <h4 style="margin: 0; font-size: 1.05rem; color: var(--text-dark);">${s.title}</h4>
                  <span style="background: ${b.bg}; color: ${b.color}; font-size: 0.72rem; font-weight: 800; padding: 2px 9px; border-radius: var(--radius-pill);">${b.label}</span>
                </div>
                <p style="margin: 4px 0 0 0; font-size: 0.84rem; color: var(--text-light);">
                  ${s.date || s.created_at} · Duration: ${s.duration_seconds}s ${s.wpm > 0 ? `· <strong>${s.wpm} WPM</strong> · Fillers: ${s.filler_count}` : ''}
                </p>
              </div>
            </div>

            <!-- Action Buttons Row -->
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
              ${hasAudio ? `
                <button class="btn btn-primary btn-sm btn-play-session" id="btn-play-session-${s.id}" onclick="ProgressEngine.togglePlayAudio(${s.id})" style="background: #9A633F; border: 1.5px solid #725C53; display: inline-flex; align-items: center; gap: 6px;" title="Listen to your recorded audio">
                  <i class="fa-solid fa-play" id="icon-play-session-${s.id}"></i> <span id="text-play-session-${s.id}">Play Recording</span>
                </button>
              ` : `
                <span style="font-size: 0.78rem; font-weight: 700; color: var(--text-muted); background: #FAF6F0; border: 1px solid #EAE0D5; padding: 5px 12px; border-radius: var(--radius-pill); display: inline-flex; align-items: center; gap: 5px;" title="No voice audio recorded for this session">
                  <i class="fa-solid fa-microphone-slash" style="color: #9CA3AF;"></i> No recording available
                </span>
              `}

              ${s.feedback ? `
                <button class="btn btn-secondary btn-sm" onclick="ProgressEngine.viewFeedback(${s.id})" style="border: 1.5px solid var(--border-subtle); display: inline-flex; align-items: center; gap: 5px;">
                  <i class="fa-solid fa-chart-simple"></i> View Feedback
                </button>
              ` : ''}

              <button class="btn btn-ghost btn-sm" style="color: #C0392B;" onclick="ProgressEngine.deleteSession(${s.id})" title="Delete session log">
                <i class="fa-solid fa-trash"></i>
              </button>
            </div>
          </div>

          <!-- Audio Replay Player Bar (Collapsible / Interactive) -->
          ${hasAudio ? `
            <div id="player-container-${s.id}" class="history-session-player" style="display: none; width: 100%; margin-top: 4px; padding: 12px 16px; background: #FFFDF9; border-radius: var(--radius-md); border: 1.5px solid #FFE082;">
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; font-size: 0.85rem; font-weight: 800; color: #7A4E10; flex-wrap: wrap; gap: 6px;">
                <span style="display: flex; align-items: center; gap: 6px;">
                  <i class="fa-solid fa-headphones" style="color: #D35400;"></i>
                  <span>Session Audio: <strong>${s.title}</strong> (${s.date || s.created_at})</span>
                </span>
                <span style="font-size: 0.76rem; color: #9A633F; background: #FFF0B8; padding: 2px 8px; border-radius: 4px; font-weight: 800;">
                  ${s.duration_seconds}s recording
                </span>
              </div>
              <audio id="audio-player-${s.id}" controls preload="none" src="${s.audio_data_url || ''}" style="width: 100%; height: 38px; display: block; border-radius: 6px;"></audio>
            </div>
          ` : ''}

        </div>
      `;
    }).join('');
  },

  async togglePlayAudio(sessionId) {
    const playerBox = document.getElementById(`player-container-${sessionId}`);
    const audioEl = document.getElementById(`audio-player-${sessionId}`);
    const btn = document.getElementById(`btn-play-session-${sessionId}`);
    const icon = document.getElementById(`icon-play-session-${sessionId}`);
    const text = document.getElementById(`text-play-session-${sessionId}`);

    if (!audioEl || !playerBox) return;

    // If another session is playing, pause it and reset its button
    if (this.currentlyPlayingId && this.currentlyPlayingId !== sessionId) {
      this.pauseSessionAudio(this.currentlyPlayingId);
    }

    // Lazy load audio data URL if not already loaded into src
    if (!audioEl.src || audioEl.src === window.location.href || audioEl.src.endsWith('/null') || audioEl.src.endsWith('/undefined')) {
      const session = this.sessionsCache.find(s => s.id === sessionId);
      if (session && session.audio_data_url) {
        audioEl.src = session.audio_data_url;
      } else {
        // Fetch single session from database
        try {
          const res = await fetch(`/api/practice/sessions/${sessionId}`);
          const d = await res.json();
          if (d.session && d.session.audio_data_url) {
            audioEl.src = d.session.audio_data_url;
            if (session) session.audio_data_url = d.session.audio_data_url;
          } else {
            showToast("No recording data found for this session.", "warning");
            return;
          }
        } catch(e) {
          showToast("Failed to load recording.", "error");
          return;
        }
      }
    }

    // Attach listeners once
    if (!audioEl.dataset.hasListeners) {
      audioEl.dataset.hasListeners = "true";

      audioEl.addEventListener('play', () => {
        if (icon) icon.className = "fa-solid fa-pause";
        if (text) text.innerText = "Pause";
        if (btn) {
          btn.style.background = "#D32F2F";
          btn.style.borderColor = "#B71C1C";
        }
        this.currentlyPlayingId = sessionId;
      });

      audioEl.addEventListener('pause', () => {
        if (icon) icon.className = "fa-solid fa-play";
        if (text) text.innerText = "Play Recording";
        if (btn) {
          btn.style.background = "#9A633F";
          btn.style.borderColor = "#725C53";
        }
        if (this.currentlyPlayingId === sessionId) {
          this.currentlyPlayingId = null;
        }
      });

      audioEl.addEventListener('ended', () => {
        if (icon) icon.className = "fa-solid fa-play";
        if (text) text.innerText = "Play Recording";
        if (btn) {
          btn.style.background = "#9A633F";
          btn.style.borderColor = "#725C53";
        }
        if (this.currentlyPlayingId === sessionId) {
          this.currentlyPlayingId = null;
        }
      });
    }

    if (audioEl.paused) {
      playerBox.style.display = 'block';
      try {
        await audioEl.play();
      } catch (err) {
        console.warn("Audio play interrupted or blocked by browser policy:", err);
      }
    } else {
      audioEl.pause();
    }
  },

  pauseSessionAudio(sessionId) {
    const audioEl = document.getElementById(`audio-player-${sessionId}`);
    const btn = document.getElementById(`btn-play-session-${sessionId}`);
    const icon = document.getElementById(`icon-play-session-${sessionId}`);
    const text = document.getElementById(`text-play-session-${sessionId}`);
    if (audioEl && !audioEl.paused) {
      audioEl.pause();
    }
    if (icon) icon.className = "fa-solid fa-play";
    if (text) text.innerText = "Play Recording";
    if (btn) {
      btn.style.background = "#9A633F";
      btn.style.borderColor = "#725C53";
    }
    if (this.currentlyPlayingId === sessionId) {
      this.currentlyPlayingId = null;
    }
  },

  populateComparisonDropdowns() {
    const selectA = document.getElementById('compare-select-a');
    const selectB = document.getElementById('compare-select-b');
    if (!selectA || !selectB) return;

    const speechSessions = this.sessionsCache.filter(s => s.wpm > 0);

    if (speechSessions.length < 2) {
      selectA.innerHTML = '<option value="">Record at least 2 speech sessions first</option>';
      selectB.innerHTML = '<option value="">Record at least 2 speech sessions first</option>';
      return;
    }

    const optionsA = speechSessions.map((s, idx) => `<option value="${s.id}" ${idx === 0 ? 'selected' : ''}>${s.title} (${s.date} - ${s.wpm} WPM)</option>`).join('');
    const optionsB = speechSessions.map((s, idx) => `<option value="${s.id}" ${idx === 1 ? 'selected' : ''}>${s.title} (${s.date} - ${s.wpm} WPM)</option>`).join('');

    selectA.innerHTML = optionsA;
    selectB.innerHTML = optionsB;
  },

  async compareSelectedRecordings() {
    const idA = document.getElementById('compare-select-a')?.value;
    const idB = document.getElementById('compare-select-b')?.value;

    if (!idA || !idB) {
      showToast("Please select two recordings to compare.", "warning");
      return;
    }

    if (idA === idB) {
      showToast("Please select two different recordings for comparison.", "warning");
      return;
    }

    try {
      const res = await fetch('/api/practice/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_a_id: idA, session_b_id: idB })
      });

      const data = await res.json();
      if (data.recording_a && data.recording_b) {
        this.renderComparisonResult(data);
      } else {
        showToast(data.error || "Comparison error.", "error");
      }
    } catch (err) {
      console.error("Comparison failed:", err);
    }
  },

  renderComparisonResult(data) {
    const container = document.getElementById('comparison-results-box');
    if (!container) return;

    const { recording_a: a, recording_b: b, deltas: d, comparative_notes: notes } = data;

    container.innerHTML = `
      <div class="fluency-card" style="padding: 28px; border: 2px solid var(--brand-brown-border); margin-top: 20px;">
        <h3 style="margin-bottom: 20px; color: var(--brand-brown);"><i class="fa-solid fa-scale-balanced"></i> Honest Comparison Analysis</h3>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px;">
          <!-- Attempt A -->
          <div style="background: var(--bg-warm-cream); border: 1.5px solid var(--border-subtle); border-radius: var(--radius-md); padding: 18px;">
            <div style="font-weight: 800; color: var(--text-dark); margin-bottom: 10px;">Recording A: ${a.title}</div>
            <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">Recorded on ${a.date} (${a.duration_seconds}s)</div>
            <ul style="list-style: none; font-size: 0.92rem; display: flex; flex-direction: column; gap: 6px;">
              <li><strong>Pace:</strong> ${a.wpm} WPM</li>
              <li><strong>Filler Words:</strong> ${a.filler_count}</li>
              <li><strong>Pauses / Hesitations:</strong> ${a.pauses_count}</li>
              <li><strong>Clarity Index:</strong> ${a.clarity_score}%</li>
            </ul>
            ${a.audio_data_url ? `
              <audio controls src="${a.audio_data_url}" style="width: 100%; height: 36px; margin-top: 12px; display: block;"></audio>
            ` : '<div style="margin-top: 10px; font-size: 0.8rem; color: var(--text-muted);">No audio recorded</div>'}
          </div>

          <!-- Attempt B -->
          <div style="background: var(--surface-cream); border: 1.5px solid var(--brand-brown-border); border-radius: var(--radius-md); padding: 18px;">
            <div style="font-weight: 800; color: var(--brand-brown); margin-bottom: 10px;">Recording B: ${b.title}</div>
            <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">Recorded on ${b.date} (${b.duration_seconds}s)</div>
            <ul style="list-style: none; font-size: 0.92rem; display: flex; flex-direction: column; gap: 6px;">
              <li><strong>Pace:</strong> ${b.wpm} WPM <span style="font-size: 0.8rem; color: ${d.wpm_diff > 0 ? '#3E885B' : '#725C53'};">(${d.wpm_diff > 0 ? '+' : ''}${d.wpm_diff} WPM)</span></li>
              <li><strong>Filler Words:</strong> ${b.filler_count} <span style="font-size: 0.8rem; color: ${d.filler_diff <= 0 ? '#3E885B' : '#C0392B'};">(${d.filler_diff > 0 ? '+' : ''}${d.filler_diff})</span></li>
              <li><strong>Pauses / Hesitations:</strong> ${b.pauses_count} <span style="font-size: 0.8rem; color: ${d.pauses_diff <= 0 ? '#3E885B' : '#C0392B'};">(${d.pauses_diff > 0 ? '+' : ''}${d.pauses_diff})</span></li>
              <li><strong>Clarity Index:</strong> ${b.clarity_score}% <span style="font-size: 0.8rem; color: ${d.clarity_diff >= 0 ? '#3E885B' : '#C0392B'};">(${d.clarity_diff > 0 ? '+' : ''}${d.clarity_diff}%)</span></li>
            </ul>
            ${b.audio_data_url ? `
              <audio controls src="${b.audio_data_url}" style="width: 100%; height: 36px; margin-top: 12px; display: block;"></audio>
            ` : '<div style="margin-top: 10px; font-size: 0.8rem; color: var(--text-muted);">No audio recorded</div>'}
          </div>
        </div>

        <!-- Comparative Observations -->
        <div style="background: var(--surface-white); border-left: 4px solid var(--accent-yellow); padding: 14px 18px; border-radius: 0 var(--radius-md) var(--radius-md) 0;">
          <div style="font-weight: 800; font-size: 0.95rem; margin-bottom: 6px;">Key Measurable Differences:</div>
          <ul style="padding-left: 20px; font-size: 0.9rem; color: var(--text-dark);">
            ${notes.map(n => `<li>${n}</li>`).join('')}
          </ul>
        </div>
      </div>
    `;
    container.scrollIntoView({ behavior: 'smooth' });
  },

  viewFeedback(sessionId) {
    const session = this.sessionsCache.find(s => s.id === sessionId);
    if (session && session.feedback) {
      showFeedbackScreen(session.feedback, session);
    }
  },

  async deleteSession(sessionId) {
    if (!confirm("Are you sure you want to delete this practice recording?")) return;

    if (this.currentlyPlayingId === sessionId) {
      this.pauseSessionAudio(sessionId);
    }

    try {
      await fetch(`/api/practice/sessions/${sessionId}`, { method: 'DELETE' });
      showToast("Recording deleted.", "info");
      this.loadProgressData(true);
      this.loadSessionsHistory(true);
    } catch (err) {
      console.error("Delete failed:", err);
    }
  }
};

window.ProgressEngine = ProgressEngine;
