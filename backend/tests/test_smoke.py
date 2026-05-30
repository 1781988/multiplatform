import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from database.db import init_db, list_records
from models.schemas import ContentGenerateRequest, MediaFiles
from services.adapter_service import adapt_content
from services import llm_service
from services.publish_service import simulate_publish


class SmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = ContentGenerateRequest(
            title="如何提高学习效率",
            content="用清晰目标和持续复盘提升学习效率。",
            tags=["学习", "效率", "方法"],
            platforms=["wechat", "zhihu", "bilibili", "xiaohongshu"],
            media_files=MediaFiles(
                images=["/uploads/images/cover.jpg"],
                videos=["/uploads/videos/demo.mp4"],
                cover="/uploads/covers/cover.jpg",
            ),
        )

    def test_adapt_content_all_platforms(self) -> None:
        result = adapt_content(self.payload)
        self.assertEqual(set(result.keys()), set(self.payload.platforms))

        wechat = result["wechat"]
        self.assertIn("title", wechat)
        self.assertIn("content", wechat)

        bilibili = result["bilibili"]
        self.assertIn("description", bilibili)
        self.assertIn("category", bilibili)
        self.assertIn("cover", bilibili)
        self.assertIn("video", bilibili)

        for platform in self.payload.platforms:
            self.assertEqual(result[platform].get("cover"), self.payload.media_files.cover)

    def test_adapt_content_unsupported_platform(self) -> None:
        payload = ContentGenerateRequest(
            title="Test",
            content="Test content",
            platforms=["wechat", "unknown"],
        )

        with self.assertRaises(ValueError):
            adapt_content(payload)

    def test_ai_failure_falls_back_to_all_selected_platforms(self) -> None:
        payload = self.payload.model_copy(update={"use_ai": True, "llm_provider": "openai"})
        original = llm_service.get_llm_provider
        llm_service.get_llm_provider = lambda provider: None
        try:
            result = adapt_content(payload)
        finally:
            llm_service.get_llm_provider = original

        self.assertEqual(set(result.keys()), set(payload.platforms))
        self.assertIn("content", result["wechat"])
        self.assertIn("description", result["bilibili"])

    def test_simulate_publish_records(self) -> None:
        init_db()
        contents = adapt_content(self.payload)
        results = simulate_publish(
            task_id=1, platforms=self.payload.platforms, contents=contents
        )
        self.assertEqual(len(results), len(self.payload.platforms))
        for item in results:
            self.assertEqual(item["status"], "success")

        records = list_records(limit=5)
        self.assertGreaterEqual(len(records), 1)

    def test_simulate_publish_missing_content(self) -> None:
        init_db()
        contents = {
            "wechat": {"title": "", "content": ""},
            "zhihu": {"title": "Valid", "content": ""},
        }
        results = simulate_publish(
            task_id=2, platforms=["wechat", "zhihu"], contents=contents
        )
        self.assertEqual(results[0]["status"], "failed")
        self.assertEqual(results[1]["status"], "failed")


if __name__ == "__main__":
    unittest.main()
