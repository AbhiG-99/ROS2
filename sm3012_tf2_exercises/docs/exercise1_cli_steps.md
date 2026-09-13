# Exercise 1 — Read a tree you didn't build (CLI walkthrough)

No Python file is required for this exercise — it is pure TF2 CLI work.

## 1. Start turtlesim + teleop (two terminals)

Terminal 1:

```bash
ros2 run turtlesim turtlesim_node
```

Terminal 2:

```bash
ros2 run turtlesim turtle_teleop_key
```

## 2. Publish static `world -> checkpoint`

```bash
ros2 run tf2_ros static_transform_publisher \
  --x 3 --y 3 --z 0 --yaw 0.785398 \
  --frame-id world --child-frame-id checkpoint
```

(For older ROS 2 versions the positional form also works:
`ros2 run tf2_ros static_transform_publisher 3 3 0 0.785398 0 0 world checkpoint`.)

`yaw = 45 deg = pi/4 = 0.785398 rad`.

## 3. Generate a diagram of the tree

```bash
ros2 run tf2_tools view_frames
```

A file `frames_<timestamp>.pdf` is written in the current folder. Open it —
you will see `world` as the root with branches to `turtle1` (live) and
`checkpoint` (static).

Alternative live view in RViz2: Fixed Frame = `world`, add the *TF* display.

## 4. Print the live transform `world -> turtle1`

```bash
ros2 run tf2_ros tf2_echo world turtle1
```

This streams the turtle's position/orientation as it moves.

## 5. Drive the turtle to roughly (3, 3) and read `checkpoint -> turtle1`

Use the teleop keys until the turtle is near (x=3, y=3), then:

```bash
ros2 run tf2_ros tf2_echo checkpoint turtle1
```

## 6. Prediction (write this in your submission)

Before looking, predict:

> If the turtle is exactly at (3, 3) heading at 0 deg, then
> `checkpoint -> turtle1` should be a **translation of ≈ (0, 0, 0)**
> (the turtle is sitting on top of the checkpoint) and a **rotation of
> yaw = -45 deg** (the turtle's 0-deg heading expressed in the rotated
> 45-deg checkpoint frame).

When the turtle is not exactly on the checkpoint, the numbers show the
small offset — that is exactly what the transform tree computed for you.