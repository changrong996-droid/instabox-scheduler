# S3 — 多智能体编排（角色 / 对话模型）

核查日期：2026-10-25。星数均为搜索到的约数，不同来源有数千差异，已注明范围；未核查到的项明说。

## 1. CrewAI

- **仓库：** `crewAIInc/crewAI` — https://github.com/crewAIInc/crewAI
- **一句话：** 按角色（role / goal / backstory）定义智能体，用 Crew + Task 做委派协作，另有 Flows 做事件驱动编排。
- **核查：** 星数约 59k（59,446，2026-10-08 表；另有来源记 59.7k / 59,725）；许可证 MIT；仍在维护，最近发布 1.15.25（2026-10-07），最近推送 2026-10-08。
- **与 scheduler-spec 对应点：** 角色分工（≈ ACCT-A/B 分工、CLAIMS 登记）、`max_rpm`（rate limit）、`max_retry_limit` 默认 2 / `guardrail_max_retries` 默认 3（retry，但重试会重跑已成功的工具，需外部幂等）、`human_input=True`（human-in-the-loop）、Flows（≈ heartbeat 轮次）、memory（short-term / long-term / entity，近似 checkpoint，非 durable execution）。
- **不对应：** lease、heartbeat、pause/resume、yield 让位。
- **Verdict：参考** — 借角色/任务委派、`max_rpm`、`human_input` 的模式；不把它当调度器用。
- **来源：** https://agent-orchestrators.com/tools/crewai/ ；https://aireviewrating.com/articles/best-open-source-ai-agent-frameworks ；https://docs.crewai.com/llms-full.txt ；https://automatelab.tech/blog/ai-agents/crewai-task-retry-tool-idempotency/

## 2. AutoGen / AG2 / Microsoft Agent Framework（三条线，必须分开）

- **仓库：**
  - 旧 AutoGen：`microsoft/autogen` — https://github.com/microsoft/autogen
  - AG2：`ag2ai/ag2` — https://github.com/ag2ai/ag2
  - Microsoft Agent Framework：`microsoft/agent-framework` — https://github.com/microsoft/agent-framework
- **一句话：** 智能体之间用对话 / 群聊（GroupChat）协作、互相批判和委派，行为从对话中涌现。
- **核查：**
  - 旧 AutoGen：星数约 61k（61,293）；MIT 代码 / CC-BY-4.0 文档；**维护模式**，README 横幅自 2025-10-02 起，不再加新功能，最后发布 `autogen-agentchat` 0.7.5（2025-09-30），最后推送 2026-04-15。是否已“归档”、是否还修安全问题，各来源说法冲突，此处只确认维护模式，不定论归档。
  - AG2：星数约 5k（4,976；另有来源记 ~4.6k）；Apache-2.0；**仍在积极维护**，v1.0.0（2026-07-27），1.1.2（2026-10-03）。2024-11 原作者离开微软后 fork 自 AutoGen 0.2，保留 `import autogen` 命名空间，0.2 代码近乎免改迁移。
  - Microsoft Agent Framework：星数约 14k（13,945）；MIT；**当前微软主推**，1.0 GA（2026-04-02/03），2026-10 月已到 1.20.0（Python）/ 1.24.0（.NET，不同语言版本号不同）。由 AutoGen + Semantic Kernel 合并而来，支持 MCP / A2A。
- **与 scheduler-spec 对应点：** GroupChat / speaker selection（多智能体协调，非 lease）、UserProxyAgent（human-in-the-loop）、Microsoft Agent Framework 的 WorkflowBuilder 在 superstep 边界 checkpoint（checkpoint / durable execution、pause/resume 的近似）、resilient background execution、AG2 的 Docker 沙箱代码执行。
- **不对应：** lease、heartbeat、yield 让位、rate limit（均需外部实现）。
- **Verdict：不适用（旧 `microsoft/autogen`，新项目勿用）/ 参考（AG2 的对话模型、Microsoft Agent Framework 的 checkpoint 与 A2A/MCP 互操作）** — 要借就借后两者，不借旧 AutoGen。
- **来源：** https://intelligenttools.co/blog/what-happened-to-autogen ；https://docs.massgen.ai/en/latest/reference/comparisons/autogen.html ；https://dev.to/avenotech/ai-agent-frameworks-compared-langgraph-vs-crewai-vs-autogen-2l2o ；https://www.developersdigest.tech/blog/microsoft-agent-framework-whats-new-2026

## 3. MetaGPT

- **仓库：** `geekan/MetaGPT` — https://github.com/geekan/MetaGPT
  - 注：部分来源写作 `FoundationAgents/MetaGPT`（OSV 记录亦为 `github.com/foundationagents/metagpt`），疑似组织改名后的同一仓库，未能核查确认，星数按同一仓库计。
- **一句话：** 用 SOP 把 PM / 架构师 / 项目经理 / 工程师等角色串成“虚拟软件公司”，一句话需求输出用户故事、API、数据结构和代码。
- **核查：** 星数约 70k（69.8k–70,773）；许可证 MIT；**维护明显放缓**：最近发布 v0.8.1（2026-10-08 表记 2024-04-22），另有来源称自 2025-03 起无新发布；最近推送 2026-01-21。团队重心已转向商业产品 MGX。
- **与 scheduler-spec 对应点：** SOP（≈ 实验模板里的“操作序列”，固定流程）、角色分工、消息池发布/订阅（≈ 用 CLAIMS / 共享文件协调，非实时通讯）。
- **不对应：** lease、heartbeat、pause/resume、yield 让位、rate limit、retry、durable execution、checkpoint、human-in-the-loop。
- **Verdict：参考（仅 SOP 思想）** — 不适用作代码库或调度底座，维护停滞。
- **来源：** https://aitools.fyi/geekanmetagpt-github ；https://aireviewrating.com/articles/best-open-source-ai-agent-frameworks ；https://geekflare.com/open-source/ai-agent-frameworks/ ；https://test.osv.dev/vulnerability/CVE-2024-23750

## 4. OpenAI Agents SDK

- **仓库：** `openai/openai-agents-python` — https://github.com/openai/openai-agents-python（另有 TypeScript 兄弟库，星数约 3,348）
- **一句话：** 极简的多智能体 SDK：Agent + Handoffs（委派给另一智能体）+ Guardrails（输入/输出校验）+ Sessions + Tracing，2025-03-11 发布，是实验项目 Swarm 的生产继任者。
- **核查：** 星数约 28–30k（29,903，2026-10-08 表；另有来源记 27,730 / 约 30k）；许可证 MIT；**仍在积极维护**，最近发布 v0.23.1（2026-10-02），v0.24.0（2026-10-15），最近推送 2026-10-08。2026-04-15 起 Python 版加入沙箱执行。
- **与 scheduler-spec 对应点：** Handoffs（委派，近似 yield 的“交接”但无抢占）、Guardrails（策略校验）、Sessions（对话历史，非虚拟机 checkpoint）、human-in-the-loop（工具审批可暂停运行、从保存状态恢复，最接近 pause/resume + yield）、Tracing（≈ experiments 日志）。
- **不对应：** lease、heartbeat、rate limit、durable execution（来源明确称崩溃恢复需外部引擎如 Temporal / DBOS）。
- **Verdict：借用（Handoffs + Guardrails + 工具审批式 human-in-the-loop 的原语）** — 借模式，不借作调度器；它没有持久执行。
- **来源：** https://aireviewrating.com/articles/best-open-source-ai-agent-frameworks ；https://geekflare.com/open-source/ai-agent-frameworks/ ；https://www.agenticwire.news/article/pydantic-ai-vs-openai-agents-sdk ；https://toolerific.ai/ai-tools/opensource/openai-openai-agents-python
