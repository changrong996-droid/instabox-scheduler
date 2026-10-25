---
id: E-20261025-008
account: ACCT-A
pair: ""
datetime: 2026-10-25 14:15 (+08:00)
agent: Muse
policy_snapshot: "免费期，5 台 × 4 vCPU，定价未公布（见 policy-history.md PH-001）；14:15 巡检无变化：Free/Personal、5/5 Paused、快照 2/5、存储 1.4 GiB/200 GiB"
theme: D-可靠性
machines: "1 台 test-1，官方基础镜像，4 vCPU / 8 GiB / 20 GiB"
status: 已完成
---

# 高峰时段单机暂停恢复延迟单样本（D2，14:15 第二白天样本）

## 假设
14:15 高峰时段的暂停恢复延迟与 08:15 白天样本（E-20261025-007，
≤60 秒）及 02:15 深夜样本（A3，约 20 秒）无显著差异；恢复后
uptime 冻结特征与前两轮一致。

## 机器组合
- 1 台 test-1，官方基础镜像
- 同账号内并行实验数：0（其余 4 台全程 Paused，未操作；
  test-3 为 D3 被试机，只确认仍为 Paused，未恢复、未打开
  终端）
- 当日累计创建+销毁：本轮 0 次（只做恢复/暂停，不计入
  创建/销毁软上限）；全天累计仍为 32 次（见
  E-20261025-004），未触日软上限 100 次

## 操作序列（可复现）
1. 控制台政策巡检：记录计划、机器数与状态、快照数、存储、
   规则文案（Machines / Snapshots / Usage / Billing 四页）。
2. 确认 test-3 仍为 Paused（D3 探活）。
3. 恢复 test-1：点击 Resume，记点击时间与首次确认 Running
   的时间。
4. 打开 test-1 终端，运行 `date -u`、`uptime -s`、`uptime`
   并逐字记录输出。
5. 暂停 test-1，确认回到 Paused；最终确认 5 台全部 Paused。

## 量化结果

计时说明：浏览器操作时间只有分钟精度；恢复点击发生在
14:16 这一分钟内的未知时刻，首次确认纯 Running 也在 14:16
这一分钟内，故延迟上界为 60 秒。

| 指标 | p50 | p95 | max | 样本数 |
|------|-----|-----|-----|--------|
| 恢复点击→首次确认纯 Running（上界，s） | — | — | ≤60 | 1 |
| 恢复点击→首次确认过渡态 Resuming · restoring（上界，s） | — | — | ≤60 | 1 |

单样本实测值：
- 恢复：14:16 点击 Resume test-1（操作面板 "resume test-1 ·
  queued"），14:16 首次确认过渡态 "Resuming · restoring"
  （操作面板 "resume test-1 · running · restoring"），14:16
  首次确认纯 Running（点击后约 30 秒内，操作面板
  "resume test-1 · succeeded"）。
- 终端（14:17 执行，UTC 06:17）：
  - `date -u` → `Sun Oct 25 06:17:11 AM UTC 2026`
  - `uptime -s` → `2026-10-25 05:05:36`
  - `uptime` → `06:17:22 up 1:11, 5 users, load average: 0.53, 0.28, 0.10`
- 暂停：14:17 点击 Pause test-1（操作面板 "suspend test-1 ·
  queued"），14:18 首次确认 Paused；14:18 最终复核
  test-1 至 test-5 全部回到 Paused，操作面板已清空。

uptime 冻结核查（第四次复现，test-1 第三时段）：
- 上轮（E-20261025-007）08:16 恢复时 test-1 的 uptime -s
  为 2026-10-24 23:06:24，uptime 1:10；08:17 点击暂停，
  暂停时长至本轮 14:16 恢复约为 5 小时 59 分钟。
- 若暂停是冻结：uptime 应停在约 1:10，恢复后继续累计；
  本轮 14:17 实测 uptime 1:11 = 冻结值约 1:10 + 恢复后
  约 1 分钟，吻合。uptime -s 应前移约等于暂停时长：
  实测 23:06:24 → 05:05:36，前移 5 小时 59 分 12 秒，
  与暂停时长（约 5 小时 59 分钟）吻合到分钟精度。
- 若是重启：恢复后 uptime 应约为恢复后经过的 1 分钟，
  uptime -s 应约为 06:16 UTC；实测 1:11 与 05:05:36
  均不符，重启假设被证伪。
- 结论：本次恢复仍是冻结续跑，非重启；uptime 冻结在
  test-1 上第三时段复现（全部观测中的第四次）。

政策巡检逐项（14:15）：
- 账号 changrong996@gmail.com，组织 Personal，计划 Free；
  Machines 页："Machines 5 / 5"、"Free plan: never billed;
  pauses after 30 idle minutes or 8 running hours"；Usage
  页："changrong996@gmail.com · personal"、"Oct 1 – Nov 1,
  2026"、"Free Plan"、"5 free sandboxes, never billed"；
  Billing 页："Free Plan"、"Free"、"Your personal org stays
  on the Free plan. For a paid plan or members, create a
  workspace."均与上次一致，无变化。
- 机器 5/5，test-1 至 test-5 全部 Paused，每台 4 vCPU /
  8 GiB / 20 GiB。test-5 创建于 10/25 4:32:50 AM；test-4
  创建于 10/25 12:03:52 AM；test-3 创建于 10/25 12:02:15
  AM；test-2 创建于 10/25 12:00:42 AM；test-1 创建于
  10/24 11:20:34 PM。test-2 至 test-5 来源
  base-2026-10-24；test-1 来源 standard。
- 快照 2/5：a4-test1-20261025（创建于 10/25 6:16:50 AM）
  与 base-2026-10-24（创建于 10/24 11:52:40 PM，Last used
  10/25 4:32:50 AM）；存储 1.4 GiB / 200 GiB，与上次
  完全一致。
- 存储分机明细（Usage 页，Measured 10/25/2026 1:40:44 PM，
  hourly）：test-1 0.5 GiB、test-2 0.3 GiB、test-4 0.2 GiB、
  test-3 0.2 GiB、test-5 0.2 GiB，合计 1.4 GiB，各台 Of
  quota 均 <1%。此为首次记录的分机存储明细。
- 页面下方仍有常驻付费工作区推广卡片 "Need more machines?
  More machines, larger sizes and always on come with a paid
  workspace"，未点击、未创建工作区。未进设置页修改任何内容。

D3 探活（E-20261025-005）：test-3 在 Machines 页与 Usage
页均确认仍为 Paused，未恢复、未打开终端、未做任何操作。
24h 收数仍在 2026-10-26 04:00 心跳轮，48h 收数在
2026-10-27 04:00 心跳轮。

## 异常与边界
- 无拒绝、无 429、无报错。未点击任何付费/升级入口。
- 工具层小插曲：首次点击 Resume 时浏览器动作返回
  browser_error、未执行、页面无变化，随后在同一分钟内
  重新点击成功，操作面板正常出现 queued。该问题与
  InstaBox 服务本身无关，未影响结果。
- 速率限制文案未见：Machines、Snapshots、Usage、Billing
  四页均未见"每分钟最多 3 次启动"之类的速率限制文案，
  仅见空闲暂停规则（30 idle minutes 或 8 running hours）。
  PH-001 记的"每分钟最多 3 次启动"来自限制文档，不在
  本轮巡检的四页页面文案中出现——不构成政策变化，仅
  记为巡检所见；限流阈值本身未实测触发。
- 过渡态措辞：页面实际显示为 "Resuming · restoring"，
  与 E-20261025-007 记的 "Running · restoring"不同，
  以本次页面实际为准；两者均为恢复中的过渡态，含义一致。

## 结论与调度建议
- 结论：14:15 高峰时段单机恢复点击→首次确认纯 Running
  ≤60 秒（单样本上界，分钟精度），与 08:15 白天样本
  （≤60 秒）及 A3 深夜 3 次约 20 秒一致，分钟精度下
  未见高峰变慢（低置信度，两白天样本均为单样本）。
- 结论：uptime 冻结在 test-1 上第三时段复现：uptime -s
  前移 5 小时 59 分 12 秒 ≈ 暂停时长，uptime 1:11 =
  冻结值约 1:10 + 恢复后约 1 分钟；重启假设被证伪。
- 调度建议：R-007 补充本实验为来源（14:15 白天样本与
  冻结第四次复现）；R-010 补充本实验为来源（第二次
  完整的前后对照）。
