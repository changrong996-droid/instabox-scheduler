# instabox-scheduler

本仓库是 **ACCT-A** 的实验仓库。ACCT-A 由 Muse（Muse_cr）独占
使用，账号为免费计划，5 台机器，test-1 至 test-5。

ACCT-B 由 tibo-cs 独占使用，各建各的仓库。两账号资源池完全
隔离，互不干扰；本仓库只记录 ACCT-A 的实验，以及已知的配对
复制协调信息。

## 协议

根本规范见 [PROTOCOL.md](PROTOCOL.md)，版本 1.1，日期 2026-10-24。
任何对协议的修改必须经人类负责人批准后生效。

协议摘要：

- 每个智能体绑定并独占一个账号，一智能体一账号，凭证严格
  不交叉，不得借用、代操作或触碰另一账号。
- 实验登记表 CLAIMS.md 的职责是防工作重复 + 配对复制登记。
- 分工：ACCT-A → 主题 A（生命周期）、D（可靠性）、F/G
  （调度与跨账号观测）；ACCT-B → 主题 B（性能边界）、
  C（网络）、E（兼容性）。配对复制实验不受分工限制。
- 每晚一个主题，不贪多。同一实验重复 3 晚以上、结论稳定
  后才可写入 scheduler-spec.md 为"已验证"。
- 实验记录只增不改；结论必须引用实验编号；性能指标必须
  给分布（p50/p95/max），禁止只报平均值。
- 红线：凭证严禁入仓；创建 / 销毁循环温和，间隔 ≥30 秒；
  遇到拒绝 / 429 立即停止并记录，不得重试冲击；实验仅
  针对自己账号内的机器。

## 快速上手

1. 通读 PROTOCOL.md。
2. 确认自己的账号标签是 ACCT-A，并确认只持有该账号的凭证。
3. 复制 templates/experiment-template.md 备用。
4. 在 CLAIMS.md 登记你的第一个实验。

## 仓库结构

- PROTOCOL.md — 根本规范
- CLAIMS.md — 实验登记表
- policy-history.md — 政策 / 额度 / 定价变化记录
- findings.md — 结论汇总（只允许引用实验编号）
- scheduler-spec.md — 调度器规格（草案）
- incidents.md — 异常事件日志
- FLEET.md — ACCT-A 机器清单（截至 2026-10-25 00:06）
- experiments/ — 原始实验记录（只增不改）
- templates/experiment-template.md — 实验记录模板

## 最近动态

- 2026-10-25 00:34：仓库按协议 v1.1 重构完成。旧的
  SCHEDULER.md / leases.md / heartbeat 说明已由
  PROTOCOL.md、scheduler-spec.md、CLAIMS.md 替代；
  已有实验按协议命名与模板迁移，内容未改，只补了
  frontmatter。
- 2026-10-25 00:06：E-20261025-001 快照克隆同步完成，
  5/5 Running，克隆机逐台验证通过。
- 2026-10-25 00:16：E-20261025-002 中文视频渲染完成，
  字体已在基础层镜像中，无需另装。
- 下一个实验：E-20261025-003，A3 暂停恢复，已在
  CLAIMS.md 登记为进行中。按协议第 7 节夜间流程执行。
- 需人类裁决的事项：无。
- 需人类关注：无。
