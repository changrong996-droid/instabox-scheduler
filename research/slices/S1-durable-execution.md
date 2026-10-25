## S1：持久执行与工作流调度 — 结构化清单

**核查日期：2026-10-25。星数均为搜索到的页面快照值，不同来源/时间有出入，已注明范围；未做实时 GitHub API 拉取，未凭记忆编造。**

### 1. Temporal
- **仓库：** `temporalio/temporal` — https://github.com/temporalio/temporal
- **一句话：** 分布式持久执行引擎，工作流按代码定义，失败后可从断点恢复，不重跑已完成步骤。
- **星数：** 约 18,447（GitHub API 快照，`pushed_at: 2026-02-22`，爬取时值；另有来源称 17.2k，量级一致）
- **许可证：** MIT
- **活跃度：** 仍在维护。2026 年 10 月资料提到 Server 1.31/1.32、Python SDK 1.34.0 / Server 1.32.0 实测；CVE 修复涉及 1.31.3 / 1.32 分支。
- **对应 scheduler-spec：** durable execution、checkpoint（事件历史/重放）、retry、heartbeat、human-in-the-loop（信号/审批，工作流可暂停等人）、pause/resume
- **Verdict：参考** — 概念模型最贴合（持久执行+信号+重放），但自建集群+数据库太重，不适合 5 台文件式调度器直接借用。
- **来源：** `api.github.com/repos/temporalio/temporal`（stargazers_count 18447、license MIT）、pkg.go.dev、panoply.io/tools/temporal/

### 2. Cadence
- **仓库：** `uber/cadence` — https://github.com/uber/cadence
- **一句话：** Temporal 的前身，Uber 出品的分布式持久执行编排引擎，执行异步长时业务逻辑。
- **星数：** 约 5,522–5.7k（GitPlanet 5,522；cassandra.link 称 5.7k，来源日期不明）
- **许可证：** MIT
- **活跃度：** 未拿到 2026 年发布/提交证据。搜索只见到 pkg.go.dev 的 v0.21.0 / v0.17.0 等版本页，无 2026 年活跃度可确认项。
- **对应 scheduler-spec：** durable execution、checkpoint/重放、retry、heartbeat
- **Verdict：参考** — 只作历史对照；已被 Temporal 继承，社区规模明显小于 Temporal，不借用。
- **来源：** pkg.go.dev/github.com/uber/cadence、gitplanet.com、cassandra.link

### 3. Apache Airflow
- **仓库：** `apache/airflow` — https://github.com/apache/airflow
- **一句话：** Python 写 DAG 的数据工作流管理平台，编排、调度、监控批量管道。
- **星数：** 约 43,800+（Astronomer，2026 年 8 月）至 46,202（Snyk，46.2k）
- **许可证：** Apache-2.0
- **活跃度：** 仍在维护。稳定版 3.3.0（2026-07-06，Wikipedia）；Snyk 称最新版 3.3.2 / 3.3.1，最近发布约 6 天–1 个月前，最近提交约 27 天前。
- **对应 scheduler-spec：** heartbeat（scheduler）、retry、rate limit（pool / queue / 并发上限，近似 lease 的槽位思想）、checkpoint（任务状态存元数据库）、human-in-the-loop（手动触发/暂停 DAG）
- **Verdict：参考** — DAG + 调度器 + pool 并发模型可借鉴；整体太重（scheduler + 元数据库 + workers），且面向数据管道，非虚拟机生命周期，不直接借用。
- **来源：** astronomer.io（State of Airflow 2026）、security.snyk.io/package/pip/apache-airflow、en.wikipedia.org/wiki/Apache_Airflow

### 4. Prefect
- **仓库：** `PrefectHQ/prefect` — https://github.com/PrefectHQ/prefect
- **一句话：** Python 工作流编排框架，装饰器把脚本变成可恢复、有调度、重试、缓存的弹性数据管道。
- **星数：** 约 24,043（GitHub 仓库页快照，爬取于 4 天前；另有旧快照 21,630）
- **许可证：** Apache-2.0
- **活跃度：** 仍在维护。仓库页显示 22,210 commits、923 releases；归档页显示多文件 2–4 天前有提交。
- **对应 scheduler-spec：** retry、heartbeat（flow run 跟踪/监控）、rate limit（work pool / 并发限制）、scheduling、checkpoint（flow/task 状态）
- **Verdict：参考** — work pool 并发限制 + 重试/调度模型最接近我们的 rate limit / lease 思路；不借用整套引擎。
- **来源：** https://github.com/PrefectHQ/prefect、pythonfix.com/pkg/p/prefect/

### 5. Dagster
- **仓库：** `dagster-io/dagster` — https://github.com/dagster-io/dagster
- **一句话：** 以数据资产为中心的编排平台，关注资产血缘、可观测性、数据质量检查与可测试性。
- **星数：** 约 15k–16.1k（AnyGen：截至 2026 年 9 月 >16,100；PythonFix 旧快照 14,963）
- **许可证：** Apache-2.0
- **活跃度：** 仍在维护。2026 年版本 v1.13.1 / v1.13.21 见于多来源；PythonFix 旧页称最近推送 8 小时前。
- **对应 scheduler-spec：** heartbeat（调度 daemon）、checkpoint（资产物化状态）、retry、scheduling（事件驱动/声明式自动化）
- **Verdict：参考** — 资产状态 + 调度 daemon 的思路可借鉴；数据资产导向与虚拟机生命周期不匹配，不直接借用。
- **来源：** anygen.io、dagster.io 指南页、pythonfix.com/pkg/d/dagster/

### 6. Kestra
- **仓库：** `kestra-io/kestra` — https://github.com/kestra-io/kestra
- **一句话：** YAML 声明式、事件驱动的通用编排/调度平台，任务可用任意语言，带 UI，覆盖数据、基建、AI 工作流。
- **星数：** 约 28,000–28,851（BusinessWire/Morningstar 2026-09-22：>28,000；ossjobs：28,509；webcodingcenter：28,851）
- **许可证：** Apache-2.0
- **活跃度：** 仍在维护。2.0 于 2026-09-07 发布，2.0.4 于 2026-09-29；官方称每月发版，1,500 contributors。
- **对应 scheduler-spec：** heartbeat（Schedule trigger / cron）、retry、checkpoint（执行状态）、scheduling、lease（namespace / 多租户隔离的近似思想）
- **Verdict：参考** — YAML flow + cron 触发 + 插件任务模型是 6 个里最贴近我们心跳轮次的轻量声明式模型；不借用整套 Java 服务端（对 5 台机太重）。
- **来源：** morningstar.com（BusinessWire 2026-09-22）、webcodingcenter.com、dev.to/kestra（Kestra 2.0）

### 本切片小结
- 最值得抄概念的：Temporal（持久执行/重放/信号）、Prefect（work pool 并发限制）、Kestra（YAML + cron 触发）。
- 6 个里没有一个是“直接借用整套”的：全部太重或面向数据管道；我们 5 台机 + 文件式仓库的调度层应只借模型，不引引擎。
- 未拿到项：Cadence 的 2026 年活跃度证据未拿到，已如实标注，未编造。