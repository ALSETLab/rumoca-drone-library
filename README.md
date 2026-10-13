# Beyond DroneLibrary Multi-Domain Drone Modeling: Simulating and Flying a MultiBody Quadrotor in 3-D with Rumoca

Gallery project for the open challenge of the **Rumoca workshop at the American Modelica Conference 2026**
(CogniPilot, Georgia Tech, 2026-10-12). Companion entry: the rocket landing,
[ALSETLab/rumoca-rocket-landing](https://github.com/ALSETLab/rumoca-rocket-landing).

**Question.** How far does Rumoca 0.10.2 get with a real `Modelica.Mechanics.MultiBody` quadrotor library,
and can the library's own hover test fly in Rumoca's 3-D viewer instead of the licensed DLR Visualization
library that the DroneLibrary normally uses?

## Background: the DroneLibrary and its papers

- M. Podlaski, L. Vanfretti, H. Nademi and H. Chang, "UAV Dynamic System Modeling and Visualization using
  Modelica and FMI," The Vertical Flight Society's 76th Annual Forum & Technology Display, Virginia Beach,
  October 6-8, 2020.
  [Publisher](https://vtol.org/store/product/uav-dynamics-and-electric-power-system-modeling-and-visualization-using-modelica-and-fmi-16289.cfm),
  [author's copy](https://ecse.rpi.edu/~vanfrl/documents/publications/conference/2020/CP174_Drone_Modelica_and_FMI.pdf).
- M. Podlaski, L. Vanfretti and D. Winkler, "DroneLibrary: Multi-Domain Drone Modeling in Modelica,"
  Proceedings of the 15th International Modelica Conference, Aachen, October 9-11, 2023,
  [doi:10.3384/ecp204551](https://doi.org/10.3384/ecp204551),
  [author's copy](https://sites.ecse.rpi.edu/~vanfrl/documents/publications/conference/2023/CP238_Drone_Library_IMC_2023.pdf).
- Models: [ALSETLab/Modelica-Drone-3D-FMI](https://github.com/ALSETLab/Modelica-Drone-3D-FMI).

The DroneLibrary models a quadrotor across domains: a MultiBody airframe, DC motors, rotors and blades,
power electronics and batteries, sensors, and continuous, discrete and synchronous controllers. The 2020
paper covers its 3-D visualization and FMU export. The library's virtual-reality view uses the DLR
Visualization library, which needs a commercial license.

## What Rumoca adds

| Topic | Papers (2020, 2023) | This project, with Rumoca 0.10.2 |
|---|---|---|
| Compiler | Dymola | Rumoca simulates the unmodified `Tests.simpleHoverTest` (7613 equations) and `Tests.motorTest` |
| Cross-check | Dymola only | Rumoca agrees with OpenModelica to 0.22 mm in altitude over the first 4 s |
| 3-D view | MultiBody animation in Dymola; VR with the DLR Visualization library (commercial license) | Rumoca's free, open-source Three.js viewer, live, from the MultiBody quaternion and rotor speeds |
| Support status | n/a | 3 of 7 MultiBody models from two ALSETLab libraries simulate; blockers and work-arounds documented |
| Rumoca bugs | n/a | Reset and re-initialization failure reported with a reproducer, [CogniPilot/rumoca#430](https://github.com/CogniPilot/rumoca/issues/430) |

**Starting model.** `DroneLibrary.Tests.simpleHoverTest`: a chassis of four MultiBody arms, a cylinder and
a point mass; four propellers, each with a DC motor, a revolute rotor and blades; a ramp altitude setpoint of
5 m and one PID driving all motors. The library is used unmodified: no equation, parameter or connection was
changed.

**Change.** Everything is outside the library:

1. The Modelica Standard Library 4.0.0 is given to Rumoca as one root directory holding `Modelica/`,
   `ModelicaServices/` and `Complex/` side by side (0.10.2 does not resolve references across roots).
2. In that copy, the `external "builtin"` bodies of `Modelica.Math.sin/cos/...` are rewritten as
   `algorithm y := .cos(u);`, because the 0.10.2 runtime cannot execute external builtins, and two
   OpenModelica-specific calls in `ModelicaServices` are replaced.
3. A copy of the library gets an empty `package.mo` in the three folders that lack one, because the Rumoca
   CLI rejects such a tree as a source root.
4. A Rumoca scenario and a Three.js scene put the chassis pose from the MultiBody frame variables, and the
   four rotor speeds, into Rumoca's interactive viewer.

`tools/build_rumoca_roots.py` builds items 1 to 3 from OpenModelica's installed libraries and the cloned
DroneLibrary; it never modifies the originals.

## Results

### Rumoca agrees with OpenModelica on the unmodified hover test

`check/compare_om.py`, figure `check/compare_om.png`, data `check/compare_om.json`. Rumoca 0.10.2 native
simulator against OpenModelica 1.27 (dassl, tolerance 1e-6) on the same library files, first 4 s:

| Signal | Max abs difference | Range over 4 s |
|---|---|---|
| Chassis altitude `droneChassis1.bodyCylinder.frame_a.r_0[3]` | 2.2e-4 m | 18.5 m |
| PID output (motor current command) | 6.9e-4 | 136.8 |
| Rotor speed `propellerRev.rotor3_1.revolute.w` | 1.1e-4 rad/s | 20.5 rad/s |

Rumoca compiles the 7613-equation model in about 19 s and simulates 4 s in about 75 s on this laptop.

Both tools show the same behavior, which belongs to the library's test, not to either tool: the 50 kg
chassis first sinks to 18.5 m below its start while the PID winds up, then overshoots to 70.7 m at 9.3 s
(OpenModelica, 10 s run), and the loop then diverges. Over 40 s OpenModelica ends at 2202.0 m; Rumoca's
live viewer showed 2202.3 m at 40.2 s.

### The hover test in Rumoca's 3-D viewer: live and replay

Two ways to watch it, both in Rumoca's own viewer (PowerShell; the browser opens by itself once the viewer
is up):

| Mode | Start | What runs | Controls |
|---|---|---|---|
| **Live** (http://localhost:8090) | `& C:\GIT\rumoca-drone-library\viewer\run_viewer.ps1` | Rumoca simulates the unmodified `simpleHoverTest` (7613 equations) at 0.7 to 1.1 times real time; compiling takes one to two minutes | Camera button (C), T real-time toggle, F fullscreen, H heads-up display, Q quit |
| **Replay** (http://localhost:8092) | `& C:\GIT\rumoca-drone-library\viewer\run_replay.ps1` | Plays back a recorded 10 s Rumoca run of the same test, looping; starts in seconds | Replay from the start (R), Camera (C), T, Q |

Both pages show a banner, LIVE or REPLAY, and a status line with time, altitude, set-point, rotor speed and
PID output. The quadrotor is drawn from simple Three.js geometry; its position and attitude come from the
MultiBody quaternion of the chassis cylinder, and the four rotor discs spin with the rotor speeds.

The live mode has no "fly again" or loop: Rumoca 0.10.2's reset fails on this model and ends the viewer
([CogniPilot/rumoca#430](https://github.com/CogniPilot/rumoca/issues/430)). It also stops by itself at
t = 81 s, after the test's PID loop has diverged.

The replay exists for that reason. `check/record_replay.py` records Rumoca's native simulation of the
unmodified test (10 s, every 0.02 s, about 100 s of computing) into `viewer/replay/hover_replay.json`.
`viewer/DroneReplay.mo` is only a replay clock that loops from 0 to 10 s. `viewer/drone_replay_scene.js`
interpolates the recording at that clock; it is generated from `drone_scene.js` by
`tools/make_replay_scene.py`. Nothing physical is simulated live in replay mode, and the page says so.
Screenshots: `results/viewer_live_controls.jpg` and `results/viewer_replay.jpg`.

### MultiBody support matrix

With the same two work-arounds, 3 of 7 MultiBody models from the two ALSETLab libraries simulate in Rumoca
0.10.2; 6 of 7 compile. Full table with exact diagnostics:
[multibody_support_matrix.md](https://github.com/ALSETLab/rumoca-rocket-landing/blob/master/results/reference/multibody_support_matrix.md)
in the rocket repository.

| Model | Equations | Compiles | Simulates | Blocker |
|---|---|---|---|---|
| `DroneLibrary.Tests.motorTest` | 3466 | yes | yes | none; matches OpenModelica to 3.7e-7 relative |
| `DroneLibrary.Tests.simpleHoverTest` | 7613 | yes | yes | none; this entry |
| `DroneLibrary.Tests.propellerTest` | 4256 | yes | no | algebraic projection does not converge at an event |
| `DroneLibrary.Examples.DroneWithIdealPower.TestSystem` | 8005 | yes | no | Solve-IR tensor fill extent |

## Rumoca 0.10.2 findings from this entry

- `Modelica.Math` external builtins block every MultiBody simulation ("external builtin function
  `Modelica.Math.cos` calls `cos`, which this runtime cannot execute"); the algorithm-body rewrite fixes it.
- Cross-root references do not resolve, so the MSL must be one root directory.
- The CLI rejects a source root containing a folder without `package.mo` (PKG-006), although the Python
  API loads the same model file from inside the tree.
- The Windows release binary does not ship the viewer's browser bundle: the page says "Missing Rumoca viewer
  shell". It looks for `packages/rumoca-web/viz/viewer.html` and `packages/rumoca-web/vendor/three_viewer.js`
  under the current folder. A local `rumoca-web-assets` folder holds both (see the rocket repository's viewer README): the page from the v0.10.2 source and the
  bundle built with esbuild 0.28.1 from three 0.164.1, exactly as `packages/rumoca-web/build.mjs` does. The
  launch scripts run the CLI from that folder.
- The viewer's reset (R) restores the states but not the model clock, so time-based sources such as the
  library's `Ramp` setpoint do not replay after a reset.
- On this model the reset fails outright, and so does the start of a minimally changed variant; see the next section.
- A live viewer run stops at t = 81 s with "algebraic projection did not converge at event boundary"
  (worst scaled residual ratio 1.000001, target `droneChassis1.bodyShape.frame_a.R.T[1,2]`); by then the
  library's loop has diverged and the drone is above 2 km. Restart with `viewer/run_viewer.ps1`.

## Reproducer: reset and re-initialization failure

Reported as [CogniPilot/rumoca#430](https://github.com/CogniPilot/rumoca/issues/430).

`check/repro_reset/`. Two symptoms with the same error:

1. In the viewer, pressing R on the running `simpleHoverTest` prints "reset: session reset failed ...
   initial homotopy continuation failed at lambda=0 ... algebraic projection did not converge at event
   boundary ... target=droneChassis1.bodyShape.frame_a.R.T[1,3]", and the viewer exits.
2. `DroneHoverLoop.mo` re-assembles `simpleHoverTest` with identical components and connections, plus one
   state `flight_time` (der = 1) that drives the 5 m ramp instead of `time`. It fails at session creation
   with the same error, in both the CLI and the Python API (`check_loop_model.py`, log
   `check_loop_model.log`), while `simpleHoverTest` itself initializes and runs.

## How to run

```powershell
C:\GIT\rumoca-rocket-landing\.venv\Scripts\python.exe C:\GIT\rumoca-drone-library\tools\build_rumoca_roots.py
& C:\GIT\rumoca-drone-library\viewer\run_viewer.ps1
```

Open <http://localhost:8090> once the log prints "Ready" (compiling takes one to two minutes). The comparison:

```bash
cd C:/GIT/rumoca-drone-library/check && C:/GIT/rumoca-rocket-landing/.venv/Scripts/python.exe compare_om.py
```

It needs the OpenModelica result `check/om/om_simpleHoverTest_res.csv`, produced by
`omc om_simpleHoverTest.mos` in `check/om` (OpenModelica 1.27).

## Credits

DroneLibrary: M. Podlaski, H. Chang, L. Vanfretti (RPI) and D. Winkler (USN), BSD 3-Clause. Modelica
Standard Library: Modelica Association, BSD 3-Clause. Viewer page and build recipe: Rumoca (CogniPilot,
Apache-2.0). Tools: Rumoca 0.10.2, OpenModelica 1.27. Agent: Claude Code with Claude Fable 5.1 and, after
11:30 EDT, Claude Opus 5.5.
