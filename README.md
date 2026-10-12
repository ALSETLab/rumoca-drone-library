# ALSETLab DroneLibrary through Rumoca: a MultiBody quadrotor in Rumoca's 3-D viewer

Second entry for the open challenge of the **Rumoca workshop at the American Modelica Conference 2026**
(CogniPilot, Georgia Tech, 2026-10-12). The entry text and the 45-second pitch are in `ENTRY.md`. The first
entry, the rocket landing, is in `C:\GIT\rumoca-rocket-landing`.

**Question.** How far does Rumoca 0.10.2 get with a real `Modelica.Mechanics.MultiBody` quadrotor library,
and can the library's own hover test fly in Rumoca's 3-D viewer instead of the licensed DLR Visualization
library that the DroneLibrary normally uses?

**Starting model.** `DroneLibrary.Tests.simpleHoverTest` from
[ALSETLab/Modelica-Drone-3D-FMI](https://github.com/ALSETLab/Modelica-Drone-3D-FMI) (M. Podlaski,
L. Vanfretti, D. Winkler, "DroneLibrary: Multi-Domain Drone Modeling in Modelica", 15th International Modelica
Conference, 2023). A chassis of four MultiBody arms, a cylinder and a point mass; four propellers, each with a
DC motor, a revolute rotor and blades; a ramp altitude setpoint of 5 m and one PID driving all motors. The
library is used unmodified: no equation, parameter or connection was changed.

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

### The hover test in Rumoca's 3-D viewer

`viewer/rumoca-scenario.toml` and `viewer/drone_scene.js`, started with `viewer/run_viewer.sh`, then open
<http://localhost:8090>. The quadrotor is drawn from simple Three.js geometry; its position and attitude come
from the MultiBody quaternion of the chassis cylinder, and the four rotor discs spin with the simulated rotor
speeds. Rumoca runs this model at 0.7 to 1.1 times real time on this laptop (the viewer's rate readout). Keys: R reset, T
real-time toggle, F fullscreen, C camera, H heads-up display, Q quit. Screenshots: `results/viewer_*.jpg`.

### MultiBody support matrix

With the same two work-arounds, 3 of 7 MultiBody models from the two ALSETLab libraries simulate in Rumoca
0.10.2; 6 of 7 compile. Full table with exact diagnostics:
`C:\GIT\rumoca-rocket-landing\results\reference\multibody_support_matrix.md`.

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
  under the current folder. `C:\GIT\rumoca-web-assets` holds both: the page from the v0.10.2 source and the
  bundle built with esbuild 0.28.1 from three 0.164.1, exactly as `packages/rumoca-web/build.mjs` does. The
  launch scripts run the CLI from that folder.
- The viewer's reset (R) restores the states but not the model clock, so time-based sources such as the
  library's `Ramp` setpoint do not replay after a reset.
- A live viewer run stops at t = 81 s with "algebraic projection did not converge at event boundary"
  (worst scaled residual ratio 1.000001, target `droneChassis1.bodyShape.frame_a.R.T[1,2]`); by then the
  library's loop has diverged and the drone is above 2 km. Restart with `viewer/run_viewer.sh`.

## How to run

```bash
C:/GIT/rumoca-rocket-landing/.venv/Scripts/python.exe C:/GIT/rumoca-drone-library/tools/build_rumoca_roots.py
bash C:/GIT/rumoca-drone-library/viewer/run_viewer.sh
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
