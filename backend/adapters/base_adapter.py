class BaseAdapter:
    platform_name = ""

    @staticmethod
    def _merge_tags(tags: list, extras: list, limit: int | None = None) -> list:
        seen = set()
        merged = []

        for item in tags + extras:
            if not item:
                continue
            key = str(item).strip()
            if not key or key in seen:
                continue
            merged.append(key)
            seen.add(key)
            if limit and len(merged) >= limit:
                break

        return merged

    def adapt_title(self, title: str) -> str:
        raise NotImplementedError

    def adapt_content(self, content: str) -> str:
        raise NotImplementedError

    def adapt_tags(self, tags: list) -> list:
        raise NotImplementedError

    def adapt(self, data: dict) -> dict:
        images, videos, cover = self._extract_media(data)
        result = {
            "platform": self.platform_name,
            "title": self.adapt_title(data["title"]),
            "content": self.adapt_content(data["content"]),
            "tags": self.adapt_tags(data.get("tags", [])),
            "images": images,
            "videos": videos,
            "cover": cover,
        }
        return result

    @staticmethod
    def _extract_media(data: dict) -> tuple[list, list, str | None]:
        media = data.get("media_files") or {}
        images = list(media.get("images", []))
        videos = list(media.get("videos", []))
        cover = media.get("cover") or data.get("cover_image")
        return images, videos, cover

    @staticmethod
    def _summary(content: str, limit: int = 80) -> str:
        cleaned = str(content).strip().replace("\n", " ")
        if len(cleaned) <= limit:
            return cleaned
        return cleaned[:limit].rstrip() + "..."
