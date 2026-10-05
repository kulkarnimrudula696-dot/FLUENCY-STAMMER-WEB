import json
from app import app, db
from models import User, PracticeSession, ConversationSession, UserProgressSnapshot, BugReport

def run_tests():
    client = app.test_client()
    print("=== STARTING END-TO-END MYSQL TEST SUITE ===")

    # 1. Register a new user
    test_email = "test_speaker@fluency.com"
    with app.app_context():
        existing = User.query.filter_by(email=test_email).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()

    reg_payload = {
        "name": "Jane Doe",
        "email": test_email,
        "password": "SecurePassword2026!",
        "actual_age": 22,
        "practice_age": 22,
        "age_group": "18-23",
        "selected_avatar": "avatar-breeze",
        "birthdate": "2004-08-15"
    }
    reg_resp = client.post('/api/auth/register', json=reg_payload)
    print("1. Register:", reg_resp.status_code, reg_resp.json.get("message"))
    assert reg_resp.status_code == 201
    user_data = reg_resp.json["user"]
    assert user_data["email"] == test_email
    assert user_data["selected_avatar"] == "avatar-breeze"
    assert user_data["age_group"] == "18-23"

    # Verify password hash in DB (password is NOT plain text)
    with app.app_context():
        u = User.query.filter_by(email=test_email).first()
        assert u is not None
        assert u.password_hash != "SecurePassword2026!"
        assert u.check_password("SecurePassword2026!") is True
        assert u.check_password("WrongPassword") is False
        print(" -> Password Hashing Verified: Werkzeug PBKDF2/SHA256 hash stored securely in MySQL")

    # 2. Test Login
    login_resp = client.post('/api/auth/login', json={"email": test_email, "password": "SecurePassword2026!"})
    print("2. Login:", login_resp.status_code, login_resp.json.get("message"))
    assert login_resp.status_code == 200

    # 3. Test Auth Me
    me_resp = client.get('/api/auth/me')
    print("3. Auth Me:", me_resp.status_code, me_resp.json["user"]["name"], "Avatar:", me_resp.json["user"]["selected_avatar"])
    assert me_resp.json["authenticated"] is True
    assert me_resp.json["user"]["selected_avatar"] == "avatar-breeze"

    # 4. Update Profile (change avatar to avatar-spark & update age group)
    profile_update_resp = client.put('/api/user/profile', json={
        "name": "Jane D. Smith",
        "selected_avatar": "avatar-spark",
        "age_group": "24-30",
        "bio": "Speaking with natural tempo and mindful rhythm."
    })
    print("4. Update Profile:", profile_update_resp.status_code, "New avatar:", profile_update_resp.json["user"]["selected_avatar"])
    assert profile_update_resp.status_code == 200
    assert profile_update_resp.json["user"]["selected_avatar"] == "avatar-spark"
    assert profile_update_resp.json["user"]["age_group"] == "24-30"

    # 5. Test Practice Analysis for Reading Mode
    reading_analyze_resp = client.post('/api/practice/analyze', json={
        "mode": "reading",
        "title": "Finding Your Natural Pace",
        "duration_seconds": 25,
        "transcript": "Finding your natural rhythm is not about speaking quickly um it is about breathing steadily and giving words room.",
        "prompt_text": "Finding your natural rhythm is not about speaking quickly, it is about breathing steadily."
    })
    print("5. Reading Analysis Saved:", reading_analyze_resp.status_code, "Session ID:", reading_analyze_resp.json.get("session_id"))
    assert reading_analyze_resp.status_code == 200
    s_id_1 = reading_analyze_resp.json["session_id"]
    metrics_1 = reading_analyze_resp.json["feedback"]["metrics"]
    print(" -> Metrics 1: WPM =", metrics_1["wpm"], "Clarity =", metrics_1["clarity_score"], "Fillers =", metrics_1["filler_count"])

    # 6. Test Practice Analysis for Image/Video Mode
    media_analyze_resp = client.post('/api/practice/analyze', json={
        "mode": "media",
        "title": "Video Scene Description",
        "duration_seconds": 30,
        "transcript": "In this scene the chef is carefully preparing fresh vegetables and explaining the step by step process.",
        "prompt_text": "Describe what you see happening in the video."
    })
    print("6. Video Analysis Saved:", media_analyze_resp.status_code, "Session ID:", media_analyze_resp.json.get("session_id"))
    assert media_analyze_resp.status_code == 200
    s_id_2 = media_analyze_resp.json["session_id"]

    # 7. Test Practice Analysis for Conversation Mode
    convo_analyze_resp = client.post('/api/practice/analyze', json={
        "mode": "conversation",
        "title": "Conversation: Ordering Coffee at a Cafe",
        "duration_seconds": 40,
        "transcript": "Hi could I please have an iced oat latte with a little bit of cinnamon on top thank you.",
        "prompt_text": "Ordering at a local coffee shop"
    })
    print("7. Convo Analysis Saved:", convo_analyze_resp.status_code, "Session ID:", convo_analyze_resp.json.get("session_id"))
    assert convo_analyze_resp.status_code == 200
    s_id_3 = convo_analyze_resp.json["session_id"]

    # 8. Test Conversation Chatbot Engine API
    chat_resp = client.post('/api/conversation/chat', json={
        "scenario_id": "scen_cafe",
        "user_message": "Hello, what iced drinks do you recommend today?",
        "history": [],
        "persona": "buddy_mascot"
    })
    print("8. Conversation AI Reply:", chat_resp.status_code, "Reply:", chat_resp.json.get("reply")[:50], "...")
    assert chat_resp.status_code == 200
    assert len(chat_resp.json.get("reply", "")) > 0

    # 9. Test Progress Stats
    stats_resp = client.get('/api/practice/progress-stats')
    print("9. Progress Stats:", stats_resp.status_code, "Total Sessions:", stats_resp.json.get("total_sessions"), "Streak:", stats_resp.json.get("streak"))
    assert stats_resp.status_code == 200
    assert stats_resp.json["total_sessions"] == 3
    assert stats_resp.json["charts"]["mode_distribution"]["reading"] == 1
    assert stats_resp.json["charts"]["mode_distribution"]["media"] == 1
    assert stats_resp.json["charts"]["mode_distribution"]["conversation"] == 1

    # 10. Test Compare Recordings
    compare_resp = client.post('/api/practice/compare', json={
        "session_a_id": s_id_1,
        "session_b_id": s_id_2
    })
    print("10. Compare Sessions:", compare_resp.status_code, "Deltas:", compare_resp.json.get("deltas"))
    assert compare_resp.status_code == 200

    # 11. Test Bug Reporting
    bug_resp = client.post('/api/bugs', json={
        "title": "Microphone volume meter sensitivity check",
        "page_occurred": "Reading Mode",
        "severity": "Minor",
        "description": "The microphone volume visualizer displays smoothly but could have higher gain sensitivity."
    })
    print("11. Bug Report:", bug_resp.status_code, "Ticket:", bug_resp.json.get("ticket", {}).get("ticket_code"))
    assert bug_resp.status_code == 201

    # 12. Test Logout and verify unauthenticated access behavior
    logout_resp = client.post('/api/auth/logout')
    print("12. Logout:", logout_resp.status_code, logout_resp.json.get("message"))
    assert logout_resp.status_code == 200

    unauth_me = client.get('/api/auth/me')
    assert unauth_me.json["authenticated"] is False

    # 13. Re-login and verify all MySQL persistent data remains intact
    relogin_resp = client.post('/api/auth/login', json={"email": test_email, "password": "SecurePassword2026!"})
    print("13. Re-login:", relogin_resp.status_code, "User:", relogin_resp.json["user"]["name"], "Avatar:", relogin_resp.json["user"]["selected_avatar"])
    assert relogin_resp.status_code == 200
    assert relogin_resp.json["user"]["selected_avatar"] == "avatar-spark"
    assert relogin_resp.json["user"]["age_group"] == "24-30"

    # Query MySQL directly to confirm persistent records
    with app.app_context():
        user_in_db = User.query.filter_by(email=test_email).first()
        sessions_in_db = PracticeSession.query.filter_by(user_id=user_in_db.id).all()
        bugs_in_db = BugReport.query.filter_by(user_id=user_in_db.id).all()
        snapshot_in_db = UserProgressSnapshot.query.filter_by(user_id=user_in_db.id).first()

        print(f" -> Direct MySQL Check: User {user_in_db.name} has {len(sessions_in_db)} practice sessions, {len(bugs_in_db)} bug reports, and snapshot streak {snapshot_in_db.current_streak}")
        assert len(sessions_in_db) == 3
        assert len(bugs_in_db) == 1
        assert snapshot_in_db is not None

    print("=== ALL TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    run_tests()
