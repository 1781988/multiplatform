from datetime import datetime, timezone

from database.db import create_publish_record


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
        if not video:
            return "failed", "缺少视频", title, main_content

    return "success", "发布成功", title, main_content


def simulate_publish(task_id: int, platforms: list, contents: dict) -> list:
    results = []

    for platform in platforms:
        content = contents.get(platform)
        status = "failed"
        message = "内容缺失"
        title = ""
        final_content = ""

        if content:
            status, message, title, final_content = _validate_platform(platform, content)

        publish_time = datetime.now(timezone.utc).isoformat()
        create_publish_record(
            task_id=task_id,
            platform=platform,
            final_title=title,
            final_content=final_content,
            status=status,
            message=message,
            publish_time=publish_time,
        )

        results.append(
            {
                "platform": platform,
                "status": status,
                "message": message,
                "publish_time": publish_time,
            }
        )

    return results
