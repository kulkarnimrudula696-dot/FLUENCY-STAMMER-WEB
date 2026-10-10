import unittest
import json
from app import app
from content_data import THERAPY_VIDEOS, get_therapy_videos

class TestTherapyVideosModule(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_1_twenty_videos_present(self):
        """Verify that exactly 20 therapy videos are defined with complete metadata."""
        self.assertEqual(len(THERAPY_VIDEOS), 20)
        for v in THERAPY_VIDEOS:
            self.assertTrue(v["id"].startswith("therapy_vid_"))
            self.assertTrue(bool(v["title"]))
            self.assertTrue(bool(v["source"]))
            self.assertTrue(bool(v["youtube_id"]))
            self.assertEqual(v["thumbnail"], f"https://img.youtube.com/vi/{v['youtube_id']}/hqdefault.jpg")
            self.assertTrue(v["category_key"] in ["kids", "teens", "parents", "techniques", "emotions"])
            self.assertTrue(len(v["key_takeaways"]) > 0)
            self.assertTrue(bool(v["description"]))

    def test_2_api_endpoint_all(self):
        """Test GET /api/content/therapy-videos returns all 20 videos."""
        res = self.app.get('/api/content/therapy-videos')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["count"], 20)
        self.assertEqual(data["total"], 20)
        self.assertEqual(len(data["items"]), 20)

    def test_3_api_categories(self):
        """Test filtering by category returns matching videos."""
        categories = ["kids", "teens", "parents", "techniques", "emotions"]
        total_categorized = 0
        for cat in categories:
            res = self.app.get(f'/api/content/therapy-videos?category={cat}')
            self.assertEqual(res.status_code, 200)
            data = json.loads(res.data)
            self.assertGreater(data["count"], 0)
            for item in data["items"]:
                self.assertEqual(item["category_key"], cat)
            total_categorized += data["count"]
        self.assertEqual(total_categorized, 20)

    def test_4_search_filter(self):
        """Test search query filtering."""
        res = self.app.get('/api/content/therapy-videos?q=ADHD')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["items"][0]["id"], "therapy_vid_18")

if __name__ == '__main__':
    unittest.main()
