import unittest
import json
from speech_analyzer import analyze_speech_data
from app import app, db
from models import User, PracticeSession

class TestFeedbackNoFiller(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        self.ctx.pop()

    def test_1_speech_analysis_metrics_contain_no_filler_fields(self):
        """Verify that metrics returned across modes contain no filler words count or lists."""
        modes = ["reading", "conversation", "twister", "media"]
        transcript = "I was, um, wondering if we could, uh, meet tomorrow to basically discuss the project."
        
        for mode in modes:
            result = analyze_speech_data(
                transcript=transcript,
                audio_duration_seconds=12.0,
                prompt_text="Discussing the project",
                mode=mode,
                language="English"
            )
            metrics = result["metrics"]
            self.assertNotIn("filler_words", metrics, f"Mode {mode} must not return 'filler_words'")
            self.assertNotIn("filler_words_display", metrics, f"Mode {mode} must not return 'filler_words_display'")
            self.assertNotIn("fillers_list", metrics, f"Mode {mode} must not return 'fillers_list'")
            self.assertNotIn("filler_count", metrics, f"Mode {mode} must not return 'filler_count'")

            # Verify preserved metrics
            self.assertIn("speaking_time_seconds", metrics)
            self.assertIn("speaking_time_display", metrics)
            self.assertIn("words_spoken", metrics)
            self.assertIn("words_spoken_display", metrics)
            self.assertIn("speaking_rate_wpm", metrics)
            self.assertIn("speaking_rate_display", metrics)
            self.assertIn("long_pauses", metrics)
            self.assertIn("repetitions", metrics)
            self.assertIn("practice_score", metrics)
            self.assertIn("clarity_score", metrics)
            self.assertIn("consistency_score", metrics)

    def test_2_feedback_messages_and_cards_contain_no_filler_references(self):
        """Verify no filler-word-specific messages, cards, or notes exist in feedback."""
        transcript = "Um, uh, well, you know, I think we should start now."
        result = analyze_speech_data(
            transcript=transcript,
            audio_duration_seconds=10.0,
            prompt_text="Starting the meeting",
            mode="conversation",
            language="English"
        )
        # Check what_went_well
        for item in result["what_went_well"]:
            self.assertNotIn("filler", item.lower())
            self.assertNotIn("um", item.lower())
        
        # Check needs_improvement cards and list
        for card in result["needs_improvement"]:
            self.assertNotIn("filler", card["issue"].lower())
        
        feedback_dict = result["your_speech_feedback"]
        for item in feedback_dict.get("what_needs_improvement", []):
            self.assertNotIn("filler", item.lower())

        self.assertNotIn("filler", feedback_dict.get("what_to_practise_next", "").lower())
        self.assertNotIn("filler", result.get("pattern_noticed", "").lower())
        self.assertNotIn("filler", result.get("practice_score_focus", "").lower())

    def test_3_multilingual_feedback_has_no_filler_text(self):
        """Verify Hindi and Marathi feedback contain no filler sound text."""
        # Hindi
        hi_result = analyze_speech_data(
            transcript="मैं मतलब जा रहा था और उम थक गया था।",
            audio_duration_seconds=8.0,
            prompt_text="घर जाना",
            mode="conversation",
            language="Hindi"
        )
        for card in hi_result["needs_improvement"]:
            self.assertNotIn("फ़िलर", card["issue"])
            self.assertNotIn("फिलर", card["issue"])
        self.assertNotIn("फ़िलर", hi_result["pattern_noticed"])

        # Marathi
        mr_result = analyze_speech_data(
            transcript="मला म्हणजे छान वाटले आणि म्हणजे अभ्यास पूर्ण झाला.",
            audio_duration_seconds=8.0,
            prompt_text="सराव पूर्ण",
            mode="conversation",
            language="Marathi"
        )
        for card in mr_result["needs_improvement"]:
            self.assertNotIn("फिलर्स", card["issue"])
            self.assertNotIn("अनावश्यक शब्द", card["issue"])
        self.assertNotIn("अनावश्यक शब्द", mr_result["pattern_noticed"])

    def test_4_empty_audio_returns_cleanly_without_filler_fields(self):
        """Verify empty/silent audio produces clean feedback without filler words count."""
        result = analyze_speech_data(
            transcript="",
            audio_duration_seconds=0.0,
            prompt_text="Sample prompt",
            mode="reading"
        )
        metrics = result["metrics"]
        self.assertNotIn("filler_words", metrics)
        self.assertNotIn("filler_count", metrics)
        self.assertNotIn("fillers_list", metrics)
        self.assertEqual(metrics["speaking_time_seconds"], 0.0)
        self.assertEqual(metrics["words_spoken"], 0)

    def test_5_api_and_database_persistence_flow(self):
        """Verify POST /api/practice/analyze handles response and saves DB record without error."""
        user = User.query.filter_by(email="test_no_filler@fluency.com").first()
        if not user:
            user = User(name="No Filler User", email="test_no_filler@fluency.com", password_hash="dummy", practice_age=22)
            db.session.add(user)
            db.session.commit()

        with self.app.session_transaction() as sess:
            sess['user_id'] = user.id

        transcript = "The sunset was bright orange and the waves were calm."
        res = self.app.post('/api/practice/analyze', json={
            "mode": "reading",
            "title": "Ocean Sunset",
            "duration_seconds": 15.0,
            "transcript": transcript,
            "prompt_text": "The sunset was bright orange and the waves were calm.",
            "audio_data_url": "data:audio/webm;base64,GkXfo59ChoEBQveBAULygQRC84EIQoKEd2VibUKHgQRChYECGFOAZwH///..."
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("feedback", data)
        self.assertIn("session", data)
        self.assertNotIn("filler_words", data["feedback"]["metrics"])
        self.assertNotIn("filler_count", data["feedback"]["metrics"])

        # DB session has no filler_count or fillers_list attributes/columns
        session_id = data["session"]["id"]
        saved = PracticeSession.query.get(session_id)
        self.assertIsNotNone(saved)
        self.assertFalse(hasattr(saved, "filler_count"))
        self.assertFalse(hasattr(saved, "fillers_list"))
        self.assertNotIn("filler_count", data["session"])
        self.assertNotIn("fillers_list", data["session"])
        self.assertEqual(saved.duration_seconds, 15)

    def test_6_database_table_columns_do_not_contain_filler_fields(self):
        """Verify the database table schema itself does not contain filler_count or fillers_list."""
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [c['name'] for c in inspector.get_columns('practice_sessions')]
        self.assertNotIn('filler_count', columns)
        self.assertNotIn('fillers_list', columns)
        # Verify other columns are properly preserved
        self.assertIn('wpm', columns)
        self.assertIn('pauses_count', columns)
        self.assertIn('repetitions_count', columns)
        self.assertIn('clarity_score', columns)

if __name__ == '__main__':
    unittest.main()
