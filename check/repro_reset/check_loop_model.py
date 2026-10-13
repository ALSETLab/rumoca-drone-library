"""DroneHoverLoop (viewer/DroneHoverLoop.mo) must reproduce DroneLibrary.Tests.simpleHoverTest: compare its
first 4 s in Rumoca with the OpenModelica result of the original test (check/om/om_simpleHoverTest_res.csv)."""
import csv, json, time
from pathlib import Path
import numpy as np
import rumoca as rum

HERE = Path(__file__).resolve().parent
ROOTS = [str(HERE.parents[1] / "msl" / "msl400_patched"), str(HERE.parents[1] / "libroot")]
t0 = time.perf_counter()
m = rum.Session(roots=ROOTS).load(str(HERE / "DroneHoverLoop.mo"), model="DroneHoverLoop")
tc = time.perf_counter() - t0
t0 = time.perf_counter()
r = m.simulate(4.0, dt=0.01)
ts = time.perf_counter() - t0
rows = list(csv.reader(open(HERE.parent / "om" / "om_simpleHoverTest_res.csv")))
h = rows[0]; d = np.array([[float(x) for x in row] for row in rows[1:] if row]); om = {n: d[:, i] for i, n in enumerate(h)}
g = np.arange(0, 4.0 + 1e-9, 0.01)
out = {"model": "DroneHoverLoop", "compile_s": round(tc, 1), "simulate_4s_s": round(ts, 1)}
for ours, ref in [("z", "droneChassis1.bodyCylinder.frame_a.r_0[3]"), ("PID.y", "PID.y"), ("ramp.y", "ramp.y")]:
    a = np.interp(g, np.asarray(r.time), np.asarray(r[ours], dtype=float)); b = np.interp(g, om["time"], om[ref])
    out[ours] = {"max_abs_diff_vs_OM_original_test": float(np.max(np.abs(a - b))), "range": float(np.ptp(b))}
out["flight_time_end"] = float(np.asarray(r["flight_time"])[-1])
(HERE / "check_loop_model.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps(out, indent=2))
