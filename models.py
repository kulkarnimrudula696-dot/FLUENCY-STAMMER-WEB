import os
import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.mysql import LONGTEXT, MEDIUMTEXT

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    actual_age = db.Column(db.Integer, default=21)
    practice_age = db.Column(db.Integer, default=21)
    age_group = db.Column(db.String(20), default="18-23") # 6-11, 12-17, 18-23, 24-30, 31-40
    birthdate = db.Column(db.String(20), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    bio = db.Column(db.Text, default="Practicing my voice step by step.")
    preferred_language = db.Column(db.String(30), default="English")
    
    # Personalization & Avatar & Mascot
    selected_avatar = db.Column(db.String(50), default="avatar-sunny") # avatar-sunny, avatar-breeze, avatar-spark, avatar-river, etc.
    selected_mascot = db.Column(db.String(30), default="otter") # otter, koala, capybara, red_panda, hamster, duck, seal, axolotl
    theme_preference = db.Column(db.String(30), default="warm_cream") # warm_cream, soft_amber, calm_dark
    ai_persona = db.Column(db.String(40), default="supportive_alex") # supportive_alex, patient_maya, energetic_leo, buddy_mascot
    ai_speaking_style = db.Column(db.String(30), default="gentle") # gentle, direct, conversational
    ai_feedback_rigor = db.Column(db.String(30), default="balanced") # gentle, balanced, detailed
    custom_api_key = db.Column(db.String(256), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    sessions = db.relationship('PracticeSession', backref='user', lazy=True, cascade="all, delete-orphan")
    conversation_sessions = db.relationship('ConversationSession', backref='user', lazy=True, cascade="all, delete-orphan")
    progress_snapshot = db.relationship('UserProgressSnapshot', backref='user', uselist=False, cascade="all, delete-orphan")
    bug_reports = db.relationship('BugReport', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_age_group(self):
        if self.age_group:
            normalized = self.age_group.strip().replace("–", "-")
            if normalized in ["6-11", "12-17", "18-23", "24-30", "31-40"]:
                return normalized
        age = self.practice_age or self.actual_age or 21
        if age <= 11:
            return "6-11"
        elif age <= 17:
            return "12-17"
        elif age <= 23:
            return "18-23"
        elif age <= 30:
            return "24-30"
        else:
            return "31-40"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "actual_age": self.actual_age,
            "practice_age": self.practice_age,
            "age_group": self.get_age_group(),
            "selected_avatar": self.selected_avatar or "avatar-sunny",
            "birthdate": self.birthdate or "",
            "phone": self.phone or "",
            "bio": self.bio or "",
            "preferred_language": self.preferred_language,
            "selected_mascot": self.selected_mascot,
            "theme_preference": self.theme_preference,
            "ai_persona": self.ai_persona,
            "ai_speaking_style": self.ai_speaking_style,
            "ai_feedback_rigor": self.ai_feedback_rigor,
            "has_custom_api_key": bool(self.custom_api_key),
            "created_at": self.created_at.strftime("%Y-%m-%d") if self.created_at else ""
        }


class PracticeSession(db.Model):
    __tablename__ = 'practice_sessions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)
    mode = db.Column(db.String(30), nullable=False, index=True) # 'breath', 'reading', 'media', 'conversation'
    title = db.Column(db.String(200), default="Speech Practice")
    duration_seconds = db.Column(db.Integer, default=0)
    practice_age_used = db.Column(db.Integer, default=21)
    
    # Speech Metrics (Real Measurable Metrics)
    wpm = db.Column(db.Float, default=0.0)
    filler_count = db.Column(db.Integer, default=0)
    fillers_list = db.Column(db.JSON, default=list)
    pauses_count = db.Column(db.Integer, default=0)
    repetitions_count = db.Column(db.Integer, default=0)
    clarity_score = db.Column(db.Float, default=0.0) # 0 to 100
    sentence_completion_pct = db.Column(db.Float, default=100.0)
    consistency_score = db.Column(db.Float, default=80.0)
    
    # Content & Transcripts
    prompt_text = db.Column(db.Text, nullable=True)
    transcript = db.Column(db.Text, nullable=True)
    audio_data_url = db.Column(db.Text().with_variant(MEDIUMTEXT, "mysql"), nullable=True) # Base64 audio blob for replay & waveform
    
    # Structured Feedback (Stored as JSON)
    feedback_json = db.Column(db.JSON, default=dict)
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "mode": self.mode,
            "title": self.title,
            "duration_seconds": self.duration_seconds,
            "practice_age_used": self.practice_age_used,
            "wpm": round(self.wpm, 1),
            "filler_count": self.filler_count,
            "fillers_list": self.fillers_list or [],
            "pauses_count": self.pauses_count,
            "repetitions_count": self.repetitions_count,
            "clarity_score": round(self.clarity_score, 1),
            "sentence_completion_pct": round(self.sentence_completion_pct, 1),
            "consistency_score": round(self.consistency_score, 1),
            "prompt_text": self.prompt_text,
            "transcript": self.transcript,
            "feedback": self.feedback_json,
            "has_audio": bool(self.audio_data_url),
            "audio_data_url": self.audio_data_url if self.audio_data_url else None,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else "",
            "date": self.created_at.strftime("%b %d, %Y") if self.created_at else ""
        }


class ConversationSession(db.Model):
    __tablename__ = 'conversation_sessions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)
    scenario_id = db.Column(db.String(100), nullable=False)
    scenario_title = db.Column(db.String(200), default="Face-to-Face Conversation")
    persona = db.Column(db.String(50), default="buddy_mascot")
    turns_count = db.Column(db.Integer, default=0)
    dialogue_history = db.Column(db.JSON, default=list)
    speech_metrics = db.Column(db.JSON, default=dict)
    duration_seconds = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "scenario_id": self.scenario_id,
            "scenario_title": self.scenario_title,
            "persona": self.persona,
            "turns_count": self.turns_count,
            "dialogue_history": self.dialogue_history or [],
            "speech_metrics": self.speech_metrics or {},
            "duration_seconds": self.duration_seconds,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else ""
        }


class UserProgressSnapshot(db.Model):
    __tablename__ = 'user_progress_snapshots'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), unique=True, nullable=False, index=True)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    total_practice_minutes = db.Column(db.Float, default=0.0)
    total_sessions_completed = db.Column(db.Integer, default=0)
    average_clarity = db.Column(db.Float, default=0.0)
    last_practice_date = db.Column(db.String(20), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "current_streak": self.current_streak,
            "longest_streak": self.longest_streak,
            "total_practice_minutes": round(self.total_practice_minutes, 1),
            "total_sessions_completed": self.total_sessions_completed,
            "average_clarity": round(self.average_clarity, 1),
            "last_practice_date": self.last_practice_date,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M") if self.updated_at else ""
        }


class BugReport(db.Model):
    __tablename__ = 'bug_reports'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
    ticket_code = db.Column(db.String(50), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    page_occurred = db.Column(db.String(100), default="General")
    severity = db.Column(db.String(50), default="Minor")
    description = db.Column(db.Text, nullable=False)
    steps_to_reproduce = db.Column(db.Text, nullable=True)
    attachment_name = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(50), default="Received")
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "ticket_code": self.ticket_code or f"FL-{self.id:04d}",
            "title": self.title,
            "page_occurred": self.page_occurred,
            "severity": self.severity,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else ""
        }
