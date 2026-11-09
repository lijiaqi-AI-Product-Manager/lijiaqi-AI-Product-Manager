# 李佳奇的项目档案

**中文** · [English](project-atlas.en.md) · [中英双语主页](../README.md)

这里记录每个公开项目解决的问题、使用人群、技术与功能、上手路径，以及迭代中真正处理过的难题。它既是作品集的阅读入口，也是后续更新介绍时可继续维护的项目知识库。

基准审阅日期：**2026-11-03**，覆盖当时的 **12 个公开仓库**：8 个产品项目、3 个上游 Fork 和本个人主页。这是有日期的档案范围，不是账号当前全部仓库清单。2026-11-09 根据当期公开文档更新了 AgentCompare 简介。依据包括 README、依赖清单、代表性实现、回归用例、产品范围说明及提交历史；AirStudy 另核对了本地工程。历史报告中的计划与测试数字不直接作为当前完成证明。

## 产品项目

| 项目 | 解决的问题 | 主要技术 | 适用人群 | 详细档案 |
| :--- | :--- | :--- | :--- | :--- |
| **job_radar** | 招聘入口分散，条件、时效和原文难以统一核对 | Python、SQLite、CLI、MCP、GitHub Actions | 中国校招、实习、社招求职者；招聘数据分析者；Agent 使用者 | [功能、教程、数据口径与迭代](projects/job-radar.md) |
| **QGauss AI** | 多模型与多种创作工具分散，个人工作流和站点运营相互割裂 | TypeScript、Vue、NestJS、Prisma、SQLite | 个人创作者、小型 AI 站点运营者 | [功能、部署与任务恢复](projects/qgauss.md) |
| **AgentCompare** | 同一任务的 AI 回答、文件与网页难以比较和采用 | TypeScript、React、Git worktree、DSH、浏览器验收 | 开发者、产品与设计人员、AI Coding 使用者 | [A/B 体验、共同验收与采用](projects/agent-compare.md) |
| **BugGPS** | 口头描述难复现，Agent 宣称修复后缺少同场景证据 | JavaScript、Playwright、Git、DSH | 前端开发者、测试人员、提交交互问题的人 | [录制、锁定与重放验证](projects/bug-gps.md) |
| **skill-healthcheck** | 技能文件仍在，但触发条件或加载行为已经改变 | TypeScript、Git、YAML、宿主规则与会话证据 | Claude Code、Codex、DeepSeek Harness 使用者 | [只读体检与时间线排查](projects/skill-healthcheck.md) |
| **unremember** | 删掉一条聊天后，本地摘要、记忆及其他副本仍保留目标内容 | TypeScript、JSONL、Zstandard、SHA-256 | Claude Code、DeepSeek Harness 使用者 | [定向遗忘、验证与回滚](projects/unremember.md) |
| **湘村小灶** | 门店点单、后厨、储值和财务口径难以贯通 | TypeScript、React、Hono、SQLite、SSE | 独立餐厅、门店经营与运营人员 | [点单闭环、账本与打印](projects/xiangcun.md) |
| **AirStudy** | 专注计时缺少可感知的过程与连续体验 | Kotlin、View/XML、Room、Hilt、DataStore、Ktor | 以飞行体验组织专注时间的 Android 用户 | [产品概览、本地工程与公开范围](projects/airstudy.md) |

## 上游 Fork 与主页

| 仓库 | 性质与阅读范围 |
| :--- | :--- |
| [lobe-chat](https://github.com/lijiaqi-AI-Product-Manager/lobe-chat) | LobeHub 上游 Fork；多模型工作台、知识库、工具生态、前端与数据库架构。[阅读记录](projects/ecosystem.md#lobe-chat) |
| [coai](https://github.com/lijiaqi-AI-Product-Manager/coai) | CoAI 上游 Fork；Go 后端、React 前端、渠道路由、订阅与点数计费。[阅读记录](projects/ecosystem.md#coai) |
| [blob-service](https://github.com/lijiaqi-AI-Product-Manager/blob-service) | CoAI Blob Service 上游 Fork；文件解析、OCR、语音转写与存储适配。[阅读记录](projects/ecosystem.md#blob-service) |
| [lijiaqi-AI-Product-Manager](https://github.com/lijiaqi-AI-Product-Manager/lijiaqi-AI-Product-Manager) | 本主页：中文 / 英文入口、代表作品、履历与有日期的项目档案。[维护说明](maintaining.md) |

Fork 的功能与历史提交属于上游项目，不作为个人原创开发或个人解决过的难题。MUNity、旅行智能体原型与多 Agent 投研工作流在本次范围内依据本人简历描述，见[经历与能力](experience.md)，不冒充已公开审阅的代码。

## 贯穿这些项目的工程经验

**错误结论比报错更难发现。** 技能读取失败不能判成“已删除”，招聘抓取失败不能判成“已下架”，只检查“不报错”也不能证明功能已经修好。这些项目逐步把“明确成立”“仍未知”“需要复核”变成不同结果。

**验证必须绑定原来的条件。** BugGPS 保留原始预期与完整操作；AgentCompare 绑定基线、验收文件和实际构建产物；unremember 在分叉里追问。让修改后的系统自己解释“我已经好了”，不足以替代独立证据。

**中断、重试和并发是日常路径。** 门店的重复提交、创作任务的扣费恢复、Agent 候选的采用中断、Android 的后台恢复，都要求状态机、事务或持久记录共同工作，而不是只照顾顺利完成的一次演示。

**接口之外还有真实使用成本。** Windows 路径、Git 换行、打印纸宽与编码、跨夜营业、图片流量、手机进程生命周期，往往决定产品能否被持续使用。项目档案保留这些问题的原因与处理方式。

[返回个人主页](../README.md) · [履历与能力](experience.md) · [档案维护与来源](maintaining.md)
