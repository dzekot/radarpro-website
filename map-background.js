(function () {
  const canvas = document.getElementById('map-bg');
  if (!canvas) return;

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isMobile = window.matchMedia('(max-width: 640px)').matches;
  const isCoarse = window.matchMedia('(pointer: coarse)').matches;

  const COLORS = {
    radar: '#ff2e63',
    eds: '#00c7ff',
    corridor: 'rgba(0, 199, 255, 0.55)',
    corridorGlow: 'rgba(0, 199, 255, 0.12)',
    grid: 'rgba(255, 255, 255, 0.03)',
  };

  let data = null;
  let width = 0;
  let height = 0;
  let dpr = 1;
  let rafId = 0;
  let startTime = performance.now();

  const view = {
    panX: 0,
    panY: 0,
    scale: 1,
    targetPanX: 0,
    targetPanY: 0,
    dragPanX: 0,
    dragPanY: 0,
  };

  const pointer = { x: 0.5, y: 0.5 };
  let dragging = false;
  let dragStart = { x: 0, y: 0, panX: 0, panY: 0 };

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, isMobile ? 1.5 : 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.floor(width * dpr);
    canvas.height = Math.floor(height * dpr);
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
  }

  function project(lon, lat, bounds, layout) {
    const nx = (lon - bounds.minLon) / (bounds.maxLon - bounds.minLon);
    const ny = (bounds.maxLat - lat) / (bounds.maxLat - bounds.minLat);
    const x = layout.offsetX + nx * layout.mapW * layout.fitScale;
    const y = layout.offsetY + ny * layout.mapH * layout.fitScale;
    return [
      (x + view.panX + view.dragPanX) * view.scale,
      (y + view.panY + view.dragPanY) * view.scale,
    ];
  }

  function computeLayout(bounds) {
    const pad = isMobile ? 48 : 80;
    const aspect = (bounds.maxLon - bounds.minLon) / (bounds.maxLat - bounds.minLat);
    let mapW = width - pad * 2;
    let mapH = mapW / aspect;
    if (mapH > height - pad * 2) {
      mapH = height - pad * 2;
      mapW = mapH * aspect;
    }
    const fitScale = isMobile ? 1.08 : 1.18;
    return {
      mapW,
      mapH,
      fitScale,
      offsetX: (width - mapW * fitScale) / 2,
      offsetY: (height - mapH * fitScale) / 2,
    };
  }

  function sliceData(source) {
    if (!source || !isMobile) return source;
    return {
      ...source,
      radars: source.radars.slice(0, 320),
      eds: source.eds.slice(0, 180),
      corridors: source.corridors.slice(0, 70),
    };
  }

  function drawGrid(ctx, bounds, layout) {
    ctx.strokeStyle = COLORS.grid;
    ctx.lineWidth = 1;
    const steps = isMobile ? 4 : 6;
    for (let i = 1; i < steps; i++) {
      const lon = bounds.minLon + ((bounds.maxLon - bounds.minLon) * i) / steps;
      const lat = bounds.minLat + ((bounds.maxLat - bounds.minLat) * i) / steps;
      const top = project(lon, bounds.maxLat, bounds, layout);
      const bottom = project(lon, bounds.minLat, bounds, layout);
      const left = project(bounds.minLon, lat, bounds, layout);
      const right = project(bounds.maxLon, lat, bounds, layout);
      ctx.beginPath();
      ctx.moveTo(top[0] * dpr, top[1] * dpr);
      ctx.lineTo(bottom[0] * dpr, bottom[1] * dpr);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(left[0] * dpr, left[1] * dpr);
      ctx.lineTo(right[0] * dpr, right[1] * dpr);
      ctx.stroke();
    }
  }

  function drawCorridors(ctx, corridors, bounds, layout) {
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    for (const path of corridors) {
      if (path.length < 2) continue;
      ctx.beginPath();
      const first = project(path[0][0], path[0][1], bounds, layout);
      ctx.moveTo(first[0] * dpr, first[1] * dpr);
      for (let i = 1; i < path.length; i++) {
        const pt = project(path[i][0], path[i][1], bounds, layout);
        ctx.lineTo(pt[0] * dpr, pt[1] * dpr);
      }
      ctx.strokeStyle = COLORS.corridorGlow;
      ctx.lineWidth = 5 * dpr;
      ctx.stroke();
      ctx.strokeStyle = COLORS.corridor;
      ctx.lineWidth = 1.4 * dpr;
      ctx.stroke();
    }
  }

  function drawPoints(ctx, points, color, radius, pulsePhase, bounds, layout) {
    for (let i = 0; i < points.length; i++) {
      const [lon, lat] = points[i];
      const [x, y] = project(lon, lat, bounds, layout);
      const px = x * dpr;
      const py = y * dpr;
      const pulse = prefersReducedMotion ? 1 : 1 + Math.sin(pulsePhase + i * 0.17) * 0.15;
      const r = radius * pulse * dpr;
      ctx.beginPath();
      ctx.arc(px, py, r * 2.4, 0, Math.PI * 2);
      ctx.fillStyle = color === COLORS.radar ? 'rgba(255, 46, 99, 0.1)' : 'rgba(0, 199, 255, 0.1)';
      ctx.fill();
      ctx.beginPath();
      ctx.arc(px, py, r, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();
    }
  }

  function render(now) {
    if (!data) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const elapsed = (now - startTime) / 1000;
    const bounds = data.bounds;
    const layout = computeLayout(bounds);

    if (!prefersReducedMotion) {
      view.targetPanX = Math.sin(elapsed * 0.08) * (isMobile ? 6 : 14);
      view.targetPanY = Math.cos(elapsed * 0.06) * (isMobile ? 4 : 10);
      if (!isCoarse && !dragging) {
        view.targetPanX += (pointer.x - 0.5) * (isMobile ? 8 : 22);
        view.targetPanY += (pointer.y - 0.5) * (isMobile ? 6 : 16);
      }
      const lerp = dragging ? 0.35 : 0.04;
      view.panX += (view.targetPanX - view.panX) * lerp;
      view.panY += (view.targetPanY - view.panY) * lerp;
    }

    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawGrid(ctx, bounds, layout);
    drawCorridors(ctx, data.corridors, bounds, layout);
    drawPoints(ctx, data.radars, COLORS.radar, isMobile ? 1.1 : 1.4, elapsed * 1.6, bounds, layout);
    drawPoints(ctx, data.eds, COLORS.eds, isMobile ? 1.3 : 1.7, elapsed * 1.2 + 1.5, bounds, layout);

    if (!prefersReducedMotion) rafId = requestAnimationFrame(render);
  }

  function onPointerMove(event) {
    pointer.x = event.clientX / width;
    pointer.y = event.clientY / height;
    if (dragging && !isCoarse && !prefersReducedMotion) {
      const dx = event.clientX - dragStart.x;
      const dy = event.clientY - dragStart.y;
      view.dragPanX = clamp(dragStart.panX + dx * 0.35, -40, 40);
      view.dragPanY = clamp(dragStart.panY + dy * 0.35, -30, 30);
    }
  }

  function onPointerDown(event) {
    if (isCoarse || prefersReducedMotion || event.button !== 0) return;
    if (event.target.closest('a, button, input, textarea, select')) return;
    dragging = true;
    dragStart = { x: event.clientX, y: event.clientY, panX: view.dragPanX, panY: view.dragPanY };
    canvas.classList.add('is-dragging');
  }

  function onPointerUp() {
    dragging = false;
    canvas.classList.remove('is-dragging');
  }

  window.addEventListener('resize', () => {
    resize();
    if (prefersReducedMotion && data) render(performance.now());
  });
  window.addEventListener('pointermove', onPointerMove, { passive: true });
  window.addEventListener('pointerdown', onPointerDown);
  window.addEventListener('pointerup', onPointerUp);
  window.addEventListener('pointercancel', onPointerUp);

  fetch('assets/map-data.json')
    .then((res) => res.json())
    .then((json) => {
      data = sliceData(json);
      resize();
      render(performance.now());
    })
    .catch(() => canvas.classList.add('map-bg--fallback'));
})();
