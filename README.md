# SM3012 — ROS 2 TF2 Exercises (All 9 Solved)

**Name:** Abhinav Giri
**Roll Number:** 24BSM001
**Batch:** A
**Subject Code:** SM3012

---

## What's inside

```
sm3012_tf2_exercises/
├── README.md                     <- this file
├── src/tf2_lessons/              <- ROS 2 Python package (build with colcon)
│   ├── package.xml
│   ├── setup.py
│   ├── setup.cfg
│   └── tf2_lessons/
│       ├── sensor_mounts.py      <- Ex 2  (two static transforms, one node)
│       ├── figure_eight.py       <- Ex 3  (odom -> base_link lemniscate @50Hz)
│       ├── odometer.py           <- Ex 4  (pos / distance / yaw, warn-don't-crash)
│       ├── obstacle_mapper.py    <- Ex 6  (laser hit -> odom)
│       ├── time_traveller.py     <- Ex 7  (now / 2 s ago / 30 s ago exception)
│       ├── broken_original.py    <- Ex 8  (as given, for demoing the errors)
│       ├── broken.py             <- Ex 8  (all four bugs FIXED)
│       ├── robot_a.py            <- Ex 9  (circle r=3.0, +0.3 rad/s)
│       ├── robot_b.py            <- Ex 9  (circle r=1.5, -0.7 rad/s, opposite)
│       └── rendezvous.py         <- Ex 9  (range / bearing / FOV / past pose @2Hz)
└── docs/
    ├── exercise1_cli_steps.md    <- Ex 1  (commands + prediction)
    ├── exercise5_explanation.md  <- Ex 5  (TF tree-walking explanation)
    ├── exercise8_bugs.md         <- Ex 8  (4 bugs -> error message -> fix)
    ├── predictions.md            <- predictions for Ex 1, 2, 6
    └── RUN_COMMANDS.md           <- terminal commands for every exercise
```

## Exercise -> file map (per the assignment)

| Exercise | Needed implementation            | Where                                        |
| -------- | -------------------------------- | -------------------------------------------- |
| 1        | CLI work, no Python file         | `docs/exercise1_cli_steps.md`                |
| 2        | `sensor_mounts.py`               | `src/tf2_lessons/tf2_lessons/sensor_mounts.py` |
| 3        | `figure_eight.py`                | `src/tf2_lessons/tf2_lessons/figure_eight.py`  |
| 4        | `odometer.py`                    | `src/tf2_lessons/tf2_lessons/odometer.py`      |
| 5        | existing nodes + explanation     | `docs/exercise5_explanation.md`              |
| 6        | `obstacle_mapper.py`             | `src/tf2_lessons/tf2_lessons/obstacle_mapper.py` |
| 7        | `time_traveller.py`              | `src/tf2_lessons/tf2_lessons/time_traveller.py` |
| 8        | `broken.py` — fix 4 bugs         | `broken.py` (fixed) + `broken_original.py` + `docs/exercise8_bugs.md` |
| 9        | rendezvous node                  | `robot_a.py`, `robot_b.py`, `rendezvous.py`  |

## Build & run

```bash
cd ~/sm3012_tf2_exercises        # copy this folder into your WSL/Linux home first
colcon build
source install/setup.bash
# then follow docs/RUN_COMMANDS.md for each exercise
```

## Quick answers to the "predict" questions

- **Ex 1:** turtle at (3,3) => `checkpoint -> turtle1` = translation (0,0,0), yaw -45 deg.
- **Ex 2:** `tf2_echo laser camera_link` => translation **(-0.10, 0.00, 0.25)**, yaw **90 deg**.
- **Ex 6:** obstacle at t=0 => **(1.70, 0.00, 0.15)** in `odom`.
  (Details: docs/predictions.md)

## Submission checklist (what the email requires)

1. All 9 exercises completed (done above).
2. Email to **sm3012@iiitdmj.ac.in**.
3. Mention **Name, Roll Number, Batch** in the email body.
4. Attach a ZIP of the whole `sm3012_tf2_exercises` folder.

Suggested email:

```
Subject: SM3012 TF2 Exercises - Abhinav Giri - 24BSM001 - Batch A

Name  : Abhinav Giri
Roll  : 24BSM001
Batch : A

All 9 TF2 exercises are attached (ZIP). Exercises 1, 5 and 8 include
the required written explanations/predictions in the docs/ folder.
```

## Note for Windows users

ROS 2 code should run inside **WSL/Ubuntu** (or a ROS 2 Windows install).
Copy the `sm3012_tf2_exercises` folder into your Linux home, build with
`colcon`, and source the install before running the nodes.
