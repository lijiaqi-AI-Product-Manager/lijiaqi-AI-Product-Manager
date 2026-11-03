# skill-healthcheck

**找出悄悄失效的 Agent 技能，以及行为从什么时候开始变化。** 面向安装了多个 Skill 的 Claude Code、Codex 与 DeepSeek Harness 使用者，帮助区分模型问题、加载问题和上游提示词变化。

## 功能与技术

TypeScript CLI，使用 YAML、Git、确定性规则和本地会话证据。检查宿主实际上会发现、加载、截断或忽略哪些技能；比较上游的名称、description、正文与脚本变化；结合会话中的技能目录、调用记录和语言变化，排出可疑项。

工具不自动更新技能。默认规则检查不调用大模型；可选解释只发送相关技能变化文本，不发送会话原文或用户抱怨。自己的历史与派生记录写进独立工具目录，源技能和用户仓库保持只读。

## 上手路径

```bash
npx skill-healthcheck
npx skill-healthcheck ls
npx skill-healthcheck why "为什么不再用中文回答"
```

用 `--offline` 做离线体检，`--no-sessions` 跳过会话分析，`--json` 接入脚本。如果技能来自复制而非 Git checkout，可用 `adopt --repo <来源仓库>` 登记来源。DSH 配套插件在启动和技能目录变化时记录快照，并提供聊天命令入口。

## 迭代中解决的难题

- **宿主规则不同：** Claude Code 的回退描述、目录优先级和不完整 frontmatter，不能套用 DSH 规则；Codex 的递归深度、description 要求与同名行为也单独处理。避免把实际上能加载的技能误报为失效。
- **读取失败不等于被删除：** 认证失败、缓存只读、远程 blob 读取失败或移动后新路径不可读，报告不可达；明确删除才判作删除。
- **时间先后不能倒置：** 技能早就停用、后来才改 description，不能说是这次编辑导致；归因结合变更时间、最后调用与安静会话的位置，只提供嫌疑顺序。
- **来源登记与换行：** 一个上游路径只匹配一个本地技能；接受原始与规范化换行哈希，避免 CRLF 产生永久假变化；Windows 跨盘路径无法确定时保留未知。
- **隐私与可执行输入：** `--offline` 覆盖所有命令；上游地址和 Git 错误脱敏，拒绝参数注入；可选解释严格限制载荷；会话解压有上限。

## 范围

`why` 是可解释的排查顺序，不证明因果；“技能文件加载正常”也不保证模型每次都会调用。未知来源不会被编造为已核验上游。宿主规则随实际软件变化，使用时以项目维护说明和对应证据为准。

依据：[README](https://github.com/lijiaqi-AI-Product-Manager/skill-healthcheck/blob/main/README.zh.md)、[宿主规则](https://github.com/lijiaqi-AI-Product-Manager/skill-healthcheck/blob/main/src/platforms.ts)、[归因实现](https://github.com/lijiaqi-AI-Product-Manager/skill-healthcheck/blob/main/src/why.ts)、[错误结论回归](https://github.com/lijiaqi-AI-Product-Manager/skill-healthcheck/blob/main/test/review-1.1.test.ts)及更新日志。审阅于 2026-11-03。

[仓库与安装](https://github.com/lijiaqi-AI-Product-Manager/skill-healthcheck) · [全部项目](../project-atlas.md)
