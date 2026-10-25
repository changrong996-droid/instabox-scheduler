## JOB-20261025-001 / S5 — 沙箱/机器池调度与协议（test-5）

核查日期：2026-10-25。星数均为搜索页面给出的约数，未拿到当日精确值处已注明。

### 1. Kubernetes — Job / CronJob
- 仓库：`kubernetes/kubernetes` — https://github.com/kubernetes/kubernetes
- 查的是：整个 K8s 单体仓，相关部分为 `batch/v1` Job 与 CronJob（`pkg/controller/job`、`pkg/controller/cronjob`、CronJob controller），不是一个独立小框架。
- 一句话：容器编排的事实标准；Job = 跑完即停的一次性任务，CronJob = 按 cron 表达式周期性生成 Job。
- 星数/许可/活跃度：星数未拿到 2026-10-25 当日精确值；可查的最近明确数字是 2024 年底 >112,000 stars、>40,000 forks（Collabnix，2024-12-31）。许可 Apache-2.0（源码文件头逐字确认）。仍在维护：CNCF 旗舰项目，搜索中仍有数日内的文件抓取/提交记录。
- 对应 scheduler-spec：heartbeat（CronJob 的定时触发、missed-schedule 处理）、retry（Job 的 `backoffLimit`、CronJob 的 `concurrencyPolicy` / `startingDeadlineSeconds`）、durable execution（Job 控制器持续调和期望状态）、rate limit（API 限流/退避）、lease（K8s 的 Lease 租约对象，本是节点心跳/leader election 用）。
- Verdict：**参考** — 借概念不借实现：Job/CronJob 的语义（重试上限、并发策略、错过窗口、租约）可直接抄进 scheduler-spec；整套 K8s 对 5 台 InstaBox 来说过重，不适用。
- 来源：Collabnix《Deep Dive into Kubernetes Source Code》；K8s 源码文件头（Apache-2.0）。

### 2. Fly Machines
- 仓库：`superfly/flyctl` — https://github.com/superfly/flyctl（Machines 本身是 Fly.io 的平台 REST API，没有独立开源仓库；flyctl 是其 CLI 客户端，另有 Go 客户端 `superfly/fly-go`）
- 一句话：以 API 创建/启动/停止/销毁 Firecracker 微型虚拟机，秒级启动、停机后可按需唤醒，与 InstaBox 机器的形态最接近。
- 星数/许可/活跃度：flyctl 约 1.6k stars（GitHub release 页 v0.3.236 / v0.3.232 抓取，日期未在页内标明年份，抓取于约 249 天前）。许可 Apache-2.0（LICENSE 文件逐字确认）。仍在维护：Fly 文档 2026-10-15、2026-10-21 仍在更新；2026 年 1 月又推了 Sprites（持久微 VM）。
- 对应 scheduler-spec：pause/resume（Machines 有 `POST /machines/{id}/suspend` 内存快照暂停、`start` 恢复，另有 `stop`）、lease（Machines API 有 `POST /machines/{id}/lease`，专防两个控制器争抢同一台机——与我们 CLAIMS 的防冲突思路同源）、heartbeat（`GET /machines/{id}/wait` 长轮询等状态变化，比轮询更省）、rate limit（API 明确约每动作 1 req/s、可突发到 3）、retry（文档明确写明容量不足时创建失败要由调用方重试或换 region）。
- Verdict：**借用** — 最接近的参照实现：`lease`、`suspend`、`wait` 三个端点语义可直接借进 scheduler-spec；InstaBox 没有这些端点时用 CLAIMS + 心跳轮询模拟。
- 来源：Fly Machines API 文档（docs.fly.io，更新于 2026-10-15 / 2026-10-21）；superfly/flyctl release 页；aicassindra《Fly.io Machines, in depth》（含 lease / rate limit）。

### 3. HashiCorp Nomad
- 仓库：`hashicorp/nomad` — https://github.com/hashicorp/nomad
- 一句话：轻量工作负载编排器：声明式 Job（service / batch / periodic / parameterized），调度器把任务打包到有空闲资源的节点，失败自动重调度。
- 星数/许可/活跃度：星数未拿到 2026-10-25 当日精确值；可查约数约 15.9k（StackShare，未标日期）、另有旧资料写 10k+。许可**注意：不是 MPL-2.0 了**——2023-08 起改为 Business Source License 1.1（BUSL，source-available；4 年后转回 MPL-2.0），自用无碍，但不能用来提供竞品托管服务。仍在维护：Nomad 2.0（2026 年中）、v1.11.2 于 2026-02 发布、v1.11.x 发布说明 2026-04-21；现属 IBM（2025 年收购完成）。
- 对应 scheduler-spec：lease（Nomad 的 allocation / 乐观并发调度）、heartbeat（client 定期心跳，失联后 server 标记 lost 并重调度）、retry（job 的 `reschedule` 块）、rate limit（调度限流/退避）、跨账号/跨智能体协调（federation、多 region / 多 datacenter 是一等概念）、yield 让位（preemption / 优先级抢占，Nomad 有作业优先级与抢占）。
- Verdict：**参考** — 调度模型最值得抄（Job spec、reschedule、优先级抢占、federation），且单二进制、无 etcd，轻量思路贴合 5 台小池；但 BUSL 许可与“另起一个控制面”对我们过重，只借设计不引入。
- 来源：devopspack《HashiCorp Nomad + Autoscaler》（2.0 / BUSL）；HashiCorp 开发者文档 Nomad v1.11.x 发布说明；StackShare 对比页（15.9K stars）。

### 4. MCP（Model Context Protocol）
- 仓库：**不是单一仓库**，是 `modelcontextprotocol` 组织下的协议 + 多语言 SDK。查的仓库：
  - 规范：`modelcontextprotocol/specification` — https://github.com/modelcontextprotocol/specification
  - TS SDK：`modelcontextprotocol/typescript-sdk` — https://github.com/modelcontextprotocol/typescript-sdk
  - Python SDK：`modelcontextprotocol/python-sdk`
  - 参考服务器合集：`modelcontextprotocol/servers`
- 一句话：智能体与外部工具/数据的标准接入协议（Resources / Tools / Prompts，JSON-RPC over stdio 或 Streamable HTTP）；解决“智能体怎么调工具”，不解决“机器怎么调度”。
- 星数/许可/活跃度：按组织页抓取（约 50 天前）：specification ~8.4k、typescript-sdk ~12.7k、python-sdk ~23.3k、servers ~87.1k；另一篇 dev.to 写 servers 约 90,950 stars。许可 MIT（各 SDK README 均注明）。仍在维护：2024-11 Anthropic 发布，2025-12 捐给 Linux Foundation 下的 Agentic AI Foundation（AAIF）；SDK 月下载据称 >9700 万；2026-01-23 仍有更新记录。
- 对应 scheduler-spec：human-in-the-loop（MCP 本身无此原语，但 Inspector / 采样审批是配套做法）、跨账号/跨智能体协调（MCP 是 agent↔tool，不是 agent↔agent；跨智能体协调应看 A2A）、checkpoint / durable execution（无，MCP 是无状态调用协议）、lease / heartbeat / pause-resume / rate limit（均无对应）。
- Verdict：**参考（仅限接口层）** — 未来调度器若要把“在某台机器上跑一个工具”暴露给智能体，MCP 是现成的调用面；但它不回答任何调度问题，不能作为 scheduler-spec 的来源。
- 来源：modelcontextprotocol 组织页（各仓库星数）；DeepWiki《Technical Architecture》（specification 是 source of truth、SDK 实现它）；clawbot MCP 词条（AAIF 捐赠、MIT）。

### 5. A2A（Agent2Agent Protocol）
- 仓库：`a2aproject/A2A` — https://github.com/a2aproject/A2A
- 一句话：不同框架的智能体之间互通的开放协议：Agent Card（`/.well-known/agent-card.json` 能力发现）+ Task（任务生命周期）+ Message（JSON-RPC 2.0 over HTTP，可 SSE 流式回推）。
- 星数/许可/活跃度：26,190 stars、2,678 forks、654 commits、11 releases，Apache-2.0，创建于 2025-03-25（GitHub 仓库页抓取，约 7 天前）。仍在维护：规范 v1.0.0 已发布；2025-06-23 Google 捐给 Linux Foundation，2026-08 加入 AAIF；另一篇 2026-04 文章写 150+ 支持组织、22,000+ stars，与仓库页数字方向一致。
- 对应 scheduler-spec：跨账号/跨智能体协调（**直接对应**：ACCT-A 与 ACCT-B 今天靠 CLAIMS 登记表“隔空协调”，A2A 的 Agent Card + Task 状态机是把这套协调标准化的现成答案）、human-in-the-loop（Task 状态含 input-required，可挂人工审批）、durable execution / checkpoint（Task 有明确生命周期状态，可断点续跑）、lease（无直接对应；A2A 不管资源租约）、heartbeat / pause-resume / rate limit / retry（无直接对应，属传输/调度层）。
- Verdict：**借用（协议层）** — G1 跨账号对照与未来“多智能体协调调度多账号机器池”那一步，应按 A2A 的 Agent Card + Task 模型设计，而不是各家自造登记表格式；现阶段 CLAIMS 可先行，但要注明未来向 A2A 对齐。
- 来源：a2aproject/A2A GitHub 仓库页（26,190 stars、Apache-2.0）；Pandromeda《A2A Protocol Explained》（v1.0.0、Apache-2.0、AAIF）。

### 未拿到项（明说）
- Kubernetes、Nomad 的 2026-10-25 当日精确星数未拿到，只给出了有来源的约数/旧数。
- flyctl 的 1.6k stars 抓取页未标年份；Fly Machines 本身无 GitHub 仓库，无法给“Machines 仓库星数”。
- MCP 的 servers 约 87k–91k 在不同二手来源间有出入，且旧的 servers 存档仓与现行 servers 仓容易混淆，已按组织页的拆分写法交回。