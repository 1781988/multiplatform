from .base_adapter import BaseAdapter


class XiaohongshuAdapter(BaseAdapter):
    platform_name = "xiaohongshu"

    _sentence_marks = (".", "!", "?", "\u3002", "\uff01", "\uff1f")

    def adapt_title(self, title: str) -> str:
        return f"{title}，真的好用！"

    def adapt_content(self, content: str) -> str:
        adjusted = content
        for mark in self._sentence_marks:
            adjusted = adjusted.replace(mark, f"{mark}\n")
        return adjusted.strip() + "\n\n#学习方法 #效率提升"

    def adapt_tags(self, tags: list) -> list:
        return self._merge_tags(tags, ["学习方法", "效率提升"])

    def adapt(self, data: dict) -> dict:
        result = super().adapt(data)
        if result.get("videos"):
            result["video"] = result["videos"][0]
        return result
