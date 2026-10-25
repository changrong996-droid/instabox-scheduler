# 作业：GitHub 调度与智能体编排框架搜集筛选

- 作业编号：JOB-20261025-001
- 下达时间：2026-10-25 10:46 (+08:00)
- 下达人：人类负责人（ACCT-A 的真实任务，非实验）
- 目的：为 instabox-scheduler 的 scheduler-spec 找可借鉴的成熟框架，
  不是照搬，而是看哪些概念、哪些规则可以直接参考。
- 说明：这是真实任务，不是协议第 4 节的矩阵实验，不计入
  CLAIMS.md 的实验登记，不占用实验编号。日间实验的机器
  预算（最多 2 台）只约束实验，不约束人类真实任务；
  按协议 7.6，人类真实任务永远优先。

## 分工（5 台并行）

| 机器 | 切片 | 搜集范围 |
|------|------|----------|
| test-1 | S1 持久执行与工作流调度 | Temporal、Cadence、Apache Airflow、Prefect、Dagster、Kestra |
| test-2 | S2 多智能体编排（图模型） | LangGraph、Google ADK、Microsoft Agent Framework、Mastra |
| test-3 | S3 多智能体编排（角色/对话模型） | CrewAI、AutoGen / AG2、MetaGPT、OpenAI Agents SDK |
| test-4 | S4 轻量任务调度与队列 | Quartz、Celery、BullMQ、Sidekiq、Argo Workflows、Nomad（调度部分） |
| test-5 | S5 沙箱/机器池调度与协议 | Kubernetes（Job/CronJob）、Fly Machines、HashiCorp Nomad、MCP、A2A |

## 每路输出格式（统一，便于汇总筛选）

每路交回一个清单，每项包含：
- 仓库：owner/repo 与 GitHub 链接
- 星数：约数，并注明核查日期（2026-10-25）
- 许可：MIT / Apache-2.0 等
- 活跃度：最近一次发布或提交的大致时间，是否仍在维护
- 解决什么问题：一句话
- 与我们 scheduler-spec 的对应点：例如 lease、heartbeat、
  pause/resume、yield（让位）、rate limit、retry、durable execution、
  checkpoint、human-in-the-loop
- verdict：借用 / 参考 / 不适用，并给一句话理由
- 来源：核查过的页面或搜索结果，不编造星数与版本号

## 筛选标准（汇总时用）

- 优先：概念能直接落到 scheduler-spec 的规则上（R-001 至 R-010），
  而不是只看星数。
- 降级：只解决数据管道、只解决单机任务、不处理跨机器/跨账号
  调度的，标为参考或不适用。
- 排除：已停更、许可有采购风险、需要重型自建集群才能跑的，
  注明原因，不硬塞。

## 状态

- 2026-10-25 10:46：作业单建立，5 路并行启动。
- 汇总文件：本文件同目录的 `github-frameworks-2026-10-25.md`
  （待 5 路回齐后写）。
