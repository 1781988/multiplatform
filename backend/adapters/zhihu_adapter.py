from .base_adapter import BaseAdapter


class ZhihuAdapter(BaseAdapter):
    platform_name = "zhihu"

    def adapt_title(self, title: str) -> str:
        cleaned = str(title).strip()
        if cleaned.endswith(("?", "？")):
            return cleaned.replace("?", "？")
        return f"{cleaned}？"

    def adapt_content(self, content: str) -> str:
        return (
            "简短回答：把 AI 当作学习助手，而不是代写工具。\n\n"
            "分析思路：\n"
            "1. 先拆解目标，再组织材料。\n"
            "2. 保持固定的整理与复盘流程。\n"
            "3. 用 AI 追踪进度与反馈。\n\n"
            "展开说明：\n"
            + content
            + "\n\n结论：持续复盘，比临时冲刺更有效。"
        )

    def adapt_tags(self, tags: list) -> list:
        return tags[:5]

    def adapt(self, data: dict) -> dict:
        result = super().adapt(data)
        result["summary"] = self._summary(result.get("content", ""))
        return result
