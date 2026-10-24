---
id: E-20261025-001
account: ACCT-A
pair:
datetime: 2026-10-25 00:06 (+08:00)
agent: Muse
policy_snapshot: "免费期，5 台 × 4 vCPU，定价未公布（见 policy-history.md PH-001）"
theme: A-生命周期
machines: "5 台，test-1 原机 + test-2 至 test-5 快照克隆"
status: 已完成
---

# 快照克隆同步通用层

## 假设
从母快照克隆的机器与原机通用层一致，且 5 台可同时 Running。

## 机器组合
- test-1：原机，来源 standard，创建于 2026-10-24 23:20:34
- test-2 至 test-5：从快照 base-2026-10-24 重建的同名机
- 同账号内并行实验数: 0

## 操作序列（可复现）
1. 在控制台逐台删除原空机 test-2、test-3、test-4、test-5，确认删除提示后等待约 30 秒，计数由 5/5 变为 4/5。
2. 从快照 base-2026-10-24 创建同名新机，名称栏预填的随机名改回原测试名，资源默认 4 vCPU / 8 GiB / 20 GiB。
3. 等待新机变为 Running，创建间隔约 1.5-2 分钟。
4. 在新机终端运行 ffmpeg --version、venv-base 的 Python 导入 Pillow 与 numpy、node --version、git --version。
5. 只有一台验证通过后，才处理下一台。

## 量化结果
| 指标 | p50 | p95 | max | 样本数 |
|------|-----|-----|-----|--------|
| 克隆机创建→Running（约，秒） | 30 | 30 | 30 | 4 |
| 删除→列表消失（约，秒） | 30 | 30 | 30 | 4 |

注：创建到 Running 的时间是约数（对话框显示 Stopped 后约 30 秒变 Running），非精确计时，不作为 A1/A5 的正式延迟数据。

逐台结果：
- test-2：创建于 2026-10-25 00:00:42，直接 Running。
- test-3：创建于 00:02:15，曾短暂显示 Stopped · downloading，约 30 秒后 Running。
- test-4：创建于 00:03:52，曾短暂显示 Stopped · scheduling，约 30 秒后 Running。
- test-5：创建于 00:05:29，曾显示 create queued，约 30 秒后 Running。

终端验证（4 台克隆机，结果与 test-1 完全一致）：
- ffmpeg 7.7.1.5-0+deb13u1
- Pillow 13.0.0
- numpy 2.5.4
- node v22.23.3
- git 2.47.3

## 异常与边界
- 原 test-5 在约 00:02 因闲置 30 分钟自动变为 Paused，后被删除重建。恢复行为未验证，见 A3。
- 本次创建间隔 1.5-2 分钟，未触发每分钟 3 次启动限制。
- 本次验证只做了版本核查，未在克隆机上重复视频冒烟测试，也未核查 test-1 的冒烟测试文件是否随快照继承。

## 结论与调度建议
- 结论：快照克隆可以完整复制通用层，5 台可同时 Running，最终计数 5/5。
- 调度建议：应写入 scheduler-spec.md 的 R-001、R-002、R-003 草案。
