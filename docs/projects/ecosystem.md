# 上游 Fork 阅读记录

这三个公开仓库是上游 Fork。这里记录读到的功能、技术与适用场景，用于保留技术理解与参考来源，不把上游作者的开发、修复或社区成绩记为个人原创贡献。审阅于 2026-11-03。

<a id="lobe-chat"></a>

## Lobe Chat

[个人 Fork](https://github.com/lijiaqi-AI-Product-Manager/lobe-chat) · [上游 LobeHub](https://github.com/lobehub/lobehub)

**问题与人群：** 为个人和团队组织多模型对话、知识文件、工具与 Agent 工作空间，适合需要自托管、模型选择与可扩展交互的使用者和开发者。

**功能与技术：** 阅读的分支使用 Next.js、React、TypeScript、Zustand、Ant Design / LobeHub UI，数据库涉及 PostgreSQL、Drizzle 与本地存储。功能包括分支对话、文件与知识库、Artifacts、联网搜索、多模态、语音、MCP 市场、助手和插件生态、桌面端及主题。

**使用路径：** 根据对应分支的部署文档选择服务端数据库、本地模式或容器部署，配置模型提供方；源码开发按该分支依赖与 `pnpm run dev` 入口进行。上游持续变化，个人 Fork 的 README 不代替最新部署文档。

**工程理解：** 模型运行时、数据库、会话流、工具与 UI 拆成模块；桌面桥接、认证、文件加载和模型配置都有独立层。功能很多时，统一入口与可扩展模块边界同样重要。此次未核实个人新增提交，不将上游缺陷修复归为个人经历。

依据：Fork 的中文 README、根依赖清单、工作空间目录、开发约定与提交历史。其许可为 LobeHub 社区许可，应按仓库实际条款使用，不能假定为 MIT。

<a id="coai"></a>

## CoAI

[个人 Fork](https://github.com/lijiaqi-AI-Product-Manager/coai) · [上游 CoAI](https://github.com/coaidev/coai)

**问题与人群：** 将用户聊天界面与站点模型渠道、配额和运营管理连接起来，面向自托管 AI 服务运营者，以及需要统一模型接口的开发者。

**功能与技术：** Go 后端、React / TypeScript / Vite 前端，使用 MySQL 与 Redis；界面包含 Radix、Shadcn 风格组件与 Tremor 图表。支持多提供方格式、渠道优先级和权重、重试、模型重定向、对话分享与同步、预设、文件解析、搜索、订阅和点数、用户与后台管理，提供兼容 API。

**使用路径：** 按上游 Docker Compose 或源码指引配置数据库、Redis、认证与模型渠道，进入管理端配置模型和定价，再测试对话和账务。实际服务依赖与敏感默认项应在部署时独立核对，不直接复制 README 中的示例凭据。

**工程理解：** 渠道路由、WebSocket、缓存、配额、订阅和用户体验共同决定服务质量。文件能力由 Blob Service 协作提供；README 中商业版扩展与社区代码分别阅读，不能把商业版宣传自动算作本 Fork 的实现。

依据：中文 README、`go.mod`、前端依赖、`main.go` 与提交历史。许可为 Apache-2.0。

<a id="blob-service"></a>

## Blob Service

[个人 Fork](https://github.com/lijiaqi-AI-Product-Manager/blob-service) · [上游 Blob Service](https://github.com/coaidev/blob-service)

**问题与人群：** 把不同格式的附件转换成模型可消费的内容，面向 AI 聊天平台和需要文件处理接口的开发者。

**功能与技术：** Python、FastAPI、各格式处理器与 MarkItDown；支持文本、PDF、Docx、Pptx、Excel、图像与音频路径。OCR 依赖配置的识别服务，语音转写依赖 Azure Speech；可选本地、S3 兼容存储、R2 与 MinIO 等路径。

**使用路径：** 源码安装 `requirements.txt` 后运行 `uvicorn main:app`，向 `POST /upload` 发送 multipart 文件及 OCR、vision、save-all 等表单字段，读取状态、类型、内容与错误。服务也有容器部署路径。不同外部存储与处理服务需分别配置，格式名不等于任意文件都能成功解析。

**工程理解：** 入口、处理器、存储和配置分层；MarkItDown 可以作为主处理器，出错回退内置处理。文件大小、文件格式、存储能力和 OCR / vision 条件共同限制结果。当前入口返回业务状态，接入方不能只依据 HTTP 请求成功判断解析成功。

依据：README、`main.py`、`config.py`、`requirements.txt`、处理器目录与提交历史。许可为 Apache-2.0。

[返回项目档案](../project-atlas.md) · [个人主页](../../README.md)
