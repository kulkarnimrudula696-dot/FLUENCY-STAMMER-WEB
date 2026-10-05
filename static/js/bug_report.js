/**
 * FLUENCY Bug Report Module
 * Submit and manage bug reports with generated ticket IDs.
 */

const BugReportModule = {
  isInitialized: false,

  init() {
    if (!this.isInitialized) {
      this.bindEvents();
      this.isInitialized = true;
    }
    this.loadTickets();
  },

  bindEvents() {
    const form = document.getElementById('bug-report-form');
    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        this.submitReport();
      });
    }
  },

  async submitReport() {
    const title = document.getElementById('bug-title')?.value.trim();
    const pageOccurred = document.getElementById('bug-page')?.value;
    const severity = document.getElementById('bug-severity')?.value;
    const description = document.getElementById('bug-desc')?.value.trim();
    const steps = document.getElementById('bug-steps')?.value.trim();
    const fileInput = document.getElementById('bug-file');
    const attachmentName = fileInput && fileInput.files[0] ? fileInput.files[0].name : '';

    if (!title || !description) {
      showToast("Please provide a Title and Description for the issue.", "warning");
      return;
    }

    try {
      const res = await fetch('/api/bugs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title,
          page_occurred: pageOccurred,
          severity,
          description,
          steps_to_reproduce: steps,
          attachment_name: attachmentName
        })
      });

      const data = await res.json();
      if (data.ticket) {
        document.getElementById('bug-report-form').reset();
        showToast(`Bug logged as ${data.ticket.ticket_code}. Thank you for helping improve FLUENCY!`, "success");
        this.loadTickets();
      }
    } catch (err) {
      console.error("Bug report error:", err);
      showToast("Could not submit bug report.", "error");
    }
  },

  async loadTickets() {
    const container = document.getElementById('user-bug-tickets-list');
    if (!container) return;

    try {
      const res = await fetch('/api/bugs');
      const data = await res.json();
      const tickets = data.tickets || [];

      if (tickets.length === 0) {
        container.innerHTML = `<p style="font-size: 0.9rem; color: var(--text-muted); font-style: italic;">No bugs reported yet.</p>`;
        return;
      }

      container.innerHTML = tickets.map(t => `
        <div class="fluency-card" style="padding: 16px 20px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div style="font-weight: 800; font-size: 0.95rem;">${t.ticket_code}: ${t.title}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted);">${t.page_occurred} · Severity: ${t.severity} · ${t.created_at}</div>
          </div>
          <span style="background: #E8F5E9; color: #2E7D32; font-size: 0.78rem; font-weight: 800; padding: 4px 12px; border-radius: var(--radius-pill);">${t.status}</span>
        </div>
      `).join('');
    } catch (err) {
      console.error("Failed to load tickets:", err);
    }
  }
};
