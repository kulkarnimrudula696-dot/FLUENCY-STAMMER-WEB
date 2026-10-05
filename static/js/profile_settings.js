/**
 * FLUENCY Profile & Settings Management
 * Handles Profile details, Age personalization, Mascot selector (8 mascots),
 * Themes, AI preferences, and API configuration.
 */

const ProfileSettings = {
  isInitialized: false,

  init() {
    if (!this.isInitialized) {
      this.bindEvents();
      this.isInitialized = true;
    }
    this.renderAvatarsGrid();
    this.renderMascotsGrid();
  },

  bindEvents() {
    // Save Profile Form
    document.getElementById('profile-form')?.addEventListener('submit', (e) => {
      e.preventDefault();
      this.saveProfile();
    });

    // Save Settings Form
    document.getElementById('settings-form')?.addEventListener('submit', (e) => {
      e.preventDefault();
      this.saveSettings();
    });

    // Practice Age Slider sync
    const ageRange = document.getElementById('setting-practice-age-range');
    const ageVal = document.getElementById('setting-practice-age-val');
    if (ageRange && ageVal) {
      ageRange.addEventListener('input', (e) => {
        ageVal.innerText = `${e.target.value} years`;
      });
    }
  },

  // ---------------------------------------------------------------------------
  // AVATAR SELECTION SYSTEM
  // ---------------------------------------------------------------------------
  renderAvatarsGrid() {
    const container = document.getElementById('profile-avatars-grid');
    if (!container || !window.AvatarEngine) return;

    const currentAvatarId = (AppState.user && AppState.user.selected_avatar) 
      || document.getElementById('profile-input-avatar')?.value 
      || 'avatar-sunny';

    container.innerHTML = AvatarEngine.avatars.map(a => {
      const isSelected = a.id === currentAvatarId;
      const svgMarkup = a.render(54);
      return `
        <div class="avatar-choice-card ${isSelected ? 'active' : ''}" 
             id="avatar-card-${a.id}" 
             onclick="ProfileSettings.selectAvatar('${a.id}')" 
             style="background: var(--surface-white); border: 2.5px solid ${isSelected ? 'var(--brand-brown)' : 'var(--border-subtle)'}; border-radius: var(--radius-lg); padding: 12px 6px; text-align: center; cursor: pointer; transition: all var(--transition-fast); position: relative; box-shadow: ${isSelected ? '0 4px 14px rgba(61,43,36,0.15)' : 'var(--shadow-sm)'};">
          ${isSelected ? '<div class="avatar-check-badge" style="position: absolute; top: 6px; right: 6px; background: var(--brand-brown); color: #FFF; width: 18px; height: 18px; border-radius: 50%; font-size: 10px; display: flex; align-items: center; justify-content: center;"><i class="fa-solid fa-check"></i></div>' : ''}
          <div style="margin-bottom: 6px; display: flex; justify-content: center;">
            ${svgMarkup}
          </div>
          <div style="font-weight: 800; font-size: 0.88rem; color: var(--text-dark); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${a.name}</div>
          <div style="font-size: 0.72rem; color: var(--text-muted); margin-top: 2px;">${a.tagline}</div>
        </div>
      `;
    }).join('');

    this.updateAvatarPreview(currentAvatarId);
  },

  selectAvatar(avatarId) {
    const input = document.getElementById('profile-input-avatar');
    if (input) input.value = avatarId;

    if (window.AppState && AppState.user) {
      AppState.user.selected_avatar = avatarId;
    }
    localStorage.setItem('fluency_selected_avatar', avatarId);

    const avatar = window.AvatarEngine ? AvatarEngine.getAvatar(avatarId) : null;
    const nameLabel = document.getElementById('profile-selected-avatar-name');
    if (nameLabel && avatar) {
      nameLabel.innerText = `Selected: ${avatar.name}`;
    }

    // Update highlight styles
    document.querySelectorAll('.avatar-choice-card').forEach(card => {
      card.style.borderColor = 'var(--border-subtle)';
      card.style.boxShadow = 'var(--shadow-sm)';
      card.classList.remove('active');
      const badge = card.querySelector('.avatar-check-badge');
      if (badge) badge.remove();
    });

    const activeCard = document.getElementById(`avatar-card-${avatarId}`);
    if (activeCard) {
      activeCard.style.borderColor = 'var(--brand-brown)';
      activeCard.style.boxShadow = '0 4px 14px rgba(61,43,36,0.15)';
      activeCard.classList.add('active');
      const badge = document.createElement('div');
      badge.className = 'avatar-check-badge';
      badge.style.cssText = 'position: absolute; top: 6px; right: 6px; background: var(--brand-brown); color: #FFF; width: 18px; height: 18px; border-radius: 50%; font-size: 10px; display: flex; align-items: center; justify-content: center;';
      badge.innerHTML = '<i class="fa-solid fa-check"></i>';
      activeCard.appendChild(badge);
    }

    this.updateAvatarPreview(avatarId);

    // Instant real-time synchronization with Sidebar and Conversation Mode
    if (window.AppState && AppState.updateUserUI) {
      AppState.updateUserUI();
    }
    if (window.ConversationPractice && ConversationPractice.updateUserIdentity) {
      ConversationPractice.updateUserIdentity();
    }
  },

  highlightActiveAvatar(avatarId) {
    const input = document.getElementById('profile-input-avatar');
    if (input) input.value = avatarId;

    const avatar = window.AvatarEngine ? AvatarEngine.getAvatar(avatarId) : null;
    const nameLabel = document.getElementById('profile-selected-avatar-name');
    if (nameLabel && avatar) {
      nameLabel.innerText = `Selected: ${avatar.name}`;
    }

    document.querySelectorAll('.avatar-choice-card').forEach(card => {
      card.style.borderColor = 'var(--border-subtle)';
      card.style.boxShadow = 'var(--shadow-sm)';
      card.classList.remove('active');
      const badge = card.querySelector('.avatar-check-badge');
      if (badge) badge.remove();
    });

    const activeCard = document.getElementById(`avatar-card-${avatarId}`);
    if (activeCard) {
      activeCard.style.borderColor = 'var(--brand-brown)';
      activeCard.style.boxShadow = '0 4px 14px rgba(61,43,36,0.15)';
      activeCard.classList.add('active');
      const badge = document.createElement('div');
      badge.className = 'avatar-check-badge';
      badge.style.cssText = 'position: absolute; top: 6px; right: 6px; background: var(--brand-brown); color: #FFF; width: 18px; height: 18px; border-radius: 50%; font-size: 10px; display: flex; align-items: center; justify-content: center;';
      badge.innerHTML = '<i class="fa-solid fa-check"></i>';
      activeCard.appendChild(badge);
    }

    this.updateAvatarPreview(avatarId);
  },

  updateAvatarPreview(avatarId) {
    const previewEl = document.getElementById('profile-avatar-live-preview');
    if (previewEl && window.AvatarEngine) {
      previewEl.innerHTML = AvatarEngine.render(avatarId, 64);
    }
  },

  populateProfileForm(user) {
    if (!user) return;

    const setVal = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.value = val !== undefined && val !== null ? val : '';
    };

    setVal('profile-input-name', user.name || '');
    setVal('profile-input-email', user.email || '');
    setVal('profile-input-actual-age', user.actual_age || 21);
    setVal('profile-input-practice-age', user.practice_age || 21);
    setVal('profile-input-birthdate', user.birthdate || '');
    setVal('profile-input-phone', user.phone || '');
    setVal('profile-input-bio', user.bio || '');
    
    // Avatar selection
    const userAvatar = user.selected_avatar || 'avatar-sunny';
    setVal('profile-input-avatar', userAvatar);
    this.highlightActiveAvatar(userAvatar);

    const userLang = user.preferred_language || 'English';
    const profileLangSelect = document.getElementById('profile-input-lang');
    if (profileLangSelect) profileLangSelect.value = userLang;
    
    const settingLangSelect = document.getElementById('setting-language');
    if (settingLangSelect) settingLangSelect.value = userLang;

    // Age Group selectors
    const ageGroup = user.age_group || '18-23';
    const profileAgeGroupSelect = document.getElementById('profile-input-age-group');
    if (profileAgeGroupSelect) profileAgeGroupSelect.value = ageGroup;

    const settingAgeGroupSelect = document.getElementById('setting-age-group');
    if (settingAgeGroupSelect) settingAgeGroupSelect.value = ageGroup;

    // Settings fields
    const mascotInput = document.getElementById('setting-selected-mascot');
    if (mascotInput) mascotInput.value = user.selected_mascot || 'otter';

    const themeInput = document.getElementById('setting-theme');
    if (themeInput) themeInput.value = user.theme_preference || 'warm_cream';

    const personaInput = document.getElementById('setting-ai-persona');
    if (personaInput) personaInput.value = user.ai_persona || 'supportive_alex';

    const styleInput = document.getElementById('setting-ai-style');
    if (styleInput) styleInput.value = user.ai_speaking_style || 'gentle';

    const rigorInput = document.getElementById('setting-ai-rigor');
    if (rigorInput) rigorInput.value = user.ai_feedback_rigor || 'balanced';

    this.highlightActiveMascot(user.selected_mascot || 'otter');
  },

  async renderMascotsGrid() {
    const container = document.getElementById('mascots-selection-grid');
    if (!container) return;

    try {
      const res = await fetch('/api/content/mascots');
      const data = await res.json();
      const mascots = data.mascots || [];

      const currentMascot = AppState.user ? AppState.user.selected_mascot : 'otter';

      container.innerHTML = mascots.map(m => {
        const svgMarkup = MascotEngine.render(m.id, 'smiling', 75);
        const isSelected = m.id === currentMascot;
        return `
          <div class="mascot-choice-card ${isSelected ? 'active' : ''}" id="mascot-card-${m.id}" onclick="ProfileSettings.selectMascot('${m.id}')" style="background: var(--surface-white); border: 2px solid ${isSelected ? 'var(--brand-brown)' : 'var(--border-subtle)'}; border-radius: var(--radius-lg); padding: 20px; text-align: center; cursor: pointer; transition: all var(--transition-fast);">
            <div style="margin-bottom: 10px; display: flex; justify-content: center;">
              ${svgMarkup}
            </div>
            <div style="font-weight: 800; font-size: 1.05rem; color: var(--text-dark);">${m.name}</div>
            <div style="font-size: 0.8rem; font-weight: 800; color: var(--brand-brown); margin: 4px 0;">${m.badge}</div>
            <div style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">${m.tagline}</div>
          </div>
        `;
      }).join('');
    } catch (err) {
      console.error("Failed to load mascots grid:", err);
    }
  },

  selectMascot(mascotId) {
    document.querySelectorAll('.mascot-choice-card').forEach(card => {
      card.style.borderColor = 'var(--border-subtle)';
      card.classList.remove('active');
    });

    const activeCard = document.getElementById(`mascot-card-${mascotId}`);
    if (activeCard) {
      activeCard.style.borderColor = 'var(--brand-brown)';
      activeCard.classList.add('active');
    }

    const input = document.getElementById('setting-selected-mascot');
    if (input) input.value = mascotId;

    showToast(`Mascot set to ${mascotId.replace('_', ' ').toUpperCase()}. Click Save Settings to apply.`, "info");
  },

  highlightActiveMascot(mascotId) {
    document.querySelectorAll('.mascot-choice-card').forEach(card => {
      card.style.borderColor = 'var(--border-subtle)';
      card.classList.remove('active');
    });
    const activeCard = document.getElementById(`mascot-card-${mascotId}`);
    if (activeCard) {
      activeCard.style.borderColor = 'var(--brand-brown)';
      activeCard.classList.add('active');
    }
  },

  async saveProfile() {
    const payload = {
      name: document.getElementById('profile-input-name').value.trim(),
      selected_avatar: document.getElementById('profile-input-avatar')?.value || 'avatar-sunny',
      age_group: document.getElementById('profile-input-age-group')?.value || '18-23',
      birthdate: document.getElementById('profile-input-birthdate').value,
      phone: document.getElementById('profile-input-phone').value.trim(),
      bio: document.getElementById('profile-input-bio').value.trim(),
      preferred_language: document.getElementById('profile-input-lang').value
    };

    try {
      const res = await fetch('/api/user/profile', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (data.user) {
        AppState.user = data.user;
        localStorage.setItem('fluency_selected_avatar', data.user.selected_avatar || 'avatar-sunny');
        localStorage.setItem('fluency_user_name', data.user.name || 'You');
        if (window.FluencyI18n) {
          FluencyI18n.setLanguage(payload.preferred_language, false);
        }
        AppState.updateUserUI();
        if (window.ConversationPractice && ConversationPractice.updateUserIdentity) {
          ConversationPractice.updateUserIdentity();
        }
        showToast("Profile details updated successfully.", "success");
      }
    } catch (err) {
      console.error("Profile save error:", err);
      showToast("Failed to save profile.", "error");
    }
  },

  async saveSettings() {
    const langVal = document.getElementById('setting-language')?.value || 'English';
    const payload = {
      selected_mascot: document.getElementById('setting-selected-mascot').value,
      theme_preference: document.getElementById('setting-theme').value,
      ai_persona: document.getElementById('setting-ai-persona').value,
      ai_speaking_style: document.getElementById('setting-ai-style').value,
      ai_feedback_rigor: document.getElementById('setting-ai-rigor').value,
      age_group: document.getElementById('setting-age-group')?.value || '18-23',
      preferred_language: langVal,
      custom_api_key: document.getElementById('setting-custom-api-key')?.value.trim() || ''
    };

    try {
      const res = await fetch('/api/user/settings', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (data.user) {
        AppState.user = data.user;
        if (window.FluencyI18n) {
          FluencyI18n.setLanguage(langVal, false);
        }
        AppState.updateUserUI();
        showToast("Personalization settings updated.", "success");
      }
    } catch (err) {
      console.error("Settings save error:", err);
      showToast("Failed to save settings.", "error");
    }
  }
};
