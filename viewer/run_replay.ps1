# Start the Rumoca 3-D viewer, looping REPLAY of a recorded Rumoca run of DroneLibrary.Tests.simpleHoverTest (PowerShell): http://localhost:8092
# Starts in seconds: the model is only a replay clock; the motion is replay/hover_replay.json (check/record_replay.py).
# Uses the viewer kit in the external/rumoca-web-assets submodule (browser bundle the Rumoca 0.10.2 Windows
# release binary lacks; rumoca.exe is downloaded there on first use). The browser opens by itself.
# Stop with Q in the page or Ctrl+C here.
$kit = Join-Path $PSScriptRoot "..\external\rumoca-web-assets\start_viewer.ps1"
if (-not (Test-Path $kit)) { throw "Viewer kit missing: run .\setup.ps1 (or 'git submodule update --init') in the repository root." }
& $kit -Scenario (Join-Path $PSScriptRoot "rumoca-scenario.replay.toml") -Url "http://localhost:8092"
