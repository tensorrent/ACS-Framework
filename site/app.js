// ACS Framework — Self-contained Documentary Application (ES Module)
// Zero external runtime dependencies; uses vendored three@0.186.1 and katex@0.19.0.

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

function renderMathIn(root = document) {
  if (!window.katex) return;
  for (const el of root.querySelectorAll('[data-math]')) {
    const tex = el.getAttribute('data-math') || '';
    const displayMode = el.getAttribute('data-display') === 'block';
    try {
      window.katex.render(tex, el, { displayMode, throwOnError: false, strict: false });
    } catch {
      el.textContent = tex;
    }
  }
}

function initThemeToggle() {
  const btn = document.getElementById('theme-toggle');
  if (!btn) return;
  const updateLabel = () => {
    const explicit = document.documentElement.dataset.theme;
    const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const isDark = explicit ? explicit === 'dark' : systemDark;
    btn.textContent = isDark ? 'Theme: Dark' : 'Theme: Light';
    btn.setAttribute('aria-label', `Switch color theme (currently ${isDark ? 'dark' : 'light'})`);
  };
  btn.addEventListener('click', () => {
    const explicit = document.documentElement.dataset.theme;
    const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const currentDark = explicit ? explicit === 'dark' : systemDark;
    document.documentElement.dataset.theme = currentDark ? 'light' : 'dark';
    updateLabel();
  });
  updateLabel();
}

function createRenderer(host) {
  const width = Math.max(host.clientWidth || 640, 280);
  const height = Math.max(host.clientHeight || 360, 260);
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setSize(width, height, false);
  renderer.setClearColor(0x070b14, 1);
  return { renderer, width, height };
}

function buildMobiusScene(host) {
  const { renderer, width, height } = createRenderer(host);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 100);
  camera.position.set(0, -4.4, 2.8);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.enableZoom = false;
  controls.target.set(0, 0, 0);

  const ambient = new THREE.AmbientLight(0xdbeafe, 0.85);
  const keyLight = new THREE.DirectionalLight(0x38bdf8, 1.35);
  keyLight.position.set(4, -5, 6);
  const fillLight = new THREE.DirectionalLight(0xf59e0b, 0.75);
  fillLight.position.set(-5, 4, -3);
  scene.add(ambient, keyLight, fillLight);

  const rootGroup = new THREE.Group();
  scene.add(rootGroup);

  let meshObj = null;
  let wireObj = null;
  let markerGroup = new THREE.Group();
  rootGroup.add(markerGroup);

  const R = 1.55;
  const halfW = 0.52;

  function pointOnStrip(u, v, halfTurns) {
    const halfAngle = (halfTurns * u) / 2;
    const r = R + v * Math.cos(halfAngle);
    const x = r * Math.cos(u);
    const y = r * Math.sin(u);
    const z = v * Math.sin(halfAngle);
    return new THREE.Vector3(x, y, z);
  }

  function rebuildGeometry(halfTurns, phasePi) {
    if (meshObj) {
      meshObj.geometry.dispose();
      rootGroup.remove(meshObj);
    }
    if (wireObj) {
      wireObj.geometry.dispose();
      rootGroup.remove(wireObj);
    }
    while (markerGroup.children.length) {
      const c = markerGroup.children.pop();
      if (c.geometry) c.geometry.dispose();
    }

    const uSteps = 120;
    const vSteps = 18;
    const positions = [];
    const colors = [];
    const indices = [];

    for (let i = 0; i <= uSteps; i++) {
      const u = (i / uSteps) * Math.PI * 2;
      for (let j = 0; j <= vSteps; j++) {
        const v = ((j / vSteps) * 2 - 1) * halfW;
        const p = pointOnStrip(u, v, halfTurns);
        positions.push(p.x, p.y, p.z);

        const spin = Math.cos((halfTurns * u) / 2);
        const c1 = new THREE.Color(0x22d3ee);
        const c2 = new THREE.Color(0xf43f5e);
        const mixed = c1.lerp(c2, (1 - spin) * 0.5);
        colors.push(mixed.r, mixed.g, mixed.b);
      }
    }

    for (let i = 0; i < uSteps; i++) {
      for (let j = 0; j < vSteps; j++) {
        const a = i * (vSteps + 1) + j;
        const b = (i + 1) * (vSteps + 1) + j;
        const c = (i + 1) * (vSteps + 1) + (j + 1);
        const d = i * (vSteps + 1) + (j + 1);
        indices.push(a, b, d, b, c, d);
      }
    }

    const geom = new THREE.BufferGeometry();
    geom.setIndex(indices);
    geom.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geom.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    geom.computeVertexNormals();

    const mat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      side: THREE.DoubleSide,
      roughness: 0.35,
      metalness: 0.15,
    });
    meshObj = new THREE.Mesh(geom, mat);
    rootGroup.add(meshObj);

    const wireMat = new THREE.MeshBasicMaterial({
      color: 0x94a3b8,
      wireframe: true,
      transparent: true,
      opacity: 0.16,
    });
    wireObj = new THREE.Mesh(geom.clone(), wireMat);
    rootGroup.add(wireObj);

    // Frame marker at theta = phasePi * pi
    const theta = phasePi * Math.PI;
    const pEdgePos = pointOnStrip(theta, halfW * 0.85, halfTurns);
    const pEdgeNeg = pointOnStrip(theta, -halfW * 0.85, halfTurns);
    const pCenter = pointOnStrip(theta, 0, halfTurns);

    const sphereGeom = new THREE.SphereGeometry(0.085, 16, 16);
    const sPos = new THREE.Mesh(sphereGeom, new THREE.MeshBasicMaterial({ color: 0xfbbf24 }));
    sPos.position.copy(pEdgePos);
    const sNeg = new THREE.Mesh(sphereGeom, new THREE.MeshBasicMaterial({ color: 0xf43f5e }));
    sNeg.position.copy(pEdgeNeg);
    markerGroup.add(sPos, sNeg);

    const rodGeom = new THREE.BufferGeometry().setFromPoints([pEdgeNeg, pCenter, pEdgePos]);
    const rod = new THREE.Line(rodGeom, new THREE.LineBasicMaterial({ color: 0xfbbf24 }));
    markerGroup.add(rod);

    const readout = document.getElementById('readout-mobius');
    if (readout) {
      const holonomy = Math.cos((halfTurns * theta) / 2);
      const sheet = holonomy >= 0 ? '+1 (Primary Sheet)' : '-1 (Spinor Inverted Sheet)';
      const topology = halfTurns % 2 === 1 ? 'Non-orientable Z_2 double cover (4π period)' : 'Orientable cylinder (2π period)';
      readout.textContent = `k = ${halfTurns} half-turn(s) | θ = ${phasePi.toFixed(2)}π | cos(kθ/2) = ${holonomy.toFixed(3)} | Holonomy: ${sheet} | ${topology}`;
    }
  }

  const twistInput = document.getElementById('ctrl-mobius-twist');
  const phaseInput = document.getElementById('ctrl-mobius-phase');
  const updateFromControls = () => {
    const k = Number(twistInput?.value ?? 1);
    const ph = Number(phaseInput?.value ?? 0.65);
    rebuildGeometry(k, ph);
    controls.update();
    renderer.render(scene, camera);
  };

  twistInput?.addEventListener('input', updateFromControls);
  phaseInput?.addEventListener('input', updateFromControls);
  rebuildGeometry(Number(twistInput?.value ?? 1), Number(phaseInput?.value ?? 0.65));

  return { renderer, scene, camera, controls, rootGroup };
}

function buildPalatiniScene(host) {
  const { renderer, width, height } = createRenderer(host);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 100);
  camera.position.set(0, -4.8, 2.7);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.enableZoom = false;

  const ambient = new THREE.AmbientLight(0xe2e8f0, 0.9);
  const dirLight = new THREE.DirectionalLight(0x34d399, 1.3);
  dirLight.position.set(3, -4, 6);
  scene.add(ambient, dirLight);

  const rootGroup = new THREE.Group();
  scene.add(rootGroup);

  function rebuildFlow(efolds, logXi) {
    while (rootGroup.children.length) {
      const c = rootGroup.children.pop();
      if (c.geometry) c.geometry.dispose();
    }

    // 3D Potential trough + phase space trajectories converging to the attractor spine
    const gridX = 64;
    const gridY = 36;
    const positions = [];
    const colors = [];
    const indices = [];

    for (let i = 0; i <= gridX; i++) {
      const x = (i / gridX) * 4.4 - 2.2; // field coordinate phi
      const phi = i / gridX;
      for (let j = 0; j <= gridY; j++) {
        const y = (j / gridY) * 2.8 - 1.4; // velocity defect dphi/dN - attractor
        const plateau = Math.pow(1 - Math.exp(-2.6 * (phi + 0.08)), 2);
        const z = -0.75 + 1.15 * plateau + 0.38 * y * y;
        positions.push(x, y, z);

        const cLow = new THREE.Color(0x0ea5e9);
        const cHigh = new THREE.Color(0x10b981);
        const c = cLow.lerp(cHigh, Math.min(1, Math.max(0, plateau)));
        colors.push(c.r, c.g, c.b);
      }
    }

    for (let i = 0; i < gridX; i++) {
      for (let j = 0; j < gridY; j++) {
        const a = i * (gridY + 1) + j;
        const b = (i + 1) * (gridY + 1) + j;
        const c = (i + 1) * (gridY + 1) + (j + 1);
        const d = i * (gridY + 1) + (j + 1);
        indices.push(a, b, d, b, c, d);
      }
    }

    const surfGeom = new THREE.BufferGeometry();
    surfGeom.setIndex(indices);
    surfGeom.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    surfGeom.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    surfGeom.computeVertexNormals();

    const surfMesh = new THREE.Mesh(
      surfGeom,
      new THREE.MeshStandardMaterial({
        vertexColors: true,
        side: THREE.DoubleSide,
        roughness: 0.45,
        metalness: 0.1,
        transparent: true,
        opacity: 0.82,
      })
    );
    rootGroup.add(surfMesh);

    // Attractor curve along y = 0
    const spinePts = [];
    for (let i = 0; i <= 80; i++) {
      const t = i / 80;
      const x = t * 4.4 - 2.2;
      const plateau = Math.pow(1 - Math.exp(-2.6 * (t + 0.08)), 2);
      const z = -0.72 + 1.15 * plateau;
      spinePts.push(new THREE.Vector3(x, 0, z));
    }
    const spineLine = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints(spinePts),
      new THREE.LineBasicMaterial({ color: 0xfbbf24 })
    );
    rootGroup.add(spineLine);

    // Marker for chosen e-fold N
    const normN = (efolds - 45) / (68 - 45);
    const xN = -1.6 + normN * 3.1;
    const tN = (xN + 2.2) / 4.4;
    const zN = -0.7 + 1.15 * Math.pow(1 - Math.exp(-2.6 * (tN + 0.08)), 2);
    const marker = new THREE.Mesh(
      new THREE.SphereGeometry(0.1, 16, 16),
      new THREE.MeshBasicMaterial({ color: 0xf43f5e })
    );
    marker.position.set(xN, 0, zN);
    rootGroup.add(marker);

    const readout = document.getElementById('readout-palatini');
    if (readout) {
      const xi = Math.pow(10, logXi);
      const ns = 1 - 2 / efolds;
      const rMetric = 12 / (efolds * efolds);
      const rPalatini = 2 / (xi * efolds * efolds);
      readout.textContent = `N = ${efolds} e-folds | n_s = ${ns.toFixed(4)} | r_R2 = ${rMetric.toFixed(4)} | r_Palatini(ξ=10^${logXi.toFixed(1)}) = ${rPalatini.toExponential(2)} | Tracker: φ^(-2)`;
    }
  }

  const efoldsInput = document.getElementById('ctrl-palatini-efolds');
  const xiInput = document.getElementById('ctrl-palatini-xi');
  const update = () => {
    rebuildFlow(Number(efoldsInput?.value ?? 55), Number(xiInput?.value ?? 3.5));
    controls.update();
    renderer.render(scene, camera);
  };
  efoldsInput?.addEventListener('input', update);
  xiInput?.addEventListener('input', update);
  rebuildFlow(Number(efoldsInput?.value ?? 55), Number(xiInput?.value ?? 3.5));

  return { renderer, scene, camera, controls, rootGroup };
}

function buildCriticalSeamScene(host) {
  const { renderer, width, height } = createRenderer(host);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 100);
  camera.position.set(0, -4.6, 2.9);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.enableZoom = false;

  const ambient = new THREE.AmbientLight(0xe2e8f0, 0.85);
  const key = new THREE.DirectionalLight(0xa78bfa, 1.3);
  key.position.set(3, -4, 6);
  scene.add(ambient, key);

  const rootGroup = new THREE.Group();
  scene.add(rootGroup);

  const zeros = [14.1347, 21.0220, 25.0108, 30.4249];

  function discriminantAt(sigma, t) {
    const sym = Math.pow(sigma - 0.5, 2);
    let trough = 1.0;
    for (const tz of zeros) {
      trough *= 1 - 0.82 * Math.exp(-Math.pow((t - tz) / 1.35, 2) - 18 * sym);
    }
    return (trough - 0.45) + 2.4 * sym;
  }

  function rebuildSeam(sigmaProbe, reliefScale) {
    while (rootGroup.children.length) {
      const c = rootGroup.children.pop();
      if (c.geometry) c.geometry.dispose();
    }

    const sSteps = 48;
    const tSteps = 84;
    const positions = [];
    const colors = [];
    const indices = [];

    for (let i = 0; i <= tSteps; i++) {
      const u = i / tSteps;
      const tVal = 12 + u * 20; // t in [12, 32]
      const x = u * 4.4 - 2.2;
      for (let j = 0; j <= sSteps; j++) {
        const v = j / sSteps;
        const sig = 0.1 + v * 0.8; // sigma in [0.1, 0.9]
        const y = (sig - 0.5) * 3.4;
        const dVal = discriminantAt(sig, tVal);
        const z = dVal * 0.72 * reliefScale;
        positions.push(x, y, z);

        const distSeam = Math.abs(sig - 0.5) / 0.4;
        const cSeam = new THREE.Color(0x22d3ee);
        const cWing = new THREE.Color(0xa855f7);
        const col = cSeam.lerp(cWing, Math.min(1, distSeam));
        colors.push(col.r, col.g, col.b);
      }
    }

    for (let i = 0; i < tSteps; i++) {
      for (let j = 0; j < sSteps; j++) {
        const a = i * (sSteps + 1) + j;
        const b = (i + 1) * (sSteps + 1) + j;
        const c = (i + 1) * (sSteps + 1) + (j + 1);
        const d = i * (sSteps + 1) + (j + 1);
        indices.push(a, b, d, b, c, d);
      }
    }

    const geom = new THREE.BufferGeometry();
    geom.setIndex(indices);
    geom.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geom.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    geom.computeVertexNormals();

    const mesh = new THREE.Mesh(
      geom,
      new THREE.MeshStandardMaterial({
        vertexColors: true,
        side: THREE.DoubleSide,
        roughness: 0.4,
        metalness: 0.15,
      })
    );
    rootGroup.add(mesh);

    // Probe curve at sigma = sigmaProbe
    const probePts = [];
    for (let i = 0; i <= tSteps; i++) {
      const u = i / tSteps;
      const tVal = 12 + u * 20;
      const x = u * 4.4 - 2.2;
      const y = (sigmaProbe - 0.5) * 3.4;
      const z = discriminantAt(sigmaProbe, tVal) * 0.72 * reliefScale + 0.03;
      probePts.push(new THREE.Vector3(x, y, z));
    }
    const probeLine = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints(probePts),
      new THREE.LineBasicMaterial({ color: 0xfbbf24 })
    );
    rootGroup.add(probeLine);

    const readout = document.getElementById('readout-seam');
    if (readout) {
      const defect = Math.abs(sigmaProbe - 0.5);
      const status = defect < 0.015 ? 'On Critical Seam (σ = 1/2, ξ(s)=ξ(1-s) self-dual)' : `Off-axis slice |σ - 1/2| = ${defect.toFixed(3)} (reflection-paired with ${(1 - sigmaProbe).toFixed(2)})`;
      readout.textContent = `Probe σ = ${sigmaProbe.toFixed(2)} | ${status} | Tier: T3 Numerical / T4 Global Closure Falsified`;
    }
  }

  const sigmaInput = document.getElementById('ctrl-seam-sigma');
  const reliefInput = document.getElementById('ctrl-seam-relief');
  const update = () => {
    rebuildSeam(Number(sigmaInput?.value ?? 0.5), Number(reliefInput?.value ?? 1.0));
    controls.update();
    renderer.render(scene, camera);
  };
  sigmaInput?.addEventListener('input', update);
  reliefInput?.addEventListener('input', update);
  rebuildSeam(Number(sigmaInput?.value ?? 0.5), Number(reliefInput?.value ?? 1.0));

  return { renderer, scene, camera, controls, rootGroup };
}

function initScenes() {
  const builders = {
    'mobius-framing': buildMobiusScene,
    'palatini-attractor': buildPalatiniScene,
    'critical-seam': buildCriticalSeamScene,
  };

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const activeScenes = [];

  for (const host of document.querySelectorAll('[data-scene]')) {
    const id = host.dataset.scene;
    const builder = builders[id];
    if (!builder) {
      host.dataset.state = 'fallback';
      continue;
    }
    try {
      const instance = builder(host);
      host.prepend(instance.renderer.domElement);
      instance.controls.update();
      instance.renderer.render(instance.scene, instance.camera);
      host.dataset.state = 'running';
      activeScenes.push({ host, ...instance });

      const ro = new ResizeObserver(() => {
        const w = Math.max(host.clientWidth || 640, 280);
        const h = Math.max(host.clientHeight || 360, 260);
        instance.camera.aspect = w / h;
        instance.camera.updateProjectionMatrix();
        instance.renderer.setSize(w, h, false);
        instance.renderer.render(instance.scene, instance.camera);
      });
      ro.observe(host);
    } catch {
      host.dataset.state = 'fallback';
    }
  }

  if (!reducedMotion && activeScenes.length > 0) {
    const tick = () => {
      for (const s of activeScenes) {
        s.rootGroup.rotation.z += 0.0018;
        s.controls.update();
        s.renderer.render(s.scene, s.camera);
      }
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }
}

async function initDataExplorers() {
  try {
    const [claimsRes, catalogRes, timelineRes] = await Promise.all([
      fetch('./data/claims.json'),
      fetch('./data/catalog.json'),
      fetch('./data/timeline.json'),
    ]);
    const claimsData = await claimsRes.json();
    const catalogData = await catalogRes.json();
    const timelineData = await timelineRes.json();

    renderClaimsExplorer(claimsData.claims || []);
    renderCatalogExplorer(catalogData.papers || []);
    renderTimeline(timelineData.events || []);
  } catch (err) {
    console.warn('Data explorer initialization warning:', err);
  }
}

function renderClaimsExplorer(claims) {
  const grid = document.getElementById('claims-grid');
  const countEl = document.getElementById('claims-count');
  const searchInput = document.getElementById('claims-search');
  const pillButtons = [...document.querySelectorAll('[data-tier-filter]')];
  if (!grid) return;

  let activeTier = 'ALL';
  let query = '';

  const update = () => {
    const filtered = claims.filter(c => {
      const matchTier = activeTier === 'ALL' || c.tier === activeTier;
      const hay = `${c.id} ${c.claim} ${c.domain} ${c.metric} ${c.scope} ${c.axis}`.toLowerCase();
      const matchQuery = !query || hay.includes(query);
      return matchTier && matchQuery;
    });

    if (countEl) {
      countEl.textContent = `Showing ${filtered.length} of ${claims.length} audited claims`;
    }

    grid.innerHTML = filtered
      .map(
        c => `
      <article class="claim-card" data-tier="${c.tier}">
        <div class="claim-meta">
          <span class="tier-badge tier-${c.tier}">${c.tier} · ${c.axis}</span>
          <span class="claim-id">${c.id} · ${c.domain}</span>
        </div>
        <h3 class="claim-title">${c.claim}</h3>
        <div class="equation-block mono">${c.metric}</div>
        <p class="claim-summary">${c.scope}</p>
        <div class="claim-footer">
          <span>${c.script}</span>
          <div style="display:flex;gap:0.4rem;">
            <a href="${c.pdf}" class="btn-link primary">PDF</a>
            <a href="${c.tex}" class="btn-link">LaTeX</a>
          </div>
        </div>
      </article>
    `
      )
      .join('');
  };

  for (const btn of pillButtons) {
    btn.addEventListener('click', () => {
      for (const b of pillButtons) b.classList.remove('active');
      btn.classList.add('active');
      activeTier = btn.getAttribute('data-tier-filter') || 'ALL';
      update();
    });
  }

  searchInput?.addEventListener('input', e => {
    query = (e.target.value || '').trim().toLowerCase();
    update();
  });

  update();
}

function renderCatalogExplorer(papers) {
  const grid = document.getElementById('catalog-grid');
  const countEl = document.getElementById('catalog-count');
  const searchInput = document.getElementById('catalog-search');
  const groupButtons = [...document.querySelectorAll('[data-group-filter]')];
  if (!grid) return;

  let activeGroup = 'ALL';
  let query = '';

  const update = () => {
    const filtered = papers.filter(p => {
      const matchGroup = activeGroup === 'ALL' || p.group === activeGroup;
      const hay = `${p.label} ${p.group} ${p.summary} ${p.pdf} ${p.source}`.toLowerCase();
      const matchQuery = !query || hay.includes(query);
      return matchGroup && matchQuery;
    });

    if (countEl) {
      countEl.textContent = `Showing ${filtered.length} of ${papers.length} canonical manuscripts`;
    }

    grid.innerHTML = filtered
      .map(
        p => `
      <article class="paper-card" data-group="${p.group}">
        <div class="paper-top">
          <span class="paper-group-tag">${p.group}</span>
        </div>
        <h3 class="paper-title">${p.label}</h3>
        <p class="paper-summary">${p.summary}</p>
        <div class="paper-links">
          <a class="btn-link primary" href="${p.pdf}">PDF Manuscript</a>
          <a class="btn-link" href="${p.source}">LaTeX Source (.tex)</a>
        </div>
      </article>
    `
      )
      .join('');
  };

  for (const btn of groupButtons) {
    btn.addEventListener('click', () => {
      for (const b of groupButtons) b.classList.remove('active');
      btn.classList.add('active');
      activeGroup = btn.getAttribute('data-group-filter') || 'ALL';
      update();
    });
  }

  searchInput?.addEventListener('input', e => {
    query = (e.target.value || '').trim().toLowerCase();
    update();
  });

  update();
}

function renderTimeline(events) {
  const container = document.getElementById('timeline-list');
  if (!container) return;
  container.innerHTML = events
    .map(
      ev => `
    <article class="timeline-step">
      <div class="timeline-period">${ev.date} · ${ev.phase}</div>
      <h3 class="timeline-title">${ev.title}</h3>
      <p class="timeline-summary">${ev.detail}</p>
      <div class="paper-links">
        <a class="btn-link primary" href="${ev.pdf}">Primary PDF</a>
        <a class="btn-link" href="${ev.tex}">LaTeX</a>
      </div>
    </article>
  `
    )
    .join('');
}

window.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  renderMathIn(document);
  initScenes();
  initDataExplorers();
});
