import sys
import json
import unittest
from app import app, db
from models import User, PracticeSession
import content_data
from speech_analyzer import analyze_speech_data, detect_filler_words
from conversation_engine import generate_conversation_reply

sys.stdout.reconfigure(encoding='utf-8')

class TestConversationMode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()
        with app.app_context():
            user = User.query.filter_by(email="tester_convo@fluency.com").first()
            if not user:
                user = User(
                    name="Tester Alex",
                    email="tester_convo@fluency.com",
                    actual_age=21,
                    practice_age=21,
                    preferred_language="English"
                )
                user.set_password("pass123")
                db.session.add(user)
                db.session.commit()
            cls.user_id = user.id

    def login(self):
        return self.client.post('/api/auth/login', json={
            "email": "tester_convo@fluency.com",
            "password": "pass123"
        })

    def test_1_ten_scenarios_available(self):
        """Verify all 10 required real-life scenarios are present."""
        scenarios = content_data.CONVERSATION_SCENARIOS
        self.assertEqual(len(scenarios), 10, "Must have exactly 10 scenarios")
        
        expected_ids = [
            'scen_intro', 'scen_friend', 'scen_college', 'scen_interview',
            'scen_restaurant', 'scen_shopping', 'scen_directions',
            'scen_teacher', 'scen_doctor', 'scen_phone'
        ]
        
        actual_ids = [s['id'] for s in scenarios]
        for eid in expected_ids:
            self.assertIn(eid, actual_ids, f"Scenario {eid} must be present")

        # Test API endpoint
        res = self.client.get('/api/content/scenarios')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(len(data['items']), 10)

    def test_2_scenarios_multilingual(self):
        """Verify scenario translations for Hindi and Marathi."""
        res_hi = self.client.get('/api/content/scenarios?language=Hindi')
        data_hi = res_hi.get_json()
        self.assertEqual(len(data_hi['items']), 10)
        intro_hi = next(s for s in data_hi['items'] if s['id'] == 'scen_intro')
        self.assertIn("परिचय", intro_hi['title'])

        res_mr = self.client.get('/api/content/scenarios?language=Marathi')
        data_mr = res_mr.get_json()
        self.assertEqual(len(data_mr['items']), 10)
        intro_mr = next(s for s in data_mr['items'] if s['id'] == 'scen_intro')
        self.assertIn("ओळख", intro_mr['title'])

    def test_3_conversation_chat_multi_turn_no_repetition(self):
        """Test dynamic AI dialogue with strict zero question repetition across 5 turns."""
        history = []
        user_turns = [
            "Hi, my name is Alex and I enjoy programming and developing web apps.",
            "I got into it when I built my first website in high school.",
            "I really love collaborating with creative designers and solving algorithms.",
            "In my free time, I like hiking in national parks and taking photos.",
            "I would love to explore Japan next year."
        ]

        asked_questions = set()
        for u_text in user_turns:
            reply_obj = generate_conversation_reply(
                scenario_id="scen_intro",
                user_message=u_text,
                history=history,
                language="English"
            )
            reply = reply_obj['reply']
            self.assertTrue(len(reply) > 10)
            self.assertNotIn(reply, asked_questions, "AI must not repeat identical replies")
            asked_questions.add(reply)
            
            history.append({"sender": "user", "text": u_text})
            history.append({"sender": "ai", "text": reply})

        self.assertEqual(len(history), 10)

    def test_4_filler_word_disambiguation(self):
        """Test that grammatical words ('like', 'well', 'so') are NOT false-positive fillers."""
        # 1. Grammatical 'like'
        f1, c1 = detect_filler_words("I like this movie very much and I like reading.")
        self.assertEqual(c1, 0, f"Expected 0 fillers for grammatical like, got {c1}: {f1}")

        f2, c2 = detect_filler_words("I would like to order a fresh garden salad.")
        self.assertEqual(c2, 0, f"Expected 0 fillers, got {c2}: {f2}")

        f3, c3 = detect_filler_words("It looks like rain outside today.")
        self.assertEqual(c3, 0, f"Expected 0 fillers, got {c3}: {f3}")

        # 2. Filler 'like'
        f4, c4 = detect_filler_words("I was, like, really surprised when they arrived.")
        self.assertEqual(c4, 1, f"Expected 1 filler ('like'), got {c4}: {f4}")
        self.assertEqual(f4[0]['word'], 'like')

        # 3. Pure fillers + phrases
        f5, c5 = detect_filler_words("Um, well, basically I arrived late, you know.")
        # 'um' (1) + 'well' (1) + 'basically' (1) + 'you know' (1) = 4
        self.assertEqual(c5, 4, f"Expected 4 fillers, got {c5}: {f5}")

        # 4. Hindi filler
        f6, c6 = detect_filler_words("मैं मतलब घर जा रहा था और उम थक गया था।", language="Hindi")
        self.assertGreaterEqual(c6, 2)

        # 5. Marathi filler
        f7, c7 = detect_filler_words("मला म्हणजे खूप छान वाटले आणि सांगायचं म्हणजे अभ्यास पूर्ण झाला.", language="Marathi")
        self.assertGreaterEqual(c7, 2)

    def test_5_conversation_speech_analysis(self):
        """Verify conversation mode analysis feedback and scoring."""
        transcript = "I was, um, thinking about the project, and, like, we should basically meet tomorrow, you know."
        result = analyze_speech_data(
            transcript=transcript,
            audio_duration_seconds=18.0,
            prompt_text="Talking about presentation",
            mode="conversation",
            language="English"
        )

        metrics = result['metrics']
        self.assertGreater(metrics['words_spoken'], 10)
        self.assertNotIn('filler_words', metrics)
        self.assertNotIn('filler_count', metrics)
        self.assertIn('speaking_time_seconds', metrics)
        self.assertIn('speaking_rate_wpm', metrics)
        self.assertIn('long_pauses', metrics)
        self.assertIn('repetitions', metrics)
        self.assertEqual(result['paragraph_match']['is_reading_mode'], False)
        
        # Verify no filler feedback cards exist
        cards = result['needs_improvement']
        filler_card = next((c for c in cards if 'Filler' in c['issue']), None)
        self.assertIsNone(filler_card, "Filler words count feature must be completely removed from feedback cards")

    def test_6_conversation_chat_api_endpoint(self):
        """Test POST /api/conversation/chat endpoint."""
        self.login()
        res = self.client.post('/api/conversation/chat', json={
            "scenario_id": "scen_interview",
            "user_message": "I have 3 years of software engineering experience focusing on Python and React.",
            "history": [],
            "language": "English"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('reply', data)
        self.assertIn('speaking_tip', data)
        self.assertEqual(data['scenario_title'], 'Job Interview')


if __name__ == '__main__':
    unittest.main(verbosity=2)
