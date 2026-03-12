/* ═══════════════════════════════════════════════════════
   CardioLens — Chart Utilities
═══════════════════════════════════════════════════════ */

const COLORS = {
  accent:  '#e8365d',
  accent2: '#ff6b6b',
  accent3: '#f7c948',
  blue:    '#4a9eff',
  green:   '#2ecc71',
  purple:  '#9b59b6',
  orange:  '#e67e22',
  teal:    '#1abc9c',
  surface: '#111520',
  border:  'rgba(255,255,255,0.07)',
  text:    '#e8ecf4',
  text2:   '#8892aa',
};

const PALETTE = [
  COLORS.accent, COLORS.blue, COLORS.green,
  COLORS.accent3, COLORS.purple, COLORS.teal, COLORS.orange
];

// Chart.js global defaults
Chart.defaults.color = COLORS.text2;
Chart.defaults.borderColor = COLORS.border;
Chart.defaults.font.family = "'DM Sans', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.plugins.legend.labels.boxWidth = 12;
Chart.defaults.plugins.legend.labels.padding = 16;
Chart.defaults.plugins.tooltip.backgroundColor = '#0d1220';
Chart.defaults.plugins.tooltip.borderColor = 'rgba(255,255,255,0.1)';
Chart.defaults.plugins.tooltip.borderWidth = 1;
Chart.defaults.plugins.tooltip.padding = 10;

// Helper: fetch JSON from API
async function fetchData(url) {
  try {
    const r = await fetch(url);
    return await r.json();
  } catch (e) {
    console.error('Fetch error:', e);
    return null;
  }
}

// Helper: build bar chart
function makeBar(ctx, labels, datasets, options = {}) {
  return new Chart(ctx, {
    type: 'bar',
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'top' }, ...options.plugins },
      scales: {
        x: { grid: { color: COLORS.border }, ticks: { color: COLORS.text2 } },
        y: { grid: { color: COLORS.border }, ticks: { color: COLORS.text2 } },
        ...options.scales
      },
      ...options
    }
  });
}

// Helper: build horizontal bar
function makeHBar(ctx, labels, data, color, options = {}) {
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        data,
        backgroundColor: color || COLORS.accent,
        borderRadius: 4,
        borderSkipped: false,
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false }, ...options.plugins },
      scales: {
        x: { grid: { color: COLORS.border }, ticks: { color: COLORS.text2 } },
        y: { grid: { display: false }, ticks: { color: COLORS.text2 } },
      },
      ...options
    }
  });
}

// Helper: build doughnut
function makeDoughnut(ctx, labels, data, colors) {
  return new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data,
        backgroundColor: colors || PALETTE,
        borderColor: COLORS.surface,
        borderWidth: 3,
        hoverOffset: 8,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '65%',
      plugins: { legend: { position: 'bottom' } }
    }
  });
}

// Helper: build line chart
function makeLine(ctx, labels, datasets, options = {}) {
  return new Chart(ctx, {
    type: 'line',
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'top' }, ...options.plugins },
      scales: {
        x: { grid: { color: COLORS.border }, ticks: { color: COLORS.text2 } },
        y: { grid: { color: COLORS.border }, ticks: { color: COLORS.text2 } },
        ...options.scales
      },
      ...options
    }
  });
}

// Helper: build scatter chart
function makeScatter(ctx, datasets, options = {}) {
  return new Chart(ctx, {
    type: 'scatter',
    data: { datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'top' }, ...options.plugins },
      scales: {
        x: { grid: { color: COLORS.border }, ticks: { color: COLORS.text2 } },
        y: { grid: { color: COLORS.border }, ticks: { color: COLORS.text2 } },
      },
      ...options
    }
  });
}

// Render risk factor bars
function renderRiskBars(containerId, data) {
  const container = document.getElementById(containerId);
  if (!container || !data) return;
  const max = Math.max(...data.map(d => d.disease_rate));
  container.innerHTML = data.map(d => `
    <div class="risk-item">
      <div class="risk-row">
        <span class="risk-name">${d.factor}</span>
        <span class="risk-pct">${d.disease_rate}%</span>
      </div>
      <div class="risk-bar-track">
        <div class="risk-bar-fill" style="width:${(d.disease_rate/max*100).toFixed(1)}%"></div>
      </div>
    </div>
  `).join('');
}

// Number counter animation
function animateCounter(el, end, suffix = '') {
  const start = 0;
  const duration = 1200;
  const step = end / (duration / 16);
  let current = start;
  const timer = setInterval(() => {
    current += step;
    if (current >= end) { current = end; clearInterval(timer); }
    el.textContent = Number.isInteger(end)
      ? Math.floor(current).toLocaleString() + suffix
      : current.toFixed(1) + suffix;
  }, 16);
}

// Animate all KPI values on page load
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-counter]').forEach(el => {
    const val = parseFloat(el.dataset.counter);
    const suffix = el.dataset.suffix || '';
    animateCounter(el, val, suffix);
  });

  // Accordion
  document.querySelectorAll('.accordion-header').forEach(h => {
    h.addEventListener('click', () => {
      const body = h.nextElementSibling;
      body.classList.toggle('open');
      h.querySelector('.acc-arrow').textContent = body.classList.contains('open') ? '−' : '+';
    });
  });

  // Tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const group = btn.dataset.group;
      document.querySelectorAll(`[data-group="${group}"]`).forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const target = btn.dataset.target;
      document.querySelectorAll(`[data-panel="${group}"]`).forEach(p => {
        p.style.display = p.id === target ? 'block' : 'none';
      });
    });
  });
});
