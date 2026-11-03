<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/hero-mobile-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/hero-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <img src="assets/hero-light.svg" width="1280" alt="李佳奇 Li Jiaqi / Gauss — AI 产品经理，厦门大学 2029 届。把真实问题，做成好用的产品。">
</picture>

<p align="center">
  <a href="#projects">代表作品</a> &nbsp; / &nbsp;
  <a href="#practice">产品实践</a> &nbsp; / &nbsp;
  <a href="docs/project-atlas.md">项目全景与使用指南</a> &nbsp; / &nbsp;
  <a href="docs/experience.md">经历与能力</a> &nbsp; / &nbsp;
  <a href="README.en.md">English</a>
</p>

# 你好，我是李佳奇。

**AI 产品经理 · 开源作者 · Product builder**

我把用户研究、产品设计、AI Coding 和验证串成一条工作流。关注 Agent 的可控性，也把 AI 带进创作、求职和门店经营：理解真实需求，做出能用的工具，再用证据持续改进。

厦门大学广告学本科，**2029 届**。曾在 **阿里巴巴 · 飞猪** 从事 C 端 AI 产品工作，主导 **QGauss AI** 与 **湘村小灶数字化**，发起 **MUNity**。

[联系我](mailto:lijiaqi.mun@gmail.com) · [LinkedIn](https://www.linkedin.com/in/jiaqi-li-ai-product-manager/) · [全部公开仓库](https://github.com/lijiaqi-AI-Product-Manager?tab=repositories)

<br>

<a id="projects"></a>

## 代表作品

从可追溯的数据、可体验的创作工具，到可检验的 Agent 工作流。每个项目都从一个具体问题出发。

<table>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/lijiaqi-AI-Product-Manager/job_radar">
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/job-radar-dark.svg"><img src="assets/job-radar-light.svg" width="624" alt="job_radar 产品示意：招聘岗位、JD、来源与日历在本地统一查询"></picture>
</a>
<p>中国校招、实习、社招与招聘日历。用 <strong>Python + SQLite</strong> 整理公开来源，CLI、MCP 与 Skill 共用查询规则，保留原文、出处和未知条件。</p>
<p><a href="https://github.com/lijiaqi-AI-Product-Manager/job_radar">代码与安装 ↗</a> · <a href="docs/projects/job-radar.md">功能、用法与工程故事</a></p>
</td>
<td width="50%" valign="top">
<a href="https://github.com/lijiaqi-AI-Product-Manager/QGauss-AI">
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/qgauss-dark.svg"><img src="assets/qgauss-light.svg" width="624" alt="QGauss AI 产品示意：对话、绘画、视频与声音的统一工作空间"></picture>
</a>
<p>面向个人创作与小型站点运营的自托管平台。<strong>Vue + NestJS + Prisma</strong> 连接多模型对话、图像编辑、视频、声音、思维导图与运营后台。</p>
<p><a href="https://github.com/lijiaqi-AI-Product-Manager/QGauss-AI">代码与部署 ↗</a> · <a href="docs/projects/qgauss.md">功能、用法与工程故事</a></p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare">
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/agent-compare-dark.svg"><img src="assets/agent-compare-light.svg" width="624" alt="AgentCompare 产品示意：从同一基线生成两版前端，真实运行后盲选"></picture>
</a>
<p>把前端方案比较带进 DeepSeek Harness。<strong>独立 Git worktree、共同验收、真实预览、先选后揭晓</strong>，采用前审查改动，保留恢复与撤销记录。</p>
<p><a href="https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare">代码与使用 ↗</a> · <a href="docs/projects/agent-compare.md">功能、用法与工程故事</a></p>
</td>
<td width="50%" valign="top">
<a href="https://github.com/lijiaqi-AI-Product-Manager/dsh-bug-gps">
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/bug-gps-dark.svg"><img src="assets/bug-gps-light.svg" width="624" alt="BugGPS 产品示意：录制问题、锁定失败、按原预期重放验证"></picture>
</a>
<p>把“我操作时出了问题”变成可重复检查。<strong>JavaScript + Playwright</strong> 录下操作和预期，锁定稳定失败，再用当前代码启动应用、重放复核。</p>
<p><a href="https://github.com/lijiaqi-AI-Product-Manager/dsh-bug-gps">代码与使用 ↗</a> · <a href="docs/projects/bug-gps.md">功能、用法与工程故事</a></p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/lijiaqi-AI-Product-Manager/skill-healthcheck">
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/skill-healthcheck-dark.svg"><img src="assets/skill-healthcheck-light.svg" width="624" alt="skill-healthcheck 产品示意：结合加载规则、上游改动和使用时间线检查技能"></picture>
</a>
<p>找出“文件还在，模型却不再调用”的技能。结合<strong>宿主加载规则、上游 Git 变化和会话时间线</strong>，为 Claude Code、Codex 与 DSH 提供体检与排查线索。</p>
<p><a href="https://github.com/lijiaqi-AI-Product-Manager/skill-healthcheck">代码与安装 ↗</a> · <a href="docs/projects/skill-healthcheck.md">功能、用法与工程故事</a></p>
</td>
<td width="50%" valign="top">
<a href="https://github.com/lijiaqi-AI-Product-Manager/unremember">
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/unremember-dark.svg"><img src="assets/unremember-light.svg" width="624" alt="unremember 产品示意：计划、备份、定向清理、分叉验证与回滚"></picture>
</a>
<p>给本地编码 Agent 做定向遗忘。清理会话及相关副本，先计划、再备份与执行，使用<strong>哈希核验、原子写入、隔离追问与回滚</strong>保护其余上下文。</p>
<p><a href="https://github.com/lijiaqi-AI-Product-Manager/unremember">代码与安装 ↗</a> · <a href="docs/projects/unremember.md">功能、用法与工程故事</a></p>
</td>
</tr>
</table>

<details>
<summary><strong>看一次真实运行：AgentCompare 从两版预览到审查采用</strong></summary>

<br>

[![AgentCompare 固定候选演示：真实运行两版应用，共同验收、选择并审查采用](https://raw.githubusercontent.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/main/docs/media/comparison-preview.gif)](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/blob/main/docs/media/comparison-workflow.mp4)

固定候选示例，应用运行、共同验收与采用实际执行；等待段已剪辑。[演示条件与结果](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/blob/main/docs/demo.md)。

</details>

<br>

<a id="practice"></a>

## 从用户问题到产品交付

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/process-mobile-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/process-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/process-dark.svg">
  <img src="assets/process-light.svg" width="1280" alt="我的工作方式：看见问题，定义行为，实现产品，用证据迭代">
</picture>

**飞猪 · 让 AI 旅行助手的体验可比较。** 在实习中构建 22 道统一题库，对 6 家 OTA 平台开展约 330 轮对话评测；把多轮约束、长辈交互和订单感知等发现，转成家庭出行智能体的 PRD、状态机、失败降级与可交互原型。[经历与方法 →](docs/experience.md)

**湘村小灶 · 把产品做到门店的日常里。** 从扫码点单、后厨实时收单，做到会员储值账本、退款对账、跨夜日结与小票打印。React、Hono、SQLite 与店铺配置共同支撑顾客端和老板端；加菜、重试和跨日统计都有明确规则。[项目与使用路径 →](docs/projects/xiangcun.md)

**AirStudy · 把专注时间变成一段飞行。** Android 专注体验，围绕机场、路线、计时会话、登机牌与飞行记录组织交互。使用 Kotlin、View/XML、Room、Hilt 与 Ktor，重点处理后台生命周期、状态恢复和账号边界。[项目概览与公开范围 →](docs/projects/airstudy.md)

<br>

## 我带来的能力

| 方向 | 工作方式与工具 |
| :--- | :--- |
| **产品研究与定义** | 竞品实测、用户问题拆解、PRD、状态机、验收标准、SOP、Roadmap、Figma / Axure |
| **AI 应用与工作流** | 多模型 API、Agent 设计、提示词与上下文工程、Coze / GLM 工作流、MCP / Skill 集成 |
| **实现与交付** | TypeScript / JavaScript、Python、React / Vue、NestJS / Hono、SQLite / Prisma、GitHub Actions |
| **验证与迭代** | 浏览器重放、共同验收、数据来源追溯、回归用例、事务与幂等、失败恢复、实际业务复盘 |

## 经历与视野

| 经历 | 方向 | 时间 |
| :--- | :--- | :--- |
| **阿里巴巴 · 飞猪** | C 端 AI 产品经理实习 | 2026.07 – 2026.09 |
| **湘村小灶** | 数字化转型项目经理 / 产品与运营负责人 | 2026.04 起 |
| **QGauss AI** | 创始人 / 负责人，早期多模型平台孵化 | 2025.12 – 2026.07 |
| **MUNity** | 创始人 / 首席产品研发负责人，模联 AI Agent 与社群平台 | 2026.09 起 |
| **联想 · 百应** | B 端 AI 产品经理实习，**已录取、待实习** | 计划 2027.01 – 2027.02 |

**研究与组织之外，也持续面向真实的人。** 参与北京大学全国模联大会、中国日报社全国模联大会学术与主席团工作，担任 20 余场模联活动主席团负责人或主席；创办石家庄市模联协会并任首任秘书长。

北京大学国际关系学院暑期课堂优秀营员 · IMMC 国际数学建模挑战赛中华赛区全国二等奖。英语雅思口语 **7.0**，法语 **DELF B1**；俄语、日语、印尼语、马来语基础沟通。

<details>
<summary><strong>生态阅读与技术参考</strong></summary>

我也保留了 [Lobe Chat](https://github.com/lijiaqi-AI-Product-Manager/lobe-chat)、[CoAI](https://github.com/lijiaqi-AI-Product-Manager/coai) 和 [Blob Service](https://github.com/lijiaqi-AI-Product-Manager/blob-service) 的上游 Fork，阅读多模型工作台、渠道与计费、文件解析的产品和工程设计。它们的原创工作归上游作者；[逐仓库阅读记录](docs/projects/ecosystem.md) 单独保留来源。

</details>

<br>

<a href="mailto:lijiaqi.mun@gmail.com">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/footer-dark.svg">
  <img src="assets/footer-light.svg" width="1280" alt="欢迎交流 AI 产品、开源工具与真实业务。联系邮箱：lijiaqi.mun@gmail.com">
</picture>
</a>

<p align="center"><a href="mailto:lijiaqi.mun@gmail.com">lijiaqi.mun@gmail.com</a> &nbsp; · &nbsp; <a href="https://www.linkedin.com/in/jiaqi-li-ai-product-manager/">LinkedIn</a> &nbsp; · &nbsp; <a href="docs/project-atlas.md">全部项目档案</a></p>
