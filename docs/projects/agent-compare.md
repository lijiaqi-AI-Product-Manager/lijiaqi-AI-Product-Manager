# AgentCompare

在 DeepSeek Harness 主对话中比较同一任务的 2–4 个方案，结果可以是回答、文件或可运行的网页。面向需要比较 AI 输出、代码方案与界面交互的开发者、产品和设计人员。

当前功能描述依据 2026-11-09 的公开 README 与使用文档更新。下方工程问题保留首轮源码审阅的记录；具体平台兼容性与实际模型表现以源仓库当期验证为准。

## 功能与技术

TypeScript、React 和 DSH 宿主接口负责方案设置、并行任务、结果展示与主对话衔接。可选择不同模型与风格，进行盲选或公开比较；可运行网页提供实际预览，回答与文件提供各自的阅读、复制和保存入口。

Git 项目使用独立工作副本，从相同基线开始。生成前绑定验收脚本及相关配置，生成后封存候选。用户检查差异与组合结果后，再确认采用；采用、撤销与中断恢复有持久记录。非 Git 文件夹可以从空白隔离目录比较，将选定结果保存到新子目录。

比较、选择、采用和撤销结果进入所属主对话的记忆；后续可以继续讨论和修改选定结果。主对话上下文可以选择共享范围。

## 上手路径

DSH 桌面端通过“插件 → 添加插件”安装 dsh-agent-compare；自行管理的 Web profile 按[源仓库安装说明](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare#install)操作。

在输入框左下角点 A|B，选择方案数、模型、风格、盲选或公开比较及时间上限，发送任务。逐个阅读结果或操作网页，选择后检查文件改动；需要写回时核对目标并确认采用，也可将结果另存。

[英文安装与教程](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/blob/main/README.en.md#install)

## 迭代中解决的难题

以下记录始于 2026-11-03 的代码审阅，保留问题与处理原因，不用一次演示代替所有场景的验证。

- 起点不一致：临时 Git index 捕获包含未提交、未跟踪文件的共同基线，候选依赖和运行分别隔离。
- 修改验收来获得通过：绑定脚本、配置、测试与锁文件，再封存候选提交和补丁。
- 生成期间用户继续编辑：核对重叠改动，并在写入前检查当前工作区和候选的组合结果。
- 中断与回滚：先保存写入意图和采用前快照，恢复时保留随后发生的用户编辑。
- 并发与资源归属：验证工作副本、记录和进程归属，避免清理不属于本次任务的资源。
- Windows 与浏览器差异：处理路径、Git 管理目录、子进程及浏览器存储边界；平台约束与实际执行能力分别说明。

## 演示与范围

[![固定候选四方案的实际操作：预览、选择与保存](https://raw.githubusercontent.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/main/docs/media/comparison-preview.gif)](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/blob/main/docs/media/comparison-workflow.mp4)

演示在真实 DSH 宿主中操作固定候选，等待段经过剪辑，不代表外部模型生成质量或任务耗时。[演示条件与结果](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/blob/main/docs/demo.md)

当前支持文件夹中的回答、文件比较，以及 Git 项目根目录或子目录中的 Vite、Node 和静态网页路径。内容比较不等于任意语言的运行与功能验证。登录、共享后端和外部数据库仍需独立验证；程序检查覆盖已定义行为，审美判断由使用者完成。宿主约束有平台边界，不将其描述为完整的恶意代码沙箱。

依据：[README](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/blob/main/README.md)、[项目与文件夹范围](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/blob/main/docs/workspaces-and-projects.md)、[对话上下文](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/blob/main/docs/conversation-memory.md)、[采用与恢复](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/blob/main/docs/runs-and-recovery.md)。

[仓库与安装](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare) · [全部项目档案](../project-atlas.md)
