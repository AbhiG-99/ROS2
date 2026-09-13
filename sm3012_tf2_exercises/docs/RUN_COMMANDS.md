# RUN COMMANDS — every exercise, terminal by terminal

> All commands assume a ROS 2 (Humble or newer) terminal on Linux/WSL with
> `turtlesim`, `tf2_tools` and `rviz2` installed, and the workspace built:
>
> ```bash
> cd ~/sm3012_tf2_exercises
> colcon build
> source install/setup.bash
> ```

## Exercise 1 — turtlesim / static frame / view_frames

```bash
# T1
ros2 run turtlesim turtlesim_node
# T2
ros2 run turtlesim turtle_teleop_key
# T3
ros2 run tf2_ros static_transform_publisher --x 3 --y 3 --z 0 --yaw 0.785398 --frame-id world --child-frame-id checkpoint
# T4
ros2 run tf2_tools view_frames
# T4a (live transform)
ros2 run tf2_ros tf2_echo world turtle1
# After driving the turtle to ~(3,3):
ros2 run tf2_ros tf2_echo checkpoint turtle1
```

## Exercise 2 — sensor_mounts.py

```bash
# T1 (must be running so base_link exists — that's Exercise 3's broadcaster)
ros2 run tf2_lessons figure_eight
# T2
ros2 run tf2_lessons sensor_mounts
# T3 (verification)
ros2 run tf2_ros tf2_echo base_link camera_link
ros2 run tf2_ros tf2_echo base_link laser
ros2 run tf2_ros tf2_echo laser camera_link
```

## Exercise 3 — figure_eight.py

```bash
# T1
ros2 run tf2_lessons figure_eight
# T2 (see TF + laser/camera ride along)
ros2 run tf2_lessons sensor_mounts
# T3
rviz2      # Fixed Frame = odom, add TF display
```

## Exercise 4 — odometer.py (start it BEFORE the broadcaster!)

```bash
# T1 (start listener first — it must not crash)
ros2 run tf2_lessons odometer
# T2 (then start the broadcaster)
ros2 run tf2_lessons figure_eight
```

## Exercise 5 — chaining (no new code)

```bash
# T1
ros2 run tf2_lessons figure_eight
# T2
ros2 run tf2_lessons sensor_mounts
# T3
ros2 run tf2_ros tf2_echo odom camera_link
# explanation: see docs/exercise5_explanation.md
```

## Exercise 6 — obstacle_mapper.py

```bash
# T1
ros2 run tf2_lessons figure_eight
# T2
ros2 run tf2_lessons sensor_mounts
# T3
ros2 run tf2_lessons obstacle_mapper
```

## Exercise 7 — time_traveller.py

```bash
# T1
ros2 run tf2_lessons figure_eight
# T2 (run for at least ~5-10 s so the buffer has history)
ros2 run tf2_lessons time_traveller
```

## Exercise 8 — broken broadcaster

```bash
# T1 (original — expect the four errors)
ros2 run tf2_lessons broken_original
# T2
ros2 run tf2_lessons odometer
# --- then the FIXED version ---
# T1
ros2 run tf2_lessons broken
# T2
ros2 run tf2_lessons odometer
# write-up: see docs/exercise8_bugs.md
```

## Exercise 9 — two-robot rendezvous

```bash
# T1
ros2 run tf2_lessons robot_a
# T2
ros2 run tf2_lessons robot_b
# T3
ros2 run tf2_lessons rendezvous
# optional visualization
rviz2   # Fixed Frame = world, add TF display
```