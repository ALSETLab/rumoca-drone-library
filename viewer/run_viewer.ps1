# Start the Rumoca 3-D viewer for DroneLibrary.Tests.simpleHoverTest (PowerShell), then open http://localhost:8090
# Compiling the 7613-equation model takes one to two minutes; reload the page once the console prints "Ready".
# Started from C:\GIT\rumoca-web-assets so the release binary finds its browser bundle (packages/rumoca-web).
# Stop with Q in the page or Ctrl+C here.
$rumoca = "C:\GIT\rumoca-web-assets\bin\rumoca.exe"   # Rumoca 0.10.2 Windows CLI (release asset rumoca-windows-x86_64.exe)
Push-Location C:\GIT\rumoca-web-assets
try {
    Start-Process "http://localhost:8090" | Out-Null
    & $rumoca sim -c C:\GIT\rumoca-drone-library\viewer\rumoca-scenario.toml
}
finally {
    Pop-Location
}
