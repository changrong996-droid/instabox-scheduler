---
id: E-20261025-003
account: ACCT-A
pair:
datetime: 2026-10-25 02:25 (+08:00)
agent: Muse
policy_snapshot: "免费期，5 台 × 4 vCPU，定价未公布（见 policy-history.md PH-001）；02:15 巡检无政策变化，快照存储 1.5 GiB / 200 GiB"
theme: A-生命周期
machines: "1 台，test-2，快照克隆机"
status: 已完成
---

# 暂停→恢复的延迟与状态完整性（A3）

## 假设
暂停是冻结虚拟机：恢复后进程（同一 PID）与文件完整，uptime 冻结而非重置；恢复点击→Running 在 1 分钟左右。

## 机器组合
- test-2，base-2026-10-24 克隆机，4 vCPU / 8 GiB / 20 GiB
- 同账号内并行实验数: 0（其余 4 台全程 Paused，未操作）
- 实验前状态：5 台因闲置超 30 分钟全部 Paused（02:15 巡检确认）

## 操作序列（可复现）
1. 控制台观察：记录 5 台状态、数量 5/5、快照 1/5、存储 1.5 GiB / 200 GiB、Free 计划文案。
2. 周期 1：Resume test-2，记点击时间；等 Running，记首次确认时间；开终端，记 date 与 /proc/uptime；ls 视频文件并 ffprobe；启动标记进程（每 5 秒向 /data/workspace/a3-marker.log 写一行 UTC 时间戳），记 PID；Pause test-2，记点击与 Paused 时间；等 60 秒以上。
   - 标记进程命令：`nohup bash -c 'while true; do date "+%Y-%m-%d %H:%M:%S" >> /data/workspace/a3-marker.log; sleep 5; done' >/dev/null 2>&1 & echo started PID $!`
3. 周期 2：Resume test-2；终端查 date、uptime、pgrep、marker 日志、ls 视频文件；等 12 秒再 cat 日志；Pause test-2；等 60 秒以上。
4. 周期 3：Resume test-2；终端查 date、uptime、pgrep、tail 日志；pkill 标记进程并确认清除，保留日志文件；Pause test-2，留为 Paused。
5. 每次恢复/暂停之间间隔 ≥60 秒；全程无创建/销毁，无速率限制、无 429。

## 量化结果
| 指标 | p50 | p95 | max | 样本数 |
|------|-----|-----|-----|--------|
| 恢复点击→首次确认 Running (s) | 约 20 | 约 20 | ≤119（上限） | 3 |
| 暂停点击→首次确认 Paused (s) | 约 20 | 约 20 | ≤119（上限） | 3 |
| 暂停后存活进程（同一 PID） | 2/2 | — | — | 2 次暂停 |
| 文件完整（字节数与 ffprobe 一致） | 3/3 | — | — | 3 次检查 |

注：浏览器侧时间戳只精确到分钟，单次约 20 秒为操作侧观测值；max 列为分钟精度下的严格上限。机器内 date 提供秒级时间，终端可用时刻分别为 02:17:31、02:21:20、02:24:12 CST。

逐周期：
- 周期 1：Resume 点击 02:16 → Running 首次确认 02:17（中途显示 Resuming · restoring）；终端可用 02:17:31，uptime 2963.47（未重置）；视频文件 cjk-1280x720.png 41388 B、cjk-720p-2s.mp4 24858 B、make_cjk_image.py 1292 B 与 00:16 时一致，ffprobe 时长 2.000000；标记进程 PID 6373 启动，日志 18:17:55–18:18:25（UTC）；uptime 18:18:18 时 3010.81（较首次 +47.34 s，与实际经过一致）；Pause 点击 02:18 → Paused 首次确认 02:18。
- 周期 2：Resume 点击 02:20 → Running 02:20；终端 02:21:20，uptime 3064.31（较周期 1 末 +53.50 s，实际经过约 182 s）；PID 6373 仍在；日志缺口 18:18:25→18:20:39，共 134 s，暂停期间无写入，恢复后每 5 s 继续写（至 18:21:44）；视频文件不变；Pause 点击 02:21 → Paused 02:22（中途显示 suspend queued）。
- 周期 3：Resume 点击 02:23 → Running 02:23；终端 02:24:12，uptime 3148.00（较周期 2 +83.69 s，实际经过约 172 s）；PID 6373 仍在；日志缺口 ≥128 s（18:21:44→18:23:52）；清理标记进程，pgrep 无输出，日志文件保留（700 B）；Pause 点击 02:24 → Paused 02:25；最终 5 台全部 Paused。

## 异常与边界
- 首条 nohup 命令因指令笔误（`& then`）报语法错误未启动，随即改用等效命令重跑成功；是指令问题，非机器行为。
- 恢复/暂停延迟受浏览器时间戳分钟精度限制，只能给约 20 秒观测值与 ≤119 秒严格上限；正式延迟分布见 A1。
- 仅在 test-2（快照克隆机）上验证；未验证 8 小时最长运行后恢复是否重置 8 小时时钟（见 R-005）；未验证暂停 24/48 小时（见 D3）。
- 暂停期间 uptime 冻结：两次暂停的 uptime 增量（53.50 s、83.69 s）均远小于实际经过时间（182 s、172 s），增量对应暂停生效前与恢复后的运行时间。

## 结论与调度建议
- 结论：暂停是冻结虚拟机：进程以同一 PID 存活、文件字节级完整、uptime 冻结；恢复点击→Running 约 20 秒（3 次）。
- 调度建议：应写入 scheduler-spec.md 的 R-007 草案；R-004 可更新为已验证恢复完整性，R-005 补充 uptime 冻结证据。
