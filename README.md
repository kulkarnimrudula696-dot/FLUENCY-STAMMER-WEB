# FLUENCY — Modern Speech-Practice Companion Web Application

> **"Practice your voice. Build your confidence."**

FLUENCY is a full-featured, supportive web application designed to help individuals overcome speech hesitation, stuttering, and communication anxiety through evidence-based speech-language practice, diaphragmatic breathwork, reading articulation drills, interactive AI conversations, and real-time speech analytics.

---

## 🌟 Key Highlights & Features

### 1. 🫁 Guided Breathing Mode
* **Box Breathing (4-4-4-4)**: Calms diaphragmatic tension, lowers pulse, and prepares the vocal cords before speaking.
* **Visual Pacing Circle**: Synchronized inhalation, holding, exhalation, and rest phases.
* **Mindful Vocal Relaxation**: Promotes smooth phonation on the exhale.

### 2. 📖 Multi-Lingual Reading Practice Mode
* **5 Age Group Levels**: Tailored vocabulary and sentence structures for:
  * `6–11` (Kids & Early Learners)
  * `12–17` (Teens)
  * `18–23` (Young Adults)
  * `24–30` (Adults & Professionals)
  * `31–40` (Mature Communicators)
* **3 Lengths & Difficulties**: Short (15–30s), Medium (45–60s), and Long (90–120s) passages with Easy, Medium, and Advanced levels.
* **8 Practice & Interface Languages**:
  * English
  * Hindi (हिंदी)
  * Marathi (मराठी)
  * Spanish (Español)
  * French (Français)
  * German (Deutsch)
  * Japanese (日本語)
  * Chinese (中文)
* **Automated Speech Alignment Engine**:
  * Exact word-by-word paragraph comparison.
  * Measures matched words, omissions, extra filler words, and substitutions.
  * Calculates Speaking Rate (WPM), natural vs. prolonged pauses, repetitions, and a comprehensive Practice Score (0–100).

### 3. 👅 Articulation & Tongue Twister Mode
* Phonics and consonant transition drills designed to increase vocal clarity and overcome mechanical hesitation.
* Progressive speed and repetition challenges.

### 4. 🖼️ Media & Video Description Mode
* Image prompts and silent video clips encouraging spontaneous narration.
* Helps transition from structured reading to spontaneous, real-time thought formulation.

### 5. 💬 Interactive AI Conversation Companion
* **Multi-Scenario Dialogue**: Practice ordering at a cafe, job interviews, meeting updates, or friendly conversations.
* **Context-Aware Dialogue Engine**: Tracks entities, sentiment, and conversation history without repetitive loops.
* **Speech Synthesis & Speech-to-Text**: Real-time microphone capture and spoken feedback.

### 6. 📊 Progress & Speech Analytics Dashboard
* **Practice Streak Tracker**: Monitors consecutive days of practice.
* **Clarity & Fluency Metrics**: Interactive Chart.js graphs displaying Words Per Minute (WPM), speech duration, pause frequencies, and overall clarity trends over time.

### 7. 👤 Personalized Profiles & Custom Avatars
* Full user profile management backed by database persistence.
* **Illustrated Vector Avatars**: Curated lightweight avatars (Sunny, Breeze, Spark, River, etc.).
* **Companion Mascots**: 8 supportive practice mascots (Otter, Koala, Capybara, Red Panda, Hamster, Duck, Seal, Axolotl).
* **Centralized i18n**: User-selected language seamlessly controls UI text, quotes, reading passages, and voice recognition.

### 8. 🛡️ Administrator Control Center
* Secure administrative portal for platform oversight.
* Real-time metrics: Total registered users, total completed practice sessions, platform minutes, age group distributions, and recent practice sessions.
* Database connection status monitor (MySQL / SQLite).
* Integrated Bug Reporting system to manage and review user feedback tickets.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python 3.10+, Flask, Flask-SQLAlchemy, Werkzeug (PBKDF2 Password Hashing), Flask-CORS |
| **Database** | MySQL 8.0 (Production) / SQLite (Fallback / Local Dev) |
| **Frontend** | Vanilla JavaScript (ES6+ Modules), HTML5 Semantic Elements, Modern CSS3 Design System |
| **Data & Charts** | Chart.js 4.4, Web Speech API (SpeechRecognition & SpeechSynthesis) |
| **Icons & Fonts** | FontAwesome 6, Google Fonts (Plus Jakarta Sans) |

---

## 📂 Project Directory Structure

```text
├── app.py                      # Flask Application Server, REST APIs, & Routing
├── models.py                   # SQLAlchemy Models (User, PracticeSession, BugReport, etc.)
├── speech_analyzer.py          # Speech analysis algorithms, WPM, pause, & diff engine
├── conversation_engine.py      # Natural dialogue state machine & entity extractor
├── content_data.py             # Practice passages, age groups, & mascots database
├── reading_content_i18n.py     # Localized multi-language reading library (8 languages)
├── view_db.py                  # CLI inspection tool for database verification
├── test_mysql_e2e.py           # End-to-end integration test suite
├── .env                        # Environment configuration (DB credentials & keys)
├── templates/
│   └── index.html              # Single-page Application UI structure & modals
└── static/
    ├── css/                    # Clean custom design system (Warm Cream aesthetic)
    └── js/
        ├── app.js              # Application router, state management, & session lifecycle
        ├── profile_settings.js # Profile database fetch, validation, & update controller
        ├── i18n.js             # Centralized multi-language translation engine
        ├── audio_recorder.js   # Browser microphone capture & Web Audio API
        ├── reading.js          # Reading Practice mode controller
        ├── conversation.js     # AI conversation companion controller
        ├── breathing.js        # Box breathing visual pacer
        ├── progress.js         # Progress analytics & Chart.js renderer
        ├── avatar_engine.js    # Scalable vector avatar renderer
        ├── mascots.js          # Animated SVG mascot companion renderer
        └── video_mode.js       # Video & image narration practice
```

---

## 🚀 Getting Started & Installation

### Prerequisites
* **Python 3.10** or higher
* **MySQL 8.0** (or SQLite for quick local setup)
* Modern web browser with microphone access (Chrome, Edge, Safari, Firefox)

### 1. Clone & Set Up Virtual Environment

```bash
# Clone the repository
git clone https://github.com/kulkarnimrudula696-dot/Fluency-AI.git
cd Fluency-AI

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install flask flask-sqlalchemy flask-cors python-dotenv pymysql cryptography werkzeug
```

### 3. Configure Environment Variables (`.env`)

Create or update the `.env` file in the root directory:

```env
# Database Configuration
# Options: 'mysql' or 'sqlite'
DB_TYPE=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=YourMySQLPassword
DB_NAME=fluency_db

# Flask Application Secret Key
SECRET_KEY=fluency_secure_random_production_key_2026_speech_app
FLASK_ENV=production
FLASK_DEBUG=0
PORT=5000

# Fixed Administrator Credentials
ADMIN_ID=MruSwatiSwami
ADMIN_PASSWORD=mruKulkarni1
```

> **Note on SQLite:** If you don't have MySQL installed locally, simply set `DB_TYPE=sqlite` in `.env`. FLUENCY will automatically initialize a local SQLite database (`instance/database.db`).

### 4. Run the Application

```bash
python app.py
```

The application will be live at: **`http://127.0.0.1:5000`**

---

## 🔑 Default Credentials & Access

### 1. Quick Demo User
* Click **"Quick Demo Sign In"** on the login popup, or enter:
  * **Email**: `buddy@fluency.com`
  * **Password**: `practice123`

### 2. Administrator Access
* Navigate to the login popup and sign in with:
  * **Email / Admin ID**: `MruSwatiSwami`
  * **Password**: `mruKulkarni1`
* Direct access to the Admin Dashboard will automatically unlock in the sidebar navigation.

---

## 🧪 Testing & Verification

FLUENCY comes with built-in automated test suites to ensure database integrity, authentication security, and profile persistence:

```bash
# 1. Run Profile Database Loading & Saving Persistence Test
python scratch/test_profile_persistence.py

# 2. Run Full MySQL End-to-End Test Suite
python test_mysql_e2e.py

# 3. Inspect Current Database Records (CLI viewer)
python view_db.py
```

---

## 🌐 Internationalization & Speech Recognition

FLUENCY features a centralized i18n architecture:
1. When a user changes their preferred language in **Profile** or **Settings**, the selection is stored directly in `users.preferred_language`.
2. The change immediately updates the DOM, localized motivational quotes, reading content, and the browser's `SpeechRecognition` language model (e.g., `hi-IN` for Hindi, `mr-IN` for Marathi, `es-ES` for Spanish, etc.).
3. The selected language persists across browser refreshes, route changes, and future logins.

---

## 🔒 Security & Privacy

* **Microphone Permissions**: Explicit HTTP security header `Permissions-Policy: microphone=(self), camera=(self)` ensures microphone streams stay strictly within the local browser context.
* **Password Encryption**: All user passwords are salted and hashed using standard PBKDF2/SHA-256 before writing to the database.
* **Session Authentication**: State modifications and profile updates rely exclusively on authenticated session `user_id` validation to protect user data from unauthorized cross-user modifications.

---

## 📄 License & Credits

Developed with ❤️ as a compassionate, scientifically grounded communication tool.
Designed to empower speakers of all ages to practice at their own pace, celebrate small wins, and build lifelong speaking confidence.
