# 项目增长图表 · Project growth charts

各公开仓库的 README 使用本仓库生成的 SVG 图片，支持浅色、深色和手机布局。公开数据每日自动更新，更新时间采用 UTC，逐日统计口径以来源说明为准；源服务和 GitHub 图片缓存可能有延迟。

The public repositories embed SVG charts maintained here, with light, dark and mobile layouts. A daily workflow refreshes public data. Refresh timestamps use UTC; daily boundaries follow each source's definitions. Source services and GitHub image caches can lag.

## 统计口径 · Definitions

- **GitHub Star**：曲线由 GitHub 官方公开聚合历史重建，右上角的当前 Star 另取官方计数接口。聚合日边界不保证与 UTC 一致；取消 Star 或统计延迟可能使累计历史与当前总数不同。Fork 图表只统计账号下的这份 Fork，不使用上游仓库的成绩。收藏很少或历史较短时，图中可能只有一个数据点。
- **npm 下载请求**：使用 npm download-counts 的逐日数据，最多展示最近 90 天；不补造软件包发布前的历史。
- **PyPI 下载请求**：使用 PyPI Stats 的逐日 `without_mirrors` 类别，排除其已识别的镜像请求。只绘制源服务实际返回的日期。
- **请求不等于用户**：重复安装、自动化和测试可能产生下载请求；这些曲线不代表独立用户、成功安装、活跃或付费。
- **缺失不等于零**：新包暂未产生统计时显示等待状态；请求失败时保留最近一次成功数据并标明更新不可用。没有发布 npm/PyPI 包的项目只展示自己的 Star 曲线。

GitHub curves use official public daily aggregates; the header separately reports the current Star count. API day boundaries may differ from UTC, and history can differ from the current total after removals or reporting delays. Fork charts refer only to this account's fork. Package charts show reported daily requests, not unique users, successful installs, active users or revenue. Missing data is not converted to zero. An unavailable source retains the last successful data with a visible notice; a newly published package can remain pending until statistics arrive.

## 包与来源 · Packages and sources

GitHub: [公开 Star 历史与计数接口 / Public Star history and count endpoints](https://docs.github.com/en/rest/activity/starring#get-repository-star-history).

| Project | Package | Public statistics |
| :--- | :--- | :--- |
| job_radar | PyPI `jobsearchradar` | [PyPI Stats](https://pypistats.org/packages/jobsearchradar) |
| AgentCompare | npm `dsh-agent-compare` | [npm](https://www.npmjs.com/package/dsh-agent-compare) |
| skill-healthcheck | npm `skill-healthcheck` | [npm](https://www.npmjs.com/package/skill-healthcheck) |
| unremember | npm `unremember` | [npm](https://www.npmjs.com/package/unremember) |

维护范围由 [配置](../data/growth-config.json) 明确列出，不自动枚举或公开私人仓库。保存的 [数据](../data/growth.json) 只有公开统计与聚合日期，不包含收藏者账号、私人联系方式或凭据。

The [configuration](../data/growth-config.json) explicitly lists the public repositories. Private repositories are not discovered or published. The [stored data](../data/growth.json) contains only public counts and aggregate dates, without stargazer identities or credentials.

## 维护 · Maintenance

```bash
python -m unittest discover -s tests -p 'test_growth.py'
python scripts/update_growth.py
python scripts/update_growth.py --anonymous
python scripts/update_growth.py --render-only
python scripts/check_profile.py
```

手动刷新可运行 [Project growth charts](https://github.com/lijiaqi-AI-Product-Manager/lijiaqi-AI-Product-Manager/actions/workflows/growth-charts.yml)。`--render-only` 只根据已保存的公开数据重建图片，不访问网络。定时任务只向本主页仓库保存统计图片和数据，不改写其他仓库或业务数据。

Use the [workflow](https://github.com/lijiaqi-AI-Product-Manager/lijiaqi-AI-Product-Manager/actions/workflows/growth-charts.yml) for a manual refresh. `--anonymous` reads public GitHub data without ambient credentials and is subject to the public API rate limit. Offline rendering uses committed data only. The scheduled job writes charts and metrics only to this profile repository; it does not modify other repositories or product data.

[返回主页 · Back to profile](../README.md)
