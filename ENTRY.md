# Gallery post: Beyond DroneLibrary Multi-Domain Drone Modeling: Simulating and Flying a MultiBody Quadrotor in 3-D with Rumoca

Additional gallery project (not a second draw entry) for
https://github.com/CogniPilot/rumoca_workshop_amc2026/issues/1.

## Gallery post (paste as a comment)

### Beyond DroneLibrary Multi-Domain Drone Modeling: Simulating and Flying a MultiBody Quadrotor in 3-D with Rumoca

**Name / question.** Luigi Vanfretti, ALSETLab, Rensselaer Polytechnic Institute (an additional gallery project; my draw entry is the rocket landing above). How far does Rumoca 0.10.2 get with our open-source multi-domain drone library, a real `Modelica.Mechanics.MultiBody` quadrotor, and can the library's own hover test fly in Rumoca's 3-D viewer instead of the licensed DLR Visualization library?

**Starting model and authors.** The DroneLibrary in [ALSETLab/Modelica-Drone-3D-FMI](https://github.com/ALSETLab/Modelica-Drone-3D-FMI), from two papers:
- M. Podlaski, L. Vanfretti, H. Nademi and H. Chang, "UAV Dynamic System Modeling and Visualization using Modelica and FMI," Vertical Flight Society 76th Annual Forum, 2020 ([publisher](https://vtol.org/store/product/uav-dynamics-and-electric-power-system-modeling-and-visualization-using-modelica-and-fmi-16289.cfm), [author's copy](https://ecse.rpi.edu/~vanfrl/documents/publications/conference/2020/CP174_Drone_Modelica_and_FMI.pdf)).
- M. Podlaski, L. Vanfretti and D. Winkler, "DroneLibrary: Multi-Domain Drone Modeling in Modelica," 15th International Modelica Conference, Aachen, 2023 ([doi:10.3384/ecp204551](https://doi.org/10.3384/ecp204551), [author's copy](https://sites.ecse.rpi.edu/~vanfrl/documents/publications/conference/2023/CP238_Drone_Library_IMC_2023.pdf)).

I used `DroneLibrary.Tests.simpleHoverTest` unmodified: four MultiBody arms, four propellers with DC motors, revolute rotors and blades, and one PID holding a 5 m setpoint, 7613 equations.

**My change.** Everything is around the library, built by one script: the Modelica Standard Library passed to Rumoca as one root folder, its `Modelica.Math` external builtins rewritten as algorithm bodies (the 0.10.2 runtime cannot call them), and three empty `package.mo` files so the CLI accepts the library tree. A Rumoca scenario and a Three.js scene feed the chassis quaternion and the four rotor speeds into Rumoca's 3-D viewer.

**Before/after and checked result.**
- **Before:** every MultiBody model compiled in Rumoca, but none simulated. **After:** the library's motor test and full hover test simulate, and the hover test flies live in Rumoca's free 3-D viewer at 0.7 to 1.1 times real time.
- **Check:** Rumoca and OpenModelica agree on the unmodified hover test to 0.22 mm in altitude over an 18.5 m swing in the first 4 s, and to 7e-4 on the PID output. Both reproduce the test's poorly damped loop: the 50 kg chassis sinks 18.5 m, overshoots to 70.7 m, then diverges. After 40 s OpenModelica is at 2202.0 m; Rumoca's live viewer showed 2202.3 m.
- **Support status:** 3 of 7 MultiBody models from two ALSETLab libraries simulate; the blockers are documented.
- **For the Rumoca team:** resetting this model fails with an initialization error, and so does a minimal variant with one extra state. I reported it with a reproducer: [CogniPilot/rumoca#430](https://github.com/CogniPilot/rumoca/issues/430).

**Tool and time.** Claude Code (Claude Fable 5.1, then Claude Opus 5.5), Rumoca 0.10.2, OpenModelica 1.27. About 1 h 30 min wall time including debugging, plus the write-up.

**Links.** Rumoca project: https://github.com/ALSETLab/rumoca-drone-library. Models: https://github.com/ALSETLab/Modelica-Drone-3D-FMI. Papers: https://doi.org/10.3384/ecp204551 and the VFS 2020 paper above.
