# GitHub 调度与智能体编排框架：搜集与筛选

- 作业：JOB-20261025-001
- 日期：2026-10-25
- 方式：5 台机器并行分工（test-1 至 test-5），每路独立搜集，
  汇总时按“能否落到 scheduler-spec 的规则上”筛选，不按星数排队。
- 结论先说：**没有一个框架可以直接拿来当我们的调度器。**
  最值得借的是语义，不是引擎。最贴近的三个参照是
  Fly Machines（lease / suspend / wait）、LangGraph
  （checkpoint / interrupt / durable execution）、BullMQ
  （rate limit / 原子认领 / 重试退避）。

## 星数说明（先读这段）

以下星数均为 2026-10-25 搜集到的页面快照约数，不同来源、
不同抓取时间有出入，已在各切片里注明范围；**没有一个是
2026-10-25 当天的实时 GitHub 数值**，不要把它当实时排名用。
个别项未拿到直接快照，已明说未拿到，例如 Google ADK 星数
在 14k–21.7k 之间各来源不一致、Kubernetes 与 Nomad 的当日
精确星数未拿到。Temporal 的星数按 S1 的 API 快照记为约
18k（2026-02-22 快照），不要与某些对比文章里的 50k+ 混淆。

## 总表（按 verdict）

### 借用（借语义/原语，可直接写进 scheduler-spec 的草案）

| 框架 | 仓库 | 星数约数 | 许可 | 借什么 |
|------|------|----------|------|--------|
| Fly Machines | `superfly/flyctl`（Machines 是平台 API，无独立仓库） | flyctl 约 1.6k | Apache-2.0 | lease（防两个控制器争抢同一台机）、suspend（内存快照暂停）、wait（长轮询等状态变化）、rate limit（约 1 req/s，可突发到 3）、容量不足时调用方重试 |
| LangGraph | `langchain-ai/langgraph` | 约 43.8k | MIT | checkpoint、interrupt、durable execution；可直接作 R-004 / R-007（暂停恢复、恢复完整性）的模板 |
| BullMQ | `taskforcesh/bullmq` | 约 9k | MIT | rate limit（原生，含按组限速）、Lua 原子“取任务并标记 active”、retry 指数退避 |
| A2A | `a2aproject/A2A` | 约 26k | Apache-2.0 | Agent Card（能力发现）+ Task（任务生命周期状态机）；未来“多智能体协调调度多账号机器池”那一步按它设计，现阶段 CLAIMS 先行并注明向 A2A 对齐 |
| OpenAI Agents SDK | `openai/openai-agents-python` | 约 28–30k | MIT | Handoffs（委派）、Guardrails（策略校验）、工具审批式 human-in-the-loop（可暂停运行、从保存状态恢复） |

### 参考（借模式，不引整套）

| 框架 | 仓库 | 星数约数 | 许可 | 参考什么 |
|------|------|----------|------|----------|
| Temporal | `temporalio/temporal` | 约 18k | MIT | durable execution、事件历史/重放、信号/审批；概念最贴合，但自建集群+数据库太重 |
| Apache Airflow | `apache/airflow` | 约 44–46k | Apache-2.0 | DAG、scheduler、pool 并发上限（近似 lease 的槽位思想） |
| Prefect | `PrefectHQ/prefect` | 约 24k | Apache-2.0 | work pool 并发限制、重试/调度模型 |
| Dagster | `dagster-io/dagster` | 约 15–16k | Apache-2.0 | 资产状态、调度 daemon |
| Kestra | `kestra-io/kestra` | 约 28k | Apache-2.0 | YAML flow、cron 触发、插件任务模型；5 路里最贴近心跳轮次的轻量声明式模型 |
| Cadence | `uber/cadence` | 约 5.5k | MIT | 仅作历史对照；已被 Temporal 继承，2026 年活跃度证据未拿到 |
| Kubernetes Job/CronJob | `kubernetes/kubernetes`（batch/v1） | 未拿到当日精确值，2024 年底 >112k | Apache-2.0 | backoffLimit、concurrencyPolicy、startingDeadlineSeconds、错过窗口、Lease 租约对象 |
| Quartz | `quartz-scheduler/quartz` | 约 6.6–6.7k | Apache-2.0 | cron 触发器、misfire 处理、pause（触发器 PAUSED 状态）、集群抢占 |
| Celery | `celery/celery` | 约 27.5k | New BSD | Celery Beat 定时任务、重试、任务级限速 |
| Sidekiq | `sidekiq/sidekiq` | 约 13.3–13.6k | LGPLv3 | 队列 + Web UI + 重试；cron 是扩展，限速在 Pro 版 |
| Argo Workflows | `argoproj/argo-workflows` | 约 16k | Apache-2.0 | DAG、步骤重试、suspend 模板；必须有 K8s 集群 |
| Nomad | `hashicorp/nomad` | 约 16k | **BSL 1.1，非开源** | allocation、binpack/spread、preemption（≈让位）、federation；只借概念，绝不整体采用 |
| Google ADK | `google/adk-python` | 14k–21.7k，未定 | Apache-2.0 | require_confirmation、Session Service、MCP/A2A 原生支持；偏 GCP/Gemini 生态 |
| Microsoft Agent Framework | `microsoft/agent-framework` | 约 14k | MIT | 图工作流 + checkpoint + time travel + HITL；偏 Azure/.NET，2026-04 才 GA |
| Mastra | `mastra-ai/mastra` | 约 29k | Apache-2.0（部分功能企业许可） | 工作流挂起/恢复、审批；TS 栈 |
| CrewAI | `crewAIInc/crewAI` | 约 59k | MIT | 角色/任务委派、max_rpm、human_input、Flows |
| AG2 | `ag2ai/ag2` | 约 5k | Apache-2.0 | 对话模型、Docker 沙箱代码执行 |
| MetaGPT | `geekan/MetaGPT` | 约 70k | MIT | 仅 SOP 思想；维护明显放缓，团队重心已转商业产品 |
| MCP | `modelcontextprotocol/specification` 等 | spec 约 8.4k、python-sdk 约 23k | MIT | 仅限接口层：把“在某台机器上跑一个工具”暴露给智能体的调用面；不回答任何调度问题 |

### 不适用（新项目勿用 / 不整体采用）

- 旧 `microsoft/autogen`：维护模式，自 2025-10-02 起不再加新功能；
  要借就借 AG2 或 Microsoft Agent Framework，不借旧 AutoGen。
- Nomad 整套：BSL 1.1 许可 + 完整集群管理器，太重。
- Kubernetes 整套：对 5 台 InstaBox 过重。
- Temporal / Airflow / Prefect / Dagster 整套：太重或面向数据管道。
- MetaGPT 代码库：维护停滞，不作调度底座。

## 与 scheduler-spec 的对应（借用的落点）

- R-001 机器总数按账号配额：K8s Lease、Nomad allocation、
  Fly Machines lease。我们的 CLAIMS + 账号配额是文件版的
  同一思想。
- R-002 启动按每分钟 3 次限速：BullMQ 原生 rate limit、
  Celery 任务级限速、K8s API 限流/退避。我们的 3 次/分钟
  与 70 秒等待是同一类规则，只是数值来自实测。
- R-004 / R-007 暂停视为冻结、任务可跨暂停续跑：
  LangGraph checkpoint/interrupt、Fly Machines suspend、
  Quartz pause、Mastra 工作流挂起。我们的 A3 已实测
  暂停是冻结，这与它们的语义一致。
- R-008 创建延迟按上界预留：没有直接对应的框架规则；
  创建延迟是 InstaBox 实测值（E-20261025-004），不从
  框架抄。
- R-009 快照制作按 ≤2 分钟预留：没有直接对应的框架规则；
  快照耗时是实测值（E-20261025-006），不从框架抄。
- R-010 恢复后用 uptime -s 判定冻结/重启：我们自己的
  核查方法，框架里没有现成对应。
- 让位规则 7.6（人类真实任务永远优先）：Nomad preemption
  （优先级抢占）、Google ADK require_confirmation、
  OpenAI Agents SDK 工具审批。这三者是“可被打断、可审批”
  的现成原语，与我们的“中止-让位”状态同源。
- 跨账号协调（未来）：A2A 的 Agent Card + Task 状态机。
  今天 ACCT-A 与 ACCT-B 靠 CLAIMS 登记表隔空协调，
  未来应向 A2A 对齐，而不是各家自造登记表格式。

## 筛选结论

1. 调度层分两层：**资源调度**（机器的 lease、配额、暂停、
   恢复、快照）与**智能体编排**（任务的图、角色、对话、
   委派）。前者最贴近 Fly Machines / K8s Job / Nomad，
   后者最贴近 LangGraph / OpenAI Agents SDK / CrewAI。
   两层不要混成一个框架。
2. 我们的调度器是文件式 + 心跳轮询（CLAIMS + experiments +
   scheduler-spec），没有常驻控制面。借用的应该是各框架
   的**语义**（lease、checkpoint、backoffLimit、preemption、
   Agent Card），不是它们的**运行时**。
3. 下一步可直接落到 scheduler-spec 草案的只有三条：
   Fly Machines 的 lease/suspend/wait 语义、LangGraph 的
   checkpoint/interrupt 语义、BullMQ 的 rate limit 与原子
   认领语义。其余全部记为参考，不改现有规则。

## 切片来源

- S1（test-1，持久执行）：`research/slices/S1-durable-execution.md`
- S2（test-2，图模型编排）：`research/slices/S2-graph-orchestration.md`
- S3（test-3，角色/对话编排）：`research/slices/S3-role-conversation.md`
- S4（test-4，轻量调度与队列）：`research/slices/S4-lightweight-scheduling.md`
- S5（test-5，机器池调度与协议）：`research/slices/S5-fleet-scheduling-protocols.md`
