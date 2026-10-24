---
id: E-20261024-002
account: ACCT-A
pair:
datetime: 2026-10-24 23:57 (+08:00)
agent: Muse
policy_snapshot: "免费期，5 台 × 4 vCPU，定价未公布（见 policy-history.md PH-001）"
theme: E-兼容性
machines: "1 台，test-1，官方基础镜像 + 通用层"
status: 已完成
---

# 视频冒烟：Pillow 生成图片 + ffmpeg 烧 2 秒 720p

## 假设
通用层装好后，Pillow + ffmpeg 可在 test-1 上完成端到端视频小活。

## 机器组合
- test-1，Debian 13，4 vCPU / 8 GiB / 20 GiB
- 同账号内并行实验数: 4（test-2 至 test-5 当时也在 Running，但未操作）

## 操作序列（可复现）
1. 在 /data/workspace/smoke-test-2026-10-24/ 用 venv-base 的 Pillow 生成 1280x720 图片。
2. 用 ffmpeg 把图片烧成 2 秒 720p MP4。
3. 用 ffprobe 核验编码、尺寸、像素格式、帧率与时长。
4. 记录文件大小与 node、git 版本复核结果。

## 量化结果
| 指标 | 数值 | 样本数 |
|------|------|--------|
| 图片 | 1280x720，8.0K | 1 |
| 视频 | H.264，1280x720，yuv420p，30fps，时长 2.000000 秒，9.1K | 1 |

## 异常与边界
- 无。
- 未重存快照；未在克隆机上重复本实验。

## 结论与调度建议
- 结论：视频小活在 test-1 上一次通过。
- 调度建议：应写入 scheduler-spec.md 的 R-003 草案。
