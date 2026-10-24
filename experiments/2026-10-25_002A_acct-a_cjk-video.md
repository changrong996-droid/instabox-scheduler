---
id: E-20261025-002
account: ACCT-A
pair:
datetime: 2026-10-25 00:16 (+08:00)
agent: Muse
policy_snapshot: "免费期，5 台 × 4 vCPU，定价未公布（见 policy-history.md PH-001）"
theme: E-兼容性
machines: "1 台，test-2，快照克隆机"
status: 已完成
---

# 中文视频渲染验证

## 假设
Pillow 可用基础层已有的中文字体渲染中文，并用 ffmpeg 烧成 720p 视频。

## 机器组合
- test-2，base-2026-10-24 克隆机，4 vCPU / 8 GiB / 20 GiB
- 同账号内并行实验数: 4（其他 4 台当时也在 Running，但未操作）

## 操作序列（可复现）
1. 在 test-2 终端运行 fc-list，检查 Noto / CJK 字体。
2. 运行 sudo apt-get install -y fonts-noto-cjk，记录是否新装。
3. 用 /data/workspace/venv-base 的 Pillow 加载 NotoSansCJK-Regular.ttc 的 SC 索引，渲染“洛神赋”与“测试 1280x720 2s 30fps”到 1280x720 图片，统计文字区非背景像素。
4. 用 ffmpeg 把图片烧成 2 秒 720p MP4，用 ffprobe 核验。

## 量化结果
| 指标 | 数值 | 样本数 |
|------|------|--------|
| 字体包新装数 | 0（已是最新版 1:20240730+repack1-1） | 1 |
| 图片 | 1280x720 RGB，41K | 1 |
| 视频 | H.264，1280x720，yuv420p，30fps，时长 2.000000 秒，25K | 1 |
| 文字区非背景像素 | 标题 14303，副标题 12729 | 1 |

字体文件：/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc，加载结果为 Noto Sans CJK SC，Regular，index 2。

## 异常与边界
- fonts-noto-cjk 其实已包含在基础层镜像中，本次未实际新装任何软件包。
- 证据为字体正确加载与文字区像素计数，未在图片查看器中逐字目视核对字形。
- 其他机器未逐台复核字体。

## 结论与调度建议
- 结论：视频专用层在 test-2 上可用，且中文字体无需另装。
- 调度建议：应写入 scheduler-spec.md 的 R-006 草案。
