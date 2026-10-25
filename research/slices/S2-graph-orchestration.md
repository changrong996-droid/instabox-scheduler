# JOB-20261025-001 / S2 — 多智能体编排（图模型）

核查日期：2026-10-25。星数均为约数，以搜索到的页面为准；拿不到的已明说。

## 1. LangGraph

- **仓库：** `langchain-ai/langgraph` — https://github.com/langchain-ai/langgraph
- **星数 / 许可证 / 活跃度：** 约 43,842 stars（GitHub 仓库页本次 fetch，2026-10-25；搜索快照为 43,795，量级一致）；MIT；7,211 commits、585 releases，未归档。最近一次提交的确切日期本次未拿到，标记未核实到日；2026-10 月多篇对比仍列其为活跃开发。
- **一句话：** 把智能体工作流做成有状态的有向图，节点是步骤、边是流转，支持循环、分支与持久化。
- **与 scheduler-spec 对应点：** durable execution、checkpoint、human-in-the-loop、retry（通过持久化+断点续跑实现）。
- **Verdict：借用** — checkpoint / interrupt / durable execution 的语义最成熟，可直接作为我们 R-004（暂停恢复）、R-007（恢复完整性）等规则的模板。
- **来源：** GitHub 仓库页 `langchain-ai/langgraph`（stars 43,842、MIT、7,211 commits）；README“Durable execution / Human-in-the-loop”。

## 2. Google ADK

- **仓库：** `google/adk-python` — https://github.com/google/adk-python （另有 `adk-js` / `adk-go` / `adk-java` 同系仓库）
- **星数 / 许可证 / 活跃度：** 星数**未拿到 GitHub 仓库页直接快照，不编造**。次级来源互相不一致：约 17,500+（know.2nth）、21,739（aireviewrating 2026-10 表）、约 19k（Intuz 2026-07）、约 14k（2025-09 文章），区间约 14k–21.7k，待在仓库页复核。许可证 Apache 2.0（多源一致，PyPI 页亦同）。活跃：v2.12.0 发布于 2026-10-13，PyPI `google-adk` 2.11.0 为 2026-10-02，README 称约双周发布 — 仍在积极维护。
- **一句话：** Google 的代码优先智能体框架，确定性工作流智能体（Sequential / Parallel / Loop）+ LLM 智能体，原生支持 MCP 与 A2A。
- **与 scheduler-spec 对应点：** human-in-the-loop / yield（v2.12.0 新增 workflow `require_confirmation`）、pause/resume（resume Gemini generations、task 子智能体委托与恢复）、checkpoint（Session Service）、lease（无直接对应）。
- **Verdict：参考** — 确认/恢复/会话模式可直接借鉴，但整体偏 GCP / Gemini 生态、2025-04 才发布，不宜整套采用。
- **来源：** GitHub Release v2.12.0（2026-10-13）；PyPI `google-adk` 2.11.0（2026-10-02，Apache 2.0）；know.2nth.ai ADK 页（Apache 2.0、四仓库结构）。

## 3. Microsoft Agent Framework

- **仓库：** `microsoft/agent-framework` — https://github.com/microsoft/agent-framework
- **星数 / 许可证 / 活跃度：** 约 14,226 stars（GitHub 仓库页快照；第三方表为约 14,000，一致）；MIT；3,628 commits、127 releases，创建于 2025-04-28。活跃：Geekflare 2026-10-19 实测 1.22.0，最新发布 1.23.0 为 2026-10-22 — 仍在积极维护。
- **一句话：** 微软统一 AutoGen 与 Semantic Kernel 后的新框架，Python + .NET 双栈，图工作流 + 多智能体编排，原生 MCP / A2A。
- **与 scheduler-spec 对应点：** checkpoint、human-in-the-loop、durable execution（图工作流 checkpoint + time travel）、retry、heartbeat（OpenTelemetry tracing，非心跳调度本身）。
- **Verdict：参考** — 图工作流 + checkpoint + HITL + time travel 的功能组合与我们需求最贴合，但偏 Azure / .NET 生态、2026-04 才 GA，宜参考其模式而非整套引入。
- **来源：** GitHub 仓库页 `microsoft/agent-framework`（14,226 stars、MIT）；Geekflare 2026-10-19 实测（14k stars、1.23.0、2026-10-22）；aireviewrating 2026-10 表（14,000 stars、MIT）。

## 4. Mastra

- **仓库：** `mastra-ai/mastra` — https://github.com/mastra-ai/mastra
- **星数 / 许可证 / 活跃度：** 约 29k stars（Geekflare 2026-10-19 实测，700 contributors；2026-05 对比为约 27,100，量级一致）；许可证：核心 Apache 2.0，部分团队功能为 Mastra Enterprise License（open core，Geekflare 2026-10）。注意：旧 GitHub API 快照曾显示 MIT，已过时，以 2026 年来源为准。活跃：最新发布 1.78.0 为 2026-10-16 — 仍在积极维护。
- **一句话：** TypeScript 优先的智能体框架，智能体 + 多步工作流 + 记忆 + RAG + 评估 + 可观测性，带本地 Studio。
- **与 scheduler-spec 对应点：** pause/resume（工作流可挂起待审批后从保存状态恢复）、checkpoint（工作流状态存储）、human-in-the-loop（经工作流暂停实现审批）。
- **Verdict：参考（TS 优先）** — 挂起/恢复与审批模式值得借鉴；但我们的 spec 是 Python / Markdown 层，且其为 TS 栈 + 部分功能企业许可证，不宜作为运行时采用。
- **来源：** Geekflare 2026-10-19 实测（29k stars、1.78.0、2026-10-16、Apache-2.0 + Enterprise License）；Altaitools 2026-05 对比（约 27,100 stars、Apache 2.0、工作流暂停）。

## 未拿到 / 待复核

- Google ADK（`google/adk-python`）的 GitHub 仓库页星数直接快照未拿到，次级来源区间约 14k–21.7k 不一致，需在仓库页复核后才能定数。
- LangGraph 最近一次提交的确切日期本次未拿到，只确认未归档、多源仍列为活跃。
