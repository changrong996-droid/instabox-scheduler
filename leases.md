# Leases

A machine is usable only while you hold its lease here. Copy the
template, fill it in, commit it before you start work, and mark it
released when you are done.

## Template

```
- Machine:
- Agent:
- Purpose:
- Started (Beijing):
- Expected end:
- Left on the machine:
- Status: active / released / expired
```

## Active leases

None. All 5 machines are unleased as of 2026-10-25 00:06, after the
base sync. The heartbeat does not hold a lease; it only reads status
and runs short tests, and it must not run a test on a leased machine
without that agent's note in the lease.

## Lease history

- 2026-10-24 23:20-23:57, test-1, Muse: base install, snapshot, video
  smoke test. Released by completion; smoke files left in
  `/data/workspace/smoke-test-2026-10-24/`.
- 2026-10-25 00:00-00:06, test-2 to test-5, Muse: snapshot-clone sync,
  version checks. Released by completion.
- 2026-10-25 00:14-00:16, test-2, Muse: Chinese video pilot.
  Released by completion; files left in
  `/data/workspace/video-test-2026-10-25/`.
