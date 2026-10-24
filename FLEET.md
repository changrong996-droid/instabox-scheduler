# Fleet inventory

Last verified: 2026-10-25 06:17 Beijing time. All 5 machines Paused
(A4 round: test-1 resumed 06:16, snapshot a4-test1-20261025 saved
06:16:50, paused 06:17; test-3 D3 plant untouched, still Paused).
Snapshot count now 2/5. Storage observed 1.4 GiB / 200 GiB at 06:15
(was 1.5 GiB at 04:15; 0.1 GiB difference unexplained, likely
rounding/display, not a policy change).

## Account

- Plan: Free, Personal org. Never billed.
- Machines: 5 total, in any state. Paused and stopped count.
- Snapshots: 2 of 5 used (`base-2026-10-24`, `a4-test1-20261025`
  saved 2026-10-25 06:16:50 from test-1).
- Limits: idle 30 minutes pauses; max runtime 8 hours pauses;
  3 starts per minute.

## Machines

| Machine | Source | Created (Beijing) | Run started | Status at last check |
| --- | --- | --- | --- | --- |
| test-1 | standard | 2026-10-24 23:20:34 | 23:20:49 | Paused (06:17 check; A4 snapshot a4-test1-20261025 saved 06:16:50) |
| test-2 | base-2026-10-24 | 2026-10-25 00:00:42 | — | Paused (04:35 check) |
| test-3 | base-2026-10-24 | 2026-10-25 00:02:15 | — | Paused 04:35, D3 planted (marker PID 5125, harvest 2026-10-26 04:00 / 2026-10-27 04:00) |
| test-4 | base-2026-10-24 | 2026-10-25 00:03:52 | — | Paused (04:35 check) |
| test-5 | base-2026-10-24 | 2026-10-25 04:32:50 | — | Paused at 04:33 (rebuilt this round, id m_agqw7hn5d3p3sl4cbll4o2rf5e) |

Run-started times for the clones were not all recorded in the sync
run; the important verified fact is that each clone reached Running
and passed its terminal check. Do not invent a run-started time for
them from the creation time.

Original test-2 to test-5 (created 23:23-23:25 on 2026-10-24) were
deleted as empty test machines and recreated from the snapshot.
Original test-5 paused for idle time at about 00:02 before it was
deleted; that matches the 30-minute rule.

## Base snapshot

- Name: `base-2026-10-24`
- Saved: 2026-10-24 23:52:40, from test-1.
- Resources: 4 vCPU, 8 GiB, 20 GiB.
- Contents: Debian 13 (trixie), kernel 6.18.54-instabox, user `user`,
  home is `/data/home`, workspace is `/data/workspace` (empty at
  snapshot time, except the base venv below).
- Installed in the base layer: ffmpeg 7.1.5 (Debian trixie package
  7.1.5-0+deb13u1; corrected 2026-10-25, E-20261025-006 — earlier
  records saying 7.7.1 were a transcription error), python3-pip 25.1.1,
  python3-venv, rsync 3.5.0, tmux 3.5a, Pillow 13.0.0 and numpy 2.5.4
  in `/data/workspace/venv-base`.
- Already present, not reinstalled: node 22.23.3, npm 10.9.9,
  python 3.13.5, git 2.47.3, gh 2.102.0, docker client 29.8.2
  (daemon not checked), codex 0.160.0, claude 2.1.288,
  Chromium 154, curl 8.14.1, jq 1.7, unzip, fonts-noto-cjk
  1:20240730 (Noto Sans/Serif CJK SC/TC/HK/KR/JP).
- Missing at inventory time: pip/pip3 before the base install
  (now installed), ffmpeg before the base install (now installed),
  chromium-browser, google-chrome.
- Disk after base install on test-1: root 16G, used 4.3G;
  /data 20G, used 127M.
- A snapshot saves installed software and files, including home,
  workspace and credentials; running processes and unwritten data
  are not saved.

## Per-machine notes

- test-1: original machine, base layer installed here, smoke test
  files in `/data/workspace/smoke-test-2026-10-24/` (not in the
  snapshot, which was saved before the smoke test).
- test-2: video pilot machine. Chinese render test files in
  `/data/workspace/video-test-2026-10-25/`. No new snapshot saved
  for it yet. A3 marker log `/data/workspace/a3-marker.log`
  (700 B, kept); marker process killed after the test.
- test-3, test-4, test-5: base clones, version checks only.
  No video smoke test repeated on them yet, and whether the
  smoke-test files are inherited from the snapshot was not checked.

## What the dashboard alone cannot tell you

- OS distro/version beyond "standard" (found inside the machine:
  Debian 13 trixie).
- Used storage, live CPU/memory use, remaining idle-pause countdown,
  remaining max-runtime countdown.
- Public IP, SSH token value, existing snapshot list beyond the
  dashboard snapshot page.
