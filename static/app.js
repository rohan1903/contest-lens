/* ── Contest-Lens Frontend ────────────────────────────────────────────────── */

// Neutral, warm color palette (no blue/purple)
const CHART_COLORS = [
  "#e8590c", // warm orange
  "#2b8a3e", // forest green
  "#d9480f", // deep orange
  "#c92a2a", // crimson
  "#5c5c5c", // dark gray
  "#e67700", // amber
  "#087f5b", // teal-green
  "#862e9c", // — skipped, using below instead
  "#495057", // cool gray
  "#d6336c", // rose
  "#1a1a1a", // black
];

// Override slot 7 — keep it non-purple
CHART_COLORS[7] = "#846022"; // warm brown

const BAND_ORDER = ["800-1000", "1000-1200", "1200-1400", "1400-1600", "1600-1900"];

const STAGE_NAMES = {
  "800-1000":  "Foundation",
  "1000-1200": "Core Skills",
  "1200-1400": "Intermediate",
  "1400-1600": "Advanced",
  "1600-1900": "Expert",
};

// Key techniques to track in the progression chart
const KEY_TECHNIQUES = [
  "Implementation",
  "Greedy",
  "Math",
  "Binary Search",
  "Dynamic Programming",
  "Data Structures",
  "Constructive Algorithms",
];

let analysisData = null;
let sampleData = null;
let barChart = null;
let lineChart = null;
let activeBand = BAND_ORDER[0];


/* ── Data Fetching ───────────────────────────────────────────────────────── */

async function fetchData() {
  const [analysisRes, sampleRes] = await Promise.all([
    fetch("/api/analysis"),
    fetch("/api/sample"),
  ]);

  if (analysisRes.ok) analysisData = await analysisRes.json();
  if (sampleRes.ok) sampleData = await sampleRes.json();

  // Use sample data as fallback for analysis data
  if (!analysisData && sampleData && sampleData.rating_bands) {
    analysisData = sampleData.rating_bands;
  }

  return { analysisData, sampleData };
}


/* ── Render: Overview Stats ──────────────────────────────────────────────── */

function renderStats() {
  const container = document.getElementById("stats-row");
  if (!analysisData) return;

  const bands = Object.keys(analysisData);
  let totalProblems = 0;
  const allTechniques = new Set();

  for (const key of bands) {
    totalProblems += analysisData[key].total_problems || 0;
    const techs = analysisData[key].techniques || {};
    Object.keys(techs).forEach((t) => allTechniques.add(t));
  }

  const stats = [
    { value: totalProblems.toLocaleString(), label: "Total Problems Analyzed" },
    { value: bands.length, label: "Rating Bands" },
    { value: allTechniques.size, label: "Techniques Tracked" },
    { value: "800–1900", label: "Rating Range" },
  ];

  container.innerHTML = stats
    .map(
      (s) => `
      <div class="stat-card">
        <div class="stat-value">${s.value}</div>
        <div class="stat-label">${s.label}</div>
      </div>`
    )
    .join("");
}


/* ── Render: Band Navigation (header) ────────────────────────────────────── */

function renderBandNav() {
  const nav = document.getElementById("band-nav");
  if (!analysisData) return;

  nav.innerHTML = BAND_ORDER
    .filter((b) => analysisData[b])
    .map(
      (b) => `<button class="nav-pill${b === activeBand ? " active" : ""}"
                data-band="${b}">${b}</button>`
    )
    .join("");

  nav.querySelectorAll(".nav-pill").forEach((btn) => {
    btn.addEventListener("click", () => {
      activeBand = btn.dataset.band;
      setActiveBand(activeBand);
    });
  });
}


/* ── Render: Band Tabs (chart section) ───────────────────────────────────── */

function renderBandTabs() {
  const container = document.getElementById("band-tabs");
  if (!analysisData) return;

  container.innerHTML = BAND_ORDER
    .filter((b) => analysisData[b])
    .map((b) => {
      const label = analysisData[b].label || b;
      return `<button class="band-tab${b === activeBand ? " active" : ""}"
                data-band="${b}">${b} <span style="color:#9a9a9a;font-weight:400">${label}</span></button>`;
    })
    .join("");

  container.querySelectorAll(".band-tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      activeBand = btn.dataset.band;
      setActiveBand(activeBand);
    });
  });
}


/* ── Set Active Band (updates tabs + chart) ──────────────────────────────── */

function setActiveBand(band) {
  activeBand = band;

  // Update nav pills
  document.querySelectorAll(".nav-pill").forEach((el) => {
    el.classList.toggle("active", el.dataset.band === band);
  });

  // Update band tabs
  document.querySelectorAll(".band-tab").forEach((el) => {
    el.classList.toggle("active", el.dataset.band === band);
  });

  renderBarChart(band);
}


/* ── Render: Horizontal Bar Chart ────────────────────────────────────────── */

function renderBarChart(band) {
  const bandData = analysisData[band];
  if (!bandData) return;

  const header = document.getElementById("band-chart-header");
  header.innerHTML = `
    <h3>${band} &middot; ${bandData.label || ""}</h3>
    <div class="chart-meta">${bandData.total_problems.toLocaleString()} problems &middot; Techniques with &ge;3% frequency shown</div>
  `;

  const techniques = bandData.techniques || {};

  // Sort by frequency, filter to >= 3%
  const sorted = Object.entries(techniques)
    .sort((a, b) => b[1].frequency - a[1].frequency)
    .filter(([, v]) => v.frequency >= 0.03);

  const labels = sorted.map(([name]) => name);
  const frequencies = sorted.map(([, v]) => +(v.frequency * 100).toFixed(1));
  const counts = sorted.map(([, v]) => v.problem_count);

  // Assign colors based on frequency tier
  const bgColors = frequencies.map((f) => {
    if (f >= 30) return "#2b8a3e";
    if (f >= 15) return "#e8590c";
    return "#868686";
  });

  const ctx = document.getElementById("band-bar-chart").getContext("2d");

  if (barChart) barChart.destroy();

  barChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Frequency (%)",
          data: frequencies,
          backgroundColor: bgColors,
          borderRadius: 4,
          barThickness: 22,
        },
      ],
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: { right: 16 },
      },
      scales: {
        x: {
          beginAtZero: true,
          max: Math.min(Math.ceil(Math.max(...frequencies) / 10) * 10 + 5, 100),
          ticks: {
            callback: (v) => v + "%",
            font: { family: "Inter", size: 12 },
            color: "#9a9a9a",
          },
          grid: {
            color: "#f0f0f0",
          },
        },
        y: {
          ticks: {
            font: { family: "Inter", size: 13, weight: "500" },
            color: "#4a4a4a",
          },
          grid: {
            display: false,
          },
        },
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#1a1a1a",
          titleFont: { family: "Inter", size: 13 },
          bodyFont: { family: "Inter", size: 12 },
          cornerRadius: 8,
          padding: 12,
          callbacks: {
            label: (ctx) => {
              const idx = ctx.dataIndex;
              return `${frequencies[idx]}% — ${counts[idx]} problems`;
            },
          },
        },
      },
    },
  });
}


/* ── Render: Progression Line Chart ──────────────────────────────────────── */

function renderProgressionChart() {
  if (!analysisData) return;

  const availableBands = BAND_ORDER.filter((b) => analysisData[b]);
  const labels = availableBands.map((b) => {
    const label = analysisData[b].label || b;
    return `${b}\n${label}`;
  });

  const datasets = KEY_TECHNIQUES.map((tech, i) => {
    const data = availableBands.map((b) => {
      const freq = analysisData[b]?.techniques?.[tech]?.frequency || 0;
      return +(freq * 100).toFixed(1);
    });

    return {
      label: tech,
      data,
      borderColor: CHART_COLORS[i % CHART_COLORS.length],
      backgroundColor: CHART_COLORS[i % CHART_COLORS.length] + "18",
      borderWidth: 2.5,
      pointRadius: 5,
      pointHoverRadius: 7,
      pointBackgroundColor: "#ffffff",
      pointBorderColor: CHART_COLORS[i % CHART_COLORS.length],
      pointBorderWidth: 2,
      tension: 0.3,
      fill: false,
    };
  });

  const ctx = document.getElementById("progression-chart").getContext("2d");

  if (lineChart) lineChart.destroy();

  lineChart = new Chart(ctx, {
    type: "line",
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: "index",
        intersect: false,
      },
      scales: {
        x: {
          ticks: {
            font: { family: "Inter", size: 12 },
            color: "#6b6b6b",
            maxRotation: 0,
          },
          grid: {
            color: "#f0f0f0",
          },
        },
        y: {
          beginAtZero: true,
          ticks: {
            callback: (v) => v + "%",
            font: { family: "Inter", size: 12 },
            color: "#9a9a9a",
          },
          grid: {
            color: "#f0f0f0",
          },
        },
      },
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            usePointStyle: true,
            pointStyle: "circle",
            padding: 20,
            font: { family: "Inter", size: 12, weight: "500" },
            color: "#4a4a4a",
          },
        },
        tooltip: {
          backgroundColor: "#1a1a1a",
          titleFont: { family: "Inter", size: 13 },
          bodyFont: { family: "Inter", size: 12 },
          cornerRadius: 8,
          padding: 12,
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.y}%`,
          },
        },
      },
    },
  });
}


/* ── Render: Roadmap Timeline ────────────────────────────────────────────── */

function renderRoadmap() {
  const container = document.getElementById("roadmap");

  // Use sample data if available (it has roadmap arrays), else derive from analysis
  const source = sampleData?.rating_bands || sampleData;

  const bandKeys = BAND_ORDER;

  container.innerHTML = bandKeys
    .map((band, idx) => {
      const sampleBand = source?.[band];
      const analysisBand = analysisData?.[band];
      const label = analysisBand?.label || sampleBand?.label || band;
      const stage = STAGE_NAMES[band] || "";

      // Roadmap items — prefer sample data (has curated roadmap), fallback to top techniques
      let topics = [];
      if (sampleBand?.roadmap) {
        topics = sampleBand.roadmap;
      } else if (analysisBand?.techniques) {
        topics = Object.entries(analysisBand.techniques)
          .sort((a, b) => b[1].frequency - a[1].frequency)
          .slice(0, 5)
          .map(([name, info]) => `${name} (${(info.frequency * 100).toFixed(0)}%)`);
      }

      return `
        <div class="roadmap-item roadmap-item--stage-${idx}">
          <div class="roadmap-item-header">
            <span class="band-label">${band} — ${stage}</span>
            <span class="stage-label">${label}</span>
          </div>
          <ul class="roadmap-topics">
            ${topics.map((t) => `<li>${t}</li>`).join("")}
          </ul>
        </div>`;
    })
    .join("");
}


/* ── Render: Insights Cards ──────────────────────────────────────────────── */

function renderInsights() {
  const container = document.getElementById("insights-grid");

  // Insights are only in the sample data
  const source = sampleData?.rating_bands || sampleData;
  if (!source) {
    container.innerHTML = '<p style="color:#9a9a9a;font-size:14px;">No insight data available.</p>';
    return;
  }

  const bandKeys = BAND_ORDER;

  container.innerHTML = bandKeys
    .filter((b) => source[b]?.insights)
    .map((band) => {
      const bandInfo = source[band];
      return `
        <div class="insight-card">
          <div class="insight-band">${band} &middot; ${bandInfo.label || ""}</div>
          <ul class="insight-list">
            ${bandInfo.insights.map((ins) => `<li>${ins}</li>`).join("")}
          </ul>
        </div>`;
    })
    .join("");
}


/* ── Bootstrap ───────────────────────────────────────────────────────────── */

async function init() {
  await fetchData();
  renderStats();
  renderBandNav();
  renderBandTabs();
  renderBarChart(activeBand);
  renderProgressionChart();
  renderRoadmap();
  renderInsights();
}

init();

