/**
 * FLUENCY — Main Application Controller & Single-Page Router
 * Tagline: "Practice your voice. Build your confidence."
 */

const AppState = {
  user: null,
  currentRoute: 'dashboard',
  quotes: [],

  init() {
    // Initialize Internationalization
    if (window.FluencyI18n) {
      FluencyI18n.init();
    }

    this.bindGlobalEvents();
    this.checkAuth();
    this.loadQuotes();
  },

  toggleSidebar() {
    document.body.classList.toggle('sidebar-open');
  },

  closeSidebar() {
    document.body.classList.remove('sidebar-open');
  },

  closeMobileSidebar() {
    this.closeSidebar();
  },

  async checkAuth() {
    try {
      const res = await fetch('/api/auth/me');
      const data = await res.json();
      if (data.authenticated && data.user) {
        this.user = data.user;
        this.hideAuthModal();
        if (this.user.preferred_language) {
          localStorage.setItem('fluency_language', this.user.preferred_language);
        }
        if (this.user.selected_avatar) {
          localStorage.setItem('fluency_selected_avatar', this.user.selected_avatar);
        }
        if (this.user.name) {
          localStorage.setItem('fluency_user_name', this.user.name);
        }
        if (window.FluencyI18n && this.user.preferred_language) {
          FluencyI18n.setLanguage(this.user.preferred_language, false);
        }
        this.updateUserUI();
        if (window.ProfileSettings) {
          ProfileSettings.populateProfileForm(this.user);
        }
        if (this.user.is_admin || this.user.role === 'admin') {
          this.navigateTo('admin-dashboard');
        } else {
          this.navigateTo('dashboard');
        }
      } else {
        this.showAuthModal();
      }
    } catch (err) {
      console.error("Auth check failed:", err);
      this.showAuthModal();
    }
  },

  updateUserUI() {
    if (!this.user) return;

    const isAdmin = Boolean(this.user.is_admin || this.user.role === 'admin');

    // Sidebar Admin Button visibility
    const adminNavBtn = document.getElementById('sidebar-nav-admin');
    if (adminNavBtn) {
      adminNavBtn.style.display = isAdmin ? 'flex' : 'none';
    }

    // Language Sync
    if (window.FluencyI18n && this.user.preferred_language) {
      FluencyI18n.setLanguage(this.user.preferred_language, false);
    }

    if (isAdmin) {
      // Header for Admin
      const headerName = document.getElementById('header-user-name');
      if (headerName) headerName.innerHTML = `Admin: ${this.user.name} 🛡️`;
      const headerTag = document.getElementById('header-practice-age-tag');
      if (headerTag) headerTag.innerText = `Role: Administrator`;
      
      // Mini Profile in Sidebar
      const sidebarName = document.getElementById('sidebar-user-name');
      if (sidebarName) sidebarName.innerText = this.user.name;
      const sidebarRole = document.getElementById('sidebar-user-role');
      if (sidebarRole) sidebarRole.innerText = `Admin Access`;
      const sidebarAvatarEl = document.getElementById('sidebar-user-avatar');
      if (sidebarAvatarEl && window.AvatarEngine) {
        sidebarAvatarEl.innerHTML = AvatarEngine.render(this.user.selected_avatar || 'avatar-spark', 38);
      }

      // Mascots in Sidebar & Top
      if (window.MascotEngine) {
        const mascotSvgMini = MascotEngine.render('otter', 'smiling', 36);
        const sideMascot = document.getElementById('sidebar-mascot-avatar');
        if (sideMascot) sideMascot.innerHTML = mascotSvgMini;
        const headMascot = document.getElementById('header-mascot-badge');
        if (headMascot) headMascot.innerHTML = MascotEngine.render('otter', 'waving', 42);
      }
      return;
    }

    // Normal User UI Update
    document.getElementById('header-user-name').innerText = `Welcome, ${this.user.name.split(' ')[0]} 👋`;
    document.getElementById('header-practice-age-tag').innerText = `Age Group: ${this.user.age_group || '18–23'}`;
    
    // Mini Profile in Sidebar
    document.getElementById('sidebar-user-name').innerText = this.user.name;
    document.getElementById('sidebar-user-role').innerText = `Age: ${this.user.age_group || '18–23'}`;
    const sidebarAvatarEl = document.getElementById('sidebar-user-avatar');
    if (sidebarAvatarEl && window.AvatarEngine) {
      sidebarAvatarEl.innerHTML = AvatarEngine.render(this.user.selected_avatar || 'avatar-sunny', 38);
    }

    // Mascots in Sidebar & Top
    const mascotSvgMini = MascotEngine.render(this.user.selected_mascot || 'otter', 'smiling', 36);
    document.getElementById('sidebar-mascot-avatar').innerHTML = mascotSvgMini;
    document.getElementById('header-mascot-badge').innerHTML = MascotEngine.render(this.user.selected_mascot || 'otter', 'waving', 42);

    // Dashboard Mascot Greeting
    const dashMascotContainer = document.getElementById('dashboard-mascot-container');
    if (dashMascotContainer) {
      dashMascotContainer.innerHTML = MascotEngine.render(this.user.selected_mascot || 'otter', 'waving', 150);
    }

    // Dashboard Welcome Title
    const welcomeTitle = document.getElementById('dashboard-welcome-title');
    if (welcomeTitle) {
      welcomeTitle.innerText = `Welcome back, ${this.user.name.split(' ')[0]}!`;
    }

    // Update Profile Forms
    if (window.ProfileSettings) {
      ProfileSettings.populateProfileForm(this.user);
    }

    // Sync Conversation Mode User PiP Avatar & Name
    if (window.ConversationPractice && ConversationPractice.updateUserIdentity) {
      ConversationPractice.updateUserIdentity();
    }

    // Refresh Reading Practice content cache on age group changes
    if (window.ReadingPractice) {
      ReadingPractice.contentCache = {};
      ReadingPractice.passageIndexMap = {};
      if (document.getElementById('screen-reading')?.style.display !== 'none') {
        ReadingPractice.loadContent(false);
      }
    }
  },

  showAuthModal() {
    const modal = document.getElementById('auth-modal-overlay');
    if (modal) modal.style.display = 'flex';
  },

  hideAuthModal() {
    const modal = document.getElementById('auth-modal-overlay');
    if (modal) modal.style.display = 'none';
  },

  bindGlobalEvents() {
    // Navigation links in Sidebar
    document.querySelectorAll('[data-route]').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const route = link.dataset.route;
        this.navigateTo(route);
      });
    });

    // Menu / Three-dots Sidebar Toggle Button
    const sidebarToggleBtn = document.getElementById('btn-sidebar-toggle') || document.getElementById('btn-mobile-menu');
    if (sidebarToggleBtn) {
      sidebarToggleBtn.addEventListener('click', (e) => {
        e.preventDefault();
        this.toggleSidebar();
      });
    }

    // Backdrop click to close on mobile
    const backdrop = document.getElementById('sidebar-backdrop');
    if (backdrop) {
      backdrop.addEventListener('click', () => {
        this.closeMobileSidebar();
      });
    }

    // Auth Form Tabs (Login vs Register)
    document.getElementById('tab-btn-login')?.addEventListener('click', () => {
      document.getElementById('tab-btn-login').classList.add('active');
      document.getElementById('tab-btn-register').classList.remove('active');
      document.getElementById('auth-login-form').style.display = 'block';
      document.getElementById('auth-register-form').style.display = 'none';
    });

    document.getElementById('tab-btn-register')?.addEventListener('click', () => {
      document.getElementById('tab-btn-register').classList.add('active');
      document.getElementById('tab-btn-login').classList.remove('active');
      document.getElementById('auth-register-form').style.display = 'block';
      document.getElementById('auth-login-form').style.display = 'none';
    });

    // Password visibility toggles
    document.querySelectorAll('.btn-toggle-pwd').forEach(btn => {
      btn.addEventListener('click', () => {
        const input = btn.parentElement.querySelector('input');
        if (input.type === 'password') {
          input.type = 'text';
          btn.innerHTML = `<i class="fa-solid fa-eye-slash"></i>`;
        } else {
          input.type = 'password';
          btn.innerHTML = `<i class="fa-solid fa-eye"></i>`;
        }
      });
    });

    // Login Form Submit
    document.getElementById('auth-login-form')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email').value.trim();
      const password = document.getElementById('login-password').value.trim();

      try {
        const res = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (data.user) {
          this.user = data.user;
          this.hideAuthModal();
          if (this.user.preferred_language) {
            localStorage.setItem('fluency_language', this.user.preferred_language);
          }
          if (this.user.selected_avatar) {
            localStorage.setItem('fluency_selected_avatar', this.user.selected_avatar);
          }
          if (this.user.name) {
            localStorage.setItem('fluency_user_name', this.user.name);
          }
          if (window.FluencyI18n && this.user.preferred_language) {
            FluencyI18n.setLanguage(this.user.preferred_language, false);
          }
          this.updateUserUI();
          if (window.ProfileSettings) {
            ProfileSettings.populateProfileForm(this.user);
          }
          if (data.is_admin || data.role === 'admin' || this.user.is_admin) {
            this.navigateTo('admin-dashboard');
            showToast("Welcome to Administrator Control Center!", "success");
          } else {
            this.navigateTo('dashboard');
            showToast(`Welcome back, ${this.user.name}!`, "success");
          }
        } else {
          showToast(data.error || "Invalid login credentials.", "error");
        }
      } catch (err) {
        showToast("Network error during login.", "error");
      }
    });

    // Register Form Submit
    document.getElementById('auth-register-form')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('reg-name').value.trim();
      const email = document.getElementById('reg-email').value.trim();
      const age_group = document.getElementById('reg-age-group')?.value || '18-23';
      const actual_age = parseInt(document.getElementById('reg-actual-age').value) || 21;
      const practice_age = actual_age;
      const birthdate = document.getElementById('reg-birthdate').value;
      const password = document.getElementById('reg-password').value.trim();

      try {
        const res = await fetch('/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, email, age_group, actual_age, practice_age, birthdate, password })
        });
        const data = await res.json();
        if (data.user) {
          this.user = data.user;
          this.hideAuthModal();
          if (this.user.preferred_language) {
            localStorage.setItem('fluency_language', this.user.preferred_language);
          }
          if (this.user.selected_avatar) {
            localStorage.setItem('fluency_selected_avatar', this.user.selected_avatar);
          }
          if (this.user.name) {
            localStorage.setItem('fluency_user_name', this.user.name);
          }
          if (window.FluencyI18n && this.user.preferred_language) {
            FluencyI18n.setLanguage(this.user.preferred_language, false);
          }
          this.updateUserUI();
          if (window.ProfileSettings) {
            ProfileSettings.populateProfileForm(this.user);
          }
          this.navigateTo('dashboard');
          showToast("Account created! Let's practice your voice.", "success");
        } else {
          showToast(data.error || "Registration failed.", "error");
        }
      } catch (err) {
        showToast("Network error during registration.", "error");
      }
    });

    // Quick Demo Sign In
    document.getElementById('btn-demo-login')?.addEventListener('click', async () => {
      try {
        const res = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: "buddy@fluency.com", password: "practice123" })
        });
        const data = await res.json();
        if (data.user) {
          this.user = data.user;
          this.hideAuthModal();
          if (this.user.preferred_language) {
            localStorage.setItem('fluency_language', this.user.preferred_language);
          }
          if (this.user.selected_avatar) {
            localStorage.setItem('fluency_selected_avatar', this.user.selected_avatar);
          }
          if (this.user.name) {
            localStorage.setItem('fluency_user_name', this.user.name);
          }
          if (window.FluencyI18n && this.user.preferred_language) {
            FluencyI18n.setLanguage(this.user.preferred_language, false);
          }
          this.updateUserUI();
          if (window.ProfileSettings) {
            ProfileSettings.populateProfileForm(this.user);
          }
          this.navigateTo('dashboard');
          showToast("Logged in as Demo Practice Buddy.", "success");
        }
      } catch (err) {
        showToast("Demo sign in failed.", "error");
      }
    });

    // Logout
    document.querySelectorAll('.btn-action-logout').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();
        await fetch('/api/auth/logout', { method: 'POST' });
        this.user = null;
        localStorage.removeItem('fluency_language');
        localStorage.removeItem('fluency_selected_avatar');
        localStorage.removeItem('fluency_user_name');
        if (window.ProfileSettings) {
          ProfileSettings.clearProfileForm();
        }
        if (window.FluencyI18n) {
          FluencyI18n.setLanguage('English', false);
        }
        this.showAuthModal();
        showToast("You have been safely logged out.", "info");
      });
    });
  },

  statsCache: null,
  statsCacheTime: 0,

  invalidateStatsCache() {
    this.statsCache = null;
    this.statsCacheTime = 0;
    if (window.ProgressEngine?.invalidateCache) {
      ProgressEngine.invalidateCache();
    }
  },

  async loadQuotes() {
    if (this.quotes && this.quotes.length > 0) {
      this.renderRandomQuote();
      return;
    }
    try {
      const res = await fetch('/api/content/quotes');
      const data = await res.json();
      this.quotes = data.quotes || [];
      this.renderRandomQuote();
    } catch (err) {}
  },

  renderRandomQuote() {
    if (this.quotes && this.quotes.length > 0) {
      const q = this.quotes[Math.floor(Math.random() * this.quotes.length)];
      const quoteEl = document.getElementById('dashboard-motivational-quote');
      if (quoteEl) {
        quoteEl.innerText = `“${q.quote}”`;
      }
    }
  },

  navigateTo(route) {
    const prevRoute = this.currentRoute;
    this.currentRoute = route;

    // Clean up active streams / recording on previous route if switching away
    if (prevRoute && prevRoute !== route) {
      if (prevRoute === 'breath' && window.BreathingPractice?.cleanup) BreathingPractice.cleanup();
      if (prevRoute === 'reading' && window.ReadingPractice?.cleanup) ReadingPractice.cleanup();
      if ((prevRoute === 'twister' || prevRoute === 'tongue-twister' || prevRoute === 'tongue_twister') && window.TongueTwisterPractice?.cleanup) TongueTwisterPractice.cleanup();
      if ((prevRoute === 'video' || prevRoute === 'media' || prevRoute === 'image') && window.MediaPractice?.cleanup) MediaPractice.cleanup();
      if (prevRoute === 'therapy' && window.TherapyVideos?.cleanup) TherapyVideos.cleanup();
      if (prevRoute === 'conversation' && window.ConversationPractice?.cleanup) ConversationPractice.cleanup();
    }

    // Close mobile menu if open
    this.closeMobileSidebar();

    // Hide all view screens
    document.querySelectorAll('.app-screen-view').forEach(screen => {
      screen.style.display = 'none';
    });

    // Highlight sidebar active item
    document.querySelectorAll('.nav-item').forEach(item => {
      item.classList.toggle('active', item.dataset.route === route);
    });

    // Show target screen (support video/image/media/therapy/twister aliases)
    let targetScreen = document.getElementById(`screen-${route}`);
    if (!targetScreen && (route === 'video' || route === 'media' || route === 'image')) {
      targetScreen = document.getElementById('screen-video') || document.getElementById('screen-media');
    }
    if (!targetScreen && (route === 'tongue-twister' || route === 'twister' || route === 'tongue_twister')) {
      targetScreen = document.getElementById('screen-tongue-twister');
    }
    if (!targetScreen && (route === 'therapy-videos' || route === 'therapy_videos')) {
      targetScreen = document.getElementById('screen-therapy');
    }
    if (targetScreen) {
      targetScreen.style.display = 'block';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Apply translations to current view
    if (window.FluencyI18n) {
      FluencyI18n.applyToDOM();
    }

    // Initialize sub-controllers based on route
    if (route === 'dashboard') {
      this.loadDashboardStats();
      this.updateUserUI();
    } else if (route === 'breath') {
      BreathingPractice.init();
    } else if (route === 'reading') {
      ReadingPractice.init();
    } else if (route === 'tongue-twister' || route === 'twister' || route === 'tongue_twister') {
      if (window.TongueTwisterPractice) {
        TongueTwisterPractice.init();
      }
    } else if (route === 'video' || route === 'media' || route === 'image') {
      if (window.MediaPractice) {
        MediaPractice.init();
        if (route === 'image') {
          MediaPractice.switchMode('image');
        } else {
          MediaPractice.switchMode('video');
        }
      }
    } else if (route === 'therapy' || route === 'therapy-videos') {
      if (window.TherapyVideos) {
        TherapyVideos.init();
      }
    } else if (route === 'conversation') {
      ConversationPractice.init();
    } else if (route === 'progress') {
      ProgressEngine.init();
    } else if (route === 'profile' || route === 'settings') {
      ProfileSettings.init();
      if (route === 'profile') {
        ProfileSettings.loadProfile();
      }
    } else if (route === 'bug') {
      BugReportModule.init();
    } else if (route === 'admin-dashboard' || route === 'admin') {
      if (window.AdminController) {
        AdminController.loadDashboard();
      }
    }

  },

  async loadDashboardStats(force = false) {
    const now = Date.now();
    if (!force && this.statsCache && (now - this.statsCacheTime < 20000)) {
      this.populateDashboardStatsUI(this.statsCache);
      return;
    }

    try {
      const res = await fetch('/api/practice/progress-stats');
      const data = await res.json();
      this.statsCache = data;
      this.statsCacheTime = now;
      this.populateDashboardStatsUI(data);
    } catch (err) {}
  },

  populateDashboardStatsUI(data) {
    const streakEl = document.getElementById('dash-streak-count');
    const practiceDaysEl = document.getElementById('dash-practice-days');
    const weeklyTimeEl = document.getElementById('dash-weekly-time');
    const sessionsEl = document.getElementById('dash-sessions-count');
    const improvEl = document.getElementById('dash-improvement-note');
    const headerStreak = document.getElementById('header-streak-count');

    if (streakEl) streakEl.innerText = `${data.streak} Days`;
    if (practiceDaysEl) practiceDaysEl.innerText = `${data.total_practice_days} Practice Days`;
    if (weeklyTimeEl) weeklyTimeEl.innerText = `${data.weekly_minutes}m`;
    if (sessionsEl) sessionsEl.innerText = data.total_sessions;
    if (improvEl) improvEl.innerText = data.improvement_summary;
    if (headerStreak) headerStreak.innerText = `${data.streak} Days`;
  }
};

/**
 * Universal Toast Notification Function
 */
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;

  const icons = {
    success: 'fa-circle-check',
    error: 'fa-circle-exclamation',
    warning: 'fa-triangle-exclamation',
    info: 'fa-circle-info'
  };

  toast.innerHTML = `
    <i class="fa-solid ${icons[type] || 'fa-circle-info'}" style="font-size: 20px;"></i>
    <div style="flex: 1;">${message}</div>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'slideInUp 0.3s ease-out reverse';
    setTimeout(() => toast.remove(), 280);
  }, 4000);
}

/**
 * Universal Feedback Screen Renderer
 * Renders the honest, measurable speech analysis report with data-driven Practice Score
 */
function showFeedbackScreen(feedback, sessionData) {
  const m = feedback.metrics || {};
  const score = m.practice_score !== undefined ? m.practice_score : (m.practice_performance_score !== undefined ? m.practice_performance_score : (m.fluency_score || 0));
  const focusText = feedback.practice_score_focus || "Your current focus: smoother phrase starts and steady conversational rhythm.";

  // Practice Score Ring, Title & Focus
  const scoreEl = document.getElementById('fb-score-val');
  if (scoreEl) scoreEl.innerText = score;

  const titleEl = document.getElementById('fb-score-title');
  if (titleEl) titleEl.innerText = `Practice Score: ${score}/100`;

  const focusEl = document.getElementById('fb-score-focus');
  if (focusEl) focusEl.innerText = focusText;

  const badgeEl = document.getElementById('fb-score-badge');
  if (badgeEl) {
    badgeEl.innerText = `Practice Progress`;
    if (score >= 75) {
      badgeEl.style.background = "#EAF5EE";
      badgeEl.style.color = "#2E7D32";
      badgeEl.style.borderColor = "#C8E6C9";
    } else if (score >= 50) {
      badgeEl.style.background = "#FFF9E6";
      badgeEl.style.color = "#9A633F";
      badgeEl.style.borderColor = "#FFE082";
    } else {
      badgeEl.style.background = "#FFF0F0";
      badgeEl.style.color = "#C0392B";
      badgeEl.style.borderColor = "#FFCDD2";
    }
  }

  // 1. Speaking Time
  const timeEl = document.getElementById('fb-time-val');
  if (timeEl) {
    timeEl.innerText = m.speaking_time_display || (m.duration_seconds ? `${Math.round(m.duration_seconds)}s` : '0s');
  }
  const timeStatusEl = document.getElementById('fb-time-status');
  if (timeStatusEl) {
    timeStatusEl.innerText = m.duration_seconds > 0 ? "Actual duration" : "No speech time";
  }

  // 2. Words Spoken
  const wordsEl = document.getElementById('fb-words-val');
  if (wordsEl) {
    wordsEl.innerText = m.words_spoken_display || `${m.word_count || 0} words`;
  }
  const wordsStatusEl = document.getElementById('fb-words-status');
  if (wordsStatusEl) {
    wordsStatusEl.innerText = (m.word_count > 0) ? "Spoken words" : "Zero detected";
  }

  // 3. Speaking Rate (WPM)
  const wpmEl = document.getElementById('fb-wpm-val');
  if (wpmEl) {
    wpmEl.innerText = m.speaking_rate_display || `${m.wpm || 0} WPM`;
  }
  const paceStatusEl = document.getElementById('fb-pace-status');
  if (paceStatusEl) {
    paceStatusEl.innerText = m.pace_status || "Target Window";
    if (m.wpm >= 85 && m.wpm <= 155) {
      paceStatusEl.style.color = "#3E885B";
    } else if (m.wpm > 175 || (m.wpm < 65 && m.wpm > 0)) {
      paceStatusEl.style.color = "#C0392B";
    } else {
      paceStatusEl.style.color = "var(--text-muted)";
    }
  }

  // 4. Long Pauses
  const pausesEl = document.getElementById('fb-pauses-val');
  if (pausesEl) {
    const longP = m.long_pauses !== undefined ? m.long_pauses : (m.long_pauses_count || 0);
    pausesEl.innerText = m.long_pauses_display || `${longP} long ${longP === 1 ? 'pause' : 'pauses'}`;
  }
  const pausesStatusEl = document.getElementById('fb-pauses-status');
  if (pausesStatusEl) {
    const longP = m.long_pauses !== undefined ? m.long_pauses : (m.long_pauses_count || 0);
    if (longP === 0) {
      const natP = m.natural_pauses !== undefined ? m.natural_pauses : (m.natural_pauses_count || 0);
      pausesStatusEl.innerText = natP > 0 ? `${natP} natural breaths` : "Healthy rhythm";
      pausesStatusEl.style.color = "#3E885B";
    } else {
      pausesStatusEl.innerText = `${longP} pause(s) > 2.0s`;
      pausesStatusEl.style.color = "var(--text-muted)";
    }
  }

  // 5. Repetitions
  const repEl = document.getElementById('fb-repetitions-val');
  if (repEl) {
    const repC = m.repetitions !== undefined ? m.repetitions : (m.repetitions_count || 0);
    repEl.innerText = m.repetitions_display || `${repC} repetition${repC === 1 ? '' : 's'}`;
  }
  const repStatusEl = document.getElementById('fb-repetitions-status');
  if (repStatusEl) {
    const repC = m.repetitions !== undefined ? m.repetitions : (m.repetitions_count || 0);
    if (repC === 0) {
      repStatusEl.innerText = "Clean initiation";
      repStatusEl.style.color = "#3E885B";
    } else {
      const reps = m.repetitions_list || [];
      repStatusEl.innerText = reps.length > 0 ? reps.slice(0, 2).join(', ') : `${repC} flagged`;
      repStatusEl.style.color = "#C0392B";
    }
  }

  // 6. Filler Words
  const fillersEl = document.getElementById('fb-fillers-val');
  if (fillersEl) {
    const fCount = m.filler_words !== undefined ? m.filler_words : (m.filler_count || 0);
    fillersEl.innerText = m.filler_words_display || `${fCount} filler${fCount === 1 ? '' : 's'}`;
  }
  const fillersStatusEl = document.getElementById('fb-fillers-status');
  if (fillersStatusEl) {
    const fCount = m.filler_words !== undefined ? m.filler_words : (m.filler_count || 0);
    if (fCount === 0) {
      fillersStatusEl.innerText = "Zero detected";
      fillersStatusEl.style.color = "#3E885B";
    } else {
      const flist = m.fillers_list || [];
      if (flist.length > 0) {
        fillersStatusEl.innerText = flist.map(f => typeof f === 'object' ? `${f.word} (${f.count}x)` : f).slice(0, 2).join(', ');
      } else {
        fillersStatusEl.innerText = `${fCount} in session`;
      }
      fillersStatusEl.style.color = "var(--text-muted)";
    }
  }

  // Mascot celebratory state & encouragement
  const mascot = AppState.user ? AppState.user.selected_mascot : 'otter';
  const mascotState = score >= 75 ? 'smiling' : (score >= 45 ? 'listening' : 'waving');
  const mascotAvatar = document.getElementById('fb-mascot-avatar');
  if (mascotAvatar) mascotAvatar.innerHTML = MascotEngine.render(mascot, mascotState, 120);

  const mascotEncouragement = document.getElementById('fb-mascot-encouragement');
  if (mascotEncouragement) {
    if (score >= 85) mascotEncouragement.innerText = "Smooth, steady delivery!";
    else if (score >= 60) mascotEncouragement.innerText = "Solid speaking practice!";
    else if (score >= 40) mascotEncouragement.innerText = "Good effort! Let's practise next.";
    else mascotEncouragement.innerText = "Every practice builds confidence.";
  }

  // Pattern I Noticed
  const patternEl = document.getElementById('fb-pattern-noticed');
  if (patternEl) {
    const patternText = feedback.pattern_noticed || 
      (feedback.your_speech_feedback && feedback.your_speech_feedback.speech_pattern_noticed) || 
      "You spoke with steady rhythm and natural phrasing.";
    patternEl.innerText = patternText;
  }

  // Transcript review
  const transReview = document.getElementById('fb-transcript-review');
  if (transReview) {
    const rawTranscript = feedback.transcript || '';
    transReview.innerText = rawTranscript.length > 0 ? `"${rawTranscript}"` : '"[No words detected in this recording]"';
  }

  // Paragraph / Tongue Twister Accuracy & Speech Matching
  const pmCard = document.getElementById('fb-paragraph-match-card');
  if (pmCard) {
    const pm = feedback.paragraph_match;
    if (pm && pm.is_reading_mode) {
      pmCard.style.display = 'block';
      const matchPct = pm.match_percentage !== undefined ? pm.match_percentage : 0;
      const isTwister = pm.is_twister_mode || (sessionData && (sessionData.mode === 'twister' || sessionData.mode === 'tongue_twister'));
      
      const matchBadge = document.getElementById('fb-paragraph-match-badge');
      if (matchBadge) {
        matchBadge.innerText = `${isTwister ? 'Twister Match' : 'Match'}: ${matchPct}%`;
        if (matchPct >= 85) {
          matchBadge.style.background = "#EAF5EE";
          matchBadge.style.color = "#2E7D32";
          matchBadge.style.borderColor = "#C8E6C9";
        } else if (matchPct >= 60) {
          matchBadge.style.background = "#FFF9E6";
          matchBadge.style.color = "#9A633F";
          matchBadge.style.borderColor = "#FFE082";
        } else {
          matchBadge.style.background = "#FFF0F0";
          matchBadge.style.color = "#C0392B";
          matchBadge.style.borderColor = "#FFCDD2";
        }
      }

      const expEl = document.getElementById('fb-match-total-expected');
      if (expEl) expEl.innerText = pm.total_expected_words !== undefined ? pm.total_expected_words : (pm.expected_words_count || 0);

      const matEl = document.getElementById('fb-match-total-matched');
      if (matEl) matEl.innerText = pm.matched_words_count !== undefined ? pm.matched_words_count : 0;

      const misEl = document.getElementById('fb-match-total-missing');
      if (misEl) misEl.innerText = pm.missing_words ? pm.missing_words.length : (pm.missing_words_count || 0);

      const extEl = document.getElementById('fb-match-total-extra');
      if (extEl) extEl.innerText = pm.extra_words ? pm.extra_words.length : (pm.extra_words_count || 0);

      const repEl = document.getElementById('fb-match-total-replaced');
      if (repEl) repEl.innerText = pm.replaced_words ? pm.replaced_words.length : (pm.replaced_words_count || 0);

      const sumEl = document.getElementById('fb-paragraph-match-summary');
      if (sumEl) sumEl.innerText = pm.summary || `Paragraph match score: ${matchPct}%`;

      const detailsEl = document.getElementById('fb-paragraph-match-details');
      if (detailsEl) {
        let detailsHtml = '';
        
        // Extra / Unrelated Words
        if (pm.extra_words && pm.extra_words.length > 0) {
          const extraBadges = pm.extra_words.map(w => `<span style="background: #FFF3E0; color: #D35400; border: 1px solid #FFE082; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.85rem; margin-right: 4px;">+ ${w}</span>`).join(' ');
          detailsHtml += `
            <div style="background: #FFFBF5; border: 1px solid #FFE082; border-radius: var(--radius-sm); padding: 8px 12px;">
              <strong style="color: #D35400; font-size: 0.85rem;"><i class="fa-solid fa-triangle-exclamation"></i> Extra / Unrelated Spoken Words:</strong>
              <div style="margin-top: 4px; display: flex; flex-wrap: wrap; gap: 4px;">${extraBadges}</div>
            </div>
          `;
        }

        // Missing / Skipped Words
        if (pm.missing_words && pm.missing_words.length > 0) {
          const missBadges = pm.missing_words.map(w => `<span style="background: #FFEBEE; color: #C0392B; border: 1px solid #FFCDD2; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.85rem; margin-right: 4px;">- ${w}</span>`).join(' ');
          detailsHtml += `
            <div style="background: #FFFBFB; border: 1px solid #FFCDD2; border-radius: var(--radius-sm); padding: 8px 12px;">
              <strong style="color: #C0392B; font-size: 0.85rem;"><i class="fa-solid fa-circle-xmark"></i> Skipped / Missing Words:</strong>
              <div style="margin-top: 4px; display: flex; flex-wrap: wrap; gap: 4px;">${missBadges}</div>
            </div>
          `;
        }

        // Replaced / Mismatched Words
        if (pm.replaced_words && pm.replaced_words.length > 0) {
          const repBadges = pm.replaced_words.map(r => `<span style="background: #EDE7F6; color: #6A1B9A; border: 1px solid #D1C4E9; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.85rem; margin-right: 4px;">${r.expected} ➔ <em>${r.spoken}</em></span>`).join(' ');
          detailsHtml += `
            <div style="background: #FAF8FD; border: 1px solid #D1C4E9; border-radius: var(--radius-sm); padding: 8px 12px;">
              <strong style="color: #6A1B9A; font-size: 0.85rem;"><i class="fa-solid fa-arrows-rotate"></i> Substituted / Mismatched Words:</strong>
              <div style="margin-top: 4px; display: flex; flex-wrap: wrap; gap: 4px;">${repBadges}</div>
            </div>
          `;
        }

        // Repeated Words / Phrases
        if (pm.repeated_words && pm.repeated_words.length > 0) {
          const repBadges = pm.repeated_words.map(w => `<span style="background: #FFF8E1; color: #F57F17; border: 1px solid #FFE082; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.85rem; margin-right: 4px;">${w}</span>`).join(' ');
          detailsHtml += `
            <div style="background: #FFFDF5; border: 1px solid #FFE082; border-radius: var(--radius-sm); padding: 8px 12px;">
              <strong style="color: #F57F17; font-size: 0.85rem;"><i class="fa-solid fa-repeat"></i> Repeated Words / Phrases:</strong>
              <div style="margin-top: 4px; display: flex; flex-wrap: wrap; gap: 4px;">${repBadges}</div>
            </div>
          `;
        }

        // Wrong Word Order
        if (pm.wrong_order_words && pm.wrong_order_words.length > 0) {
          const woBadges = pm.wrong_order_words.map(w => `<span style="background: #E0F2F1; color: #00695C; border: 1px solid #80CBC4; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.85rem; margin-right: 4px;"><i class="fa-solid fa-arrow-right-arrow-left"></i> ${w}</span>`).join(' ');
          detailsHtml += `
            <div style="background: #F4FBFB; border: 1px solid #80CBC4; border-radius: var(--radius-sm); padding: 8px 12px;">
              <strong style="color: #00695C; font-size: 0.85rem;"><i class="fa-solid fa-arrow-right-arrow-left"></i> Words Spoken Out of Order:</strong>
              <div style="margin-top: 4px; display: flex; flex-wrap: wrap; gap: 4px;">${woBadges}</div>
            </div>
          `;
        }

        detailsEl.innerHTML = detailsHtml;
      }
    } else {
      pmCard.style.display = 'none';
    }
  }

  // What Went Reasonably Well
  const wellList = document.getElementById('fb-what-went-well-list');
  if (wellList) {
    const wellItems = (feedback.your_speech_feedback && feedback.your_speech_feedback.what_went_well) || feedback.what_went_well || [];
    if (wellItems.length > 0) {
      wellList.innerHTML = wellItems.map(item => `
        <li class="feedback-list-item">
          <i class="fa-solid fa-circle-check" style="color: var(--status-success);"></i>
          <span>${item}</span>
        </li>
      `).join('');
    } else {
      wellList.innerHTML = `
        <li class="feedback-list-item">
          <i class="fa-solid fa-circle-check" style="color: var(--status-success);"></i>
          <span>You completed the practice recording session.</span>
        </li>
      `;
    }
  }

  // What Needs Improvement
  const improveContainer = document.getElementById('fb-needs-improvement-box');
  if (improveContainer) {
    if (feedback.needs_improvement && feedback.needs_improvement.length > 0) {
      improveContainer.innerHTML = feedback.needs_improvement.map(issue => `
        <div class="issue-card">
          <div class="issue-card-title"><i class="fa-solid fa-crosshairs"></i> ${issue.issue}</div>
          <div class="issue-card-why"><strong>Why it happens:</strong> ${issue.why_it_matters}</div>
          <div class="issue-card-fix"><strong>How to practise:</strong> ${issue.how_to_fix}</div>
        </div>
      `).join('');
    } else if (feedback.your_speech_feedback && feedback.your_speech_feedback.what_needs_improvement) {
      improveContainer.innerHTML = feedback.your_speech_feedback.what_needs_improvement.map(imp => `
        <div class="issue-card">
          <div class="issue-card-title"><i class="fa-solid fa-crosshairs"></i> Focus Area</div>
          <div class="issue-card-fix">${imp}</div>
        </div>
      `).join('');
    }
  }

  // Main Difficulty Location
  const diffLocationText = document.getElementById('fb-difficulty-location-text');
  if (diffLocationText) {
    const loc = (feedback.your_speech_feedback && feedback.your_speech_feedback.main_difficulty_location) || "Smooth delivery throughout.";
    diffLocationText.innerText = loc;
  }

  // Words to Practise (Only if specific difficult words exist)
  const diffCard = document.getElementById('fb-difficult-words-card');
  const diffContent = document.getElementById('fb-difficult-words-content');
  if (diffCard && diffContent) {
    const diffWords = feedback.difficult_words || [];
    if (diffWords.length > 0) {
      diffCard.style.display = 'block';
      const wordsFormatted = diffWords.map(w => `<strong style="color: var(--brand-brown); background: #FFF0B8; padding: 2px 8px; border-radius: 6px; margin: 0 4px;">${w}</strong>`).join(' ');
      diffContent.innerHTML = `
        <p style="margin-bottom: 8px;">Words to practise: ${wordsFormatted}</p>
        <div style="background: var(--surface-white); padding: 12px 16px; border-radius: var(--radius-sm); border-left: 3px solid #C0392B;">
          <strong>Target Sentence:</strong> "${feedback.next_practice && feedback.next_practice.sentences ? feedback.next_practice.sentences[0] : 'Practice these words slowly with gentle syllable gliding.'}"
        </div>
      `;
    } else {
      diffCard.style.display = 'none';
    }
  }

  // Next Practice Sentences
  const nextSentencesContainer = document.getElementById('fb-next-practice-sentences');
  if (nextSentencesContainer && feedback.next_practice && feedback.next_practice.sentences) {
    nextSentencesContainer.innerHTML = feedback.next_practice.sentences.map((sent, idx) => `
      <div style="background: #FFFFFF; border: 1.5px solid #FFE082; border-radius: var(--radius-md); padding: 16px 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;">
        <div style="flex: 1; min-width: 250px;">
          <div style="font-size: 0.78rem; font-weight: 800; color: var(--brand-brown); text-transform: uppercase; margin-bottom: 4px;">
            Sentence ${idx + 1}
          </div>
          <div style="font-size: 1.05rem; font-weight: 700; color: #3D2B24; line-height: 1.5;">
            "${sent}"
          </div>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;" title="Click each circle as you repeat">
          <span style="font-size: 0.75rem; font-weight: 800; color: var(--text-muted); margin-right: 4px;">3x Reps:</span>
          <button class="btn btn-sm" onclick="this.style.background='#3E885B'; this.style.color='#FFF'; this.innerText='✓ 1';" style="width: 38px; height: 38px; padding: 0; border-radius: 50%; font-size: 0.75rem; font-weight: 800; background: #FFF4DE; border: 1.5px solid #FFE082; color: #9A633F;">1</button>
          <button class="btn btn-sm" onclick="this.style.background='#3E885B'; this.style.color='#FFF'; this.innerText='✓ 2';" style="width: 38px; height: 38px; padding: 0; border-radius: 50%; font-size: 0.75rem; font-weight: 800; background: #FFF4DE; border: 1.5px solid #FFE082; color: #9A633F;">2</button>
          <button class="btn btn-sm" onclick="this.style.background='#3E885B'; this.style.color='#FFF'; this.innerText='✓ 3';" style="width: 38px; height: 38px; padding: 0; border-radius: 50%; font-size: 0.75rem; font-weight: 800; background: #FFF4DE; border: 1.5px solid #FFE082; color: #9A633F;">3</button>
        </div>
      </div>
    `).join('');
  }

  // Actionable Drills
  const drillsGrid = document.getElementById('fb-actionable-drills-grid');
  if (drillsGrid && feedback.actionable_drills) {
    drillsGrid.innerHTML = feedback.actionable_drills.map(drill => `
      <div class="drill-card">
        <div class="drill-card-title"><i class="fa-solid fa-dumbbell"></i> ${drill.title}</div>
        <div class="drill-card-steps">${drill.steps}</div>
      </div>
    `).join('');
  }

  // Next Practice Continuation Recommendation
  const nextBtn = document.getElementById('btn-fb-next-practice');
  if (nextBtn && feedback.next_practice) {
    const reasonEl = document.getElementById('fb-next-practice-reason');
    if (reasonEl) reasonEl.innerText = feedback.next_practice.reason || "Practicing short targeted sentences builds muscle memory for smooth, unhurried speech.";
    nextBtn.onclick = () => {
      AppState.navigateTo(feedback.next_practice.mode || 'reading');
    };
  }

  // Navigate to feedback screen
  AppState.navigateTo('feedback');
}

// ----------------- ADMIN DASHBOARD CONTROLLER -----------------
const AdminController = {
  isInitialized: false,

  init() {
    if (!this.isInitialized) {
      document.getElementById('btn-admin-refresh')?.addEventListener('click', () => {
        this.loadDashboard();
        showToast("Admin data refreshed.", "info");
      });
      this.isInitialized = true;
    }
  },

  async loadDashboard() {
    this.init();
    try {
      const res = await fetch('/api/admin/stats');
      if (!res.ok) {
        showToast("Administrator privileges required.", "error");
        AppState.navigateTo('dashboard');
        return;
      }
      const data = await res.json();
      this.render(data);
    } catch (err) {
      console.error("Admin dashboard fetch error:", err);
      showToast("Failed to load admin statistics.", "error");
    }
  },

  render(data) {
    if (!data || !data.metrics) return;

    // KPI Metrics
    const usersEl = document.getElementById('admin-stat-users');
    if (usersEl) usersEl.innerText = data.metrics.total_users || 0;

    const sessionsEl = document.getElementById('admin-stat-sessions');
    if (sessionsEl) sessionsEl.innerText = data.metrics.total_sessions || 0;

    const minutesEl = document.getElementById('admin-stat-minutes');
    if (minutesEl) minutesEl.innerText = `${data.metrics.total_practice_minutes || 0}m`;

    const bugsEl = document.getElementById('admin-stat-bugs');
    if (bugsEl) bugsEl.innerText = data.metrics.total_bug_reports || 0;

    const dbEl = document.getElementById('admin-stat-db');
    if (dbEl && data.database) {
      dbEl.innerText = data.database.name || 'fluency_db';
    }

    // Admin Mascot SVG
    const mascotContainer = document.getElementById('admin-mascot-container');
    if (mascotContainer && window.MascotEngine) {
      mascotContainer.innerHTML = MascotEngine.render('otter', 'waving', 140);
    }

    // Helper for string escaping
    const safeStr = (s) => (s ? String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;') : '');

    // 1. Users Directory Table
    const usersTbody = document.getElementById('admin-users-table-body');
    if (usersTbody) {
      if (!data.users || data.users.length === 0) {
        usersTbody.innerHTML = `<tr><td colspan="8" style="text-align: center; padding: 24px; color: var(--text-muted);">No user accounts registered yet.</td></tr>`;
      } else {
        usersTbody.innerHTML = data.users.map(u => `
          <tr style="border-bottom: 1px solid var(--border-cream); font-size: 0.9rem;">
            <td style="padding: 12px 14px; font-weight: 700; color: var(--brand-brown);">#${u.id}</td>
            <td style="padding: 12px 14px; font-weight: 700; color: #2D3748;">${safeStr(u.name)}</td>
            <td style="padding: 12px 14px; color: var(--text-muted);">${safeStr(u.email)}</td>
            <td style="padding: 12px 14px;"><span class="badge" style="background: #EBF8FF; color: #2B6CB0; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 700;">${safeStr(u.age_group || '18-23')}</span></td>
            <td style="padding: 12px 14px;"><span style="font-size: 0.82rem; color: #4A5568;">${safeStr(u.selected_avatar || 'avatar-sunny')}</span></td>
            <td style="padding: 12px 14px; color: var(--text-muted); font-size: 0.85rem;">${safeStr(u.created_at || '-')}</td>
            <td style="padding: 12px 14px; font-weight: 800; color: var(--brand-brown);">${u.total_sessions || 0}</td>
            <td style="padding: 12px 14px; font-weight: 800; color: #059669;">${u.avg_clarity || 0}%</td>
          </tr>
        `).join('');
      }
    }

    // 2. Recent Practice Sessions Table
    const sessionsTbody = document.getElementById('admin-sessions-table-body');
    if (sessionsTbody) {
      if (!data.recent_sessions || data.recent_sessions.length === 0) {
        sessionsTbody.innerHTML = `<tr><td colspan="8" style="text-align: center; padding: 24px; color: var(--text-muted);">No practice sessions logged yet.</td></tr>`;
      } else {
        sessionsTbody.innerHTML = data.recent_sessions.map(s => {
          let badgeColor = '#FEF3C7; color: #92400E;';
          if (s.mode === 'reading') badgeColor = '#E0E7FF; color: #3730A3;';
          if (s.mode === 'media') badgeColor = '#FCE7F3; color: #9D174D;';
          if (s.mode === 'breath') badgeColor = '#ECFDF5; color: #065F46;';
          if (s.mode === 'conversation') badgeColor = '#EDE9FE; color: #5B21B6;';

          return `
            <tr style="border-bottom: 1px solid var(--border-cream); font-size: 0.88rem;">
              <td style="padding: 12px 14px; font-weight: 700;">#${s.id}</td>
              <td style="padding: 12px 14px;"><span class="badge" style="background: ${badgeColor} padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 700; text-transform: capitalize;">${safeStr(s.mode)}</span></td>
              <td style="padding: 12px 14px; font-weight: 600; color: #2D3748;">${safeStr(s.title || 'Practice Session')}</td>
              <td style="padding: 12px 14px; font-weight: 700;">${s.duration_seconds}s</td>
              <td style="padding: 12px 14px; font-weight: 700; color: var(--brand-brown);">${s.wpm}</td>
              <td style="padding: 12px 14px; font-weight: 800; color: #059669;">${s.clarity_score}%</td>
              <td style="padding: 12px 14px; color: var(--text-muted); font-size: 0.82rem;">${s.filler_count} fillers / ${s.pauses_count} pauses</td>
              <td style="padding: 12px 14px; color: var(--text-muted); font-size: 0.82rem;">${safeStr(s.created_at || s.date || '-')}</td>
            </tr>
          `;
        }).join('');
      }
    }

    // 3. Bug Reports Table
    const bugsTbody = document.getElementById('admin-bugs-table-body');
    if (bugsTbody) {
      if (!data.bug_reports || data.bug_reports.length === 0) {
        bugsTbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 24px; color: var(--text-muted);">No bug reports submitted yet.</td></tr>`;
      } else {
        bugsTbody.innerHTML = data.bug_reports.map(b => `
          <tr style="border-bottom: 1px solid var(--border-cream); font-size: 0.88rem;">
            <td style="padding: 12px 14px; font-weight: 800; color: var(--brand-brown);">${safeStr(b.ticket_code || `FL-${b.id}`)}</td>
            <td style="padding: 12px 14px; font-weight: 700; color: #2D3748;">${safeStr(b.title)}</td>
            <td style="padding: 12px 14px;"><span class="badge" style="background: #F3F4F6; color: #374151; padding: 3px 8px; border-radius: 4px; font-size: 0.8rem;">${safeStr(b.page_occurred || 'General')}</span></td>
            <td style="padding: 12px 14px;"><span class="badge" style="background: ${b.severity === 'Critical' ? '#FEE2E2; color: #DC2626;' : '#FEF3C7; color: #92400E;'} padding: 3px 8px; border-radius: 6px; font-size: 0.8rem; font-weight: 700;">${safeStr(b.severity || 'Minor')}</span></td>
            <td style="padding: 12px 14px; color: #4A5568; max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${safeStr(b.description)}">${safeStr(b.description)}</td>
            <td style="padding: 12px 14px;"><span class="badge" style="background: #E0E7FF; color: #3730A3; padding: 3px 8px; border-radius: 6px; font-size: 0.8rem; font-weight: 700;">${safeStr(b.status || 'Received')}</span></td>
            <td style="padding: 12px 14px; color: var(--text-muted); font-size: 0.82rem;">${safeStr(b.created_at || '-')}</td>
          </tr>
        `).join('');
      }
    }
  }
};

window.AdminController = AdminController;

// Start application on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  AppState.init();
});
