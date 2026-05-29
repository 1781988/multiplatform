# 聚发舟 MultiPost AI

一个基于 Vue 3 + FastAPI 的原型系统，支持将同一篇草稿自动生成公众号、知乎、B站和小红书的发布版本，并提供素材上传与模拟发布。

## 功能说明

- 输入标题、正文、标签、作者信息并选择平台
- 上传图片、视频、封面等素材
- 4 个平台内容自动适配生成
- 支持 AI 模型选择与一键生成
- 逐平台预览与编辑
- 模拟发布并记录状态
- 发布历史存储在 SQLite

## 技术栈

- 前端：Vue 3 + Vite
- 后端：FastAPI
- 存储：SQLite

## 项目结构

```
backend/
frontend/
docs/
```

## API 概览

- `POST /api/content/generate`：生成平台适配内容
- `GET /api/llm/providers`：获取可选模型列表
- `POST /api/upload/image`：上传图片
- `POST /api/upload/video`：上传视频
- `POST /api/upload/cover`：上传封面
- `POST /api/publish`：模拟发布并保存发布记录
- `GET /api/records`：查询发布历史

详细接口可参考 `docs/api.md`。

## 本地运行

### 启动后端

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

后端默认地址：`http://127.0.0.1:8000`

### 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端默认地址：`http://127.0.0.1:5173`

## 使用说明

1. 打开前端页面后输入标题、正文、标签、作者信息。
2. 上传图片、视频、封面素材（可选）。
3. 选择 AI 模型与平台（公众号、知乎、B 站、小红书）。
4. 点击“生成”，系统会根据平台规则生成对应预览内容。
5. 在预览区域可逐个平台编辑标题、正文、标签等字段。
6. 点击“模拟发布”，系统会保存模拟发布记录并显示发布结果。
7. 在“发布记录”中查看历史发布状态。

## 测试

在 `backend/` 下运行：

```bash
cd backend
pip install -r requirements.txt
python -m unittest discover -s tests
```

## 注意事项

- 当前发布为模拟发布，不会真正调用任何平台 API。
- 新平台适配规则可在 `backend/adapters/` 中新增适配器并注册。
- 如果需要扩展 AI 改写，可在后端适配器中补充改写逻辑。
