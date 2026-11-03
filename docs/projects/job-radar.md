# job_radar

**把中国招聘信息整理成能在本地查询、核对和分析的数据。** 面向校招、实习、社招求职者，也面向需要接入招聘信息的脚本、研究工作流和 AI 助手。

## 功能与技术

使用 Python 适配公开招聘平台，归一化岗位、公司、城市、招聘类型、届次与原始链接。SQLite 分开保存结构化岗位、JD 正文和招聘日历；GitHub Actions 采集，Release 分发兼容快照。CLI、MCP 与 Skill 接入共用查询层，查询无需 API key 或自建服务。

支持公司、城市并集与排除项、标题和正文检索、招聘类型与届次筛选、岗位展示分组、近期新增与变化、公司趋势和招聘日历。结果保留来源、字段缺失、资格证据与观测时间，适合先找候选，再回原始招聘页核实投递。

## 上手路径

```bash
pip install "jobsearchradar[mcp]"
jobradar update
jobradar search --city 北京 --type intern --table
jobradar doctor
```

安装包名为 `jobsearchradar`，命令为 `jobradar`。用 `jobradar show <job_id>` 阅读单岗原文；用 `jobradar calendar --table` 查看招聘日历。支持 MCP 的客户端可添加命令为 `jobradar-mcp` 的 stdio 服务，随后用自然语言提出城市、公司与招聘条件。

## 迭代中解决的难题

- **跨平台规模与可维护性：** 围绕共享招聘平台做适配器，同时保留企业自研站入口；每个启用源维护真实公开访问依据与限速，拒绝绕过登录、验证码或签名。
- **错误届次与缺失条件：** 不从通用 JD 关键词推测毕业年份；多届范围、否定标题与项目级证据分别处理。明确匹配与未知候选分开说明，避免把“搜到了”写成“符合资格”。
- **状态与新鲜度：** 抓取失败不直接改变岗位状态，列表与正文分别记录观测时间，复用旧正文不制造“刚刚更新”。停用来源与历史岗位也分别处理。
- **查询与交付：** CLI 和 MCP 保持同一筛选语义；长词全文索引与短词回退兼顾既有字面匹配规则；公开快照使用兼容导出，避免工作数据库的新索引影响旧客户端。
- **覆盖口径：** 固定目标池，官方与聚合来源分开报告。配置数量、成功读取与当天在招始终是不同指标。

## 数据范围

仓库已记录的 **2026-11-02** 核验快照包含 298,631 条岗位记录、277,567 条在招记录，在招 JD 正文覆盖率 97.3%。这是有日期的历史快照，不能作为实时岗位数量；记录中包含招聘简章，也不能都理解为独立职位。当前规模与来源状态以 `jobradar stats`、数据 Release 和原始页面为准。

本项目不承诺收录所有公司、所有岗位，未知日期与资格保持未知。其价值在于可追溯的查询、清晰的范围和可复算的统计。

依据：[README](https://github.com/lijiaqi-AI-Product-Manager/job_radar/blob/main/README.md)、[覆盖口径](https://github.com/lijiaqi-AI-Product-Manager/job_radar/blob/main/docs/COVERAGE.md)、[个人条件查询](https://github.com/lijiaqi-AI-Product-Manager/job_radar/blob/main/docs/CANDIDATE-SEARCH.md)、[开发规范](https://github.com/lijiaqi-AI-Product-Manager/job_radar/blob/main/docs/DEVELOPMENT.md)及相关提交。审阅于 2026-11-03。

[仓库与安装](https://github.com/lijiaqi-AI-Product-Manager/job_radar) · [全部项目](../project-atlas.md)
