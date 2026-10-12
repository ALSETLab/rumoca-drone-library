"""Build the two Rumoca 0.10.2 source roots this project needs, from installed libraries (originals untouched).

1. msl/msl400_patched/  One root directory holding Modelica/, ModelicaServices/ and Complex/ side by side
   (Rumoca 0.10.2 does not resolve references across separate roots), copied from OpenModelica's
   %APPDATA%/.openmodelica/libraries/{Modelica,ModelicaServices,Complex} 4.0.0+maint.om, with two patches:
     a. ModelicaServices: OpenModelica-specific calls replaced
        OpenModelica.Internal.Architecture.integerMax() -> 2147483647
        OpenModelica.Scripting.uriToFilename(uri)       -> uri
     b. Modelica.Math.{sin,cos,tan,asin,acos,atan,atan2,sinh,cosh,tanh,exp,log,log10,sqrt}:
        body 'external "builtin" y = f(u);' -> 'algorithm y := .f(u);'
        (the 0.10.2 runtime cannot execute external builtins; the leading dot calls Modelica's builtin).
2. libroot/DroneLibrary/  Copy of C:/GIT/Modelica-Drone-3D-FMI/A_Modelica/DroneLibrary (without Resources/),
   plus an empty package.mo in the three folders that lack one (Electrical/Sources/FuelCell,
   Examples/PowerSystem, Visualize/Runs); Rumoca rejects such a tree as a source root (PKG-006).

Run:  C:/GIT/rumoca-rocket-landing/.venv/Scripts/python.exe C:/GIT/rumoca-drone-library/tools/build_rumoca_roots.py
"""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OM_LIBS = Path(os.environ["APPDATA"]) / ".openmodelica" / "libraries"
DRONE_SRC = Path(r"C:\GIT\Modelica-Drone-3D-FMI\A_Modelica\DroneLibrary")
FUNCS = ["sin", "cos", "tan", "asin", "acos", "atan", "atan2", "sinh", "cosh", "tanh", "exp", "log", "log10", "sqrt"]
MISSING_PACKAGES = {
    "Electrical/Sources/FuelCell": ("DroneLibrary.Electrical.Sources", "FuelCell"),
    "Examples/PowerSystem": ("DroneLibrary.Examples", "PowerSystem"),
    "Visualize/Runs": ("DroneLibrary.Visualize", "Runs"),
}


def build_msl(dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    skip = shutil.ignore_patterns("Images", "Data", "C-Sources", "Library", "Scripts")
    for name in ("Modelica", "ModelicaServices", "Complex"):
        shutil.copytree(OM_LIBS / f"{name} 4.0.0+maint.om", dst / name, ignore=skip)
    svc = dst / "ModelicaServices" / "package.mo"
    t = svc.read_text(encoding="utf-8")
    t = t.replace("OpenModelica.Internal.Architecture.integerMax()", "2147483647")
    t = t.replace("OpenModelica.Scripting.uriToFilename(uri)", "uri")
    svc.write_text(t, encoding="utf-8")
    math = dst / "Modelica" / "Math" / "package.mo"
    t = math.read_text(encoding="utf-8")
    pat = re.compile(r'external\s+"builtin"\s+y\s*=\s*(' + "|".join(FUNCS) + r')\(([^)]*)\)\s*;')
    n = len(pat.findall(t))
    math.write_text(pat.sub(lambda m: f"algorithm\n  y := .{m.group(1)}({m.group(2)});", t), encoding="utf-8")
    print(f"MSL root: {dst}  (Modelica.Math bodies patched: {n})")


def build_libroot(dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(DRONE_SRC, dst / "DroneLibrary", ignore=shutil.ignore_patterns("Resources"))
    (dst / "DroneLibrary" / "Resources").mkdir()
    for rel, (within, name) in MISSING_PACKAGES.items():
        (dst / "DroneLibrary" / rel / "package.mo").write_text(
            f'within {within};\npackage {name} "Added for Rumoca: folder had no package.mo"\nend {name};\n', encoding="utf-8")
    print(f"Library root: {dst}  (package.mo added in {len(MISSING_PACKAGES)} folders)")


if __name__ == "__main__":
    build_msl(HERE / "msl" / "msl400_patched")
    build_libroot(HERE / "libroot")
