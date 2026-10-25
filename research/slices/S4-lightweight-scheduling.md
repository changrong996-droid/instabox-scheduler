# JOB-20261025-001 · 切片 S4：轻量任务调度与队列（test-4）

核查日期：2026-10-25。星数均为搜索快照约数，不同来源抓取时间不同，已注明快照时间；未拿到 2026-10-25 当天的实时 GitHub 数值，不编造。

## 1. Quartz — quartz-scheduler/quartz
- 仓库：`quartz-scheduler/quartz` — https://github.com/quartz-scheduler/quartz
- Stars：约 6.6–6.7k。依据：GitHub Issues 页显示 Star 6.7k；API 快照 `stargazers_count: 6685`，`pushed_at: 2026-01-30`。
- 许可证：Apache-2.0（官网与 Wikipedia 一致）。
- 活跃度：仍在维护，但节奏慢。GitHub 组织页显示该仓库 Updated Dec 1, 2025；另有资料称最新稳定版 2.4.1（2025-10），2.5.0-rc2 在途——版本号未在 GitHub 主页直接核实，仅作参考。
- 一句话：Java 企业级作业调度库，cron 触发器 + 集群 + 数据库持久化。
- 与 scheduler-spec 对应点：heartbeat（cron/interval 触发器）、pause/resume（`scheduler.pauseXXX()`，触发器 PAUSED 状态）、retry（misfire 处理）、lease（集群模式下触发器抢占，近似）。
- Verdict：参考——触发器、misfire、pause 语义可直接借鉴；但它是 Java 进程内库，不是舰队调度器，不适用整体采用。
- 来源：en.wikipedia.org/wiki/Quartz_(scheduler)；quartz-scheduler.org；GitHub 组织页快照；api.github.com/repos/quartz-scheduler/quartz。

## 2. Celery — celery/celery
- 仓库：`celery/celery` — https://github.com/celery/celery
- Stars：约 27.5k。依据：StackShare 多次快照均为 27.5K / Forks 4.9K；2025 年演讲资料为 25.8k，呈上升趋势。未拿到 2026-10-25 实时值。
- 许可证：New BSD License。
- 活跃度：活跃。PyPI 显示 celery 5.6.0rc1（2025-11-01）；文档站有 5.6.3 与 5.7.0rc1。未在搜索中拿到 2026-10-25 当天的提交日期。
- 一句话：Python 分布式任务队列，经 RabbitMQ/Redis broker 分发给 worker，支持定时任务。
- 与 scheduler-spec 对应点：heartbeat（Celery Beat 定时任务）、retry（可配重试次数与间隔）、rate limit（任务级限速）、lease（broker 分发、worker 认领，近似）。
- Verdict：参考——Beat + 重试/限速模型最贴近我们的心跳与队列设计；但需额外 broker，无虚拟机生命周期、无 pause/resume。
- 来源：pypi.org/project/celery/；docs.celeryq.dev；stackshare.io。

## 3. BullMQ — taskforcesh/bullmq
- 仓库：`taskforcesh/bullmq` — https://github.com/taskforcesh/bullmq
- Stars：约 8.5k–9.4k，且在涨。依据：API 快照 8,462（2026-02-26）；用户收藏快照 8,578（2026-03-19）、8,697（2026-04-09）；Web Coding Center 称 9,449（版本 6.3.6）。取约 9k。
- 许可证：MIT（API `license.key: mit`；bullmq.io 称 MIT）。
- 活跃度：活跃。API `pushed_at: 2026-02-26`；收藏快照 Updated 2026-04-09；另有资料称版本 6.3.6。
- 一句话：Node.js/TypeScript 后台任务与消息队列（Redis/PostgreSQL 后端），支持延迟、重复、优先级、父子流程。
- 与 scheduler-spec 对应点：heartbeat（repeatable/cron 任务）、rate limit（原生，含按组限速）、retry（指数退避）、lease（Lua 脚本原子“取任务并标记 active”，多 worker 竞争下仍原子）、durable execution（Redis 持久化，近似）。
- Verdict：借用——本切片最值得抄的队列层参考：限速、原子认领、重试/退避可直接写成规则；但需 Redis，无机器生命周期。
- 来源：api.github.com（taskforcesh/bullmq）；bullmq.io；webcodingcenter.com。

## 4. Sidekiq — sidekiq/sidekiq
- 仓库：`sidekiq/sidekiq` — https://github.com/sidekiq/sidekiq
- Stars：约 13.3k–13.6k。依据：2026 年资料称 13.3k；awesomeopensource 表为 13,554（该表最新发布栏为 2023-10-31，已过时，仅星数可用）。
- 许可证：LGPLv3（Wikipedia）。
- 活跃度：活跃。Wikipedia 稳定版 8.1.7，2026-08-17；另有资料称 8.0+ 支持 Rails 7+、Redis 7.0+。
- 一句话：Ruby 后台任务框架，Redis 队列 + 多线程 worker + Web 管理界面。
- 与 scheduler-spec 对应点：heartbeat（需 sidekiq-cron / sidekiq-scheduler 扩展，非核心）、retry（原生）、rate limit（Pro 版才有）、lease（Redis FIFO 认领，近似）、human-in-the-loop（Web UI 检查与管理，近似）。
- Verdict：参考——队列 + UI + 重试模式可学；但 Ruby 专属，cron 是扩展，限速被 Pro 门槛卡住。
- 来源：en.wikipedia.org/wiki/Sidekiq；copyprogramming.com；awesomeopensource.com。

## 5. Argo Workflows — argoproj/argo-workflows
- 仓库：`argoproj/argo-workflows` — https://github.com/argoproj/argo-workflows
- Stars：约 15k–17k。依据：Enterprise DNA 目录 16,728（2026-06-01）；较旧的 awesome.facts 表为 15,155。取约 16k。
- 许可证：Apache-2.0。
- 活跃度：很活跃。endoflife.date（2026-10-23 更新）：4.1 于 2026-08-11 发布，最新 4.1.6 于 2026-10-22；补丁约每两周一次。
- 一句话：Kubernetes 原生容器工作流引擎，YAML 定义 DAG，多步并行作业。
- 与 scheduler-spec 对应点：durable execution（工作流状态持久化）、retry（步骤重试）、checkpoint（工作流状态可查，近似）、pause/resume（suspend 模板，近似）、heartbeat（无）。
- Verdict：参考——DAG + 重试 + 挂起模型对多步作业有用；但必须有 Kubernetes 集群，对 5 台虚拟机是重炮打蚊子，不适用。
- 来源：endoflife.date/argo-workflows；enterprisedna.co；argoproj/argo-workflows README。

## 6. Nomad（只看调度部分）— hashicorp/nomad
- 仓库：`hashicorp/nomad` — https://github.com/hashicorp/nomad
- Stars：约 15.9k。依据：StackShare 多次快照均为 15.9K / Forks 2.0K。未拿到 2026-10-25 实时值。
- 许可证：Business Source License 1.1（BSL/BUSL，非开源）。依据：2023-08 HashiCorp 将 Nomad 等从 MPL-2.0 转为 BSL 1.1；每个版本在发布 4 年后重新以 MPL-2.0 许可；Nomad 2.0 为当前主线（2026 年中）。借用代码前必须注意此点。
- 活跃度：活跃（主线为 2.0，2026 年中）。本次搜索未拿到 hashicorp/nomad 主仓库 2026-10-25 前后的提交日期，明说：拿不到。
- 一句话：集群管理器与调度器，声明式作业定义，支持长期服务、批量任务、定时任务。
- 与 scheduler-spec 对应点：lease（allocation 分配 + 约束，近似）、heartbeat（client/server 健康检查与 allocation 状态）、yield 让位（preemption，抢占低优先级，近似）、rate limit（调度节流/配额，企业版为主，近似）、retry（restart/reschedule 策略）、durable execution（作业定义持久化）。
- Verdict：参考（只借概念）——binpack/spread、preemption≈让位、allocation≈租用，是本切片最贴近舰队调度的心智模型；但 BSL 许可证 + 完整集群管理器，太重，绝不整体采用。
- 来源：stackshare.io；devopspack.com；developer.hashicorp.com/nomad/docs/ce-license-support。

## 本切片小结
- 最值得借用的：BullMQ（限速 + 原子认领 + 重试/退避）。
- 概念上最贴近舰队调度：Nomad（allocation、preemption、binpack/spread），但只借概念。
- 触发器/pause 语义：Quartz；定时 + 重试：Celery；多步 DAG：Argo Workflows；队列 + UI：Sidekiq。