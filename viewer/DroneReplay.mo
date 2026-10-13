model DroneReplay
  "Replay clock for the viewer: loops t_replay from 0 to t_end. The drone motion itself is a recorded Rumoca run of DroneLibrary.Tests.simpleHoverTest (replay/hover_replay.json), played back by drone_replay_scene.js; nothing is simulated live here."
  parameter Real t_end(unit="s") = 10 "Length of the recorded run";
  Real t_replay(unit="s", start=0, fixed=true) "Replay time";
  discrete output Real loops(start=1, fixed=true) "Number of the current replay";
equation
  der(t_replay) = 1;
  when t_replay >= t_end then
    loops = pre(loops) + 1;
    reinit(t_replay, 0);
  end when;
end DroneReplay;
