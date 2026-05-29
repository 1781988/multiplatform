import sys
from pathlib import Path
import unittest

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from database.db import init_db
from main import app


class ApiIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        init_db()
        cls.client = TestClient(app)

    def test_generate_api_success(self) -> None:
        payload = {
            "title": "如何提高学习效率",
            "content": "本文介绍几种提高学习效率的方法，包括目标拆解和复盘。",
            "tags": ["学习", "效率"],
            "platforms": ["wechat", "zhihu", "bilibili", "xiaohongshu"],
            "use_ai": False,
            "llm_provider": "openai",
            "media_files": {
                "images": ["/uploads/images/cover.jpg"],
                "videos": ["/uploads/videos/demo.mp4"],
                "cover": "/uploads/covers/cover.jpg",
            },
        }

        response = self.client.post("/api/content/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["code"], 200)
        self.assertEqual(data["message"], "生成成功")
        self.assertIn("task_id", data)
        self.assertEqual(set(data["data"].keys()), set(payload["platforms"]))
        self.assertEqual(data["data"]["wechat"]["cover"], payload["media_files"]["cover"])

    def test_adapt_api_validation_error(self) -> None:
        response = self.client.post(
            "/api/content/generate", json={"title": "", "content": "", "platforms": []}
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["message"], "标题不能为空")

    def test_llm_providers(self) -> None:
        response = self.client.get("/api/llm/providers")
        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertIn("openai", data)

    def test_publish_api_full_flow(self) -> None:
        adapt_payload = {
            "title": "测试发布",
            "content": "测试内容。",
            "tags": ["测试"],
            "platforms": ["wechat", "zhihu"],
            "media_files": {
                "images": ["/uploads/images/cover.jpg"],
                "cover": "/uploads/covers/cover.jpg",
            },
        }
        adapt_response = self.client.post("/api/content/generate", json=adapt_payload)
        self.assertEqual(adapt_response.status_code, 200)
        result = adapt_response.json()
        task_id = result["task_id"]

        publish_payload = {
            "task_id": task_id,
            "platforms": ["wechat", "zhihu"],
        }
        publish_response = self.client.post("/api/publish", json=publish_payload)
        self.assertEqual(publish_response.status_code, 200)
        publish_data = publish_response.json()
        self.assertEqual(publish_data["message"], "发布完成")
        self.assertEqual(len(publish_data["data"]), 2)

        records_response = self.client.get("/api/records?limit=5")
        self.assertEqual(records_response.status_code, 200)
        records = records_response.json()["data"]
        self.assertIsInstance(records, list)
        self.assertTrue(any(record["platform"] == "wechat" for record in records))

    def test_publish_api_error_missing_contents(self) -> None:
        payload = {"task_id": 1000, "platforms": ["wechat"]}
        response = self.client.post("/api/publish", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "内容不存在")
