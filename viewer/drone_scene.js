// drone_scene.js -- ALSETLab DroneLibrary quadrotor for the Rumoca sim viewer.
// Pure Three.js geometry, no external assets.  ctx.onInit(api) / ctx.onFrame(api).
// Model world is Forward-Left-Up (Z up); Three.js uses (x3, y3, z3) = (-py, pz, px).

function num(v, d) { const n = Number(v); return Number.isFinite(n) ? n : d; }

ctx.onInit = function (api) {
  const THREE = api.THREE;
  const scene = api.scene;
  const s = api.state;

  scene.background = new THREE.Color(0x9fc5e8);
  scene.fog = new THREE.FogExp2(0x9fc5e8, 0.012);

  const sun = new THREE.DirectionalLight(0xfff4e0, 1.6);
  sun.position.set(6, 12, 4);
  scene.add(sun);
  scene.add(new THREE.HemisphereLight(0xbfdfff, 0x6b8e4e, 0.6));

  // ground: semi-transparent so the airframe stays visible if it sinks below z = 0
  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(400, 400),
    new THREE.MeshStandardMaterial({ color: 0x5f8f4a, roughness: 0.95, transparent: true, opacity: 0.7 })
  );
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -0.01;
  scene.add(ground);
  const grid = new THREE.GridHelper(400, 200, 0xe8f0e0, 0x8fb37a);
  grid.material.transparent = true;
  grid.material.opacity = 0.5;
  scene.add(grid);

  // launch pad marker at the origin
  const pad = new THREE.Mesh(
    new THREE.CircleGeometry(1.0, 32),
    new THREE.MeshStandardMaterial({ color: 0x333333, roughness: 0.9 })
  );
  pad.rotation.x = -Math.PI / 2;
  pad.position.y = 0.002;
  scene.add(pad);

  // quadrotor built from boxes/cylinders.  Group local axes follow the MODEL body
  // frame after the matrix in onFrame: local x = forward, y = up, z = right.
  const quad = new THREE.Group();
  quad.name = "quadrotor";
  scene.add(quad);
  s.quad = quad;

  const bodyMat = new THREE.MeshStandardMaterial({ color: 0xc0392b, roughness: 0.5, metalness: 0.3 });
  const armMat = new THREE.MeshStandardMaterial({ color: 0x2c3e50, roughness: 0.6, metalness: 0.4 });
  const rotorMat = new THREE.MeshStandardMaterial({ color: 0x111111, transparent: true, opacity: 0.55, side: THREE.DoubleSide });
  const motorMat = new THREE.MeshStandardMaterial({ color: 0x7f8c8d, metalness: 0.6, roughness: 0.4 });

  const hub = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.12, 0.34), bodyMat);
  quad.add(hub);
  const battery = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.08, 0.14), armMat);
  battery.position.y = -0.1;
  quad.add(battery);

  // four arms in an X; arm length 0.6 m (chassis BodyShape arms are ~0.6 m)
  const L = 0.6;
  const armDirs = [[1, 1], [-1, 1], [-1, -1], [1, -1]]; // (x3, z3) = (forward, right)
  s.rotors = [];
  armDirs.forEach((d, i) => {
    const ang = Math.atan2(d[1], d[0]);
    const arm = new THREE.Mesh(new THREE.BoxGeometry(L, 0.04, 0.05), armMat);
    arm.position.set(0.5 * L * Math.cos(ang), 0, 0.5 * L * Math.sin(ang));
    arm.rotation.y = -ang;
    quad.add(arm);
    const motor = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.08, 16), motorMat);
    motor.position.set(L * Math.cos(ang), 0.04, L * Math.sin(ang));
    quad.add(motor);
    const rotor = new THREE.Group();
    rotor.position.set(L * Math.cos(ang), 0.09, L * Math.sin(ang));
    const disc = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.26, 0.008, 32), rotorMat);
    rotor.add(disc);
    const blade = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.012, 0.05),
      new THREE.MeshStandardMaterial({ color: i < 2 ? 0x2ecc71 : 0xe74c3c }));
    rotor.add(blade);
    quad.add(rotor);
    s.rotors.push({ group: rotor, sign: (i % 2 === 0) ? 1 : -1 });
  });
  // nose marker (forward = model +x)
  const nose = new THREE.Mesh(new THREE.ConeGeometry(0.05, 0.14, 12), new THREE.MeshStandardMaterial({ color: 0xf1c40f }));
  nose.rotation.z = -Math.PI / 2;
  nose.position.set(0.24, 0.02, 0);
  quad.add(nose);

  // altitude set-point marker (sphere + thin pole) at the ramp output z_ref above the origin
  s.target = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 12),
    new THREE.MeshStandardMaterial({ color: 0xffd700, emissive: 0xaa8800, emissiveIntensity: 0.6 }));
  scene.add(s.target);
  s.pole = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 1, 8),
    new THREE.MeshBasicMaterial({ color: 0xffd700, transparent: true, opacity: 0.5 }));
  scene.add(s.pole);

  // ground shadow disc
  s.shadow = new THREE.Mesh(new THREE.CircleGeometry(0.7, 24),
    new THREE.MeshBasicMaterial({ color: 0x1a2a10, transparent: true, opacity: 0.3 }));
  s.shadow.rotation.x = -Math.PI / 2;
  s.shadow.position.y = 0.004;
  scene.add(s.shadow);

  if (api.cam) { api.cam.dist = 6; api.cam.elev = 0.35; api.cam.angle = -Math.PI / 2 + 0.6; }
};

ctx.onFrame = function (api) {
  const s = api.state;
  const get = api.get;
  const px = num(get("px"), 0), py = num(get("py"), 0), pz = num(get("pz"), 0);
  // MultiBody Q rotates world->body with Q[4] scalar; viewer wants body->world scalar-first.
  const q0 = num(get("q0"), 1);
  const q1 = -num(get("q1n"), 0), q2 = -num(get("q2n"), 0), q3 = -num(get("q3n"), 0);

  const tx = -py, ty = pz, tz = px;

  // DCM from quaternion (body-to-world), same construction as Rumoca's quadrotor_scene.js
  const R11 = 1 - 2 * (q2 * q2 + q3 * q3), R12 = 2 * (q1 * q2 - q0 * q3), R13 = 2 * (q1 * q3 + q0 * q2);
  const R21 = 2 * (q1 * q2 + q0 * q3), R22 = 1 - 2 * (q1 * q1 + q3 * q3), R23 = 2 * (q2 * q3 - q0 * q1);
  const R31 = 2 * (q1 * q3 - q0 * q2), R32 = 2 * (q2 * q3 + q0 * q1), R33 = 1 - 2 * (q1 * q1 + q2 * q2);
  // M_three = A * R_model * A^-1 with A: [x3,y3,z3] = [-y, z, x]
  s.quad.matrix.set(
    R22, -R23, -R21, tx,
    -R32, R33, R31, ty,
    -R12, R13, R11, tz,
    0, 0, 0, 1
  );
  s.quad.matrixAutoUpdate = false;
  s.quad.matrixWorldNeedsUpdate = true;

  // spin the rotors with the revolute joint speeds (rad/s); dt approx 1/60 s per frame
  const om = [get("omega_m1"), get("omega_m2"), get("omega_m3"), get("omega_m4")].map(v => num(v, 0));
  s.rotors.forEach((r, i) => { r.group.rotation.y += r.sign * om[i] / 60; });

  // set-point marker
  const zr = num(get("z_ref"), NaN);
  if (Number.isFinite(zr)) {
    s.target.visible = true; s.pole.visible = true;
    s.target.position.set(0, zr, 0);
    s.pole.scale.y = Math.max(Math.abs(zr), 0.01);
    s.pole.position.set(0, zr / 2, 0);
  } else { s.target.visible = false; s.pole.visible = false; }

  // shadow on the ground
  s.shadow.position.set(tx, 0.004, tz);
  const alt = Math.max(ty, 0.01);
  const sc = Math.max(0.3, 1.0 - alt * 0.05);
  s.shadow.scale.set(sc, sc, 1);
  s.shadow.material.opacity = Math.max(0.05, 0.3 - alt * 0.02);

  // chase camera: orbit target follows the airframe
  if (api.cameraMode === "scene" && api.cam) {
    const c = api.cam;
    c.target.set(tx, ty, tz);
    api.camera.position.set(
      tx + c.dist * Math.sin(c.angle) * Math.cos(c.elev),
      ty + c.dist * Math.sin(c.elev),
      tz + c.dist * Math.cos(c.angle) * Math.cos(c.elev)
    );
    api.camera.lookAt(c.target);
  }
};
