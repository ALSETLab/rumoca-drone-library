#!/usr/bin/env bash
# Start the Rumoca 3-D viewer for DroneLibrary.Tests.simpleHoverTest, then open http://localhost:8090
# Run from C:/GIT/rumoca-web-assets so the release binary finds packages/rumoca-web (viewer page + Three.js bundle).
cd C:/GIT/rumoca-web-assets && exec "$LOCALAPPDATA/rumoca/bin/rumoca.exe" sim -c C:/GIT/rumoca-drone-library/viewer/rumoca-scenario.toml
