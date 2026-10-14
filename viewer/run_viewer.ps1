# Start the Rumoca 3-D viewer, LIVE simulation of DroneLibrary.Tests.simpleHoverTest (PowerShell): http://localhost:8090
# Compiling the 7613-equation model takes one to two minutes.
# Uses the viewer kit in the external/rumoca-web-assets submodule (browser bundle the Rumoca 0.10.2 Windows
# release binary lacks; rumoca.exe is downloaded there on first use). The browser opens by itself.
# Needs the source roots msl/ and libroot/ (built by setup.ps1). Stop with Q in the page or Ctrl+C here.
$kit = Join-Path $PSScriptRoot "..\external\rumoca-web-assets\start_viewer.ps1"
if (-not (Test-Path $kit)) { throw "Viewer kit missing: run .\setup.ps1 (or 'git submodule update --init') in the repository root." }
& $kit -Scenario (Join-Path $PSScriptRoot "rumoca-scenario.toml") -Url "http://localhost:8090"
