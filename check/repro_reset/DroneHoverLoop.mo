model DroneHoverLoop
  "DroneLibrary.Tests.simpleHoverTest re-assembled for looping in Rumoca's viewer: identical components, parameters and connections, except that the altitude setpoint ramp runs on a flight clock that restarts with every reset"
  // The library model is not modified. Rumoca 0.10.2's viewer reset (R) restores the states but not the
  // model clock, so the library's Modelica.Blocks.Sources.Ramp (a function of time) would already sit at
  // 5 m after a reset. Here the same ramp (5 m in 0.5 s, from 0) is written on flight_time, a state that
  // starts at 0 and is therefore reset with the others.
  Real flight_time(unit="s", start=0, fixed=true) "Time since the start of the current flight";
  output Real z(unit="m") "Chassis altitude, for the viewer";
  DroneLibrary.Mechanical.Chassis.Variants.droneChassis droneChassis1(m=10);
  inner Modelica.Mechanics.MultiBody.World world(n={0,0,-1});
  Modelica.Mechanics.MultiBody.Parts.Fixed fixed;
  Modelica.Mechanics.MultiBody.Sensors.RelativePosition relativePosition;
  DroneLibrary.Blocks.Routing.RealExtract realExtract;
  Modelica.Blocks.Sources.RealExpression ramp(y = if flight_time < 0.5 then 5*flight_time/0.5 else 5)
    "Same setpoint as the test's Ramp(height=5, duration=0.5), on the flight clock";
  Modelica.Blocks.Continuous.PID PID(
    k=1.5,
    Ti=0.8,
    Td=1,
    initType=Modelica.Blocks.Types.Init.SteadyState);
  Modelica.Blocks.Math.Feedback feedback;
  DroneLibrary.Mechanical.Propeller.Variants.Propeller propellerRev(PropellerGain=1);
  DroneLibrary.Mechanical.Propeller.Variants.Propeller propellerRev1;
  DroneLibrary.Mechanical.Propeller.Variants.Propeller propellerRev3;
  DroneLibrary.Mechanical.Propeller.Variants.Propeller propellerRev2;
equation
  der(flight_time) = 1;
  z = droneChassis1.bodyCylinder.frame_a.r_0[3];
  connect(relativePosition.frame_b, droneChassis1.frame_a3);
  connect(fixed.frame_b, relativePosition.frame_a);
  connect(relativePosition.r_rel, realExtract.u);
  connect(feedback.u1, ramp.y);
  connect(feedback.u2, realExtract.y);
  connect(feedback.y, PID.u);
  connect(propellerRev1.position, propellerRev.position);
  connect(droneChassis1.frame_a1, propellerRev.Airframe);
  connect(propellerRev3.Airframe, droneChassis1.frame_a2);
  connect(propellerRev1.Airframe, droneChassis1.frame_a);
  connect(propellerRev2.Airframe, droneChassis1.frame_a3);
  connect(PID.y, propellerRev3.position);
  connect(propellerRev2.position, propellerRev3.position);
  connect(propellerRev1.position, propellerRev3.position);
end DroneHoverLoop;
