import sys
import unittest
import datetime
from app import app, db
from models import User, PracticeSession, UserProgressSnapshot

sys.stdout.reconfigure(encoding='utf-8')

class TestOverallProgress(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()
        with app.app_context():
            # Create User A
            user_a = User.query.filter_by(email="test_user_a@fluency.com").first()
            if not user_a:
                user_a = User(
                    name="User Alpha",
                    email="test_user_a@fluency.com",
                    actual_age=22,
                    practice_age=22,
                    preferred_language="English"
                )
                user_a.set_password("pass123")
                db.session.add(user_a)

            # Create User B (Empty user)
            user_b = User.query.filter_by(email="test_user_b@fluency.com").first()
            if not user_b:
                user_b = User(
                    name="User Beta",
                    email="test_user_b@fluency.com",
                    actual_age=25,
                    practice_age=25,
                    preferred_language="English"
                )
                user_b.set_password("pass123")
                db.session.add(user_b)

            db.session.commit()
            cls.user_a_id = user_a.id
            cls.user_b_id = user_b.id

            # Clean existing sessions for tests
            PracticeSession.query.filter_by(user_id=user_a.id).delete()
            PracticeSession.query.filter_by(user_id=user_b.id).delete()
            UserProgressSnapshot.query.filter_by(user_id=user_a.id).delete()
            UserProgressSnapshot.query.filter_by(user_id=user_b.id).delete()
            db.session.commit()

    def login_user(self, email):
        return self.client.post('/api/auth/login', json={
            "email": email,
            "password": "pass123"
        })

    def test_1_insufficient_data_for_new_user(self):
        """User with 0 sessions should return has_data=False and 'Not enough data yet'."""
        self.login_user("test_user_b@fluency.com")
        res = self.client.get('/api/practice/progress-stats')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('overall_progress', data)
        op = data['overall_progress']
        self.assertFalse(op['has_data'])
        self.assertIsNone(op['percentage'])
        self.assertEqual(op['status_label'], "Not enough data yet")
        self.assertIn("Complete your first practice session", op['message'])
        self.assertEqual(op['explanation'], "Based on your practice activity and speech performance.")

    def test_2_dynamic_calculation_with_real_session(self):
        """Adding a real practice session calculates dynamic percentage strictly from database."""
        self.login_user("test_user_a@fluency.com")
        
        # Add Session 1 for User A
        with app.app_context():
            s1 = PracticeSession(
                user_id=self.user_a_id,
                mode="reading",
                title="The Art of Mindful Pausing",
                duration_seconds=30,
                wpm=125.0,
                pauses_count=2,
                repetitions_count=0,
                clarity_score=88.0,
                sentence_completion_pct=95.0,
                consistency_score=84.0,
                transcript="When we rush our speech we tense up and stumble over words."
            )
            db.session.add(s1)
            
            # Snapshot
            snap = UserProgressSnapshot(
                user_id=self.user_a_id,
                current_streak=1,
                total_practice_minutes=0.5,
                total_sessions_completed=1,
                average_clarity=88.0
            )
            db.session.add(snap)
            db.session.commit()

        res = self.client.get('/api/practice/progress-stats')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        op = data['overall_progress']
        self.assertTrue(op['has_data'])
        self.assertIsNotNone(op['percentage'])
        self.assertGreaterEqual(op['percentage'], 50)
        self.assertLessEqual(op['percentage'], 100)
        self.assertEqual(op['explanation'], "Based on your practice activity and speech performance.")
        self.assertIn('metrics_breakdown', op)
        self.assertAlmostEqual(op['metrics_breakdown']['clarity'], 88.0, delta=0.5)

        score_1 = op['percentage']

        # Add Session 2 with higher metrics
        with app.app_context():
            s2 = PracticeSession(
                user_id=self.user_a_id,
                mode="conversation",
                title="Conversation: Introducing Yourself",
                duration_seconds=45,
                wpm=130.0,
                pauses_count=1,
                repetitions_count=0,
                clarity_score=94.0,
                sentence_completion_pct=100.0,
                consistency_score=90.0,
                transcript="Hello, my name is Alex and I am glad to meet you today."
            )
            db.session.add(s2)
            db.session.commit()

        res2 = self.client.get('/api/practice/progress-stats')
        data2 = res2.get_json()
        op2 = data2['overall_progress']
        score_2 = op2['percentage']
        
        # Performance increased due to higher clarity, 0 fillers, 100% completion
        self.assertGreaterEqual(score_2, score_1)
        self.assertAlmostEqual(op2['metrics_breakdown']['clarity'], 91.0, delta=0.5)

    def test_3_user_isolation(self):
        """User B must still have no data even when User A has multiple sessions."""
        self.login_user("test_user_b@fluency.com")
        res = self.client.get('/api/practice/progress-stats')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        op = data['overall_progress']
        self.assertFalse(op['has_data'])
        self.assertIsNone(op['percentage'])
        self.assertEqual(op['status_label'], "Not enough data yet")


if __name__ == '__main__':
    unittest.main(verbosity=2)
