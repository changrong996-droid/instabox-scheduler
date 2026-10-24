# instabox-scheduler

Scheduling layer for a small fleet of InstaBox cloud computers.

The machines themselves are not the valuable part. The valuable part is
the set of rules that lets one agent — and later, several agents — use,
share, and hand back those machines without stepping on each other.

This repo is the shared notebook for that layer. It is written for cloud
agents first, humans second. Every claim in it should be traceable to a
dated test run in `experiments/`, not to a guess.

## Fleet, as of 2026-10-25 00:06 Beijing time

- Account: Personal, Free plan, 5 machines total, 0 paid workspaces.
- Machines: test-1 to test-5, all Running at last check, all 4 vCPU /
  8 GiB / 20 GiB, Debian 13 (trixie).
- Base snapshot: `base-2026-10-24`, saved 2026-10-24 23:52:40, 1 of 5
  snapshots used.
- Common layer on every machine: ffmpeg 7.7.1, python3-pip 25.1.1,
  python3-venv, rsync 3.5.0, tmux 3.5a, Pillow 13.0.0, numpy 2.5.4 in
  `/data/workspace/venv-base`, plus node 22.23.3, git 2.47.3, gh 2.102.0,
  claude 2.1.288, codex 0.160.0, Chromium 154.
- Chinese fonts (fonts-noto-cjk) were already in the base image; Pillow
  rendering of Chinese text and a 2-second 720p H.264 clip were verified
  on test-1 and test-2.

See `FLEET.md` for the full inventory and `SCHEDULER.md` for the rules.

## Hard limits (verified, not assumed)

- 5 machines total, in any state. Paused and stopped machines count.
  Delete one to free a slot; pausing does not.
- Free plan: never billed. Idle 30 minutes pauses a machine; max
  runtime 8 hours, then it pauses. Pause is not delete and not a charge.
- Start rate limit: 3 starts per minute on the Free plan. The 4th
  start in a minute is refused; wait a minute and retry.
- Snapshots: the dashboard shows a limit of 5 for this account, not the
  10 in the public limits doc. A snapshot saves installed software and
  files, including home, workspace and credentials; running processes
  and unwritten data are not saved.
- Storage per machine is fixed on the Free plan: 20 GiB total, system
  takes 16 GiB in the settings view.

## How to use this repo (agents)

1. Read `SCHEDULER.md` before touching a machine.
2. Claim a machine in `leases.md` before you use it; release it when
   you are done. Never assume a machine is free because it is Running.
3. Do every test through the heartbeat checklist in `heartbeat/`.
4. Write the result into `experiments/` the same run, with date, machine,
   command, result, and what changed. A test with no log did not happen.
5. Never put a secret, token, password, API key, invite code, email
   address, or machine identifier in this repo. Secrets are injected at
   boot or passed per task, never committed.

## Heartbeat

A heartbeat run, about once an hour overnight, checks the fleet status,
resumes a paused machine only if a test needs it, runs one combination
test from the matrix in `SCHEDULER.md`, and logs the result here. It does
not create machines, does not pay, does not upgrade, and does not delete
anything unless a test explicitly says so and the owner approved it.

See `heartbeat/README.md`.

## Status

- 2026-10-24: fleet built, base layer installed and snapshotted,
  5 machines verified Running at the same time.
- 2026-10-25 00:06: base layer synced to all 5 machines by snapshot
  clone, each verified in its terminal.
- Next: second-layer roles, and the first real parallel job.
