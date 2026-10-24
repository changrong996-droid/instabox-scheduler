# Heartbeat

## What it is

A short, regular check on the fleet, about once an hour, run by a
cloud agent that is online when humans are not. Its job is to notice
change early, run one combination test at a time, and write the result
down so the next agent does not have to re-learn it.

## What it does, every run

1. Read the fleet list. Record status for all 5 machines.
2. If a machine a test needs is Paused, resume it and record whether
   the resume worked and whether its files were still there.
3. Run exactly one test from the matrix in `../SCHEDULER.md`.
4. Write the result to `../experiments/` with a dated filename.
5. Update `../FLEET.md` only if a durable fact changed.

## What it never does

- Pay, upgrade, or create a paid workspace.
- Create or delete a machine, unless a test explicitly says so and
  the owner approved that test in advance.
- Log in to Claude, Codex, GitHub, or any personal account.
- Enter a secret, token, password, or API key.
- Message the owner for a routine "still Running, nothing new" run.
  It messages only on material change: a resume failure, a limit
  behaving differently from the docs, a conclusive test result, or
  a change in fleet count.

## Cadence

About once an hour overnight. The idle-pause limit is 30 minutes, so
an hourly heartbeat will often find machines Paused; that is expected,
and the resume behaviour is itself a test (see matrix test 5). Do not
tighten the cadence to chase the pause timer; the pause is a feature
of the Free plan, not a bug to work around by keeping machines busy
for no reason.

## Run log

Each run writes one file in `../experiments/` named
`YYYY-MM-DD-HHMM-<test>.md`. The log in this folder is only an index;
the dated experiment files are the record.

- 2026-10-25 00:06: sync completed, 5/5 Running. See
  `../experiments/2026-10-25-sync-base.md`.
- Next run: test 5, pause-resume, on one machine only.
