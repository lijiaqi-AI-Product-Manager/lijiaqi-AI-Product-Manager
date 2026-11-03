# unremember

**给本地编码 Agent 做可回滚、可验证的定向遗忘。** 面向 Claude Code 与 DeepSeek Harness 使用者，处理目标内容在会话、摘要、记忆和缓存中被重复保存的问题，保留其余上下文。

## 功能与技术

TypeScript 与 Node 内置能力实现本地文件适配，处理 JSONL、Zstandard、多代会话、记忆索引、工具结果和相关副本。流程是：**计划 → 检查 → 备份 → 执行 → 分叉验证 → 必要时回滚**。

计划先在内存中模拟删除或局部清理并检查残留；执行核验 SHA-256、允许的路径和会话状态，再备份、原子写入。Claude Code 需要维护父消息和工具调用对应关系；DSH 保留行与序号，只清理目标字段并按宿主帧结构重新编码。

## 上手路径

```bash
npm install -g unremember
unremember sessions
unremember plan last --text "要清理的内容"
```

检查生成的计划后，使用 `apply <plan-id> --yes` 执行，再用 `verify <session> --canary <目标内容>` 在分叉上追问；需要恢复时用 `rollback <plan-id>`。执行前应结束目标会话，因为磁盘修改不会替换运行中 Agent 已加载的上下文。

默认字面匹配留在本地。可选语义匹配需要显式配置模型接口，相关片段会发送到该接口；备份与待执行请求可使用 AES-256-GCM 加密保存。

## 迭代中解决的难题

- **聊天之外还有副本：** 将 compact 摘要、history、memory、file-history、API 请求与 DSH inbox 等作为正式存储适配，而非仅删除 UI 上一行。
- **结构不能损坏：** 清理 Claude 父指针、工具对，保留 DSH 序号；多帧压缩不能只读第一帧，未知或损坏格式阻止执行。
- **验证产生假阴性：** 空回答、模型沉默、全未知结果都不作为成功；分叉验证防止问题污染原会话，清理分叉前验证会话标识。
- **计划本身泄露秘密：** 去除计划中的会话预览，保留哈希与操作；默认掩码展示会话，文件权限限制为所有者。
- **路径、并发与恢复：** 执行时重新检查路径属于当前适配器的存储集合，拒绝符号链接；计划锁防止重复执行，预检发现文件变化则停止，自动恢复失败明确报告。
- **运行状态与大文件：** 无法确认会话是否停止时拒绝写入，大会话使用可配置上限，避免意外消耗巨大内存。

## 范围

工具处理本机已支持的 Agent 文件，不删除云服务留存、其他设备副本或模型权重，不重写项目代码与 Git 历史。分叉追问是特定探测条件下的泄露检查，不能证明所有语义记忆均已消失。目前不包含 Codex 文件适配器。

依据：[README](https://github.com/lijiaqi-AI-Product-Manager/unremember/blob/main/README.md)、[执行核心](https://github.com/lijiaqi-AI-Product-Manager/unremember/blob/main/src/apply-core.ts)、[验证实现](https://github.com/lijiaqi-AI-Product-Manager/unremember/blob/main/src/verify.ts)、[回归用例](https://github.com/lijiaqi-AI-Product-Manager/unremember/blob/main/test/security-regressions.test.ts)及更新日志。审阅于 2026-11-03。

[仓库与安装](https://github.com/lijiaqi-AI-Product-Manager/unremember) · [全部项目](../project-atlas.md)
