---
id: E-20261026-004
account: ACCT-A
pair: ""
datetime: 2026-10-26 06:15 (+08:00)
agent: Muse
policy_snapshot: "免费期，5 台 × 4 vCPU，定价未公布（见 policy-history.md PH-001）；06:15 巡检无变化：API usage 限额与 PH-001 一致（maxMachines 5、maxSnapshots 5、maxStoredGiB 200、autoSuspend 1800 秒、maxRun 480 分钟），快照 2/5、存储约 3.36 GiB"
theme: D-可靠性
machines: "test-1（D2 06:15 样本）与 test-2（通宵 pi TASK-B 核查），官方基础镜像，4 vCPU / 8 GiB / 20 GiB"
status: 已完成
---

# 深夜时段单机暂停恢复延迟单样本（D2，06:15 深夜样本）+ 通宵 pi TASK-B 核查

## 假设
06:15 深夜时段的暂停恢复延迟与 00:15、02:15、04:15 深夜样本
及 A3 深夜样本无显著差异；恢复后 uptime 冻结特征与前八次
观测一致。本轮为夜间最后一轮，D2 至此覆盖 7 个时段样本
（08:15、14:15、20:15、00:15、02:15、04:15、06:15）。

## 机器组合
- test-1：D2 06:15 样本，API 路径恢复/暂停，秒级时间戳
- test-2：通宵 pi 任务 TASK-B（租约/队列模块 + pytest）的
  状态核查，恢复后只读检查、随后暂停；不启动新任务
- test-3 为 D3 重埋对象（E-20261025-010），本轮全程未触碰；
  test-4、test-5 全程 Paused，未操作
- 同账号内并行实验数：0
- 当日累计创建+销毁：本轮 0 次（只做恢复/暂停，不计入
  创建/销毁软上限）；2026-10-26 计数仍为 0，未触日软上限
  100 次

## 操作序列（可复现）
1. API 政策巡检：`instabox_api.py ls`（5 台状态与规格）、
   `usage`（限额与存储）、`snapshots`（快照清单）。
2. 恢复 test-2：`instabox_api.py resume test-2 --wait`，
   以 API 操作时间戳计时（创建→runStartedAt→succeeded）。
3. 在 test-2 上执行只读检查：`date -u`、`cat /proc/uptime`、
   `uptime`、`uptime -s`、`tmux ls`、pi 队列 tasks/ 与 done/
   清单、supervisor.log 首 8 行与末 15 行、done/TASK-B 内
   容清单与 TASK.md、a380 目录清单与日志首行、全工作区
   lease/queue/pytest/test_*.py 搜索。
4. 暂停 test-2：`instabox_api.py suspend test-2 --wait`。
5. 恢复 test-1：`instabox_api.py resume test-1 --wait`，
   以 API 操作时间戳计时。
6. 恢复后在 test-1 上执行：`date -u`、`cat /proc/uptime`、
   `uptime`、`uptime -s`、`tmux ls`、pi 队列目录清单与
   supervisor.log 末 3 行，逐字记录输出，与 04:15 样本做
   前后对照。
7. 暂停 test-1：`instabox_api.py suspend test-1 --wait`，
   最终 `ls` 确认 5 台全部 suspended。

方法说明：与 E-20261025-009、E-20261026-001、E-20261026-002、
E-20261026-003 相同，API 路径操作恢复/暂停，秒级时间戳。
恢复延迟为精确到 0.01 秒的实测值。

## 量化结果

| 指标 | p50 | p95 | max | 样本数 |
|------|-----|-----|-----|--------|
| test-1 恢复操作创建→runStartedAt（Running，s） | — | — | 2.32 | 1 |
| test-1 恢复操作创建→操作 succeeded（s） | — | — | 6.19 | 1 |
| test-1 暂停操作创建→操作 succeeded（s） | — | — | 1.93 | 1 |
| test-2 恢复操作创建→runStartedAt（Running，s） | — | — | 2.99 | 1 |
| test-2 恢复操作创建→操作 succeeded（s） | — | — | 7.72 | 1 |
| test-2 暂停操作创建→操作 succeeded（s） | — | — | 0.48 | 1 |

单样本实测值（UTC）：
- test-2 恢复操作：操作创建 22:15:46.294Z，runStartedAt
  22:15:49.284Z（创建→Running 2.99 秒），succeeded
  22:15:54.015Z（创建→成功 7.72 秒）。test-2 的首个
  API 路径恢复秒级样本。
- test-2 暂停：操作创建 22:16:36.736Z，succeeded
  22:16:37.214Z（0.48 秒）。
- test-1 恢复操作：操作创建 22:16:41.174Z，runStartedAt
  22:16:43.498Z（创建→Running 2.32 秒），succeeded
  22:16:47.368Z（创建→成功 6.19 秒）。
- 终端（22:16:51 UTC 执行，即 06:16:51 CST，恢复后
  约 8 秒）：
  - `date -u` → `Sun Oct 25 10:16:51 PM UTC 2026`
  - `/proc/uptime` → `13272.41 52296.08`
  - `uptime` → `22:16:51 up  3:41,  4 users, load average: 0.18, 0.08, 0.04`
  - `uptime -s` → `2026-10-25 18:35:38`
  - `tmux ls` → `pi-super: 1 windows (created Sun Oct 25 15:01:50 2026)`
  - pi 队列：tasks/ 为空；done/ 有 TASK-001、TASK-002、TASK-A
  - supervisor.log 末 3 行：网关 502 JSON 报错行、
    `[TASK-A] attempt 12 exit=1 1792943596`、
    `[TASK-A] done 1792943626`（与 00:15、02:15、04:15 三轮
    末行完全一致，自 00:15 轮后无新增 502、无新任务尝试）
- test-1 暂停：操作创建 22:16:58.500Z，succeeded
  22:17:00.426Z（1.93 秒）；随后最终复核 test-1 至
  test-5 全部回到 suspended。

跨轮对照（D2 样本序列）：
- 08:15（E-20261025-007）：≤60 秒（控制台点击，分钟精度上界）
- 14:15（E-20261025-008）：≤60 秒（控制台点击，分钟精度上界）
- 20:15（E-20261025-009）：2.05 秒（API 路径，秒级实测）
- 00:15（E-20261026-001）：2.59 秒（API 路径，秒级实测）
- 02:15（E-20261026-002）：4.67 秒（API 路径，秒级实测）
- 04:15（E-20261026-003）：5.50 秒（API 路径，秒级实测）
- 06:15（本轮）：2.32 秒（API 路径，秒级实测）
- A3 深夜（E-20261025-003）：3 次约 20 秒（控制台点击，分钟精度）
- 结论：06:15 深夜未见变慢；API 路径五次秒级实测
  （2.05、2.59、4.67、5.50、2.32 秒）同为个位数秒，
  中位数 2.59 秒、极差仍为 3.45 秒，单样本间存在数秒量级
  的恢复方差，D2 分布仍需多样本才能收敛。

跨轮汇总（API 路径 5 样本，20:15 / 00:15 / 02:15 / 04:15 / 06:15）：

| 指标 | min | 中位数 | max | 样本数 |
|------|-----|--------|-----|--------|
| 恢复创建→Running（s） | 2.05 | 2.59 | 5.50 | 5 |

中位数为排序后中间值 2.59 秒；n=5，p95 不单独估计，
以 max 5.50 秒代之。

uptime 冻结核查（第九次复现，test-1 第八时段）：
- 上轮（E-20261026-003）04:16:01 实测：uptime -s
  2026-10-25 16:35:14 UTC，/proc/uptime 13246.79 秒（3:40:47）。
- 本轮 06:16:51 实测：uptime -s 2026-10-25 18:35:38 UTC，
  /proc/uptime 13272.41 秒（3:41:12）。
- 墙钟经过 20:16:01 → 22:16:51 = 2 小时 00 分 50 秒。
  uptime -s 前移 2 小时 00 分 24 秒。
- 两次读数之间 test-1 的状态：04:16:17 暂停（E-20261026-003
  轮末，暂停操作 succeeded 20:16:17Z）→ 本轮 06:16:43 恢复
  （runStartedAt 22:16:43Z），中间无其他恢复，单段暂停
  约 2 小时 00 分 26 秒，与前移 2:00:24 相差约 2 秒，在
  读数时刻取整与操作时间戳口径误差内。
- uptime 增长 13272.41 − 13246.79 = 25.62 秒，与两次读数
  之间的运行总时长（暂停前约 16 秒 + 恢复后约 8 秒 ≈ 24 秒，
  另有 exec 调用开销）相差约 2 秒，在同一误差口径内。
- 校验和：前移 2:00:24 + 增长 0:00:26 = 2:00:50 = 墙钟经过，
  精确吻合，冻结模型自洽。
- 若是重启：恢复后 uptime 应约为恢复后经过的 8 秒，
  uptime -s 应约为 22:16:43 UTC；实测 3:41:12 与 18:35:38
  均不符，重启假设被证伪。
- 结论：本次恢复仍是冻结续跑，非重启；uptime 冻结在
  test-1 上第八时段复现（全部观测中的第九次）。

政策巡检逐项（06:15，API）：
- 限额与 PH-001 一致，无变化：maxMachines 5、
  machineSpec 4 vCPU / 8192 MiB / 20 GiB、
  maxSnapshots 5、maxStoredGiB 200、maxImages 5、
  autoSuspendAfterSeconds 1800、maxRunMinutes 480、
  vault maxItems 100。未见付费提示、未见新限额文案。
- 机器 5/5，test-1 至 test-5 恢复前全部 suspended，
  每台 4 vCPU / 8 GiB / 20 GiB，free: true；模板均为
  agent-browser 2026-10-15.4。
- 快照 2/5：base-2026-10-24（创建于 10/24 15:52:40Z）
  与 a4-test1-20261025（创建于 10/24 22:16:50Z），
  状态均为 ready。
- 存储（API usage，computedAt 2026-10-25T21:05:48Z）：
  storedBytes 3,606,665,935（约 3.36 GiB），分机
  diskBytes：test-1 1,161,611,488（约 1.08 GiB）、test-2
  831,428,120（约 0.77 GiB）、test-3 635,046,144
  （约 0.59 GiB）、test-4 448,855,644（约 0.42 GiB）、
  test-5 409,066,747（约 0.38 GiB），合计约 3.34 GiB，
  test-1 快照字节 120,657,792。与 04:15 的 3,606,824,419
  相比减少约 0.15 MiB，为重算口径波动，非政策变化；
  限额 maxStoredGiB 200 未变。
- 未点击任何付费/升级入口，未进设置页修改任何内容。

D3 探活（E-20261025-010）：
- test-3 全程 Paused，未触碰。24h 收数在 2026-10-26
  20:15 心跳轮，48h 收数在 2026-10-27 20:15 心跳轮。
  本轮只做 ls 探活，状态正常。

## 附带观测（非本实验，供主智能体参考）

### 通宵 pi 任务 TASK-B 核查（test-2，23:14–23:41 CST）
- 任务定义（done/TASK-B/TASK.md）：克隆公开仓库
  instabox-scheduler，在仓库里新建最小可用 Python 模块
  scheduler/lease.py（LeaseManager：acquire/release 租约、
  每分钟最多 3 次启动的限速、租约 TTL、FIFO 等待队列），
  再写 pytest 单元测试并本地跑通；不 push；RESULT.md 写清
  模块接口、pytest 输出与待补项。
- supervisor.log 共 24 行 attempt 记录 = 12 次尝试：
  attempt 1 start 1792941273（15:14:33 UTC = 23:14:33 CST，
  与 tmux pi-super 创建时间一致）、exit=1 1792941447
  （耗时 174 秒）；attempt 2–12 每次约 94 秒后 exit=1；
  attempt 12 start 1792942764、exit=1 1792942858；
  `[TASK-B] done 1792942888`（15:41:28 UTC = 23:41:28 CST，
  与 done/ 目录 mtime 一致）。
- 12 次尝试的退出原因全部相同：网关返回
  `{"error":{"message":"The sandbox service disconnected or is unavailable.","code":502,"status":"Bad Gateway"}}`。
- done/TASK-B 实际内容：started_at.txt、finished_at.txt、
  TASK.md、克隆的 instabox-scheduler 仓库副本——其中
  scheduler/ 只有 __init__.py，无 lease.py、无测试文件、
  无 RESULT.md。全工作区搜索 lease/queue/pytest/test_*.py
  零命中（除 pi-queue 与 venv-base 外）。
- 结论：TASK-B 失败——12/12 次尝试全死于网关 502，零交付
  物；仅完成仓库克隆与空模块占位。根因与 TASK-A（test-1）
  相同：网关闪断，非 pi 与 InstaBox 之过。supervisor 已按
  设计耗尽 12 次重试后归档，tasks/ 为空，不会再自动重试。
- test-2 的 supervisor（tmux pi-super，23:14:33 CST 启动）
  仍在运行，空闲轮询中；本轮恢复/暂停未干扰它（冻结后
  恢复继续，符合设计）。
- test-2 恢复首个 API 路径秒级样本：创建→Running 2.99 秒、
  创建→成功 7.72 秒，与 test-1 的五样本同一量级；暂停
  0.48 秒一次成功。
- test-2 的 uptime -s 2026-10-25 20:01:48 UTC、uptime
  8050.12 秒（2:14）：与冻结模型一致（test-2 于 16:11:22Z
  因 30 分钟闲置自动暂停，至本轮恢复约 6 小时 04 分钟；
  本轮无暂停前的 test-2 读数可做前后对照，test-2 的冻结
  已由 E-20261025-003（A3）验证）。
- a380/ 目录与 TASK-B 无关：为机内既有项目（figures/
  2026-10-19、scripts/ 2026-10-14、NotoSansSC.otf
  2026-10-06），其 review 日志在 TASK-B 窗口内
  （15:27–15:40 UTC）有重新渲染写入（review-a380-engine/
  flaps/section/index 四份日志，末次 15:40），随后 30 分钟
  闲置 → test-2 于 16:11:22Z 自动暂停，与 ls 所见
  autoSuspendedAt 一致。该渲染不是 TASK-B 的产物。
- TASK-C（test-3）仍未核查：test-3 是 D3 被试机、绝不能
  打断暂停，等 20:15 心跳轮 D3 24h 收数时一并核查。

### test-1 pi supervisor 状态
- tmux pi-super 仍在运行，队列 tasks/ 为空，空闲轮询中；
  TASK-001、TASK-002、TASK-A 均已在 done/，无新任务。
  supervisor.log 自 00:15 轮后无新增内容；本轮无新增网关
  502（指 test-1 的 supervisor 日志）。
- 本轮无 InstaBox API 502（02:15 轮曾遇一次短暂 502，
  本轮 6 次 API 调用——test-2 恢复/暂停、test-1 恢复/暂停、
  2 次 exec——均一次成功）。

## 异常与边界
- 本轮 ls 见 test-1 的 updatedAt 为 2026-10-25T20:28:21Z，
  约为 04:15 轮暂停操作 succeeded（20:16:17Z）后 12 分钟；
  但 test-1 状态仍为 suspended、runStartedAt 为 null、
  processesPreserved 为 true、revision 30 与 04:15 轮末
  一致，无恢复/运行痕迹。判断为平台侧冻结状态持久化的
  元数据更新，非异常、不构成风控信号，仅记录。
- test-1 恢复 2.32 秒为 API 路径五次实测中的第二小值，
  与 04:15 的 5.50 秒最大值同属个位数秒量级，属单样本方差，
  非异常。
- test-2 恢复 2.99 秒为该机首个 API 路径样本，无历史对照，
  仅作量级记录。

## 结论与调度建议
- 结论：06:15 深夜单机恢复创建→Running 2.32 秒
  （API 路径秒级实测），创建→操作成功 6.19 秒；与
  00:15 的 2.59 秒、02:15 的 4.67 秒、04:15 的 5.50 秒、
  20:15 的 2.05 秒同为个位数秒，深夜未见变慢。API 路径
  五样本中位数 2.59 秒、极差 3.45 秒，恢复延迟存在数秒
  量级的单样本方差。D2 样本至此为 7 个时段（08:15、
  14:15、20:15、00:15、02:15、04:15、06:15），结论置信度
  仍低（均为单样本、两种计时路径）。
- 结论：uptime 冻结在 test-1 上第八时段复现（全部观测
  第九次）：uptime -s 前移 2:00:24 ≈ 单段暂停时长
  2:00:26，前移量 + uptime 增长量 = 墙钟经过精确吻合，
  冻结模型自洽。
- 结论：通宵 pi 任务 TASK-B 失败（12/12 次尝试全死于网关
  502，零交付物），与 TASK-A 同因；TASK-C 仍待 20:15
  轮 D3 收数时核查。网关闪断是本次通宵实测的最大瓶颈，
  非 InstaBox 平台问题——本轮 InstaBox API 6 次操作全部
  一次成功、无 502。
- 结论：本轮无 InstaBox API 502；02:15 轮的短暂 502 未在
  04:15、06:15 两轮重现，仍属偶发闪断。
- 调度建议：R-007 补充本实验为来源（06:15 深夜样本，
  API 路径精确值 2.32 秒，七时段样本齐全；test-2 首个
  API 路径样本 2.99 秒）；R-010 补充本实验为来源（第七次
  完整的前后对照、第九次复现）。
