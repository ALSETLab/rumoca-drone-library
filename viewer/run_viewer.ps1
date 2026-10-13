# Start the Rumoca 3-D viewer for DroneLibrary.Tests.simpleHoverTest (PowerShell), then open http://localhost:8090
# Compiling the 7613-equation model takes one to two minutes; the browser opens by itself once the viewer is up.
# Started from C:\GIT\rumoca-web-assets so the release binary finds its browser bundle (packages/rumoca-web).
# Stop with Q in the page or Ctrl+C here.
$rumoca = "C:\GIT\rumoca-web-assets\bin\rumoca.exe"   # Rumoca 0.10.2 Windows CLI (release asset rumoca-windows-x86_64.exe)
Push-Location C:\GIT\rumoca-web-assets
try {
    # Open the browser only once the viewer answers (compiling can take a minute or two)
    $null = Start-Job -ScriptBlock {
        param($url)
        for ($i = 0; $i -lt 600; $i++) {
            try { Invoke-WebRequest $url -UseBasicParsing -TimeoutSec 2 | Out-Null; Start-Process $url; break }
            catch { Start-Sleep -Seconds 1 }
        }
    } -ArgumentList "http://localhost:8090"
    & $rumoca sim -c C:\GIT\rumoca-drone-library\viewer\rumoca-scenario.toml
}
finally {
    Pop-Location
}
