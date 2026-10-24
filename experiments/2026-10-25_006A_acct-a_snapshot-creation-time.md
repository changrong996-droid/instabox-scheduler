---
id: E-20261025-006
account: ACCT-A
pair: ""
datetime: 2026-10-25 06:15 (+08:00)
agent: Muse
policy_snapshot: "免费期，5 台 × 4 vCPU，定价未公布（见 policy-history.md PH-001）；06:15 巡检与基线一致，无变化：Free 计划、5/5 Paused、快照 1/5（实验后 2/5）、存储 1.4 GiB/200 GiB；Usage 页原文 'Free Plan'、'5 free sandboxes, never billed'；机器/快照/Usage 三页均未见'每分钟最多启动 3 台'文案"
theme: A-生命周期
machines: "1 台 test-1，官方基础镜像，4 vCPU / 8 GiB / 20 GiB（根盘已用 4.3G，/data 已用 127M）"
status: 已完成
---

# 快照制作耗时（A4，单样本）

## 假设
快照制作耗时与磁盘占用量相关；一台根盘已用约 4.3G 的机器，
快照在数分钟内完成。

## 机器组合
- 1 台 test-1，官方基础镜像，无额外快照来源
- 同账号内并行实验数：0（其余 4 台全程 Paused，未操作；
  test-3 为 D3 实验对象，本轮只确认其仍为 Paused，未恢复、
  未重启、未销毁、未打开终端）
- 当日累计创建+销毁：本轮 0 次（只做恢复/暂停与快照创建，
  不计入创建/销毁软上限）；全天累计仍为 32 次（见
  E-20261025-004），未触日软上限 100 次

## 操作序列（可复现）
1. 控制台政策巡检：记录计划、机器数与状态、快照数、存储、
   规则文案。
2. 确认 test-3 仍为 Paused（D3 探活）。
3. 恢复 test-1：点击 Resume，记点击时间与首次确认 Running
   的时间。
4. 打开 test-1 终端，运行 `ffmpeg -version | head -1`、
   `df -h / /data`、`date -u`、`uptime -s` 并逐字记录输出。
5. 控制台为 test-1 创建快照，命名 a4-test1-20261025：
   记提交点击时间、快照首次出现在快照列表的时间与列表显示
   的 Created 时间戳、首次确认无进行中操作的时间。
6. 暂停 test-1，确认回到 Paused；最终确认 5 台全部 Paused。

## 量化结果

计时说明：浏览器操作时间只有分钟精度；快照列表显示的
Created 时间戳为秒级（控制台当地时间）。点击→快照记录
出现只能给出上界：点击发生在 06:16 这一分钟内的未知时刻，
记录 Created 为 06:16:50，故延迟 ∈ [0, 50] 秒。

| 指标 | p50 | p95 | max | 样本数 |
|------|-----|-----|-----|--------|
| 快照提交点击→快照记录出现（上界，s） | — | — | ≤50 | 1 |
| 快照提交点击→首次确认完成（上界，s） | — | — | ≤119 | 1 |
| 恢复点击→首次确认 Running（上界，s） | — | — | ≤119 | 1 |

单样本实测值：
- 恢复：06:16 点击 Resume，先显示 queued，06:16 首次确认
  Running（状态曾为 "Running · restoring"，随后操作显示
  "resume test-1: done"/succeeded，变为纯 Running）。
- 快照：06:16 点击 Save snapshot 并提交，状态显示
  "Saving snapshot a4-test1-20261025 …"；06:16 首次在快照
  列表中看到该快照，列表变为 2/5，Created 显示
  10/25/2026, 6:16:50 AM（当时显示 "6s ago"）；06:17 再次
  确认仍为 2/5，Operations 区域已无进行中操作，其
  "New machine" 按钮可用。控制台未显示中间进度百分比，
  仅有 Saving 状态到列表出现的变化。
- 快照完成后列表：总数 2/5，含 base-2026-10-24 与
  a4-test1-20261025；a4 快照资源显示 4 vCPU、8 GiB memory、
  20 GiB storage，Last used 为 "—"。快照列表无单独的快照
  大小列；总存储在 06:17 仍显示 1.4 GiB / 200 GiB，未变化。
- 暂停：06:17 点击 Pause test-1，操作 "suspend test-1"
  显示 succeeded，通知 "suspend test-1: done"；06:17 确认
  test-1 回到 Paused，最终 5 台全部 Paused，无一台 Running。

终端命令逐字输出（test-1，提示符所在目录为
/data/workspace/smoke-test-2026-10-24）：
- `ffmpeg -version | head -1` →
  `ffmpeg version 7.1.5-0+deb13u1 Copyright (c) 2000-2026 the FFmpeg developers`
- `df -h / /data` →
  `Filesystem      Size  Used Avail Use% Mounted on`
  `/dev/root        16G  4.3G   11G  29% /`
  `/dev/vdb         20G  127M   20G   1% /data`
- `date -u` → `Sat Oct 24 10:16:34 PM UTC 2026`
- `uptime -s` → `2026-10-24 21:08:20`

政策巡检逐项（06:15—06:16）：
- 账号 changrong996@gmail.com，组织 Personal，计划 Free；
  页面原文："Free plan: never billed; pauses after 30 idle
  minutes or 8 running hours"，与预期一致，无变化。
- 机器 5/5，test-1 至 test-5 全部 Paused，每台 4 vCPU /
  8 GiB memory / 20 GiB storage。
- 快照 1/5（实验前），仅 base-2026-10-24；存储
  Storage 1.4 GiB / 200 GiB。Usage 页按机器存储：
  test-1 0.5 GiB、test-2 0.3 GiB、test-4 0.2 GiB、
  test-3 0.2 GiB、test-5 0.2 GiB，合计 1.4 GiB。
  （04:15 巡检记为 1.5 GiB，本轮为 1.4 GiB：0.1 GiB
  的差值未查原因，疑似显示口径/四舍五入，非政策变化。）
- Rules 弹窗为欢迎页 "Rules of the road"（No mining /
  No scanning or attacks / No phishing or stolen credentials /
  No spam or abusing other services），已关闭，未作其他操作。

## 异常与边界
- 无拒绝、无 429、无报错。未点击任何付费/升级入口。
- ffmpeg 版本纠正：test-1 上实际为 7.1.5-0+deb13u1（Debian
  trixie 官方包版本），不是 E-20261024-001 记的 7.7.1；
  与 A1 轮 test-3 快照历史输出的 7.1.5 一致。E-20261024-001
  的 7.7.1 记录有误（见该文件的复核意见段落）；FLEET.md
  的 base 快照内容清单相应更正为 ffmpeg 7.1.5。
  7.7.1 可能是安装时某处输出被误读，原因未再深查——
  实测版本以本轮为准。
- uptime 冻结的旁证：test-1 在 06:16 恢复、06:16 终端
  `date -u` 为 22:16:34 UTC，但 `uptime -s` 为 21:08:20 UTC，
  即机器自认已运行 68 分 14 秒。恢复仅 1 分钟前发生，68 分钟
  的 uptime 只能来自暂停前累积的运行时长在暂停期间冻结、
  恢复后继续累计——与 E-20261025-003（A3）"暂停是冻结而非
  重启，uptime 在暂停期间冻结"的结论在另一台机器上一致。
  机器时钟本身正常（date -u 与北京时间 06:16 一致），冻结
  的是 uptime 计数器，不是时钟。
- 计时精度限制：快照耗时仅 1 个样本，且点击时间只有分钟
  精度，分布（p50/p95）无法计算；"与磁盘占用量的关系"
  需多台不同占用量的样本才能回答，本轮只拿到 4.3G 这一个点。
- 快照不计入 Storage 显示：新增一个快照后总存储仍为
  1.4 GiB / 200 GiB，未变化；快照列表也无单快照大小列。
  快照的存储计量方式未查（可能不计入 200 GiB 沙箱存储，
  或显示有延迟）。

## 结论与调度建议
- 结论：根盘已用 4.3G 的单机快照，提交点击→快照记录出现
  ≤50 秒（单样本上界），06:17 确认完成；快照创建是分钟内
  操作，不构成调度瓶颈（单样本，低置信度）。
- 结论：ffmpeg 实际版本为 7.1.5（Debian 包），E-20261024-001
  的 7.7.1 记录有误，已纠正。
- 结论：uptime 冻结现象在 test-1 上复现，与 A3 结论一致。
- 调度建议：应写入 scheduler-spec.md 的 R-009 草案——调度器
  做快照时按 ≤2 分钟预留窗口（单样本上界，待多样本收紧）；
  快照不占用（或不显示占用）200 GiB 沙箱存储，调度器暂不
  把快照计入存储预算，待核查。
