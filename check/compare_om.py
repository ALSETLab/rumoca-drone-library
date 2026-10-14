"""Rumoca 0.10.2 vs OpenModelica 1.27 on the untouched DroneLibrary.Tests.simpleHoverTest.

Rumoca: native simulator, MSL 4.0.0 single root with the Modelica.Math builtin work-around.
OpenModelica: dassl, tol 1e-6, MSL as installed (check/om/om_simpleHoverTest.mos).
"""
import csv, json, time
from pathlib import Path
import numpy as np
import rumoca as rum

HERE = Path(__file__).resolve().parent
ROOT_MSL = str(HERE.parent / "msl" / "msl400_patched")  # built by tools/build_rumoca_roots.py
MODEL_FILE = str(HERE.parent / "libroot" / "DroneLibrary" / "Tests" / "simpleHoverTest.mo")
T_END = 4.0
Z = "droneChassis1.bodyCylinder.frame_a.r_0[3]"
SIG = [Z, "PID.y", "propellerRev.rotor3_1.revolute.w", "ramp.y"]

t0 = time.perf_counter()
m = rum.Session(roots=[ROOT_MSL]).load(MODEL_FILE, model="DroneLibrary.Tests.simpleHoverTest")
t_compile = time.perf_counter() - t0
t0 = time.perf_counter()
r = m.simulate(T_END, dt=0.01)
t_sim = time.perf_counter() - t0
tr = np.asarray(r.time)

rows = list(csv.reader(open(HERE / "om" / "om_simpleHoverTest_res.csv")))
h = rows[0]; data = np.array([[float(x) for x in row] for row in rows[1:] if row])
om = {n: data[:, i] for i, n in enumerate(h)}
grid = np.arange(0.0, T_END + 1e-9, 0.01)
out = {"rumoca_version": rum.version(), "t_end_s": T_END, "rumoca_compile_s": round(t_compile, 2),
       "rumoca_simulate_s": round(t_sim, 2), "rumoca_points": int(len(tr)), "signals": {}}
for s in SIG:
    a = np.interp(grid, tr, np.asarray(r[s], dtype=float)); b = np.interp(grid, om["time"], om[s])
    rng = float(np.ptp(b)) or 1.0
    out["signals"][s] = {"max_abs_diff": float(np.max(np.abs(a - b))), "range": rng,
                         "max_rel_to_range": float(np.max(np.abs(a - b)) / rng),
                         "rumoca_at_t_end": float(a[-1]), "om_at_t_end": float(b[-1])}
for tt in [1.0, 2.0, 3.0, 4.0]:
    out[f"z_at_{tt:g}s"] = {"rumoca": float(np.interp(tt, tr, np.asarray(r[Z]))), "om": float(np.interp(tt, om["time"], om[Z]))}
out["om_z_min_m_over_10s"] = float(om[Z].min()); out["om_z_max_m_over_10s"] = float(om[Z].max())
(HERE / "compare_om.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(2, 1, figsize=(9, 6), sharex=True, layout="constrained")
ax[0].plot(om["time"], om[Z], color="#d65a31", lw=2, label="OpenModelica 1.27 (dassl), 10 s")
ax[0].plot(tr, r[Z], "--", color="#007c91", lw=2, label=f"Rumoca 0.10.2 native, {T_END:g} s")
ax[0].plot(om["time"], om["ramp.y"], ":", color="gray", label="altitude setpoint (ramp to 5 m)")
ax[0].set_ylabel("chassis altitude [m]"); ax[0].legend(fontsize=9); ax[0].grid(alpha=0.2)
ax[1].plot(om["time"], om["PID.y"], color="#d65a31", lw=2, label="OpenModelica")
ax[1].plot(tr, r["PID.y"], "--", color="#007c91", lw=2, label="Rumoca")
ax[1].set_ylabel("PID output (motor current)"); ax[1].set_xlabel("time [s]"); ax[1].legend(fontsize=9); ax[1].grid(alpha=0.2)
fig.suptitle("DroneLibrary.Tests.simpleHoverTest (7613 equations, MultiBody): Rumoca vs OpenModelica")
fig.savefig(HERE / "compare_om.png", dpi=130)
print(json.dumps(out, indent=2))
