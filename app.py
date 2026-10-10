"""
FLUENCY — Modern Speech-Practice Companion Web Application
Flask Backend Server & REST API with MySQL Database Integration
"""

import os
import sys
import json
import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, session, send_from_directory
from flask_cors import CORS
from models import db, User, PracticeSession, ConversationSession, UserProgressSnapshot, BugReport
from speech_analyzer import analyze_speech_data
from conversation_engine import generate_conversation_reply
import content_data

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("SECRET_KEY", os.environ.get("FLASK_SECRET_KEY", "fluency-secure-random-production-key-2026-speech-app"))

# Database Configuration from Environment Variables (MySQL 8.0)
DB_TYPE = os.environ.get("DB_TYPE", "mysql").lower()
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "Kulkarni123")
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME", "fluency_db")

# Fixed Admin Authentication Credentials from Environment Variables
ADMIN_ID = os.environ.get("ADMIN_ID", "MruSwatiSwami")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "mruKulkarni1")

if DB_TYPE == "mysql":
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 280,
    'pool_pre_ping': True
}
app.config['JSON_SORT_KEYS'] = False

CORS(app, supports_credentials=True)
db.init_app(app)

@app.after_request
def add_security_headers(response):
    response.headers['Permissions-Policy'] = 'microphone=(self), camera=(self)'
    return response

# ----------------- DB INIT & SEEDING -----------------
with app.app_context():
    db.create_all()
    # Check if a default demo user exists for seamless testing and initial verification
    demo_user = User.query.filter_by(email="buddy@fluency.com").first()
    if not demo_user:
        demo_user = User(
            name="Alex River",
            email="buddy@fluency.com",
            actual_age=21,
            practice_age=21,
            age_group="18-23",
            selected_avatar="avatar-sunny",
            birthdate="2005-04-12",
            phone="+1 (555) 349-8821",
            bio="Working on natural pauses and speaking at job interviews with confidence.",
            preferred_language="English",
            selected_mascot="otter",
            theme_preference="warm_cream",
            ai_persona="supportive_alex",
            ai_speaking_style="gentle",
            ai_feedback_rigor="balanced"
        )
        demo_user.set_password("practice123")
        db.session.add(demo_user)
        db.session.commit()

        # Seed sample baseline practice sessions so Progress charts are immediately informative
        now = datetime.datetime.utcnow()
        sample_sessions = [
            PracticeSession(
                user_id=demo_user.id,
                mode="reading",
                title="The Art of Slowing Down",
                duration_seconds=26,
                practice_age_used=21,
                wpm=111.0,
                pauses_count=5,
                repetitions_count=2,
                clarity_score=78.5,
                sentence_completion_pct=95.0,
                consistency_score=74.0,
                prompt_text="When we speak in a hurry, our breath tightens...",
                transcript="When we speak in a hurry um our breath tightens and thoughts stumble like over each other.",
                feedback_json=analyze_speech_data("When we speak in a hurry um our breath tightens and thoughts stumble like over each other.", 26),
                created_at=now - datetime.timedelta(days=4)
            ),
            PracticeSession(
                user_id=demo_user.id,
                mode="reading",
                title="The Art of Slowing Down",
                duration_seconds=22,
                practice_age_used=21,
                wpm=131.0,
                pauses_count=3,
                repetitions_count=0,
                clarity_score=91.0,
                sentence_completion_pct=100.0,
                consistency_score=89.0,
                prompt_text="When we speak in a hurry, our breath tightens...",
                transcript="When we speak in a hurry our breath tightens and thoughts pause gently. Taking a breath gives our mind time.",
                feedback_json=analyze_speech_data("When we speak in a hurry our breath tightens and thoughts pause gently. Taking a breath gives our mind time.", 22),
                created_at=now - datetime.timedelta(days=2)
            ),
            PracticeSession(
                user_id=demo_user.id,
                mode="breath",
                title="Coherent 5-5 Breathing Cycle",
                duration_seconds=180,
                practice_age_used=21,
                wpm=0.0,
                pauses_count=0,
                repetitions_count=0,
                clarity_score=100.0,
                feedback_json={"summary": "3-minute Box Breathing practice completed. Diaphragmatic tension lowered."},
                created_at=now - datetime.timedelta(days=1)
            )
        ]
        db.session.add_all(sample_sessions)
        db.session.commit()

        # Seed progress snapshot
        snapshot = UserProgressSnapshot(
            user_id=demo_user.id,
            current_streak=2,
            longest_streak=2,
            total_practice_minutes=3.8,
            total_sessions_completed=3,
            average_clarity=89.8,
            last_practice_date=(now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        )
        db.session.add(snapshot)
        db.session.commit()


# Helper to get currently authenticated user
def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None


# ----------------- MAIN WEB ROUTE -----------------
@app.route('/')
def index():
    return render_template('index.html')


# ----------------- AUTHENTICATION APIS -----------------
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()
    actual_age = int(data.get('actual_age', 21) or 21)
    practice_age = int(data.get('practice_age', actual_age) or actual_age)
    birthdate = data.get('birthdate', '')
    selected_avatar = data.get('selected_avatar', 'avatar-sunny')

    if not name or not email or not password:
        return jsonify({"error": "Please provide your Name, Email, and Password."}), 400

    if len(password) < 6:
        return jsonify({"error": "Password should be at least 6 characters."}), 400

    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify({"error": "An account with this email already exists."}), 409

    age_group_raw = data.get('age_group')
    if age_group_raw:
        age_group = content_data.get_age_group_id(age_group_raw)
    else:
        age_group = content_data.get_age_group_id(practice_age)

    user = User(
        name=name,
        email=email,
        actual_age=actual_age,
        practice_age=practice_age,
        age_group=age_group,
        selected_avatar=selected_avatar,
        birthdate=birthdate,
        selected_mascot="otter",
        theme_preference="warm_cream"
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Create initial progress snapshot
    snapshot = UserProgressSnapshot(user_id=user.id)
    db.session.add(snapshot)
    db.session.commit()

    session['user_id'] = user.id
    return jsonify({
        "message": "Account created successfully! Welcome to FLUENCY.",
        "user": user.to_dict()
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    identifier = data.get('email', data.get('username', data.get('admin_id', ''))).strip()
    password = data.get('password', '').strip()

    if not identifier or not password:
        return jsonify({"error": "Please enter both your email/Admin ID and password."}), 400

    # 1. Check if matches fixed Admin credentials (MruSwatiSwami / mruKulkarni1)
    if identifier.lower() == ADMIN_ID.lower() and password == ADMIN_PASSWORD:
        session['user_id'] = None
        session['is_admin'] = True
        session['admin_id'] = ADMIN_ID

        admin_data = {
            "id": "admin",
            "name": "Swati Swami",
            "email": "admin@fluency.com",
            "admin_id": ADMIN_ID,
            "role": "admin",
            "is_admin": True,
            "selected_avatar": "avatar-spark",
            "selected_mascot": "otter",
            "age_group": "Admin",
            "actual_age": 30,
            "practice_age": 30,
            "theme_preference": "warm_cream",
            "created_at": datetime.datetime.utcnow().strftime("%Y-%m-%d")
        }
        return jsonify({
            "message": "Welcome, Administrator! Logged in successfully.",
            "role": "admin",
            "is_admin": True,
            "user": admin_data
        })

    # 2. Continue using existing normal User login system
    user = User.query.filter(
        (User.email == identifier.lower()) | (User.name == identifier)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email/Admin ID or password. Please try again."}), 401

    session['user_id'] = user.id
    session['is_admin'] = False
    session.pop('admin_id', None)

    user_dict = user.to_dict()
    user_dict['role'] = 'user'
    user_dict['is_admin'] = False

    return jsonify({
        "message": "Welcome back to FLUENCY!",
        "role": "user",
        "is_admin": False,
        "user": user_dict
    })


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    session.pop('admin_id', None)
    return jsonify({"message": "Logged out successfully."})


@app.route('/api/auth/me', methods=['GET'])
def get_me():
    if session.get('is_admin'):
        admin_data = {
            "id": "admin",
            "name": "Swati Swami",
            "email": "admin@fluency.com",
            "admin_id": session.get('admin_id', ADMIN_ID),
            "role": "admin",
            "is_admin": True,
            "selected_avatar": "avatar-spark",
            "selected_mascot": "otter",
            "age_group": "Admin",
            "actual_age": 30,
            "practice_age": 30,
            "theme_preference": "warm_cream",
            "created_at": datetime.datetime.utcnow().strftime("%Y-%m-%d")
        }
        return jsonify({
            "authenticated": True,
            "role": "admin",
            "is_admin": True,
            "user": admin_data
        })

    user = get_current_user()
    if not user:
        return jsonify({"authenticated": False, "role": None, "is_admin": False, "user": None}), 200

    user_dict = user.to_dict()
    user_dict['role'] = 'user'
    user_dict['is_admin'] = False
    return jsonify({
        "authenticated": True,
        "role": "user",
        "is_admin": False,
        "user": user_dict
    })


# ----------------- ADMIN DASHBOARD APIS -----------------
@app.route('/api/admin/stats', methods=['GET'])
def get_admin_dashboard_stats():
    if not session.get('is_admin'):
        return jsonify({"error": "Administrator privileges required."}), 403

    users_list = User.query.order_by(User.created_at.desc()).all()
    sessions_list = PracticeSession.query.order_by(PracticeSession.created_at.desc()).all()
    bug_reports = BugReport.query.order_by(BugReport.created_at.desc()).all()
    convo_sessions = ConversationSession.query.order_by(ConversationSession.created_at.desc()).all()

    # Aggregate statistics
    total_users = len(users_list)
    total_sessions = len(sessions_list)
    total_practice_seconds = sum(s.duration_seconds for s in sessions_list)
    total_practice_minutes = round(total_practice_seconds / 60.0, 1)

    # Mode distribution
    mode_counts = {"reading": 0, "media": 0, "breath": 0, "conversation": 0, "twister": 0, "tongue_twister": 0}
    for s in sessions_list:
        if s.mode in mode_counts:
            mode_counts[s.mode] += 1

    # Age group distribution
    age_groups_count = {"6-11": 0, "12-17": 0, "18-23": 0, "24-30": 0, "31-40": 0}
    for u in users_list:
        ag = u.get_age_group()
        if ag in age_groups_count:
            age_groups_count[ag] += 1

    # User table details with session counts
    user_table = []
    for u in users_list:
        u_sessions = [s for s in sessions_list if s.user_id == u.id]
        u_dict = u.to_dict()
        u_dict['total_sessions'] = len(u_sessions)
        u_dict['total_minutes'] = round(sum(s.duration_seconds for s in u_sessions) / 60.0, 1)
        clarity_sessions = [s for s in u_sessions if s.clarity_score > 0]
        u_dict['avg_clarity'] = round(sum(s.clarity_score for s in clarity_sessions) / max(len(clarity_sessions), 1), 1) if clarity_sessions else 0.0
        user_table.append(u_dict)

    return jsonify({
        "status": "success",
        "database": {
            "name": DB_NAME,
            "host": DB_HOST,
            "port": DB_PORT,
            "type": DB_TYPE,
            "status": "Connected"
        },
        "metrics": {
            "total_users": total_users,
            "total_sessions": total_sessions,
            "total_practice_minutes": total_practice_minutes,
            "total_bug_reports": len(bug_reports),
            "total_conversations": len(convo_sessions)
        },
        "mode_distribution": mode_counts,
        "age_group_distribution": age_groups_count,
        "users": user_table,
        "recent_sessions": [s.to_dict() for s in sessions_list[:20]],
        "bug_reports": [b.to_dict() for b in bug_reports]
    })


# ----------------- USER PROFILE & SETTINGS -----------------
@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    if session.get('is_admin'):
        admin_data = {
            "id": "admin",
            "name": "Swati Swami",
            "email": "admin@fluency.com",
            "admin_id": session.get('admin_id', ADMIN_ID),
            "role": "admin",
            "is_admin": True,
            "selected_avatar": "avatar-spark",
            "selected_mascot": "otter",
            "age_group": "18-23",
            "actual_age": 30,
            "practice_age": 30,
            "birthdate": "",
            "phone": "",
            "bio": "Administrator",
            "preferred_language": "English",
            "theme_preference": "warm_cream",
            "created_at": datetime.datetime.utcnow().strftime("%Y-%m-%d")
        }
        return jsonify({"status": "success", "user": admin_data})

    user = get_current_user()
    if not user:
        return jsonify({"error": "Authentication required."}), 401

    return jsonify({"status": "success", "user": user.to_dict()})


@app.route('/api/user/profile', methods=['PUT'])
def update_profile():
    user = get_current_user()
    if not user:
        if session.get('is_admin'):
            return jsonify({"message": "Admin profile updated.", "user": {"name": "Swati Swami"}})
        return jsonify({"error": "Authentication required."}), 401

    data = request.get_json() or {}
    if 'name' in data and data['name'].strip():
        user.name = data['name'].strip()
    if 'selected_avatar' in data and data['selected_avatar']:
        user.selected_avatar = data['selected_avatar'].strip()
    if 'actual_age' in data:
        try:
            user.actual_age = int(data['actual_age'])
        except (ValueError, TypeError):
            pass
    if 'practice_age' in data:
        try:
            user.practice_age = int(data['practice_age'])
        except (ValueError, TypeError):
            pass
    if 'age_group' in data and data['age_group']:
        user.age_group = content_data.get_age_group_id(data['age_group'])
    if 'birthdate' in data:
        user.birthdate = data['birthdate'] or ""
    if 'phone' in data:
        user.phone = data['phone'] or ""
    if 'bio' in data:
        user.bio = data['bio'] or ""
    if 'preferred_language' in data and data['preferred_language']:
        user.preferred_language = data['preferred_language'].strip()

    db.session.commit()
    db.session.refresh(user)
    return jsonify({"message": "Profile updated successfully.", "user": user.to_dict()})


@app.route('/api/user/settings', methods=['PUT'])
def update_settings():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Authentication required."}), 401

    data = request.get_json() or {}
    if 'selected_avatar' in data and data['selected_avatar']:
        user.selected_avatar = data['selected_avatar'].strip()
    if 'selected_mascot' in data:
        user.selected_mascot = data['selected_mascot']
    if 'theme_preference' in data:
        user.theme_preference = data['theme_preference']
    if 'ai_persona' in data:
        user.ai_persona = data['ai_persona']
    if 'ai_speaking_style' in data:
        user.ai_speaking_style = data['ai_speaking_style']
    if 'ai_feedback_rigor' in data:
        user.ai_feedback_rigor = data['ai_feedback_rigor']
    if 'practice_age' in data:
        user.practice_age = int(data['practice_age'])
    if 'age_group' in data and data['age_group']:
        user.age_group = content_data.get_age_group_id(data['age_group'])
    if 'preferred_language' in data:
        user.preferred_language = data['preferred_language']
    if 'custom_api_key' in data:
        user.custom_api_key = data['custom_api_key'].strip() if data['custom_api_key'] else None

    db.session.commit()
    return jsonify({"message": "Settings saved successfully.", "user": user.to_dict()})


# ----------------- CONTENT APIS -----------------
@app.route('/api/content/reading', methods=['GET'])
def get_reading_content():
    user = get_current_user()
    age_group_param = request.args.get('age_group', user.get_age_group() if user else '18-23')
    age_group = content_data.get_age_group_id(age_group_param)
    length_type = request.args.get('length_type', 'all').lower().strip()
    difficulty = request.args.get('difficulty', 'all').lower().strip()
    language = request.args.get('language') or (user.preferred_language if user else 'English')

    items = content_data.get_reading_for_age_and_diff(age_group=age_group, difficulty=difficulty, length_type=length_type, language=language)
    return jsonify({"items": items, "count": len(items), "age_group": age_group, "language": language})


@app.route('/api/content/images', methods=['GET'])
def get_image_content():
    user = get_current_user()
    age_group_param = request.args.get('age_group', user.get_age_group() if user else None)
    if not age_group_param:
        age = int(request.args.get('age', (user.practice_age if user else 21) or 21))
        age_group = content_data.get_age_group_id(age)
    else:
        age_group = content_data.get_age_group_id(age_group_param)
        age = 21

    difficulty = request.args.get('difficulty', 'all').lower().strip()
    items = content_data.get_images_for_age_and_diff(age_group, difficulty)
    return jsonify({
        "items": items,
        "count": len(items),
        "age_group": age_group,
        "age": age
    })


@app.route('/api/content/videos', methods=['GET'])
def get_video_content():
    user = get_current_user()
    age_group_param = request.args.get('age_group', user.get_age_group() if user else None)
    if not age_group_param:
        age = int(request.args.get('age', (user.practice_age if user else 21) or 21))
        age_group = content_data.get_age_group_id(age)
    else:
        age_group = content_data.get_age_group_id(age_group_param)
        age = 21

    difficulty = request.args.get('difficulty', 'all').lower().strip()
    items = content_data.get_videos_for_age_and_diff(age_group, difficulty)
    return jsonify({
        "items": items,
        "count": len(items),
        "age_group": age_group,
        "age": age
    })


@app.route('/api/content/scenarios', methods=['GET'])
def get_scenarios():
    user = get_current_user()
    age_group_param = request.args.get('age_group', user.get_age_group() if user else None)
    if age_group_param:
        age_group = content_data.get_age_group_id(age_group_param)
        group_min_age_map = {"6-11": 10, "12-17": 14, "18-23": 18, "24-30": 19, "31-40": 19}
        target_age = group_min_age_map.get(age_group, 18)
    else:
        target_age = int(request.args.get('age', user.practice_age if user else 21))
        age_group = content_data.get_age_group_id(target_age)

    language = request.args.get('language') or (user.preferred_language if user else 'English')
    items = content_data.get_conversation_scenarios(age_group=age_group, target_age=target_age, language=language)
    filtered = [i for i in items if i.get('age_min', 0) <= target_age]
    if not filtered or len(filtered) < len(items):
        filtered = items
    return jsonify({"items": filtered, "age_group": age_group, "language": language})



@app.route('/api/content/mascots', methods=['GET'])
def get_mascots():
    return jsonify({"mascots": content_data.MASCOTS_DATA})


@app.route('/api/content/quotes', methods=['GET'])
def get_quotes():
    return jsonify({"quotes": content_data.MOTIVATIONAL_QUOTES})


@app.route('/api/content/therapy-videos', methods=['GET'])
def get_therapy_videos():
    category = request.args.get('category', 'all')
    query = request.args.get('q', request.args.get('search', ''))
    items = content_data.get_therapy_videos(category=category, query=query)
    return jsonify({
        "items": items,
        "count": len(items),
        "total": len(content_data.THERAPY_VIDEOS)
    })


@app.route('/api/content/tongue-twisters', methods=['GET'])
def get_tongue_twisters():
    difficulty = request.args.get('difficulty', 'all').lower().strip()
    category = request.args.get('category', 'all').lower().strip()
    items = content_data.get_tongue_twisters(difficulty=difficulty, category=category)
    return jsonify({
        "items": items,
        "count": len(items),
        "difficulty": difficulty
    })


# ----------------- SPEECH ANALYSIS & PRACTICE SESSIONS -----------------
@app.route('/api/practice/analyze', methods=['POST'])
def analyze_practice():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Please log in to save and analyze your practice."}), 401

    data = request.get_json() or {}
    mode = data.get('mode', 'reading')
    title = data.get('title', 'Speech Practice Session')
    duration_seconds = float(data.get('duration_seconds', 0))
    transcript = data.get('transcript', '')
    prompt_text = data.get('prompt_text', '')
    audio_data_url = data.get('audio_data_url', None)

    language = data.get('language') or (user.preferred_language if user else 'English')

    # Perform real acoustic & lexical speech analysis
    analysis_result = analyze_speech_data(
        transcript=transcript,
        audio_duration_seconds=duration_seconds,
        prompt_text=prompt_text,
        user_practice_age=user.practice_age,
        custom_api_key=user.custom_api_key,
        mode=mode,
        language=language
    )

    metrics = analysis_result['metrics']

    # Store in database
    session_record = PracticeSession(
        user_id=user.id,
        mode=mode,
        title=title,
        duration_seconds=int(duration_seconds),
        practice_age_used=user.practice_age,
        wpm=metrics.get('wpm', 0.0),
        pauses_count=metrics.get('pauses_count', 0),
        repetitions_count=metrics['repetitions_count'],
        clarity_score=metrics['clarity_score'],
        sentence_completion_pct=metrics['sentence_completion_pct'],
        consistency_score=metrics['consistency_score'],
        prompt_text=prompt_text,
        transcript=transcript,
        audio_data_url=audio_data_url,
        feedback_json=analysis_result
    )

    db.session.add(session_record)

    # Update or create progress snapshot
    snapshot = UserProgressSnapshot.query.filter_by(user_id=user.id).first()
    if not snapshot:
        snapshot = UserProgressSnapshot(user_id=user.id, total_practice_minutes=0.0, total_sessions_completed=0, current_streak=0, longest_streak=0)
        db.session.add(snapshot)

    snapshot.total_practice_minutes = round((snapshot.total_practice_minutes or 0.0) + (duration_seconds / 60.0), 1)
    snapshot.total_sessions_completed = (snapshot.total_sessions_completed or 0) + 1
    today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    if snapshot.last_practice_date != today_str:
        snapshot.current_streak = (snapshot.current_streak or 0) + 1
        if snapshot.current_streak > (snapshot.longest_streak or 0):
            snapshot.longest_streak = snapshot.current_streak
        snapshot.last_practice_date = today_str

    db.session.commit()

    return jsonify({
        "message": "Practice session analyzed and saved.",
        "session_id": session_record.id,
        "feedback": analysis_result,
        "session": session_record.to_dict()
    })


@app.route('/api/practice/sessions', methods=['GET'])
def get_user_sessions():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Authentication required."}), 401

    mode = request.args.get('mode', 'all')
    query = PracticeSession.query.filter_by(user_id=user.id)
    if mode != 'all':
        query = query.filter_by(mode=mode)

    sessions_list = query.order_by(PracticeSession.created_at.desc()).all()
    return jsonify({
        "sessions": [s.to_dict() for s in sessions_list],
        "total": len(sessions_list)
    })


@app.route('/api/practice/sessions/<int:session_id>', methods=['GET', 'DELETE'])
def handle_single_session(session_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Authentication required."}), 401

    session_record = PracticeSession.query.filter_by(id=session_id, user_id=user.id).first()
    if not session_record:
        return jsonify({"error": "Session not found."}), 404

    if request.method == 'DELETE':
        db.session.delete(session_record)
        db.session.commit()
        return jsonify({"message": "Recording session deleted."})

    return jsonify({"session": session_record.to_dict()})


@app.route('/api/practice/sessions/<int:session_id>/audio', methods=['GET'])
def get_session_audio(session_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Authentication required."}), 401

    session_record = PracticeSession.query.filter_by(id=session_id, user_id=user.id).first()
    if not session_record or not session_record.audio_data_url:
        return jsonify({"error": "Audio recording not found for this session."}), 404

    return jsonify({
        "session_id": session_record.id,
        "title": session_record.title,
        "audio_data_url": session_record.audio_data_url,
        "duration_seconds": session_record.duration_seconds
    })


def calculate_overall_progress_data(user_id, sessions, snapshot=None):
    """
    Calculate dynamic Overall Progress percentage (0-100) strictly from stored database records.
    Considers clarity_score, sentence_completion_pct, consistency_score,
    pauses, repetitions, and completed practice sessions.
    Does NOT arbitrarily inflate percentage based on session count alone.
    """
    if not sessions or len(sessions) == 0:
        return {
            "has_data": False,
            "percentage": None,
            "status_label": "Not enough data yet",
            "explanation": "Based on your practice activity and speech performance.",
            "message": "Complete your first practice session to calculate your overall progress.",
            "metrics_breakdown": {
                "clarity": 0.0,
                "completion": 0.0,
                "consistency": 0.0,
                "fluency_control": 0.0,
                "practice_regularity": 0.0
            }
        }

    # Filter sessions with valid speech practice data
    speech_sessions = [
        s for s in sessions 
        if (s.wpm > 0 or s.clarity_score > 0 or s.sentence_completion_pct > 0 or (s.transcript and len(s.transcript.strip()) > 0))
    ]

    if not speech_sessions:
        return {
            "has_data": False,
            "percentage": None,
            "status_label": "Not enough data yet",
            "explanation": "Based on your practice activity and speech performance.",
            "message": "Complete a speaking practice session (Reading, Conversation, Tongue Twister, or Visuals) to calculate your overall progress.",
            "metrics_breakdown": {
                "clarity": 0.0,
                "completion": 0.0,
                "consistency": 0.0,
                "fluency_control": 0.0,
                "practice_regularity": 0.0
            }
        }

    # 1. Articulation Clarity (Weight: 30%)
    clarity_vals = [s.clarity_score for s in speech_sessions if s.clarity_score > 0]
    avg_clarity = (sum(clarity_vals) / len(clarity_vals)) if clarity_vals else 75.0
    avg_clarity = max(0.0, min(100.0, avg_clarity))

    # 2. Sentence / Passage Completion (Weight: 25%)
    completion_vals = [s.sentence_completion_pct for s in speech_sessions if s.sentence_completion_pct > 0]
    avg_completion = (sum(completion_vals) / len(completion_vals)) if completion_vals else 80.0
    avg_completion = max(0.0, min(100.0, avg_completion))

    # 3. Speaking Consistency & Rhythm (Weight: 20%)
    consistency_vals = [s.consistency_score for s in speech_sessions if s.consistency_score > 0]
    avg_consistency = (sum(consistency_vals) / len(consistency_vals)) if consistency_vals else 78.0
    avg_consistency = max(0.0, min(100.0, avg_consistency))

    # 4. Fluency Disfluency Control (Weight: 15%)
    # Evaluates controlled rate of repetitions and excessive long pauses
    avg_reps = sum(s.repetitions_count for s in speech_sessions) / len(speech_sessions)
    avg_pauses = sum(s.pauses_count for s in speech_sessions) / len(speech_sessions)

    penalty = (avg_reps * 6.0) + (max(0.0, avg_pauses - 2.0) * 3.0)
    fluency_control_score = max(40.0, min(100.0, 100.0 - penalty))

    # 5. Practice Breadth & Regularity (Weight: 10%)
    unique_modes = len(set(s.mode for s in sessions))
    mode_variety_score = min(100.0, unique_modes * 25.0)
    
    dates = set(s.created_at.strftime("%Y-%m-%d") for s in sessions if s.created_at)
    active_days = len(dates)
    streak = snapshot.current_streak if snapshot else min(active_days, 7)
    regularity_score = min(100.0, (active_days * 15.0) + (min(streak, 7) * 5.0))
    practice_regularity_score = round((mode_variety_score * 0.4) + (regularity_score * 0.6), 1)

    # Weighted Composite Score
    composite = (
        (avg_clarity * 0.30) +
        (avg_completion * 0.25) +
        (avg_consistency * 0.20) +
        (fluency_control_score * 0.15) +
        (practice_regularity_score * 0.10)
    )
    final_pct = max(10, min(100, int(round(composite))))

    if final_pct >= 85:
        status_label = "Strong Performance"
    elif final_pct >= 70:
        status_label = "Steady Progress"
    elif final_pct >= 50:
        status_label = "Developing Foundation"
    else:
        status_label = "Early Practice Phase"

    return {
        "has_data": True,
        "percentage": final_pct,
        "status_label": status_label,
        "explanation": "Based on your practice activity and speech performance.",
        "metrics_breakdown": {
            "clarity": round(avg_clarity, 1),
            "completion": round(avg_completion, 1),
            "consistency": round(avg_consistency, 1),
            "fluency_control": round(fluency_control_score, 1),
            "practice_regularity": round(practice_regularity_score, 1)
        }
    }


@app.route('/api/practice/progress-stats', methods=['GET'])
def get_progress_stats():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Authentication required."}), 401

    sessions = PracticeSession.query.filter_by(user_id=user.id).order_by(PracticeSession.created_at.asc()).all()

    total_sessions = len(sessions)
    total_seconds = sum(s.duration_seconds for s in sessions)
    total_minutes = round(total_seconds / 60, 1)

    # Unique practice days & streak
    dates = sorted(list(set(s.created_at.strftime("%Y-%m-%d") for s in sessions if s.created_at)))
    total_practice_days = len(dates)

    # Calculate current streak
    streak = 0
    today = datetime.datetime.utcnow().date()
    current_check = today
    dates_set = set(dates)
    
    # Check if practiced today or yesterday to continue streak
    if today.strftime("%Y-%m-%d") in dates_set:
        streak = 1
        current_check = today - datetime.timedelta(days=1)
    elif (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d") in dates_set:
        streak = 1
        current_check = today - datetime.timedelta(days=2)

    while current_check.strftime("%Y-%m-%d") in dates_set:
        streak += 1
        current_check -= datetime.timedelta(days=1)

    # Weekly minutes (last 7 days)
    seven_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    recent_sessions = [s for s in sessions if s.created_at and s.created_at >= seven_days_ago]
    weekly_minutes = round(sum(s.duration_seconds for s in recent_sessions) / 60.0, 1)

    # Timeline trends for charts
    speech_sessions = [s for s in sessions if s.wpm > 0 and s.created_at]
    dates_timeline = [s.created_at.strftime("%b %d") for s in speech_sessions][-10:]
    wpm_trend = [round(s.wpm, 1) for s in speech_sessions][-10:]
    clarity_trend = [round(s.clarity_score, 1) for s in speech_sessions][-10:]
    pauses_trend = [s.pauses_count for s in speech_sessions][-10:]

    # Mode breakdown
    modes_count = {"breath": 0, "reading": 0, "media": 0, "conversation": 0, "twister": 0}
    for s in sessions:
        if s.mode in modes_count:
            modes_count[s.mode] += 1
        elif s.mode in ["video", "image"]:
            modes_count["media"] += 1
        elif s.mode in ["tongue-twister", "tongue_twister"]:
            modes_count["twister"] += 1

    # Dynamic Overall Progress calculation
    snapshot = UserProgressSnapshot.query.filter_by(user_id=user.id).first()
    overall_progress = calculate_overall_progress_data(user.id, sessions, snapshot)

    # Honest Improvement Metric Calculation
    improvement_summary = "Keep practicing regularly to build comparative baseline trends."
    if len(speech_sessions) >= 2:
        early = speech_sessions[:2]
        latest = speech_sessions[-2:]
        avg_early_pauses = sum(s.pauses_count for s in early) / len(early)
        avg_late_pauses = sum(s.pauses_count for s in latest) / len(latest)
        avg_early_clarity = sum(s.clarity_score for s in early) / len(early)
        avg_late_clarity = sum(s.clarity_score for s in latest) / len(latest)

        parts = []
        if avg_late_pauses < avg_early_pauses:
            diff = round(avg_early_pauses - avg_late_pauses, 1)
            parts.append(f"Reduced pauses & hesitations by an average of {diff} per practice")
        if avg_late_clarity > avg_early_clarity:
            diff_pct = round(avg_late_clarity - avg_early_clarity, 1)
            parts.append(f"+{diff_pct}% improvement in articulation clarity")
        
        if parts:
            improvement_summary = " · ".join(parts)
        else:
            improvement_summary = "Speaking consistency stabilizing across practice modes."

    return jsonify({
        "streak": max(streak, 1 if total_practice_days > 0 else 0),
        "total_practice_days": total_practice_days,
        "weekly_minutes": weekly_minutes,
        "total_minutes": total_minutes,
        "total_sessions": total_sessions,
        "improvement_summary": improvement_summary,
        "overall_progress": overall_progress,
        "charts": {
            "dates": dates_timeline,
            "wpm": wpm_trend,
            "clarity": clarity_trend,
            "pauses": pauses_trend,
            "mode_distribution": modes_count
        }
    })


@app.route('/api/practice/compare', methods=['POST'])
def compare_sessions():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Authentication required."}), 401

    data = request.get_json() or {}
    session_a_id = data.get('session_a_id')
    session_b_id = data.get('session_b_id')

    if not session_a_id or not session_b_id:
        return jsonify({"error": "Please select two recordings to compare."}), 400

    s_a = PracticeSession.query.filter_by(id=session_a_id, user_id=user.id).first()
    s_b = PracticeSession.query.filter_by(id=session_b_id, user_id=user.id).first()

    if not s_a or not s_b:
        return jsonify({"error": "One or both recordings could not be found."}), 404

    # Calculate real mathematical deltas
    wpm_diff = round(s_b.wpm - s_a.wpm, 1)
    pauses_diff = s_b.pauses_count - s_a.pauses_count
    clarity_diff = round(s_b.clarity_score - s_a.clarity_score, 1)
    repetitions_diff = s_b.repetitions_count - s_a.repetitions_count

    comparative_notes = []
    if abs(wpm_diff) > 3:
        direction = "faster" if wpm_diff > 0 else "more relaxed/slower"
        comparative_notes.append(f"Speaking pace shifted by {abs(wpm_diff)} WPM ({direction}).")
    if pauses_diff < 0:
        comparative_notes.append(f"Pauses & hesitations reduced by {abs(pauses_diff)}.")
    if clarity_diff > 0:
        comparative_notes.append(f"Clarity score increased by +{clarity_diff}%.")

    if not comparative_notes:
        comparative_notes.append("Performance metrics remained steady between both attempts.")

    return jsonify({
        "recording_a": s_a.to_dict(),
        "recording_b": s_b.to_dict(),
        "deltas": {
            "wpm_diff": wpm_diff,
            "pauses_diff": pauses_diff,
            "clarity_diff": clarity_diff,
            "repetitions_diff": repetitions_diff
        },
        "comparative_notes": comparative_notes
    })


# ----------------- CONVERSATION AI CHATBOT ROUTE -----------------
@app.route('/api/conversation/chat', methods=['POST'])
def conversation_chat():
    user = get_current_user()
    data = request.get_json() or {}
    scenario_id = data.get('scenario_id', 'scen_intro')
    user_message = data.get('user_message', '').strip()
    history = data.get('history', [])
    persona = data.get('persona', user.ai_persona if user else 'buddy_mascot')
    practice_age = user.practice_age if user else 21
    language = data.get('language') or (user.preferred_language if user else 'English')

    if not user_message:
        return jsonify({"error": "Empty message."}), 400

    # Scenario details
    scenario = next((s for s in content_data.CONVERSATION_SCENARIOS if s['id'] == scenario_id), None)
    scenario_title = scenario['title'] if scenario else "Practice Conversation"

    # Generate natural, contextual, zero-repetition conversational response
    result = generate_conversation_reply(
        scenario_id=scenario_id,
        user_message=user_message,
        history=history,
        persona=persona,
        user_age=practice_age,
        language=language,
        custom_api_key=user.custom_api_key if user else None
    )

    return jsonify({
        "reply": result['reply'],
        "speaking_tip": result.get('speaking_tip', ''),
        "scenario_title": scenario_title,
        "persona_used": persona,
        "language": language
    })



# ----------------- BUG REPORT API -----------------
@app.route('/api/bugs', methods=['POST'])
def submit_bug():
    user = get_current_user()
    data = request.get_json() or {}
    title = data.get('title', '').strip()
    page_occurred = data.get('page_occurred', 'General')
    severity = data.get('severity', 'Minor')
    description = data.get('description', '').strip()
    steps_to_reproduce = data.get('steps_to_reproduce', '').strip()
    attachment_name = data.get('attachment_name', '')

    if not title or not description:
        return jsonify({"error": "Please provide both a Title and a Description for the issue."}), 400

    report = BugReport(
        user_id=user.id if user else None,
        title=title,
        page_occurred=page_occurred,
        severity=severity,
        description=description,
        steps_to_reproduce=steps_to_reproduce,
        attachment_name=attachment_name
    )
    db.session.add(report)
    db.session.commit()

    return jsonify({
        "message": "Thank you! Your report has been logged.",
        "ticket": report.to_dict()
    }), 201


@app.route('/api/bugs', methods=['GET'])
def list_bugs():
    user = get_current_user()
    if not user:
        return jsonify({"tickets": []})
    reports = BugReport.query.filter_by(user_id=user.id).order_by(BugReport.created_at.desc()).all()
    return jsonify({"tickets": [r.to_dict() for r in reports]})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"==================================================")
    print(f"   FLUENCY — Speech Practice Web Application      ")
    print(f"   Database: MySQL ({DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME})")
    print(f"   Server running on http://127.0.0.1:{port}      ")
    print(f"==================================================")
    app.run(host='0.0.0.0', port=port, debug=True)
