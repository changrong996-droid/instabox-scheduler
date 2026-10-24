---
id: E-20261024-001
account: ACCT-A
pair:
datetime: 2026-10-24 23:54 (+08:00)
agent: Muse
policy_snapshot: "免费期，5 台 × 4 vCPU，定价未公布（见 policy-history.md PH-001）"
theme: E-兼容性
machines: "1 台，test-1，官方基础镜像"
status: 已完成
---

# 通用层安装

## 假设
在 test-1 上补齐 ffmpeg、pip、venv 与轻量工具后，可形成可复用的通用层母快照。

## 机器组合
- test-1，Debian 13 trixie，4 vCPU / 8 GiB / 20 GiB
- 同账号内并行实验数: 4（test-2 至 test-5 当时也在 Running，但未操作）

## 操作序列（可复现）
1. 在控制台打开 test-1，点 Show the terminal，无需 SSH 令牌。
2. 复查已有工具：node、npm、python3、git、gh、docker 客户端、claude、codex、Chromium、curl、jq、unzip 已有，不重装。
3. 运行 sudo apt-get update && sudo apt-get install -y ffmpeg python3-pip python3-venv rsync tmux。sudo -n true 返回 0，未出现密码提示。
4. 在 /data/workspace/venv-base 建虚拟环境，装 Pillow 与 numpy。
5. 冒烟检查：ffmpeg -version、venv Python 导入 Pillow 与 numpy、node --version、git --version、df -h。
6. 点 Save snapshot，名称 base-2026-10-24，确认快照列表。

## 量化结果
| 指标 | 数值 | 样本数 |
|------|------|--------|
| 新装包数 | 5（ffmpeg、python3-pip、python3-venv、rsync、tmux） | 1 |
| 根盘已用变化 | 3.9G → 4.3G | 1 |
| /data 已用变化 | 约 620K → 127M | 1 |
| 快照保存时间 | 2026-10-24 23:52:40 | 1 |

版本：ffmpeg 7.7.1.5-0+deb13u1，python3-pip 25.1.1，python3-venv 3.13.5-1，rsync 3.5.0，tmux 3.5a，Pillow 13.0.0，numpy 2.5.4。

## 异常与边界
- 安装输出仅有一条说明：rsync.service is a disabled or a static unit, not starting it。
- 快照列表显示 1/5，与限制文档写的 10 个不一致，以快照页为准。
- 快照保存已安装软件与文件（含家目录、工作区与凭据），正在运行的进程与未落盘的数据不保存。

## 结论与调度建议
- 结论：通用层可在 test-1 上一次装好并存为母快照。
- 调度建议：应写入 scheduler-spec.md 的 R-003 草案。

## 复核意见
- 2026-10-25 06:15 心跳轮（E-20261025-006@A）：test-1 上实测
  `ffmpeg -version` 为 7.1.5-0+deb13u1，与 A1 轮 test-3 快照
  历史输出的 7.1.5 一致。本文件正文记的 "ffmpeg 7.7.1.5-0+deb13u1"
  有误（应为 7.1.5-0+deb13u1，疑似转录时多写一位），以本次
  复核为准。FLEET.md base 快照清单已同步更正。
