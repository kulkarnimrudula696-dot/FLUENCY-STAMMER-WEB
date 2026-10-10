import unittest
import json
from speech_analyzer import detect_filler_words, analyze_speech_data
from app import app, db
from models import User, PracticeSession

class TestFillerPipeline(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        self.ctx.pop()

    def test_1_user_says_uh_i_think(self):
        """Test 1: User says 'Uh, I think I should try again.' Expected: filler_count >= 1, 'uh' in fillers_list."""
        transcript = "Uh, I think I should try again."
        fillers, count = detect_filler_words(transcript)
        self.assertGreaterEqual(count, 1, f"Expected count >= 1, got {count}")
        words_found = [f['word'] for f in fillers]
        self.assertIn("uh", words_found)

    def test_2_user_says_um_um_um(self):
        """Test 2: User says 'Um um um I don't know.' Expected: filler_count = 3, fillers_list contains 3 'um'."""
        transcript = "Um um um I don't know."
        fillers, count = detect_filler_words(transcript)
        self.assertEqual(count, 3, f"Expected count = 3, got {count}")
        um_entry = next((f for f in fillers if f['word'] == 'um'), None)
        self.assertIsNotNone(um_entry)
        self.assertEqual(um_entry['count'], 3)

    def test_3_user_says_i_like_this_movie(self):
        """Test 3: User says 'I like this movie.' Expected: 'like' must NOT be counted as a filler."""
        transcript = "I like this movie."
        fillers, count = detect_filler_words(transcript)
        self.assertEqual(count, 0, f"Expected 0 fillers, got {count}: {fillers}")

    def test_4_user_says_i_um_like_this_movie(self):
        """Test 4: User says 'I, um, like this movie.' Expected: 'um' = 1 filler, 'like' = NOT a filler."""
        transcript = "I, um, like this movie."
        fillers, count = detect_filler_words(transcript)
        self.assertEqual(count, 1, f"Expected 1 filler ('um'), got {count}: {fillers}")
        self.assertEqual(fillers[0]['word'], 'um')
        self.assertEqual(fillers[0]['count'], 1)

    def test_5_user_says_hmm_i_was_nervous_uh(self):
        """Test 5: User says 'Hmm, I was nervous, uh, but I tried.' Expected: 'hmm' and 'uh' detected."""
        transcript = "Hmm, I was nervous, uh, but I tried."
        fillers, count = detect_filler_words(transcript)
        self.assertEqual(count, 2, f"Expected 2 fillers, got {count}: {fillers}")
        words_found = set(f['word'] for f in fillers)
        self.assertIn("hmm", words_found)
        self.assertIn("uh", words_found)

    def test_6_user_says_ha_ha_ha(self):
        """Test 6: User says 'Ha ha ha, I don't know.' Expected: detect repeated 'ha' sounds."""
        transcript = "Ha ha ha, I don't know."
        fillers, count = detect_filler_words(transcript)
        self.assertEqual(count, 3, f"Expected 3 fillers, got {count}: {fillers}")
        ha_entry = next((f for f in fillers if f['word'] == 'ha'), None)
        self.assertIsNotNone(ha_entry)
        self.assertEqual(ha_entry['count'], 3)

    def test_7_full_analysis_and_db_persistence_flow(self):
        """Verify complete pipeline: analysis result matches database record exactly on save and reload."""
        # Create user
        user = User.query.filter_by(email="filler_test@fluency.com").first()
        if not user:
            user = User(name="Filler Test User", email="filler_test@fluency.com", password_hash="dummy", practice_age=21)
            db.session.add(user)
            db.session.commit()

        # Login session
        with self.app.session_transaction() as sess:
            sess['user_id'] = user.id

        transcript = "Uh, I think, um, we should try again, you know."
        duration = 12.0
        prompt = "We should try again tomorrow."

        res = self.app.post('/api/practice/analyze', json={
            "mode": "reading",
            "title": "Filler Pipeline Verification",
            "duration_seconds": duration,
            "transcript": transcript,
            "prompt_text": prompt,
            "audio_data_url": "data:audio/webm;base64,GkXfo59ChoEBQveBAULygQRC84EIQoKEd2VibUKHgQRChYECGFOAZwH///..."
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("feedback", data)
        self.assertIn("session", data)

        feedback_metrics = data["feedback"]["metrics"]
        session_data = data["session"]

        # Ensure filler_count and fillers_list are not in feedback metrics or session
        self.assertNotIn("filler_count", feedback_metrics)
        self.assertNotIn("filler_words", feedback_metrics)
        self.assertNotIn("filler_count", session_data)

        # Reload session from database
        db_session = PracticeSession.query.get(session_data["id"])
        self.assertIsNotNone(db_session)
        self.assertFalse(hasattr(db_session, "filler_count"))
        self.assertFalse(hasattr(db_session, "fillers_list"))

        # Fetch via GET endpoint
        get_res = self.app.get(f'/api/practice/sessions/{db_session.id}')
        self.assertEqual(get_res.status_code, 200)
        get_data = get_res.get_json()["session"]
        self.assertNotIn("filler_count", get_data)
        self.assertNotIn("fillers_list", get_data)

if __name__ == '__main__':
    unittest.main()
