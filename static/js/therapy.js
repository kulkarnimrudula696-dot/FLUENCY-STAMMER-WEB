/**
 * FLUENCY — Videos on Therapy Controller
 * Curated, credible educational resources, clinical speech therapy guides,
 * and lived experiences from Stuttering Foundation, ASHA, Michael Palin Centre, and SAY.
 */

const TherapyVideos = {
  items: [],
  activeCategory: 'all',
  searchQuery: '',
  activeVideoId: null,

  async init() {
    this.bindEvents();
    if (!this.items || this.items.length === 0) {
      await this.loadVideos();
    } else {
      this.renderGrid();
    }
  },

  async loadVideos() {
    const grid = document.getElementById('therapy-cards-grid');
    if (grid) {
      grid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: var(--text-muted);">
          <i class="fa-solid fa-circle-notch fa-spin" style="font-size: 2.2rem; color: var(--brand-brown); margin-bottom: 14px;"></i>
          <p style="font-weight: 700;">Loading 20 clinical & educational therapy resources...</p>
        </div>
      `;
    }

    try {
      const res = await fetch('/api/content/therapy-videos');
      const data = await res.json();
      this.items = data.items || [];
      this.renderGrid();
    } catch (err) {
      console.error("Failed to load therapy videos:", err);
      if (grid) {
        grid.innerHTML = `
          <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: #C0392B;">
            <i class="fa-solid fa-triangle-exclamation" style="font-size: 2rem; margin-bottom: 10px;"></i>
            <p style="font-weight: 800;">Unable to load therapy resources at this time. Please check your connection.</p>
          </div>
        `;
      }
    }
  },

  bindEvents() {
    // Search input
    const searchInput = document.getElementById('therapy-search-input');
    if (searchInput && !searchInput._bound) {
      searchInput._bound = true;
      searchInput.addEventListener('input', (e) => {
        this.searchQuery = e.target.value.trim().toLowerCase();
        this.renderGrid();
      });
    }

    // Category pills
    document.querySelectorAll('.therapy-cat-pill').forEach(pill => {
      if (!pill._bound) {
        pill._bound = true;
        pill.addEventListener('click', (e) => {
          document.querySelectorAll('.therapy-cat-pill').forEach(p => p.classList.remove('active'));
          pill.classList.add('active');
          this.activeCategory = pill.dataset.category || 'all';
          this.renderGrid();
        });
      }
    });

    // Close modal on escape or backdrop
    const modal = document.getElementById('therapy-player-modal');
    if (modal && !modal._bound) {
      modal._bound = true;
      modal.addEventListener('click', (e) => {
        if (e.target === modal || e.target.classList.contains('modal-close-trigger')) {
          this.closePlayer();
        }
      });
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
          this.closePlayer();
        }
      });
    }
  },

  getFilteredItems() {
    return this.items.filter(item => {
      const matchCat = this.activeCategory === 'all' || item.category_key === this.activeCategory;
      if (!matchCat) return false;

      if (!this.searchQuery) return true;
      const q = this.searchQuery;
      return (
        item.title.toLowerCase().includes(q) ||
        item.description.toLowerCase().includes(q) ||
        item.source.toLowerCase().includes(q) ||
        item.category.toLowerCase().includes(q) ||
        (item.key_takeaways && item.key_takeaways.some(t => t.toLowerCase().includes(q)))
      );
    });
  },

  renderGrid() {
    const grid = document.getElementById('therapy-cards-grid');
    const countBadge = document.getElementById('therapy-count-badge');
    if (!grid) return;

    const filtered = this.getFilteredItems();
    if (countBadge) {
      countBadge.innerText = `Showing ${filtered.length} of ${this.items.length} videos`;
    }

    if (filtered.length === 0) {
      grid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; background: #FFFFFF; border-radius: var(--radius-lg); border: 1.5px dashed var(--border-subtle);">
          <i class="fa-solid fa-film" style="font-size: 2.5rem; color: var(--brand-brown-border); margin-bottom: 14px;"></i>
          <h3 style="color: var(--text-dark); margin-bottom: 6px;">No therapy videos matched your filter</h3>
          <p style="color: var(--text-muted); font-size: 0.95rem;">Try adjusting your search query or selecting "All Topics".</p>
          <button class="btn btn-secondary btn-sm" style="margin-top: 14px;" onclick="TherapyVideos.resetFilters()">
            Reset Filters
          </button>
        </div>
      `;
      return;
    }

    const t = (k, def) => (window.FluencyI18n ? FluencyI18n.t(k, def) : def);

    grid.innerHTML = filtered.map(item => `
      <div class="therapy-video-card" data-video-id="${item.id}">
        <!-- Thumbnail Container -->
        <div class="therapy-thumb-box" onclick="TherapyVideos.openPlayer('${item.id}')">
          <img 
            src="${item.thumbnail}" 
            alt="${item.title}" 
            class="therapy-thumb-img"
            loading="lazy"
            onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=600&auto=format&fit=crop&q=80';"
          />
          <div class="therapy-thumb-overlay">
            <div class="therapy-play-circle">
              <i class="fa-solid fa-play"></i>
            </div>
          </div>
          <span class="therapy-duration-tag"><i class="fa-regular fa-clock"></i> ${item.duration}</span>
        </div>

        <!-- Content Area -->
        <div class="therapy-card-body">
          <div class="therapy-meta-row">
            <span class="therapy-category-pill">${item.category}</span>
            <span class="therapy-source-pill" title="Source: ${item.source}">
              <i class="fa-solid fa-certificate" style="color: #9A633F;"></i> ${item.source.split('&')[0].trim()}
            </span>
          </div>

          <h3 class="therapy-card-title" onclick="TherapyVideos.openPlayer('${item.id}')" title="${item.title}">
            ${item.title}
          </h3>

          <p class="therapy-card-desc">
            ${item.description}
          </p>

          ${item.key_takeaways && item.key_takeaways.length > 0 ? `
            <div class="therapy-takeaway-preview">
              <i class="fa-solid fa-lightbulb" style="color: #FFC83D; font-size: 0.85rem; flex-shrink: 0; margin-top: 2px;"></i>
              <span class="therapy-takeaway-text"><strong>Key:</strong> ${item.key_takeaways[0]}</span>
            </div>
          ` : ''}

          <!-- Card Footer with Play Button -->
          <div class="therapy-card-footer">
            <button class="btn btn-primary btn-sm therapy-btn-play" onclick="TherapyVideos.openPlayer('${item.id}')">
              <i class="fa-solid fa-play"></i> <span data-i18n="btn_watch_video">${t('btn_watch_video', 'Watch Video')}</span>
            </button>
            <a href="${item.source_url}" target="_blank" rel="noopener noreferrer" class="therapy-link-source" title="Learn more at official organization">
              <i class="fa-solid fa-arrow-up-right-from-square"></i> Source
            </a>
          </div>
        </div>
      </div>
    `).join('');
  },

  resetFilters() {
    this.activeCategory = 'all';
    this.searchQuery = '';
    const searchInput = document.getElementById('therapy-search-input');
    if (searchInput) searchInput.value = '';
    document.querySelectorAll('.therapy-cat-pill').forEach(p => {
      p.classList.toggle('active', p.dataset.category === 'all');
    });
    this.renderGrid();
  },

  openPlayer(videoId) {
    const item = this.items.find(v => v.id === videoId);
    if (!item) return;

    this.activeVideoId = videoId;
    const modal = document.getElementById('therapy-player-modal');
    const iframeContainer = document.getElementById('therapy-player-iframe-container');
    const titleEl = document.getElementById('therapy-player-title');
    const sourceEl = document.getElementById('therapy-player-source');
    const descEl = document.getElementById('therapy-player-desc');
    const takeawaysList = document.getElementById('therapy-player-takeaways');
    const externalLink = document.getElementById('therapy-player-external-link');

    if (titleEl) titleEl.innerText = item.title;
    if (sourceEl) sourceEl.innerHTML = `<i class="fa-solid fa-shield-halved" style="color: #9A633F;"></i> <strong>Source:</strong> ${item.source} (${item.duration})`;
    if (descEl) descEl.innerText = item.description;

    if (takeawaysList) {
      if (item.key_takeaways && item.key_takeaways.length > 0) {
        takeawaysList.innerHTML = item.key_takeaways.map(t => `
          <li><i class="fa-solid fa-check" style="color: #3E885B; margin-right: 6px;"></i> ${t}</li>
        `).join('');
      } else {
        takeawaysList.innerHTML = '';
      }
    }

    if (externalLink) {
      externalLink.href = `https://www.youtube.com/watch?v=${item.youtube_id}`;
    }

    if (iframeContainer) {
      iframeContainer.innerHTML = `
        <iframe 
          src="https://www.youtube-nocookie.com/embed/${item.youtube_id}?autoplay=1&rel=0&modestbranding=1" 
          title="${item.title}"
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
          allowfullscreen
          style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; border-radius: 12px;"
        ></iframe>
      `;
    }

    if (modal) {
      modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
    }
  },

  closePlayer() {
    const modal = document.getElementById('therapy-player-modal');
    const iframeContainer = document.getElementById('therapy-player-iframe-container');
    if (iframeContainer) {
      iframeContainer.innerHTML = '';
    }
    if (modal) {
      modal.style.display = 'none';
      document.body.style.overflow = '';
    }
    this.activeVideoId = null;
  },

  playNext() {
    if (!this.activeVideoId || this.items.length === 0) return;
    const currentIndex = this.items.findIndex(v => v.id === this.activeVideoId);
    const nextIndex = (currentIndex + 1) % this.items.length;
    this.openPlayer(this.items[nextIndex].id);
  },

  playPrev() {
    if (!this.activeVideoId || this.items.length === 0) return;
    const currentIndex = this.items.findIndex(v => v.id === this.activeVideoId);
    const prevIndex = (currentIndex - 1 + this.items.length) % this.items.length;
    this.openPlayer(this.items[prevIndex].id);
  },

  cleanup() {
    this.closePlayer();
  }
};

window.TherapyVideos = TherapyVideos;
