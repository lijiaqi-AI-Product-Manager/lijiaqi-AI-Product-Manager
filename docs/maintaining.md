# 主页与项目档案维护

这是李佳奇的 GitHub 个人主页仓库，包含中英双语主页、独立英文介绍、原创 SVG 视觉、公开项目知识库与履历摘要。主页用代表作品建立第一印象，详细能力、教程、工程经历与范围保存在独立档案。

## 内容组织

- `README.md`：中英并列主页，六个代表作品、产品实践、能力与经历。
- `README.en.md`：英文入口，信息与中文主页一致。
- `docs/project-atlas.md`：全部公开仓库的持久索引。
- `docs/project-atlas.en.md`：英文项目全景、上手方法、工程经验和范围说明。
- `docs/projects/`：逐项目功能、技术、使用方法与关键工程问题。
- `docs/experience.md`：从本人简历整理的公开履历摘要。
- `docs/experience.en.md`：对应的英文履历摘要。
- `docs/review-sources.json`：本轮审阅的仓库基准与来源路径。
- `AGENTS.md`：后续维护者的事实与写作约定。
- `scripts/build_assets.py`：原创封面、产品示意卡片与流程图的生成源。

项目档案是可以再次读取和更新的长期参考。它不意味着外部记忆服务已自动接入，也不会自动追踪其他仓库的新提交。

## 视觉与兼容

使用暖白 / 墨绿、薄荷与铜色的统一视觉，封面建立人物识别，产品卡片以各自流程表达用途。示意图为原创绘制，不冒充应用截图。AgentCompare 与 BugGPS 动图直接引用各自公开仓库的实际演示，并注明演示条件。

主页的正文、导航、项目说明、经历与图示同时提供中文和英文。独立英文页与英文指南形成完整阅读路径；保留源招聘文本及实际演示界面的原语言，不把介绍的翻译写成产品已提供对应语言功能。

深浅主题通过 GitHub 支持的 `picture` 与 `prefers-color-scheme` 选择；正文使用原生 Markdown 和简单 HTML，提供可复制文字、真实链接和折叠区域。GitHub README 不执行任意 JavaScript 或自定义网页插件，因此视觉在原生支持范围内实现。

设计研究参考 [Awesome GitHub Profile README](https://github.com/abhisheknaiidu/awesome-github-profile-readme)、[Caneco](https://github.com/caneco/caneco)、[DenverCoder1](https://github.com/DenverCoder1/DenverCoder1) 与 [Sindre Sorhus](https://github.com/sindresorhus/sindresorhus)，提取人物识别、作品导航、统一卡片和简洁产品入口的组织方式。没有复制它们的代码、插画或个人陈述。

## 增长图表

各公开仓库的 Star 曲线与已发布包的每日下载请求由 `scripts/update_growth.py` 统一生成，范围在 `data/growth-config.json` 中登记。`Project growth charts` 工作流每天更新 `assets/growth/` 与公开聚合数据；图片支持深浅主题和手机布局。新包数据缺失不写成零，请求失败保留上次成功结果并标明状态。统计口径见 [增长图表说明](growth.md)。

## 更新与检查

```bash
python scripts/build_assets.py
python scripts/check_profile.py
```

CI 检查本地链接、图片替代文本、SVG 结构与版本号展示，并确认素材可从源码确定性重建。视觉检查另在实际浏览器完成；结构检查不能替代视觉判断。

更新项目时先核实对应代码、范围说明、测试和提交，再更新档案与主页。动态数据注明快照日期和统计单位；履历只保留可以表达清楚的经历。不要把原始简历或私人联系方式作为主页附件上传。

[返回主页](../README.md) · [项目知识库](project-atlas.md)
