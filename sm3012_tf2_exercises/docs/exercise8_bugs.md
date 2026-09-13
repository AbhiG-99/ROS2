# Exercise 8 — The four bugs in `broken.py`

The original file is kept as `broken_original.py`; the fixed version is `broken.py`.

## How to reproduce the errors

Terminal 1 (original, buggy):

```bash
ros2 run tf2_lessons broken_original
```

Terminal 2 (listener):

```bash
ros2 run tf2_lessons odometer
```

Fix the bugs one at a time and watch each error disappear.

## The four bugs -> error message -> fix

| # | Bug | Error message you see | Fix (in `broken.py`) |
|---|-----|-----------------------|----------------------|
| 1 | **Leading slash** in frame ID: `header.frame_id = '/odom'` | `Invalid frame ID '/odom'` passed to lookupTransform / frame does not exist | `header.frame_id = 'odom'` (never start frame ids with `/`) |
| 2 | **Stale timestamp**: `header.stamp` is set once in `__init__`, then the *same* `msg` is sent forever with that one old stamp | `Lookup would require extrapolation into the past` — the requested time is newer than the (single) transform the buffer holds | Refresh `msg.header.stamp = self.get_clock().now().to_msg()` inside `tick()` |
| 3 | **Zero / invalid quaternion**: `rotation.w = 0.0` (with x=y=z=0). Norm is 0, not 1, so TF2 rejects it | `Invalid rotation quaternion` — the broadcaster *drops* the message; the listener then reports `no transform found` because nothing gets published | Build a proper yaw quaternion: `rotation.z = sin(yaw/2)`, `rotation.w = cos(yaw/2)` |
| 4 | **Rotation is never updated in `tick()`** — even with a "valid-looking" w=1.0 the robot would still travel its circle with yaw stuck at 0 deg | No hard error, but `odometer` prints a constant / wrong yaw while x,y clearly move | Compute yaw from the motion (atan2 of velocity) and update the quaternion on every tick |

## Why bug 2 is sneaky

`self.msg` is created **once** and stamped **once** in the constructor.
`tick()` only updates x/y and re-sends the same object — so every message
carries the constructor-time stamp. The TF buffer is time-indexed; a
single frozen timestamp makes any timestamp-based lookup fail and newer
requests fall into "extrapolation into the past".

## After the fix

```bash
ros2 run tf2_lessons broken          # fixed broadcaster
ros2 run tf2_lessons odometer        # now prints sane pos / dist / yaw
```