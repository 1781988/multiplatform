from datetime import datetime, timezone
from uuid import uuid4

from database.db import create_publish_record


class MockPublisher:
    def publish(self, platform: str, title: str, content: str) -> str:
        return f"mock_{platform}_{uuid4().hex[:12]}"


def _get_main_content(platform: str, content: dict) -> str:
    if platform == "bilibili":
        return str(content.get("description", "")).strip()
    return str(content.get("content", "")).strip()


def _validate_platform(platform: str, content: dict) -> tuple[str, str, str, str]:
    title = str(content.get("title", "")).strip()
    main_content = _get_main_content(platform, content)

    if not title:
        return "failed", "缺少标题", title, main_content

    if not main_content:
        return "failed", "内容缺失", title, main_content

    if platform == "bilibili":
        video = str(content.get("video", "")).strip()
        videos = content.get("videos") or []
        if not video:
            video = str(videos[0]).strip() if videos else ""
        if not video:
            return "failed", "缺少视频素材", title, main_content

    return "success", "发布成功", title, main_content


def simulate_publish(task_id: int, platforms: list, contents: dict) -> list:
    results = []
    publisher = MockPublisher()

    for platform in platforms:
        content = contents.get(platform)
        status = "failed"
        message = "内容缺失"
        title = ""
        final_content = ""
        mock_publish_id = None

        if content:
            status, message, title, final_content = _validate_platform(platform, content)
            if status == "success":
                mock_publish_id = publisher.publish(platform, title, final_content)
                message = "模拟发布成功"

        publish_time = datetime.now(timezone.utc).isoformat()
        record_id = create_publish_record(
            task_id=task_id,
            platform=platform,
            final_title=title,
            final_content=final_content,
            status=status,
            message=message,
            publish_time=publish_time,
            mock_publish_id=mock_publish_id,
        )

        results.append(
            {
                "id": record_id,
                "platform": platform,
                "title": title,
                "status": status,
                "message": message,
                "mock_publish_id": mock_publish_id,
                "publish_time": publish_time,
            }
        )

    return results
