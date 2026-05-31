# 聚舟 MultiPost AI

聚舟 MultiPost AI 是一个面向多平台内容运营场景的智能发布工作台。系统支持从同一份标题、正文、标签和素材出发，调用真实大模型或本地规则模板，生成适配公众号、知乎、B 站、小红书的多平台内容，并完成素材管理、账号授权状态管理、模拟发布、发布记录追踪和通知反馈。

## 演示视频

- 演示视频链接：https://www.alipan.com/s/ANzp6ZTXQBE


## 项目亮点

- 多平台内容一键生成：同一份草稿自动改写为公众号、知乎、B 站、小红书版本。
- 真实大模型接入：支持 OpenAI、Qwen、Gemini、DeepSeek、Ollama、Local，OpenAI Compatible 模型通过后端 HTTP 协议调用。
- 稳定降级策略：模型不可用、Key 错误或网络异常时自动降级为本地规则模板，保证演示流程不中断。
- 全局素材库：集中管理历史上传图片、视频、封面，支持筛选、删除、复制链接、加入当前创作任务。
- 模拟发布闭环：发布前校验内容、平台和账号登录状态，生成模拟发布 ID，保存发布记录。
- 详情追踪：发布记录支持标准表格、查看详情、删除记录，详情展示帖子标题、正文、标签、素材和模拟发布 ID。
- 主题与通知：支持亮色、深色、跟随系统主题；AI 生成、发布成功/失败、模型测试等事件进入通知中心。

## 核心功能

### 1. 内容创作

- 标题、正文、标签默认空白，避免自动填充干扰。
- 提供“填充样例内容”弹窗，可选择三组演示样例：
  - AI 学习效率
  - AI 办公视频
  - 智能产品测评
- 支持选择目标平台：公众号、知乎、B 站、小红书。
- 支持图片、视频、封面上传：
  - 图片最多 9 张，单张不超过 10MB。
  - 视频最多 3 个，单个不超过 500MB。
  - 封面 1 张，不超过 10MB。

### 2. AI 设置中心

- 顶部展示当前默认模型。
- 下方以卡片形式展示 OpenAI、Qwen、Gemini、DeepSeek、Ollama、Local。
- 每个模型支持独立配置：
  - API Key
  - Base URL
  - 模型名
  - 创作随机度
  - 最大输出长度
- 支持设为默认模型、保存配置、测试连接。
- OpenAI、Qwen、DeepSeek、Local 使用 OpenAI Compatible 调用方式。
- Gemini 使用 Gemini SDK 预留/实际测试。
- Ollama 使用本地 `/api/tags` 接口测试模型可用性。

### 3. 平台预览

- 生成后按平台展示内容卡片。
- 支持逐平台编辑标题、正文、标签、描述等字段。
- 保留上传素材信息，便于后续模拟发布。

### 4. 一键模拟发布

- 发布前校验：
  - 是否已生成平台预览。
  - 所选平台账号是否已登录。
  - 必要素材是否已上传。
- 后端调用 MockPublisher 生成模拟发布 ID。
- 保存发布记录到 SQLite。
- 发布完成后生成通知并更新侧边栏发布概览。
- 当前版本不调用真实平台发帖 API。

### 5. 发布记录

- 首次打开为空状态，提示完成模拟发布后会显示记录。
- 标准表格列：
  - 发布时间
  - 任务标题
  - 发布平台
  - 状态
  - 操作
- 支持查看详情弹窗，展示任务标题、发布平台、发布时间、状态、模拟发布 ID、帖子标题、正文、标签、素材列表。
- 支持删除本地发布记录，删除后重新请求列表接口刷新。

### 6. 账号管理

- 展示各平台授权状态、账号名称、授权方式、有效期。
- 支持模拟登录、退出登录。
- 退出登录后刷新仍保持未登录状态。
- 官方授权预留入口会弹出模拟二维码和账号密码登录表单，用于展示真实平台授权流程设计。

### 7. 通知中心与主题

- 右上角铃铛展示通知中心。
- 支持暂无通知状态、未读标记、全部已读。
- 触发通知的事件：
  - AI 生成成功
  - 模型连接成功/失败
  - 模拟发布成功
  - 发布失败
- 支持亮色模式、深色模式、跟随系统，并保存到 localStorage。

## 技术架构

```text
frontend/ Vue 3 + Vite
  ├─ App.vue              # 主界面、页面状态、主题、通知、业务交互
  ├─ api/request.js       # API 请求封装、超时和错误处理
  └─ router/index.js      # 前端路由和页面标题

backend/ FastAPI + SQLite
  ├─ main.py              # FastAPI 应用入口、路由挂载、静态资源
  ├─ database/db.py       # SQLite 表结构和数据访问
  ├─ routers/             # 内容、发布、上传、账号、设置等接口
  ├─ services/            # 内容适配、LLM 调用、上传服务
  ├─ llm/                 # OpenAI Compatible、Gemini、Ollama 等模型 Provider
  └─ adapters/            # 平台内容规则适配器
```

## 技术选型

- 前端框架：Vue 3
- 构建工具：Vite
- 后端框架：FastAPI
- 数据存储：SQLite
- 文件上传：FastAPI UploadFile + 本地 uploads 目录
- 模型调用：
  - OpenAI Compatible：后端直接 HTTP POST `/chat/completions`
  - Gemini：Google Generative AI SDK
  - Ollama：本地 HTTP API
- 测试框架：pytest + FastAPI TestClient

## 本地运行

### 1. 克隆项目

```bash
git clone https://github.com/1781988/multiplatform.git
cd multiplatform
```

### 2. 安装后端依赖

```bash
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

### 3. 启动后端

```bash
cd backend
..\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

后端地址：`http://127.0.0.1:8000`

### 4. 安装前端依赖

另开一个终端：

```bash
cd frontend
npm install
```

### 5. 启动前端

```bash
npm run dev
```

前端地址：`http://127.0.0.1:5173`

Vite 已配置代理，前端请求 `/api` 会转发到 `http://127.0.0.1:8000`。

## 大模型配置示例

以 DeepSeek 为例：

1. 打开 AI 设置中心。
2. 点击 DeepSeek 卡片的“配置”。
3. 填写：
   - API Key：DeepSeek 控制台中的真实 Key
   - Base URL：`https://api.deepseek.com`
   - 模型名：`deepseek-chat`
   - 创作随机度：`0.7`
   - 最大输出长度：`2000`
4. 点击“设为默认模型”。
5. 点击“保存配置”。
6. 点击“测试连接”。
7. 返回内容创作页，填写内容并点击“一键生成内容”。

如果模型调用失败，系统会显示后端返回的具体原因，并自动降级为本地规则模板。

## 常用 API

- `POST /api/content/generate`：生成多平台内容。
- `POST /api/publish`：执行模拟发布。
- `GET /api/records`：获取发布记录。
- `GET /api/records/{record_id}`：获取发布记录详情。
- `DELETE /api/records/{record_id}`：删除发布记录。
- `POST /api/upload/image`：上传图片。
- `POST /api/upload/video`：上传视频。
- `POST /api/upload/cover`：上传封面。
- `GET /api/materials`：获取全局素材库。
- `DELETE /api/materials/{material_id}`：删除素材。
- `POST /api/settings/llm`：保存 AI 设置。
- `POST /api/settings/llm/test`：测试模型连接。
- `GET /api/settings/llm/debug`：查看当前模型调试信息。
- `POST /api/account/mock-login`：模拟平台账号登录。
- `POST /api/account/logout`：退出平台账号。
- `GET /api/account/list`：获取平台账号状态。

## 测试

### 后端测试

```bash
cd backend
..\.venv\Scripts\python.exe -m pytest
```

### 前端构建

```bash
cd frontend
npm run build
```

当前验证结果：

- 前端构建通过。
- 后端 pytest 通过。


## 当前限制

- 当前版本执行的是模拟发布，不会真正调用公众号、知乎、B 站、小红书的发布 API。
- 真实模型调用需要用户自行提供有效 API Key 和可访问网络。
- 本地上传文件存储在后端 `uploads/` 目录，生产环境建议替换为对象存储。
