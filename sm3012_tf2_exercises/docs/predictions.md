# Predictions (write-ups required by the exercises)

## Exercise 1 — `checkpoint -> turtle1` when the turtle sits at (3, 3)

If the turtle is exactly at (3, 3) heading 0 deg:

```
translation = (0, 0, 0)      # it sits on the checkpoint
rotation    = yaw -45 deg    # its 0-deg heading, in the 45-deg checkpoint frame
```

Any small error in driving shows up as a small translation — good way to
check your teleop skills.

## Exercise 2 — `tf2_echo laser camera_link`

Mounts (from `sensor_mounts.py`):

| Parent      | Child         | x     | y    | z     | yaw    |
| ----------- | ------------- | ----- | ---  | ----- | ------ |
| base_link   | laser         | 0.20  | 0.00 | 0.15  | 0 deg  |
| base_link   | camera_link   | 0.10  | 0.00 | 0.40  | 90 deg |

Prediction (camera as seen from the laser frame):

```
T(laser -> camera_link) = inverse(T(base_link -> laser)) (o) T(base_link -> camera_link)

translation = (0.10 - 0.20,  0.00 - 0.00,  0.40 - 0.15) = (-0.10,  0.00,  0.25)
rotation    = 90 deg - 0 deg                             =  90 deg about Z
```

So `tf2_echo laser camera_link` should print:
`translation: (-0.100, 0.000, 0.250)` and `rotation: (0.000, 0.000, 0.707, 0.707)`
(yaw = 90 deg => quaternion z = sin(45°) = 0.707, w = cos(45°) = 0.707).

## Exercise 6 — obstacle position in `odom` at t = 0

At t = 0:
- the robot is at the figure-eight **origin** (0, 0), facing **+x** (yaw = 0)
- `laser` is mounted at (0.20, 0, 0.15) in `base_link`, yaw 0
  -> laser origin at (0.20, 0, 0.15) in `odom`, axes aligned with odom

Laser hit at (1.5, 0, 0) in `laser`:

```
odom x = 0.20 + 1.5 = 1.70
odom y = 0.00
odom z = 0.15
```

**Prediction: the obstacle is at ≈ (1.70, 0.00, 0.15) in `odom`.**

(As the robot moves along the lemniscate the mapping will sweep, since
`laser` keeps rotating with the robot.)

> **Honest note about "facing +x at t = 0":** with the exact equations
> `x = A·sin(ωt)`, `y = A·sin(ωt)·cos(ωt)` the derivative at t = 0 is
> `(Aω, Aω)` — the lemniscate crosses the origin along the 45° diagonal.
> So `figure_eight.py` (which must "face the direction of travel") starts
> at yaw 45°, and the **first** printed mapping is ≈ **(1.20, 1.20, 0.15)**.
> Once the robot swings around to face +x (it does, later in the loop),
> the mapping becomes exactly **(1.70, 0, 0.15)** as predicted above.
> The prediction assumes the ideal "facing +x" state described in the
> assignment.