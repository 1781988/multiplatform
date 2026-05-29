# 接口文档

## POST /api/content/generate

请求参数：

```json
{
  "title": "如何提高学习效率",
  "content": "本文介绍几种提高学习效率的方法。",
  "tags": ["学习", "效率"],
  "platforms": ["wechat", "zhihu", "bilibili", "xiaohongshu"],
  "use_ai": true,
  "llm_provider": "openai",
  "media_files": {
    "images": ["/uploads/images/study_scene_1.png"],
    "videos": ["/uploads/videos/ai_learning_demo.mp4"],
    "cover": "/uploads/covers/cover_ai_learning.jpg"
  }
}
```

返回示例：

```json
{
  "code": 200,
  "message": "生成成功",
  "task_id": 1,
  "data": {
    "wechat": {
      "platform": "wechat",
      "title": "...",
      "content": "...",
      "summary": "...",
      "tags": ["..."],
      "images": ["..."],
      "cover": "..."
    }
  }
}
```

## POST /api/publish

请求参数：

```json
{
  "task_id": 1,
  "platforms": ["wechat", "zhihu"],
  "contents": {}
}
```

返回示例：

```json
{
  "code": 200,
  "message": "发布完成",
  "data": [
    {
      "platform": "wechat",
      "status": "success",
      "message": "发布成功",
      "publish_time": "2026-05-29T10:00:00"
    }
  ]
}
```

## GET /api/records

Response:

```json
{
  "code": 200,
  "data": [
    {
      "id": 1,
      "platform": "wechat",
      "title": "...",
      "status": "success",
      "message": "发布成功",
      "publish_time": "2026-05-29T10:00:00"
    }
  ]
}

## GET /api/llm/providers

返回示例：

```json
{
  "code": 200,
  "data": [
    "openai",
    "gemini",
    "qwen",
    "deepseek",
    "ollama",
    "local"
  ]
}
```

## POST /api/upload/image

请求类型：`multipart/form-data`

返回示例：

```json
{
  "code": 200,
  "message": "图片上传成功",
  "data": {
    "file_name": "cover_ai_learning.jpg",
    "file_url": "/uploads/images/cover_ai_learning.jpg",
    "file_type": "image",
    "size": 204800
  }
}
```

## POST /api/upload/video

请求类型：`multipart/form-data`

返回示例：

```json
{
  "code": 200,
  "message": "视频上传成功",
  "data": {
    "file_name": "ai_learning_demo.mp4",
    "file_url": "/uploads/videos/ai_learning_demo.mp4",
    "file_type": "video",
    "size": 10485760
  }
}
```

## POST /api/upload/cover

请求类型：`multipart/form-data`

返回示例：

```json
{
  "code": 200,
  "message": "封面上传成功",
  "data": {
    "file_name": "cover.jpg",
    "file_url": "/uploads/covers/cover.jpg",
    "file_type": "cover",
    "size": 204800
  }
}
```
```
