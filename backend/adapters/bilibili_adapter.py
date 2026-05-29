from .base_adapter import BaseAdapter


class BilibiliAdapter(BaseAdapter):
    platform_name = "bilibili"

    def adapt_title(self, title: str) -> str:
        return f"{title}，这些方法真的好用"

    def adapt_description(self, content: str) -> str:
        return "本期视频分享实用方法与案例拆解。\n\n" + content

    def adapt_tags(self, tags: list) -> list:
        return tags[:5]

    def adapt(self, data: dict) -> dict:
        images, videos, cover = self._extract_media(data)
        video = videos[0] if videos else ""
        result = {
            "platform": self.platform_name,
            "title": self.adapt_title(data["title"]),
            "description": self.adapt_description(data["content"]),
            "category": "知识",
            "tags": self.adapt_tags(data.get("tags", [])),
            "video": video,
            "images": images,
            "videos": videos,
            "cover": cover,
        }
        return result
