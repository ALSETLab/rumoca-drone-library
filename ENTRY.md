# Challenge entry: ALSETLab DroneLibrary through Rumoca

Second project. The challenge allows one entry per participant for the presenter draw, so this one is either
entered by a team member or posted to the gallery issue
(https://github.com/CogniPilot/rumoca_workshop_amc2026/issues/1) as an additional project.

## One-line entry for the presenters

ALSETLab (RPI). Question: can Rumoca simulate our 2023 MultiBody quadrotor library unmodified, and fly its
hover test in Rumoca's 3-D viewer instead of the licensed DLR Visualization library? Starting model:
`DroneLibrary.Tests.simpleHoverTest` (Podlaski, Vanfretti, Winkler, Modelica 2023). Tools: Claude Code
(Claude Fable 5.1, then Claude Opus 5.5), Rumoca 0.10.2, OpenModelica 1.27. Elapsed: about 1 h 30 min wall
time, 10:35 to 12:05 EDT, including debugging. Shown live: the Rumoca viewer at http://localhost:8090.

## Gallery post

**Name / question.** ALSETLab (RPI). How far does Rumoca 0.10.2 get with a real `Modelica.Mechanics.MultiBody`
quadrotor library, and can the library's own hover test fly in Rumoca's 3-D viewer instead of the licensed
DLR Visualization library we normally use?

**Starting model and change.** `DroneLibrary.Tests.simpleHoverTest` from ALSETLab/Modelica-Drone-3D-FMI
(M. Podlaski, L. Vanfretti, D. Winkler, 15th Modelica Conference 2023): four MultiBody arms, four propellers
with DC motors, revolute rotors and blades, and one PID holding a 5 m setpoint; 7613 equations. The library is
unmodified. My changes are around it: the Modelica Standard Library is passed as one root directory, its
`Modelica.Math` external builtins are rewritten as algorithm bodies (the 0.10.2 runtime cannot call them),
three empty `package.mo` files let the CLI accept the library tree, and a scenario plus a Three.js scene feed
the chassis quaternion and rotor speeds into Rumoca's viewer.

**Before/after and checked result.**
- Before: every MultiBody model compiled in Rumoca but none simulated. After: the motor test and the full
  hover test simulate, and the hover test runs in Rumoca's 3-D viewer at 0.7 to 1.1 times real time.
- The check: Rumoca and OpenModelica agree on the unmodified hover test to 0.22 mm in chassis altitude over
  an 18.5 m swing in the first 4 s, and to 7e-4 on the PID output. Both show the library test's own poorly
  damped loop: the 50 kg chassis sinks 18.5 m, overshoots to 70.7 m, then diverges. After 40 s OpenModelica
  is at 2202.0 m; Rumoca's live viewer showed 2202.3 m at 40.2 s.
- Findings for the Rumoca team: external builtins in `Modelica.Math`, cross-root resolution, the CLI's
  package-layout check, the missing browser bundle in the Windows release binary, and a viewer reset that
  restores the states but not the clock.

**Tool and time.** Claude Code (Claude Fable 5.1, then Claude Opus 5.5 after 11:30 EDT), Rumoca 0.10.2
(Python wheel and Windows CLI), OpenModelica 1.27. About 1 h 30 min wall time including debugging.

**Links.** Folder `C:\GIT\rumoca-drone-library` (public link to follow if published).

## 45-second pitch

"This is our DroneLibrary from the 2023 Modelica conference: a quadrotor built from MultiBody parts, motors,
rotors and blades, seventy-six hundred equations, untouched. Rumoca flattened it right away but would not
simulate it, because its runtime cannot call the standard library's external cosine. Rewriting those
thirteen functions in a copy of the MSL unlocked it, and here is the library's own hover test flying in
Rumoca's 3-D viewer, close to real time, instead of the licensed DLR visualization we normally need. The check:
Rumoca and OpenModelica agree to a fifth of a millimetre on altitude, and both show that this old test's PID
is badly tuned: it sinks, overshoots and diverges. Five Rumoca issues found along the way. Built with Claude
Code in about an hour and a half."
