"""Record one Rumoca 0.10.2 run of the unmodified DroneLibrary.Tests.simpleHoverTest (10 s) for the viewer replay.
Writes viewer/replay/hover_replay.json with the same signal names the live viewer uses."""
import json, time
from pathlib import Path
import numpy as np
import rumoca as rum

ROOT = Path(__file__).resolve().parents[1]
ROOTS = [str(ROOT / "msl" / "msl400_patched"), str(ROOT / "libroot")]
T_END, DT = 10.0, 0.02
SIG = {
    "px": "droneChassis1.bodyCylinder.frame_a.r_0[1]", "py": "droneChassis1.bodyCylinder.frame_a.r_0[2]",
    "pz": "droneChassis1.bodyCylinder.frame_a.r_0[3]",
    "q0": "droneChassis1.bodyCylinder.body.Q[4]", "q1n": "droneChassis1.bodyCylinder.body.Q[1]",
    "q2n": "droneChassis1.bodyCylinder.body.Q[2]", "q3n": "droneChassis1.bodyCylinder.body.Q[3]",
    "omega_m1": "propellerRev.rotor3_1.revolute.w", "omega_m2": "propellerRev1.rotor3_1.revolute.w",
    "omega_m3": "propellerRev2.rotor3_1.revolute.w", "omega_m4": "propellerRev3.rotor3_1.revolute.w",
    "z_ref": "ramp.y", "u_pid": "PID.y",
}
t0 = time.perf_counter()
m = rum.Session(roots=ROOTS).load(str(ROOT / "libroot" / "DroneLibrary" / "Tests" / "simpleHoverTest.mo"),
                                  model="DroneLibrary.Tests.simpleHoverTest")
r = m.simulate(T_END, dt=DT)
wall = time.perf_counter() - t0
grid = np.round(np.arange(0.0, T_END + 1e-9, DT), 6)
tr = np.asarray(r.time, dtype=float)
data = {"source": "Rumoca " + rum.version() + " native simulation of DroneLibrary.Tests.simpleHoverTest (unmodified)",
        "t_end": T_END, "dt": DT, "wall_seconds": round(wall, 1), "t": grid.tolist(), "signals": {}}
for k, name in SIG.items():
    data["signals"][k] = np.round(np.interp(grid, tr, np.asarray(r[name], dtype=float)), 6).tolist()
out = ROOT / "viewer" / "replay" / "hover_replay.json"
out.write_text(json.dumps(data), encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size/1024:.0f} kB), {len(grid)} samples, wall {wall:.0f} s; "
      f"z(10s)={data['signals']['pz'][-1]:.2f} m, z_min={min(data['signals']['pz']):.2f} m")
