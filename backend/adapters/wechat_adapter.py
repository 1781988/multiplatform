from .base_adapter import BaseAdapter


class WeChatAdapter(BaseAdapter):
    platform_name = "wechat"

    def adapt_title(self, title: str) -> str:
        if "：" in title or ":" in title:
            return title.replace(":", "：")
        return f"{title}：系统提升指南"

    def adapt_content(self, content: str) -> str:
        return (
            "导语：\n"
            + content
            + "\n\n核心要点：\n"
            "1. 明确目标与学习计划\n"
            "2. 高效整理与知识拆解\n"
            "3. 复盘与总结行动"
        )

    def adapt_tags(self, tags: list) -> list:
        return tags[:3]

    def adapt(self, data: dict) -> dict:
        result = super().adapt(data)
        result["summary"] = self._summary(result.get("content", ""))
        return result
