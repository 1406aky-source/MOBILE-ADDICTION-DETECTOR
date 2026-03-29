/**
 * MindGuard — AI Mobile Addiction Detector
 * Frontend Application Logic
 */

"use strict";

// Sync range slider with number input
const dailyInput = document.getElementById("daily_hours");
const dailyRange = document.getElementById("daily_hours_range");
if (dailyInput && dailyRange) {
  dailyInput.addEventListener("input", () => { dailyRange.value = dailyInput.value; });
  dailyRange.addEventListener("input", () => { dailyInput.value = dailyRange.value; });
}

// ===== MAIN ANALYSIS =====
async function runAnalysis() {
  const payload = collectFormData();
  if (!validatePayload(payload)) return;

  showLoading(true);
  toggleBtn(true);

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    const data = await res.json();
    renderDashboard(data);
    document.getElementById("dashboard").classList.remove("hidden");
    setTimeout(() => {
      document.getElementById("dashboard").scrollIntoView({ behavior: "smooth" });
    }, 200);
  } catch (err) {
    console.error(err);
    showToast("Analysis failed: " + err.message, "error");
  } finally {
    showLoading(false);
    toggleBtn(false);
  }
}

function collectFormData() {
  const g = (id) => {
    const el = document.getElementById(id);
    return el ? el.value : null;
  };
  return {
    daily_hours: parseFloat(g("daily_hours")) || 0,
    sleep_hours: parseFloat(g("sleep_hours")) || 7,
    social_hours: parseFloat(g("social_hours")) || 0,
    study_hours: parseFloat(g("study_hours")) || 0,
    gaming_hours: parseFloat(g("gaming_hours")) || 0,
    night_usage_days: parseInt(g("night_usage_days")) || 0,
    app_switches_per_hour: parseInt(g("app_switches_per_hour")) || 0,
    notification_clicks_per_hour: parseInt(g("notification_clicks_per_hour")) || 0,
    days_tracked: parseInt(g("days_tracked")) || 7,
    weekday_avg_hours: parseFloat(g("weekday_avg_hours")) || 0,
    weekend_avg_hours: parseFloat(g("weekend_avg_hours")) || 0,
    time_of_day: g("time_of_day") || "afternoon",
    is_weekend: new Date().getDay() % 6 === 0,
  };
}

function validatePayload(p) {
  if (p.daily_hours <= 0) {
    showToast("Please enter your daily screen time.", "warning");
    return false;
  }
  return true;
}

// ===== RENDER DASHBOARD =====
function renderDashboard(data) {
  renderKPIs(data);
  renderAlerts(data.alerts);
  renderProbBars(data.addiction);
  renderTrendChart(data.prediction.trend);
  renderForecast(data.prediction);
  renderHealthDims(data.health_score);
  renderRules(data.rules);
  renderInterventions(data.interventions);
  renderBiasVariance(data.bias_variance);
  renderFactors(data.addiction.key_factors);
  renderSchedule(data.schedule);
  renderRecommendations(data.interventions);
}

// ===== KPIs =====
function renderKPIs(data) {
  // Addiction Level
  const ad = data.addiction;
  const adCard = document.getElementById("kpi-addiction");
  adCard.style.borderTopColor = ad.color;
  document.getElementById("addiction-level").textContent = `${ad.emoji} ${ad.level}`;
  document.getElementById("addiction-level").style.color = ad.color;
  document.getElementById("addiction-score").textContent = `Score: ${ad.score}/100`;
  document.getElementById("addiction-desc").textContent = ad.description;

  // Health Score Ring
  const hs = data.health_score;
  document.getElementById("health-score").textContent = hs.total;
  document.getElementById("health-grade").textContent = hs.grade;
  document.getElementById("health-status").textContent = `${hs.status} — Better than ${hs.comparison.percentile}% of users`;
  const ringFill = document.getElementById("health-ring-fill");
  const pct = hs.total / 100;
  const circumference = 314;
  ringFill.style.strokeDashoffset = circumference * (1 - pct);
  ringFill.style.stroke = hs.color;

  // Prediction
  const pr = data.prediction;
  document.getElementById("pred-hours").textContent = `${pr.predicted_hours}h`;
  const pct_bar = Math.min(100, (pr.predicted_hours / 10) * 100);
  document.getElementById("pred-bar").style.width = pct_bar + "%";
  const exceed = pr.will_exceed_limit;
  document.getElementById("pred-desc").textContent = exceed
    ? `⚠️ ${pr.probability_exceed}% chance of exceeding ${pr.daily_limit}h limit`
    : `✅ Within recommended ${pr.daily_limit}h limit`;

  // Cluster
  const cl = data.cluster;
  document.getElementById("cluster-icon").textContent = cl.icon;
  document.getElementById("cluster-label").textContent = cl.label;
  document.getElementById("cluster-label").style.color = cl.color;
  document.getElementById("cluster-desc").textContent = `${cl.similar_users_percent}% of users match this profile`;
}

// ===== ALERTS =====
function renderAlerts(alerts) {
  const container = document.getElementById("alerts-section");
  container.innerHTML = "";
  if (!alerts || !alerts.length) return;
  alerts.forEach((a, i) => {
    const el = document.createElement("div");
    el.className = `alert-item ${a.type}`;
    el.style.animationDelay = `${i * 0.1}s`;
    el.innerHTML = `
      <span class="alert-icon">${a.icon}</span>
      <span class="alert-msg">${a.message}</span>
      <span class="alert-action">${a.action}</span>
    `;
    container.appendChild(el);
  });
}

// ===== PROBABILITY BARS =====
function renderProbBars(addiction) {
  const container = document.getElementById("prob-bars");
  const colors = { Low: "#22c55e", Moderate: "#f59e0b", High: "#f97316", Severe: "#ef4444" };
  const probs = addiction.probabilities || {};
  container.innerHTML = Object.entries(probs).map(([cls, pct]) => `
    <div class="prob-row">
      <span class="prob-label">${cls}</span>
      <div class="prob-bar-bg">
        <div class="prob-bar-fill" style="width:0%;background:${colors[cls]||'#888'}" 
             data-target="${pct}"></div>
      </div>
      <span class="prob-pct">${pct}%</span>
    </div>
  `).join("");

  document.getElementById("model-confidence").textContent = `${addiction.confidence}%`;

  // Animate bars
  requestAnimationFrame(() => {
    document.querySelectorAll(".prob-bar-fill").forEach(el => {
      el.style.width = el.dataset.target + "%";
    });
  });
}

// ===== TREND CHART =====
function renderTrendChart(trend) {
  const container = document.getElementById("trend-chart");
  if (!trend || !trend.length) return;
  const max = Math.max(...trend.map(d => d.hours), 0.1);
  container.innerHTML = trend.map(d => {
    const pct = Math.max(5, (d.hours / max) * 100);
    return `
      <div class="bar-wrap">
        <span class="bar-val">${d.hours}h</span>
        <div class="bar-col ${d.is_weekend ? 'weekend' : ''}" style="height:0%" data-target="${pct}%"></div>
        <span class="bar-label">${d.day}</span>
      </div>
    `;
  }).join("");

  requestAnimationFrame(() => {
    document.querySelectorAll(".bar-col").forEach(el => {
      el.style.height = el.dataset.target;
    });
  });
}

function renderForecast(prediction) {
  const el = document.getElementById("forecast-row");
  const wf = prediction.weekly_forecast;
  if (!wf) return;
  el.innerHTML = `
    <span>7-day total: <strong>${wf.total_week}h</strong></span>
    <span>Avg/day: <strong>${wf.average}h</strong></span>
    <span style="color:${wf.trend_direction==='improving'?'#22c55e':'#f97316'}">${wf.trend_direction === 'improving' ? '↓ Improving' : '↑ Increasing'}</span>
  `;
}

// ===== HEALTH DIMS =====
function renderHealthDims(hs) {
  const container = document.getElementById("health-dims");
  const statusColors = { good: "#22c55e", warning: "#f59e0b", critical: "#ef4444" };
  container.innerHTML = (hs.dimensions || []).map(d => `
    <div class="dim-row">
      <div class="dim-header">
        <span class="dim-name">${d.icon} ${d.label}</span>
        <span class="dim-score" style="color:${statusColors[d.status]||'#888'}">${d.score}/100</span>
      </div>
      <div class="dim-bar-bg">
        <div class="dim-bar-fill" style="width:0%;background:${statusColors[d.status]||'#888'}" data-target="${d.score}%"></div>
      </div>
    </div>
  `).join("");

  const peer = document.getElementById("peer-row");
  if (hs.comparison) {
    peer.textContent = `You're better than ${hs.comparison.percentile}% of users. Population average: ${hs.comparison.population_mean}.`;
  }

  requestAnimationFrame(() => {
    document.querySelectorAll(".dim-bar-fill").forEach(el => {
      el.style.width = el.dataset.target;
    });
  });
}

// ===== RULES =====
function renderRules(rules) {
  const container = document.getElementById("rules-list");
  const fired = rules.fired_rules || [];
  if (!fired.length) {
    container.innerHTML = `<div style="color:var(--text-dim);font-size:13px;text-align:center;padding:12px">✅ No critical rules fired.</div>`;
  } else {
    container.innerHTML = fired.slice(0, 5).map(r => `
      <div class="rule-item ${r.severity}">
        <div class="rule-name">${r.icon} ${r.name}</div>
        <div class="rule-prolog">${r.prolog}</div>
        <div class="rule-conclusion" style="color:${r.severity==='positive'?'#22c55e':r.severity==='critical'?'#ef4444':'#f59e0b'}">${r.conclusion}</div>
      </div>
    `).join("");
  }
  document.getElementById("rule-meta").textContent = `${rules.fired_count}/${rules.total_rules} rules fired — ${rules.meta_conclusion}`;
}

// ===== INTERVENTIONS =====
function renderInterventions(interventions) {
  const container = document.getElementById("interventions-grid");
  if (!interventions || !interventions.length) {
    container.innerHTML = `<div style="color:var(--text-dim);font-size:13px">No interventions needed. Great job!</div>`;
    return;
  }
  container.innerHTML = interventions.map(iv => `
    <div class="intervention-card" onclick="this.style.borderColor='var(--accent3)'">
      <div class="interv-type">${iv.type}</div>
      <div class="interv-icon">${iv.icon}</div>
      <div class="interv-title">${iv.title}</div>
      <div class="interv-desc">${iv.description}</div>
      <div class="interv-utility">Utility: ${Math.round(iv.adjusted_utility * 100)}%</div>
    </div>
  `).join("");
}

// ===== BIAS VARIANCE =====
function renderBiasVariance(bv) {
  const container = document.getElementById("bv-monitor");
  const colors = { balanced: "#22c55e", high_variance: "#f59e0b", learning: "#00d4ff" };
  const color = colors[bv.status] || "#888";
  container.innerHTML = `
    <div class="bv-status-row">
      <div class="bv-indicator" style="background:${color};box-shadow:0 0 8px ${color}"></div>
      <div>
        <div class="bv-msg">${bv.message}</div>
        <div class="bv-rec">${bv.recommendation}</div>
      </div>
    </div>
    <div class="bv-confidence-bar">
      <div class="bv-conf-label">
        <span>Model Confidence</span>
        <span style="color:var(--accent)">${bv.model_confidence}%</span>
      </div>
      <div class="bv-bar-bg">
        <div class="bv-bar-fill" style="width:0%" data-target="${bv.model_confidence}%"></div>
      </div>
    </div>
    <div style="margin-top:10px;font-size:11px;color:var(--text-muted);font-family:var(--font-mono)">
      Days tracked: ${bv.days_tracked} | Status: ${bv.status.replace("_", " ")}
    </div>
  `;
  requestAnimationFrame(() => {
    document.querySelectorAll(".bv-bar-fill").forEach(el => el.style.width = el.dataset.target);
  });
}

// ===== FACTORS =====
function renderFactors(factors) {
  const container = document.getElementById("factors-list");
  if (!factors || !factors.length) {
    container.innerHTML = `<div style="color:var(--text-dim);font-size:13px">No major risk factors detected.</div>`;
    return;
  }
  container.innerHTML = factors.map(f => `
    <div class="factor-item">
      <span class="factor-name">${f.factor}</span>
      <span class="factor-value">${f.value}</span>
      <span class="factor-badge ${f.impact}">${f.impact}</span>
    </div>
  `).join("");
}

// ===== SCHEDULE =====
function renderSchedule(schedule) {
  const meta = document.getElementById("schedule-meta");
  meta.innerHTML = `
    <div class="meta-item">Phone Time: <strong>${Math.round(schedule.phone_minutes / 60 * 10) / 10}h</strong></div>
    <div class="meta-item">Study Time: <strong>${Math.round(schedule.study_minutes / 60 * 10) / 10}h</strong></div>
    <div class="meta-item">Health Activities: <strong>${Math.round(schedule.health_minutes / 60 * 10) / 10}h</strong></div>
    <div class="meta-item">Schedule Quality: <strong style="color:var(--accent)">${schedule.quality_score}/100</strong></div>
    <div class="meta-item">Recommended Phone: <strong style="color:var(--success)">${schedule.recommended_phone_hours}h</strong></div>
    ${schedule.reduction_needed > 0 ? `<div class="meta-item" style="color:var(--orange)">Reduce by: <strong>${schedule.reduction_needed}h</strong></div>` : ''}
  `;

  const timeline = document.getElementById("schedule-timeline");
  timeline.innerHTML = (schedule.blocks || []).map(b => `
    <div class="timeline-block ${b.type}">
      <span class="block-time">${b.start_time} – ${b.end_time}</span>
      <span class="block-icon">${b.icon}</span>
      <span class="block-label">${b.label}</span>
      <span class="block-dur">${b.duration}min</span>
      ${b.type === 'phone' ? `<span class="block-limit">⚠ Limit</span>` : ''}
    </div>
  `).join("");
}

// ===== RECOMMENDATIONS =====
function renderRecommendations(interventions) {
  // Fetch personalized recs from API using current form data
  const payload = collectFormData();
  fetch("/api/recommendations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  .then(r => r.json())
  .then(recs => {
    const container = document.getElementById("recs-grid");
    const all = [
      ...(recs.apps || []).map(a => ({ icon: a.icon, name: a.app, type: a.type, reason: a.reason })),
      ...(recs.focus_apps || []).map(a => ({ icon: "🎯", name: a.app, type: a.type, reason: "Focus & productivity" })),
    ];
    container.innerHTML = all.map(r => `
      <div class="rec-card">
        <div class="rec-icon">${r.icon}</div>
        <div class="rec-app">${r.name}</div>
        <div class="rec-type">${r.type}</div>
        <div class="rec-reason">${r.reason}</div>
      </div>
    `).join("");
  })
  .catch(() => {});
}

// ===== UTILITIES =====
function showLoading(show) {
  let overlay = document.getElementById("loading-overlay");
  if (show) {
    if (!overlay) {
      overlay = document.createElement("div");
      overlay.id = "loading-overlay";
      overlay.className = "loading-overlay";
      overlay.innerHTML = `
        <div class="loading-spinner"></div>
        <div class="loading-text">🧠 AI Models Processing...</div>
      `;
      document.body.appendChild(overlay);
    }
    overlay.style.display = "flex";
  } else {
    if (overlay) overlay.style.display = "none";
  }
}

function toggleBtn(loading) {
  const btn = document.getElementById("analyze-btn");
  const loader = document.getElementById("btn-loader");
  const text = btn.querySelector(".btn-text");
  if (loading) {
    btn.classList.add("loading");
    if (loader) loader.style.display = "inline";
    if (text) text.textContent = "Analyzing...";
  } else {
    btn.classList.remove("loading");
    if (loader) loader.style.display = "none";
    if (text) text.textContent = "Run AI Analysis";
  }
}

function showToast(msg, type = "info") {
  const t = document.createElement("div");
  t.style.cssText = `
    position:fixed; bottom:24px; right:24px; z-index:300;
    background:var(--card); border:1px solid var(--card-border);
    padding:14px 20px; border-radius:8px; font-size:13px;
    box-shadow:var(--shadow); max-width:360px;
    animation: slideIn 0.3s ease;
  `;
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 4000);
}

// ===== FONT for CSS variable =====
document.addEventListener("DOMContentLoaded", () => {
  // Add font reference to CSS
  const style = document.createElement("style");
  style.textContent = `
    .loading-text { --font-mono: 'Space Mono', monospace; font-family: var(--font-mono); }
  `;
  document.head.appendChild(style);
});
