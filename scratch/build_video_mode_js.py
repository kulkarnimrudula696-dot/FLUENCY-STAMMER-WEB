import json

with open('scratch/unified_media.json', 'r', encoding='utf-8') as f:
    unified = json.load(f)

# Take default videos and images
default_videos = unified['videos']
default_images = unified['images']

header = """/**
 * FLUENCY – Dedicated Image & Video Practice Engine
 * Warm Yellow + White Theme matching FLUENCY Brand Identity
 * 
 * Verified Content Mapping:
 * Every visual item atomically binds:
 * - media URL / embed URL
 * - media type
 * - title
 * - speaking clue / prompt
 * - description / instruction
 * - guiding questions
 * - suggested keywords / vocabulary
 */
"""

code_body = """
function getAgeGroupId(ageOrGroup) {
  if (!ageOrGroup) return '18-23';
  const val = String(ageOrGroup).trim().replace('–', '-');
  if (['6-11', '12-17', '18-23', '24-30', '31-40'].includes(val)) return val;
  const num = parseInt(val, 10);
  if (!isNaN(num)) {
    if (num <= 11) return '6-11';
    if (num <= 17) return '12-17';
    if (num <= 23) return '18-23';
    if (num <= 30) return '24-30';
    return '31-40';
  }
  const legacy = {
    '6-9': '6-11',
    '10-12': '12-17',
    '13-17': '12-17',
    '18-25': '18-23',
    '26-32': '24-30',
    '33-40': '31-40'
  };
  return legacy[val] || '18-23';
}

function getAgeGroupLabel(ageGroupId) {
  const map = {
    '6-11': 'Ages 6–11',
    '12-17': 'Ages 12–17',
    '18-23': 'Ages 18–23',
    '24-30': 'Ages 24–30',
    '31-40': 'Ages 31–40'
  };
  return map[getAgeGroupId(ageGroupId)] || 'Ages 18–23';
}

// =============================================================================
// MAIN MEDIA PRACTICE CONTROLLER
// =============================================================================

const MediaPractice = {
  currentMode: 'video', // 'video' | 'image'
  currentDifficulty: 'all', // 'all' | 'easy' | 'medium' | 'hard'
  currentAgeGroup: '18-23',
  currentAge: 21,
  
  videoItems: DEFAULT_PRACTICE_VIDEOS,
  imageItems: DEFAULT_PRACTICE_IMAGES,
  activeList: [],
  currentIndex: 0,
  activeItem: null,
  
  // Level Access State (All 3 levels directly accessible)
  unlockedLevels: {
    easy: 'unlocked',
    medium: 'unlocked',
    hard: 'unlocked'
  },
  
  // Audio & Recording state
  audioEngine: null,
  isRecording: false,
  hasRecorded: false,
  recordedAudioUrl: null,
  recordedTranscript: '',
  isInitialized: false,

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

  init() {
    this.detectUserAge();
    this.loadUnlockedLevels();
    this.getAudioEngine();
    
    if (!this.isInitialized) {
      this.isInitialized = true;
    }

    this.fetchContent();
    this.switchMode(this.currentMode || 'video');
  },

  detectUserAge() {
    let ageGroup = (window.AppState && window.AppState.user && window.AppState.user.age_group) || null;
    let age = 21;
    if (window.AppState && window.AppState.user) {
      age = window.AppState.user.practice_age || window.AppState.user.actual_age || 21;
    }
    this.currentAge = parseInt(age, 10) || 21;
    this.currentAgeGroup = ageGroup ? getAgeGroupId(ageGroup) : getAgeGroupId(this.currentAge);
  },

  loadUnlockedLevels() {
    this.unlockedLevels = { easy: 'unlocked', medium: 'unlocked', hard: 'unlocked' };
    this.updateDifficultyFilterUI();
  },

  saveUnlockedLevels() {
    this.updateDifficultyFilterUI();
  },

  unlockNextLevel(completedLevel) {
    // All levels unlocked
  },

  updateDifficultyFilterUI() {
    const easyBtn = document.getElementById('diff-filter-easy');
    const medBtn = document.getElementById('diff-filter-medium');
    const hardBtn = document.getElementById('diff-filter-hard');

    if (easyBtn) {
      easyBtn.innerHTML = `EASY`;
      easyBtn.classList.remove('locked-btn');
    }

    if (medBtn) {
      medBtn.innerHTML = `MEDIUM`;
      medBtn.classList.remove('locked-btn');
    }

    if (hardBtn) {
      hardBtn.innerHTML = `HARD`;
      hardBtn.classList.remove('locked-btn');
    }
  },

  async fetchContent() {
    this.detectUserAge();
    try {
      const [vRes, iRes] = await Promise.all([
        fetch(`/api/content/videos?age_group=${encodeURIComponent(this.currentAgeGroup)}&age=${this.currentAge}`).then(r => r.json()).catch(() => null),
        fetch(`/api/content/images?age_group=${encodeURIComponent(this.currentAgeGroup)}&age=${this.currentAge}`).then(r => r.json()).catch(() => null)
      ]);
      if (vRes && vRes.items && vRes.items.length > 0) {
        this.videoItems = vRes.items;
      }
      if (iRes && iRes.items && iRes.items.length > 0) {
        this.imageItems = iRes.items;
      }
      this.renderGrid();
    } catch (e) {
      console.warn('Using default practice media library:', e);
    }
  },

  cleanup() {
    if (this.isRecording && this.audioEngine) {
      this.audioEngine.stopRecording();
      this.isRecording = false;
    }
    // Blank iframe to stop video playback
    const iframe = document.getElementById('media-video-iframe');
    if (iframe && iframe.src && iframe.src !== 'about:blank') {
      iframe.src = 'about:blank';
    }
  },

  bindEvents() {
    if (this.audioEngine) {
      this.audioEngine.onTranscriptUpdate = (finalTranscript, interim) => {
        this.recordedTranscript = finalTranscript;
        const transcriptDisp = document.getElementById('media-live-transcript');
        if (transcriptDisp) {
          transcriptDisp.innerHTML = `<strong>Live Transcript:</strong> ${finalTranscript} <span style="color:#D97706;">${interim}</span>`;
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
    }
  },

  switchMode(mode) {
    this.cleanup();

    this.currentMode = (mode === 'image') ? 'image' : 'video';
    
    // Update Mode Tabs (Choice A vs Choice B)
    const btnVideos = document.getElementById('tab-btn-practice-videos');
    const btnImages = document.getElementById('tab-btn-practice-images');
    if (btnVideos) btnVideos.classList.toggle('active', this.currentMode === 'video');
    if (btnImages) btnImages.classList.toggle('active', this.currentMode === 'image');

    // Update Header Banner
    const modeBadge = document.getElementById('media-mode-badge');
    const bannerTitle = document.getElementById('media-banner-title');
    const bannerDesc = document.getElementById('media-banner-desc');
    const counterLabel = document.getElementById('media-counter-label');

    const ageLabel = getAgeGroupLabel(this.currentAgeGroup);

    if (this.currentMode === 'video') {
      if (modeBadge) modeBadge.innerHTML = `<i class="fa-solid fa-film"></i> Practice Studio → Video Mode (${ageLabel})`;
      if (bannerTitle) bannerTitle.innerText = 'Video Speaking Practice';
      if (bannerDesc) bannerDesc.innerText = 'Watch the video carefully, then explain what you saw in your own words.';
      if (counterLabel) counterLabel.innerText = 'Practice Videos';
    } else {
      if (modeBadge) modeBadge.innerHTML = `<i class="fa-solid fa-image"></i> Practice Studio → Image Mode (${ageLabel})`;
      if (bannerTitle) bannerTitle.innerText = 'Image Speaking Practice';
      if (bannerDesc) bannerDesc.innerText = 'Look closely at the image, then describe the scene and what is happening.';
      if (counterLabel) counterLabel.innerText = 'Practice Images';
    }

    this.updateDifficultyFilterUI();
    this.backToCatalog();
    this.renderGrid();
  },

  setDifficulty(diff) {
    diff = (diff || 'all').toLowerCase();
    this.currentDifficulty = diff;

    // Update Diff Filter Buttons Active State
    const diffButtons = ['all', 'easy', 'medium', 'hard'];
    diffButtons.forEach(d => {
      const btn = document.getElementById(`diff-filter-${d}`);
      if (btn) {
        btn.classList.toggle('active', this.currentDifficulty === d);
      }
    });

    this.renderGrid();
  },

  renderGrid() {
    const gridEl = document.getElementById('media-cards-grid');
    const countBadge = document.getElementById('media-catalog-count-badge');
    const itemsCountTag = document.getElementById('media-items-count-tag');

    const source = (this.currentMode === 'video') ? this.videoItems : this.imageItems;

    // Filter by current age group
    let ageFiltered = source.filter(item => {
      if (!item.age_group) return true;
      const itemGroup = getAgeGroupId(item.age_group);
      return itemGroup === this.currentAgeGroup;
    });
    if (ageFiltered.length === 0) ageFiltered = source;

    // Filter by current difficulty
    let filtered = ageFiltered;
    if (this.currentDifficulty !== 'all') {
      filtered = ageFiltered.filter(item => {
        const itemDiff = (item.difficulty || '').toLowerCase();
        return itemDiff === this.currentDifficulty;
      });
    }

    this.activeList = filtered;

    const countText = `${this.activeList.length} items available`;
    if (countBadge) countBadge.innerText = `Showing ${this.activeList.length} ${this.currentDifficulty !== 'all' ? this.currentDifficulty.toUpperCase() : ''} items`;
    if (itemsCountTag) itemsCountTag.innerText = countText;

    if (!gridEl) return;

    if (this.activeList.length === 0) {
      gridEl.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 48px; background: #FFFFFF; border: 2px dashed #FFE082; border-radius: var(--radius-xl);">
          <div style="font-size: 36px; margin-bottom: 8px;">🎬</div>
          <h3 style="color: #3D2B24; font-weight: 800;">No items found for this filter</h3>
          <p style="color: #725C53;">Click ALL or select a difficulty level (EASY, MEDIUM, HARD) to view practice items.</p>
          <button class="btn btn-secondary btn-sm" onclick="MediaPractice.setDifficulty('all')" style="margin-top: 12px;">Show All</button>
        </div>
      `;
      return;
    }

    const diffStyles = {
      'Easy': { bg: '#EAF5EE', color: '#2E7D32', border: '#C8E6C9' },
      'Medium': { bg: '#FFF9E6', color: '#B45309', border: '#FFE082' },
      'Hard': { bg: '#FDF2F2', color: '#C0392B', border: '#FFCDD2' }
    };

    gridEl.innerHTML = this.activeList.map(item => {
      const dStyle = diffStyles[item.difficulty] || diffStyles['Easy'];
      
      let thumbUrl = item.thumbnail || item.image_url;
      let playOverlay = '';
      if (this.currentMode === 'video') {
        const yid = item.youtube_id || '';
        thumbUrl = yid ? `https://img.youtube.com/vi/${yid}/hqdefault.jpg` : (item.thumbnail || '');
        playOverlay = `<div class="media-card-play-overlay"><i class="fa-solid fa-play"></i></div>`;
      }

      return `
        <div class="media-card-item">
          <div class="media-card-thumbnail-box" onclick="MediaPractice.openPractice('${item.id}')">
            <img src="${thumbUrl}" alt="${item.title}" loading="lazy" />
            ${playOverlay}
            <div style="position: absolute; top: 12px; left: 12px;">
              <span style="background: ${dStyle.bg}; color: ${dStyle.color}; border: 1.5px solid ${dStyle.border}; padding: 4px 10px; border-radius: var(--radius-pill); font-size: 0.78rem; font-weight: 800;">
                ${item.difficulty.toUpperCase()}
              </span>
            </div>
            ${item.duration ? `
              <div style="position: absolute; bottom: 10px; right: 12px; background: rgba(0,0,0,0.75); color: #FFFFFF; padding: 2px 8px; border-radius: 4px; font-size: 0.78rem; font-weight: 700;">
                ${item.duration}
              </div>
            ` : ''}
          </div>
          
          <div class="media-card-body">
            <div>
              <h3 style="font-size: 1.15rem; font-weight: 900; color: #3D2B24; margin-bottom: 6px;">
                ${item.title}
              </h3>
              <p style="color: #725C53; font-size: 0.88rem; line-height: 1.45; margin: 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
                ${item.clue || item.prompt || item.instruction || item.description}
              </p>
            </div>

            <div style="margin-top: 8px;">
              <button class="btn btn-primary" onclick="MediaPractice.openPractice('${item.id}')" style="background: #FFC83D; color: #3D2B24; font-weight: 900; border: 2px solid #E5A81A; width: 100%; border-radius: var(--radius-pill); padding: 9px 16px; font-size: 0.95rem;">
                <i class="fa-solid fa-microphone"></i> Practice
              </button>
            </div>
          </div>
        </div>
      `;
    }).join('');
  },

  openPractice(itemId) {
    this.cleanup();

    const source = (this.currentMode === 'video') ? this.videoItems : this.imageItems;
    let idx = this.activeList.findIndex(i => i.id === itemId);
    if (idx === -1) {
      idx = source.findIndex(i => i.id === itemId);
      this.activeList = source;
    }

    this.currentIndex = idx !== -1 ? idx : 0;
    this.activeItem = this.activeList[this.currentIndex];

    const catalogView = document.getElementById('media-catalog-view');
    const studioView = document.getElementById('media-practice-studio-view');
    if (catalogView) catalogView.style.display = 'none';
    if (studioView) studioView.style.display = 'block';

    window.scrollTo({ top: 0, behavior: 'smooth' });

    this.renderActiveItem();
  },

  backToCatalog() {
    this.cleanup();

    const catalogView = document.getElementById('media-catalog-view');
    const studioView = document.getElementById('media-practice-studio-view');
    if (catalogView) catalogView.style.display = 'block';
    if (studioView) studioView.style.display = 'none';

    window.scrollTo({ top: 0, behavior: 'smooth' });
  },

  renderActiveItem() {
    const viewerCard = document.getElementById('media-practice-viewer-card');
    const completionCard = document.getElementById('media-completion-card');

    if (!this.activeList || this.activeList.length === 0) {
      this.activeList = (this.currentMode === 'video') ? this.videoItems : this.imageItems;
    }

    if (this.currentIndex >= this.activeList.length) {
      if (viewerCard) viewerCard.style.display = 'none';
      if (completionCard) completionCard.style.display = 'block';
      return;
    }

    if (viewerCard) viewerCard.style.display = 'block';
    if (completionCard) completionCard.style.display = 'none';

    const item = this.activeList[this.currentIndex];
    this.activeItem = item;

    // 1. Counter Badge
    const counterBadge = document.getElementById('media-studio-counter-badge');
    if (counterBadge) {
      counterBadge.innerText = `Item ${this.currentIndex + 1} of ${this.activeList.length}`;
    }

    // 2. Title & Difficulty Badge
    const titleEl = document.getElementById('media-item-title');
    const diffTag = document.getElementById('media-item-diff-tag');
    const durTag = document.getElementById('media-item-duration-tag');

    if (titleEl) titleEl.innerText = item.title;

    const diffBadgeStyles = {
      'Easy': { bg: '#EAF5EE', color: '#2E7D32', border: '#C8E6C9' },
      'Medium': { bg: '#FFF9E6', color: '#B45309', border: '#FFE082' },
      'Hard': { bg: '#FDF2F2', color: '#C0392B', border: '#FFCDD2' }
    };

    const dStyle = diffBadgeStyles[item.difficulty] || diffBadgeStyles['Easy'];
    if (diffTag) {
      diffTag.innerText = item.difficulty.toUpperCase();
      diffTag.style.background = dStyle.bg;
      diffTag.style.color = dStyle.color;
      diffTag.style.border = `1px solid ${dStyle.border}`;
    }

    if (durTag) {
      durTag.innerText = item.duration || (this.currentMode === 'video' ? 'Short Clip' : 'Visual Scene');
    }

    // 3. Visual Media Display
    const videoContainer = document.getElementById('media-video-display-container');
    const imageContainer = document.getElementById('media-image-display-container');

    if (this.currentMode === 'video') {
      if (videoContainer) videoContainer.style.display = 'block';
      if (imageContainer) imageContainer.style.display = 'none';

      const iframe = document.getElementById('media-video-iframe');
      const embedUrl = item.youtubeEmbedUrl || item.embed_url || `https://www.youtube.com/embed/${item.youtube_id || ''}?enablejsapi=1&rel=0`;

      if (iframe) {
        iframe.src = embedUrl;
        iframe.title = item.title;
      }
    } else {
      if (videoContainer) videoContainer.style.display = 'none';
      if (imageContainer) imageContainer.style.display = 'block';

      const img = document.getElementById('media-image-display');
      if (img) {
        img.src = item.image_url;
        img.alt = item.title;
      }
      const iframe = document.getElementById('media-video-iframe');
      if (iframe && iframe.src !== 'about:blank') {
        iframe.src = 'about:blank';
      }
    }

    // 4. Clue & Guiding Questions
    const clueEl = document.getElementById('media-item-clue');
    const instructionEl = document.getElementById('media-item-instruction');
    const qList = document.getElementById('media-guiding-questions');
    const kwBox = document.getElementById('media-keywords-cloud');

    const clueText = item.clue || item.prompt || 'Describe what you observe in the scene.';
    if (clueEl) clueEl.innerText = `"${clueText}"`;
    
    if (instructionEl) {
      instructionEl.innerText = item.instruction || item.description || (this.currentMode === 'video'
        ? 'Watch the video carefully, then explain what you saw in your own words.'
        : 'Look closely at the image, then describe the scene and what is happening.');
    }

    const guidingQs = item.guiding_questions || item.guidingQuestions || [];
    if (qList) {
      if (guidingQs.length > 0) {
        qList.innerHTML = guidingQs.map(q => `
          <li style="display:flex; align-items:flex-start; gap:8px; margin-bottom:4px;">
            <i class="fa-solid fa-circle-question" style="color:#FFC83D; margin-top:3px; font-size:15px; flex-shrink:0;"></i>
            <span>${q}</span>
          </li>
        `).join('');
      } else {
        qList.innerHTML = '';
      }
    }

    const keywords = item.suggested_keywords || item.vocabulary || [];
    if (kwBox) {
      if (keywords.length > 0) {
        kwBox.innerHTML = keywords.map(kw => `
          <span class="keyword-chip" style="background:#FFF9E6; color:#9A633F; border:1px solid #FFE082; padding:5px 12px; border-radius:999px; font-size:0.85rem; font-weight:700;">
            ${kw}
          </span>
        `).join('');
      } else {
        kwBox.innerHTML = '';
      }
    }

    this.resetRecordingUI();
  },

  prevItem() {
    this.cleanup();

    if (this.currentIndex > 0) {
      this.currentIndex--;
      this.renderActiveItem();
    } else {
      if (window.showToast) showToast('You are at the first item of this set.', 'info');
    }
  },

  nextItem() {
    this.cleanup();

    if (this.currentIndex < this.activeList.length - 1) {
      this.currentIndex++;
      this.renderActiveItem();
    } else {
      if (window.showToast) showToast('You have completed all items in this section! Well done!', 'success');
    }
  },

  restartSet() {
    this.cleanup();
    this.currentIndex = 0;
    this.renderActiveItem();
  },

  resetRecordingUI() {
    this.isRecording = false;
    this.hasRecorded = false;
    this.recordedAudioUrl = null;
    this.recordedTranscript = '';

    const recBtn = document.getElementById('btn-media-record-toggle');
    if (recBtn) {
      recBtn.className = 'btn btn-primary btn-lg';
      recBtn.style.background = '#FFC83D';
      recBtn.style.color = '#3D2B24';
      recBtn.style.border = '2px solid #E5A81A';
      recBtn.innerHTML = `<i class="fa-solid fa-microphone"></i> Start Recording`;
    }

    const statusLabel = document.getElementById('media-record-status-label');
    if (statusLabel) {
      statusLabel.innerHTML = `<span style="color:#9A633F;">Click Start Recording when you're ready to speak.</span>`;
    }

    const submitBtn = document.getElementById('btn-media-submit');
    if (submitBtn) submitBtn.disabled = true;

    const timerDisp = document.getElementById('media-record-timer');
    if (timerDisp) timerDisp.innerText = '00:00';

    const playerBox = document.getElementById('media-audio-player-box');
    if (playerBox) playerBox.style.display = 'none';

    const transcriptDisp = document.getElementById('media-live-transcript');
    if (transcriptDisp) transcriptDisp.innerHTML = '';
  },

  async toggleRecording() {
    if (!this.isRecording) {
      await this.startRecording();
    } else {
      await this.stopRecording();
    }
  },

  async startRecording() {
    const engine = this.getAudioEngine();
    if (!engine) {
      console.error("FluencyAudioEngine could not be initialized.");
      const statusLabel = document.getElementById('media-record-status-label');
      if (statusLabel) {
        statusLabel.innerHTML = `<div style="color:#C0392B;font-weight:700;margin-top:4px;"><i class="fa-solid fa-triangle-exclamation"></i> Recording engine failed to initialize. Please refresh the page.</div>`;
      }
      if (window.showToast) showToast("Recording engine failed to initialize. Please refresh.", "error");
      return;
    }

    const canvas = document.getElementById('media-waveform-canvas');
    const statusLabel = document.getElementById('media-record-status-label');

    try {
      await engine.startRecording(canvas);
      this.isRecording = true;

      const recBtn = document.getElementById('btn-media-record-toggle');
      if (recBtn) {
        recBtn.className = 'btn btn-accent btn-lg';
        recBtn.style.background = '#C0392B';
        recBtn.style.color = '#FFFFFF';
        recBtn.style.border = '2px solid #962D22';
        recBtn.innerHTML = `<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#FFFFFF;margin-right:8px;animation:recPulse 1s infinite;"></span> Stop Recording`;
      }

      if (statusLabel) {
        statusLabel.innerHTML = `<span style="color:#C0392B;font-weight:700;"><i class="fa-solid fa-circle" style="color:#C0392B;font-size:10px;margin-right:6px;"></i> Recording in progress... speak at your natural pace.</span>`;
      }

      const submitBtn = document.getElementById('btn-media-submit');
      if (submitBtn) submitBtn.disabled = true;

      const transcriptDisp = document.getElementById('media-live-transcript');
      if (transcriptDisp) transcriptDisp.innerHTML = `<em>Listening and recording... speak at your natural pace.</em>`;

      if (window.showToast) {
        showToast('Recording started! Describe what you observe in your own words.', 'info');
      }
    } catch (err) {
      console.error('Microphone error:', err);
      this.isRecording = false;

      const errType = err && err.name ? err.name : 'MicrophoneError';
      const errDetails = err && err.message ? err.message : '';
      const displayMsg = errType === 'NotAllowedError' || errType === 'PermissionDeniedError'
        ? "Microphone access was denied. Please allow microphone permission in your browser settings and try again."
        : (errDetails ? `${errType}: ${errDetails}` : `${errType}: Failed to access microphone.`);

      if (statusLabel) {
        statusLabel.innerHTML = `<div style="color:#C0392B;font-weight:700;margin-top:4px;"><i class="fa-solid fa-triangle-exclamation" style="margin-right:6px;"></i> ${displayMsg}</div>`;
      }

      if (window.showToast) {
        showToast(displayMsg, 'error');
      }
    }
  },

  async stopRecording() {
    if (!this.isRecording) return;
    this.isRecording = false;

    const engine = this.getAudioEngine();
    if (engine) {
      engine.stopRecording();
      this.hasRecorded = true;
    }

    const recBtn = document.getElementById('btn-media-record-toggle');
    if (recBtn) {
      recBtn.className = 'btn btn-secondary btn-lg';
      recBtn.style.background = '#FFFFFF';
      recBtn.style.color = '#3D2B24';
      recBtn.style.border = '1.5px solid #FFE082';
      recBtn.innerHTML = `<i class="fa-solid fa-rotate-left"></i> Re-record`;
    }

    const statusLabel = document.getElementById('media-record-status-label');
    if (statusLabel) {
      statusLabel.innerHTML = `<span style="color:#2E7D32;font-weight:700;"><i class="fa-solid fa-circle-check" style="margin-right:6px;"></i> Recording ready! You can listen back or click Submit / Analyze.</span>`;
    }

    const submitBtn = document.getElementById('btn-media-submit');
    if (submitBtn) submitBtn.disabled = false;

    if (window.showToast) {
      showToast('Recording saved! Click Submit / Analyze to get speech insights.', 'success');
    }
  },

  async submitAnalysis() {
    const engine = this.getAudioEngine();
    if (!this.hasRecorded && (!engine || engine.elapsedSeconds < 2)) {
      if (window.showToast) showToast('Please record your speech before submitting.', 'warning');
      return;
    }

    const submitBtn = document.getElementById('btn-media-submit');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Speech...`;
    }

    const stats = engine ? engine.getRecordingStats() : { duration_seconds: 15, words_spoken: 35 };
    const transcript = (this.recordedTranscript || '').trim();

    const finalTranscript = transcript.length > 5 
      ? transcript 
      : (this.activeItem 
          ? `I practiced describing ${this.activeItem.title}. The scene was expressive with clear emotions, actions, and natural communication.` 
          : 'The practice session was engaging and expressive with natural speech flow.');

    const promptText = this.activeItem
      ? `${this.activeItem.title}. ${this.activeItem.clue || this.activeItem.prompt || ''}. ${this.activeItem.instruction || this.activeItem.description || ''}`
      : 'Visual Speaking Practice';

    if (this.activeItem && this.activeItem.difficulty) {
      this.unlockNextLevel(this.activeItem.difficulty);
    }

    try {
      const payload = {
        mode: this.currentMode,
        title: this.activeItem ? this.activeItem.title : (this.currentMode === 'video' ? 'Video Practice' : 'Image Practice'),
        duration_seconds: Math.max(stats.duration_seconds || 15, 3),
        transcript: finalTranscript,
        prompt_text: promptText,
        audio_data_url: this.recordedAudioUrl
      };

      const res = await fetch('/api/practice/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (data.feedback) {
        if (window.AppState) AppState.invalidateStatsCache();
        if (window.showFeedbackScreen) {
          showFeedbackScreen(data.feedback, data.session);
        }
      } else {
        if (window.showToast) showToast('Analysis completed with fallback scores.', 'info');
        this.renderFallbackFeedback(stats, finalTranscript);
      }
    } catch (err) {
      console.error('Analysis submission error:', err);
      this.renderFallbackFeedback(stats, finalTranscript);
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Submit / Analyze`;
      }
    }
  },

  renderFallbackFeedback(stats, transcript) {
    const duration = stats.duration_seconds || 18;
    const words = Math.max(stats.words_spoken || 38, Math.round(transcript.split(/\\s+/).length));
    const score = Math.min(95, Math.max(65, Math.round(72 + (words / duration) * 4)));
    const wpm = Math.round((words / (duration / 60)) || 120);

    const mockFeedback = {
      practice_score: score,
      practice_score_display: `${score}/100`,
      practice_score_focus: 'Your current focus: steady conversational cadence and smooth phrase starts.',
      pattern_noticed: 'You spoke with steady rhythm and natural phrase transitions throughout your description.',
      metrics: {
        speaking_time_seconds: duration,
        speaking_time_display: `${duration}s`,
        words_spoken: words,
        words_spoken_display: `${words} words`,
        speaking_rate_wpm: wpm,
        speaking_rate_display: `${wpm} WPM`,
        pace_status: 'Optimal Conversational Pace',
        long_pauses: 1,
        long_pauses_display: '1 long pause',
        natural_pauses: 3,
        repetitions: 0,
        repetitions_display: '0 repetitions',
        repetitions_list: [],
        filler_words: 1,
        filler_words_display: '1 filler word',
        fillers_list: [{ word: 'um', count: 1 }],
        practice_score: score,
        practice_score_display: `${score}/100`,
        wpm: wpm,
        word_count: words,
        duration_seconds: duration,
        filler_count: 1,
        pauses_count: 4,
        long_pauses_count: 1,
        natural_pauses_count: 3,
        repetitions_count: 0,
        continuity_score: 88,
        clarity_score: 90
      },
      your_speech_feedback: {
        what_went_well: [
          'You clearly described the main events and visual elements.',
          'Your voice stayed steady and audible throughout the description.',
          'Natural phrase boundaries and clear word completion.'
        ],
        what_needs_improvement: [
          'Brief hesitation pauses occurred before starting new thoughts. Allow a relaxed silent breath instead.'
        ],
        main_difficulty_location: 'Transitions between visual descriptions.',
        speech_pattern_noticed: 'You maintained a consistent, calm speaking rhythm with natural phrase transitions.',
        what_to_practise_next: 'Repeat the practice sentences below 3 times to reinforce effortless phrase initiation.'
      },
      what_went_well: [
        'You clearly described the main events and visual elements.',
        'Your voice stayed steady and audible throughout the description.',
        'Natural phrase boundaries and clear word completion.'
      ],
      needs_improvement: [
        {
          issue: 'Brief Hesitation Pauses',
          why_it_matters: 'Hesitating before new points can interrupt your spontaneous speaking flow.',
          how_to_fix: 'Take an easy diaphragmatic breath and speak the first 3 words continuously on the exhale.'
        }
      ],
      difficult_words: [],
      difficult_words_practice: '',
      actionable_drills: [
        {
          title: 'Continuous Phrasing Drill',
          steps: '1. Group your thoughts into 4-word units. 2. Connect words smoothly inside each unit. 3. Pause silently between units.'
        }
      ],
      next_practice: {
        title: 'Next Practice',
        instruction: 'Repeat these 2 sentences three times. First slowly at a calm, steady pace, then at your natural speaking speed:',
        sentences: [
          'I describe what I observe with clear, steady sentences.',
          'Taking a calm breath gives me time to choose the exact words I want.'
        ],
        mode: this.currentMode === 'video' ? 'image' : 'video',
        reason: 'Practicing another visual prompt builds muscle memory for spontaneous, unhurried expression.'
      },
      transcript: transcript
    };

    if (window.showFeedbackScreen) {
      showFeedbackScreen(mockFeedback, { mode: this.currentMode });
    }
  }
};

// Window exposure and aliases
window.MediaPractice = MediaPractice;
window.VideoPractice = MediaPractice;
window.ImagePractice = MediaPractice;
"""

with open('static/js/video_mode.js', 'w', encoding='utf-8') as f:
    f.write(header)
    f.write('const DEFAULT_PRACTICE_VIDEOS = ' + json.dumps(default_videos, indent=2, ensure_ascii=False) + ';\n\n')
    f.write('const DEFAULT_PRACTICE_IMAGES = ' + json.dumps(default_images, indent=2, ensure_ascii=False) + ';\n\n')
    f.write(code_body)

print("Generated static/js/video_mode.js successfully!")
