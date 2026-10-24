# Scheduler design

## Principle

One machine is a sandbox. Five machines are a fleet only if there is a
scheduler: who gets which machine, for how long, what counts as done,
and how the next agent knows what happened.

The scheduler is deliberately boring: a lease file, a heartbeat, a test
matrix, and a log. No daemon, no paid service, no hidden state.

## Lease rules

- A machine is usable only while you hold its lease in `leases.md`.
- A lease names: machine, agent, purpose, start time, expected end,
  and what will be left on the machine when you release it.
- Leases are first-come, first-served, in the file, not in chat.
  If two agents want the same machine, the one with the earlier
  unexpired lease in the file wins. The other picks another machine
  or waits.
- A lease expires automatically when its expected end passes, or when
  the machine pauses for idle time or max runtime. Expiry is not a
  failure; it is the normal way a machine returns to the pool.
- Never delete a machine another agent has leased. If you must free a
  slot, delete only a machine you leased yourself and that has no
  unreleased work on it, after snapshotting anything worth keeping.
- Never log in to Claude, Codex, GitHub, or any personal account on a
  machine you do not own the lease for, and never leave a login behind
  on a released machine.

## Heartbeat

- Cadence: about once an hour. Faster than that burns agent quota and
  hits the 3-starts-per-minute limit; slower than that lets machines
  sit paused for hours without anyone noticing.
- Each run does, in order:
  1. Read the fleet list and record status for all 5 machines.
  2. If a machine a test needs is Paused, resume it and record whether
     the resume worked and whether its work was still there.
  3. Run exactly one combination test from the matrix below.
  4. Write the result to `experiments/` with a dated filename.
  5. Update `FLEET.md` only if a durable fact changed.
- A heartbeat run reports to the owner only if something changed
  materially: a machine failed to resume, a limit behaved differently
  from the docs, a test conclusively passed or failed, or the fleet
  count changed. Routine "still Running, nothing new" runs stay in
  the log and do not message anyone.
- The heartbeat never pays, never upgrades, never creates a paid
  workspace, and never enters a secret.

## Combination test matrix

Each test is one heartbeat run, unless it says otherwise. Record
pass/fail, exact times, and the exact prompt or message the dashboard
showed.

1. `status-5`: all 5 machines Running at the same time. (Done:
   2026-10-24 23:23-23:25, 5/5.)
2. `clone-base`: delete one empty machine, recreate it from
   `base-2026-10-24`, verify ffmpeg / Pillow / numpy in its terminal.
   (Done for test-2 to test-5, 2026-10-25 00:00-00:05.)
3. `video-smoke`: Pillow 1280x720 image, ffmpeg 2-second 720p H.264,
   ffprobe duration 2.000000. (Done on test-1 and on test-2 with
   Chinese text, 2026-10-24 23:55 and 2026-10-25 00:14.)
4. `cjk-render`: Pillow with Noto Sans CJK SC, render Chinese text,
   verify non-background pixels exist in the text area. (Done on
   test-2; note: the font was already in the base image.)
5. `pause-resume`: let one machine idle 30 minutes, confirm it Pauses,
   resume it, check whether its files and a running process survived.
   Not yet run. This is the most important untested claim.
6. `max-runtime`: run one machine until the 8-hour limit, confirm it
   Pauses, resume it, check whether the 8-hour clock resets.
   Not yet run; do not run it as a blocking test, run it when a real
   job happens to approach 8 hours.
7. `rate-limit`: start 4 machines within one minute, record the exact
   refusal for the 4th, wait 70 seconds, retry. (Partly done: the
   refusal was seen on test-5 creation; the retry succeeded.)
8. `parallel-5-video`: the same 2-second video job on all 5 machines,
   one after another in the same hour, record each machine's time.
   Not yet run.
9. `parallel-5-different`: five different small jobs at once, one per
   machine, record interference, if any. Not yet run.
10. `snapshot-restore`: save a snapshot from a machine that has test
    files on it, recreate from it, check whether the test files are
    in the clone. Not yet run; the smoke-test files were deliberately
    excluded from `base-2026-10-24`.
11. `port-publish`: start a tiny HTTP server on one machine, publish
    its port, fetch it from outside, then close it. Not yet run.
12. `handover`: agent A leases a machine, writes a note in the repo,
    releases it; agent B picks it up from the note alone, with no chat
    handover. Not yet run; this is the real multi-agent test.

## Roles (second layer, draft)

Roles are not baked into the base snapshot. A role is a script run on
top of the base, only on the machine that needs it, and snapshotted
only if it will be reused.

- `video`: Chinese fonts (already in base), Pillow, ffmpeg. Verified.
- `browser`: Chromium (already in base), automation dependencies
  on demand.
- `code`: build toolchain per project, on demand.
- `research`: small Python HTTP/data packages, on demand.
- `voice`: TTS only on a designated machine, keys injected per task,
  never committed, never copied to all 5 machines.

Do not pre-install a role on all 5 machines. Install it where the job
is, verify it, then decide whether it deserves its own snapshot.
Snapshot quota is 5 for this account; do not spend it on unproven roles.

## Conflicts with the public docs

Recorded here because they change decisions:

- Public pricing says Free is 1 machine and Pro is max 5 concurrent.
  This account's dashboard says 5 machines, and 5 were verified
  Running at the same time. Trust the verified fleet, not the pricing
  page, until the account owner says otherwise.
- Public limits doc says 10 snapshots. This account's snapshot page
  says 1 of 5. Trust the dashboard.
- The 8-hour pause and the resume behaviour after it are not yet
  verified. Do not promise a job that it will resume cleanly after
  8 hours until test 6 has run.
