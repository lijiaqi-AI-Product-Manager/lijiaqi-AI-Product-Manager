# BugGPS

**录下问题，按原预期复核修复。** 面向前端开发者、测试人员和遇到交互问题的使用者，将浏览器里的实际操作转成可重复检查的记录，再交给 DeepSeek Harness 中的 Agent 修复。

## 功能与技术

使用 JavaScript、Playwright、Git 快照与 DSH 工具接口。录制点击、输入、选择等操作时标出“正确应该是什么”，可额外保存检查点和不可删除的关键步骤。锁定阶段由 BugGPS 启动应用，连续重放得到同一种失败；修复后从当前代码启动应用，完整重放并持续观察所有检查。

用例有内容哈希和写保护。失败分成原故障仍在、出现不同故障、环境阻塞、偶发不一致、用例被改、代码未变等状态。只有证据足够时才给出 `VERIFIED`。

## 上手路径

按仓库说明把本地 checkout 安装到 DSH profile。先用内置示例熟悉流程：

```bash
node bin/buggps.js demo ../buggps-demo
node bin/buggps.js doctor --repo ../buggps-demo
```

在 DSH 中依次使用录制、锁定和验证工具。录制时手动标出预期；项目通过 `buggps.config.json` 提供独立本地启动命令与地址。Agent 修改正常业务代码，BugGPS 按锁定条件重放复核。

## 迭代中解决的难题

- **连错服务器也“通过”：** 只有由工具从当前工作区启动的应用，才有资格给出绑定代码的验证结论；占用端口直接报告环境阻塞。
- **删除功能来消除错误：** 只有负向检查、禁用触发按钮、模糊定位等情况进入人工复核，而不是自动判定修好。
- **把错误延后出现：** 最后一步后继续观察检查，覆盖延迟错误；验证以完整录制为准，不仅看被缩短的路径。
- **绕过原始情境：** 检查点参与复核，修复后的操作仍须到达录制时的条件。
- **用例与锁一起被改：** 内容核验配合同会话锁定记录识别篡改；路径规范化处理大小写、父路径与 junction。
- **冷启动与秘密输入：** 预热按需编译页面后再计数；密码等字段只保存引用，重放从环境变量读取，不落入录制内容。

## 演示与范围

![BugGPS 实际示例：录制、锁定、错误修复被驳回、正确修复通过](https://raw.githubusercontent.com/lijiaqi-AI-Product-Manager/dsh-bug-gps/main/docs/media/buggps-demo.gif)

演示使用植入故障的内置示例，光标与字幕后期叠加。`VERIFIED` 只覆盖录制场景。当前实测以 Chromium 系浏览器、React / Vite、可重置前端状态和 DOM 断言为主；不将拖拽、任意全局键盘操作或会修改服务端数据的流程写成已支持。

依据：[README](https://github.com/lijiaqi-AI-Product-Manager/dsh-bug-gps/blob/main/README.md)、[复现分类实现](https://github.com/lijiaqi-AI-Product-Manager/dsh-bug-gps/blob/main/src/core/reproduce.js)、[反例回归](https://github.com/lijiaqi-AI-Product-Manager/dsh-bug-gps/blob/main/test/counterexamples.test.js)、[实际案例记录](https://github.com/lijiaqi-AI-Product-Manager/dsh-bug-gps/blob/main/bench/spike-s2-s3.md)与提交历史。审阅于 2026-11-03。

[仓库与安装](https://github.com/lijiaqi-AI-Product-Manager/dsh-bug-gps) · [全部项目](../project-atlas.md)
