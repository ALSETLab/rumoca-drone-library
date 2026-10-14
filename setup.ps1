# One-time setup after cloning (PowerShell, from anywhere):
#   1. fetch the submodules external/Modelica-Drone-3D-FMI and external/rumoca-web-assets,
#   2. create .venv from requirements.txt (Python 3.12),
#   3. build the Rumoca source roots msl/ and libroot/ (needs OpenModelica 1.27 with MSL 4.0.0 installed),
#   4. download the Rumoca 0.10.2 CLI into the viewer kit (SHA-256 checked).
$ErrorActionPreference = "Stop"
Push-Location $PSScriptRoot
try {
    git submodule update --init --recursive
    if (-not (Test-Path ".venv\Scripts\python.exe")) {
        if (Get-Command py -ErrorAction SilentlyContinue) { py -3.12 -m venv .venv } else { python -m venv .venv }
    }
    .venv\Scripts\python.exe -m pip install --upgrade pip
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    .venv\Scripts\python.exe tools\build_rumoca_roots.py
    & .\external\rumoca-web-assets\get_rumoca.ps1
    Write-Host "Setup done. Viewers: .\viewer\run_replay.ps1 (starts in seconds), .\viewer\run_viewer.ps1 (live)"
}
finally {
    Pop-Location
}
