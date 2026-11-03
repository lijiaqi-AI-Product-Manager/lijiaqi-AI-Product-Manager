# AgentCompare

**同一需求，两版真跑，盲选再揭晓。** 这是 DeepSeek Harness 插件，面向需要比较界面与交互方案的前端开发者、产品与设计人员，以及 AI Coding 使用者。

## 功能与技术

使用 TypeScript、React、Git worktree 与 DSH 宿主接口，把同一基线复制成两份候选，支持“同一模型、两种策略”与“两个模型、同一要求”。候选分别生成、安装依赖、构建并真实运行，在同一窗口交互体验；选定后揭晓模型、策略与 token 用量。

共同验收在生成前确定并绑定内容，结合项目脚本、页面加载、交互步骤与桌面 / 手机截图。采用前展示差异和目标仓库，验证组合结果后写回，保留采用、恢复和撤销记录。历史比较可跨对话搜索，预览停止后仍可看验收截图。

## 上手路径

克隆源码，运行 `npm ci` 与 `npm pack`，按仓库安装说明将打出的本地包添加到自己的 DSH profile。桌面版使用应用的插件入口。

在输入框点 **A|B**，选择比较方式与生成上限，写下前端需求。两版运行后先体验再选；展开差异，点“审查并采用”，核对目标与验收结果后写回。内置示例在独立仓库运行，适合先熟悉全流程。

## 迭代中解决的难题

- **起点不一致：** 私有临时 index 捕获包括未提交、未跟踪文件的同一基线，不改用户原 index；依赖与候选各用独立副本。
- **改测试来获得通过：** 绑定脚本、配置、测试与锁文件，生成后封存提交和补丁；改验收内容的候选不能直接采用。
- **候选期间用户继续编辑：** 重叠改动直接阻止；其他改动先与候选组合预演。每次写入前再次核对工作区、HEAD 和暂存区。
- **中断与回滚：** 先持久保存写入意图和采用前快照；恢复只处理本次尝试写过的路径，保护随后发生的用户编辑。
- **并发与资源归属：** 预先占用启动名额，验证 worktree 双向链接与归属标记；仅结束可证明属于插件的进程。旧记录与损坏历史保留可读状态。
- **Windows 与浏览器环境：** 处理路径大小写、Git 管理目录和受限命令行为；预览使用独立随机 localhost 主机名，减少两个候选共享浏览器存储。

## 演示与范围

[![固定候选演示：真实运行、共同验收、选择与采用](https://raw.githubusercontent.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/main/docs/media/comparison-preview.gif)](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/blob/main/docs/media/comparison-workflow.mp4)

演示使用固定候选，运行与采用实际执行，等待段已剪辑。首期支持本地 Git 仓库根目录的 Vite 前端；登录、共享后端与外部数据库等工作流不在当前验收范围。程序检查覆盖已定义行为，自由文本需求的审美与体验仍由人判断。宿主提供的 Windows 约束有明确边界，不能称为完整恶意代码沙箱。

依据：[README](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/blob/main/README.md)、[采用实现](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/blob/main/src/core/adopt.ts)、[恢复说明](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare/blob/main/docs/runs-and-recovery.md)、回归用例与提交记录。审阅于 2026-11-03。

[仓库与安装](https://github.com/lijiaqi-AI-Product-Manager/dsh-agent-compare) · [全部项目](../project-atlas.md)
