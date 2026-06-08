/* ═══════════════════════════════════════════════════
   SISTEMA DA EVOLUÇÃO — script.js
   Toda a lógica do frontend + integração com backend
═══════════════════════════════════════════════════ */

"use strict";

const API = "http://localhost:5000/api";

// ─── Estado global ────────────────────────────────
let playerData     = null;
let selectedObj    = null;
let currentMissTab = "daily";
let allAchievements= [];
let allMissions    = {};
let currentAchCat  = "Todas";

// Cores dos atributos
const ATTR_COLORS = {
  forca:       "#ff6b6b",
  resistencia: "#ff9f43",
  inteligencia:"#54a0ff",
  conhecimento:"#48dbfb",
  disciplina:  "#9b59b6",
  foco:        "#a29bfe",
  saude:       "#00d2d3",
  energia:     "#ffd32a",
  carisma:     "#fd79a8",
  aparencia:   "#fdcb6e",
};

const ATTR_ICONS = {
  forca: "⚔️", resistencia: "🛡️", inteligencia: "🧠", conhecimento: "📚",
  disciplina: "🔩", foco: "🎯", saude: "❤️", energia: "⚡",
  carisma: "🌐", aparencia: "✨",
};

const ATTR_NAMES_BR = {
  forca: "Força", resistencia: "Resistência", inteligencia: "Inteligência",
  conhecimento: "Conhecimento", disciplina: "Disciplina", foco: "Foco",
  saude: "Saúde", energia: "Energia", carisma: "Carisma", aparencia: "Aparência",
};

// ── INIT ────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  updateSystemDate();
  checkPlayerExists();
  setInterval(pollNotifications, 12000);
  setInterval(updateSystemDate, 60000);
});

function updateSystemDate() {
  const el = document.getElementById("system-date");
  if (!el) return;
  const now = new Date();
  const opts = { weekday: "long", year: "numeric", month: "long", day: "numeric" };
  el.textContent = now.toLocaleDateString("pt-BR", opts).toUpperCase();
}

// ── VERIFICAR JOGADOR ──────────────────────────────
async function checkPlayerExists() {
  try {
    const res = await fetch(`${API}/player/exists`);
    const data = await res.json();
    if (data.exists) {
      await loadAndShowMain();
    } else {
      showScreen("creation");
    }
  } catch {
    // Backend offline — mostrar tela offline
    showOfflineMode();
  }
}

function showOfflineMode() {
  showScreen("creation");
  showToast("[SISTEMA] Backend offline. Inicie main.py para jogar.", "red");
}

// ── TELA DE CRIAÇÃO ───────────────────────────────
function goStep(step) {
  const name = document.getElementById("input-name").value.trim();
  const age  = document.getElementById("input-age").value;
  if (!name) { shakeElement("input-name"); return; }
  if (!age || age < 10) { shakeElement("input-age"); return; }
  document.querySelectorAll(".creation-step").forEach(s => s.classList.remove("active"));
  document.getElementById(`step-${step}`).classList.add("active");
}

function selectObjective(card) {
  document.querySelectorAll(".objective-card").forEach(c => c.classList.remove("selected"));
  card.classList.add("selected");
  selectedObj = card.dataset.obj;
  document.getElementById("btn-create").disabled = false;
}

async function createPlayer() {
  const name = document.getElementById("input-name").value.trim();
  const age  = parseInt(document.getElementById("input-age").value);
  if (!name || !age || !selectedObj) return;

  document.getElementById("btn-create").textContent = "INICIANDO...";
  document.getElementById("btn-create").disabled = true;

  try {
    const res = await fetch(`${API}/player/create`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, age, main_objective: selectedObj }),
    });
    const data = await res.json();
    if (data.success) {
      playerData = data.player;
      await loadAndShowMain();
      setTimeout(() => showToast(data.message, "blue"), 500);
    }
  } catch {
    showToast("[SISTEMA] Erro ao criar perfil. Verifique o backend.", "red");
    document.getElementById("btn-create").textContent = "INICIAR EVOLUÇÃO ⚡";
    document.getElementById("btn-create").disabled = false;
  }
}

function shakeElement(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.style.animation = "none";
  el.offsetHeight;
  el.style.borderColor = "#ff3366";
  setTimeout(() => { el.style.borderColor = ""; }, 1500);
}

// ── CARREGAR E MOSTRAR TELA PRINCIPAL ─────────────
async function loadAndShowMain() {
  try {
    const res = await fetch(`${API}/player`);
    playerData = await res.json();
    if (playerData.error) { showScreen("creation"); return; }
    showScreen("main");
    renderDashboard();
    loadMissions("daily");
    loadSystemMessages();
    updateMissionBadge();
  } catch {
    showOfflineMode();
  }
}

// ── NAVEGAÇÃO ─────────────────────────────────────
function showScreen(name) {
  document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
  const map = { creation: "creation-screen", main: "main-screen" };
  const el = document.getElementById(map[name] || name);
  if (el) el.classList.add("active");
}

function showSection(name) {
  document.querySelectorAll(".section").forEach(s => s.classList.remove("active"));
  document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));
  const section = document.getElementById(`section-${name}`);
  const navItem = document.querySelector(`[data-section="${name}"]`);
  if (section) section.classList.add("active");
  if (navItem) navItem.classList.add("active");
  // Carregar conteúdo específico
  switch (name) {
    case "dashboard":   renderDashboard(); loadSystemMessages(); break;
    case "profile":     renderProfile(); break;
    case "missions":    loadMissions(currentMissTab); break;
    case "achievements":loadAchievements(); break;
    case "rankings":    loadRankings(); break;
    case "legacy":      loadLegacy(); break;
    case "nofap":       renderNoFap(); break;
    case "reports":     loadReport("daily", null); break;
  }
}

// ── DASHBOARD ─────────────────────────────────────
function renderDashboard() {
  if (!playerData) return;
  const p = playerData;
  const attrs = p.attributes || {};
  const dt = p.day_tracker || {};
  const xpPct = Math.min(100, (p.xp / p.xp_next) * 100);

  // Sidebar mini
  set("mini-name", p.name);
  set("mini-level", `Nível ${p.level}`);
  set("mini-rank", p.rank);

  // Player card
  set("dash-name", p.name);
  set("dash-title", p.title || "Iniciante");
  set("dash-objective", p.main_objective || "—");
  set("dash-rank", p.rank);
  set("dash-level", p.level);
  set("dash-gold", formatNum(p.gold));
  set("dash-missions", formatNum((p.missions || {}).total || 0));

  // XP
  set("dash-xp", formatNum(p.xp));
  set("dash-xp-next", formatNum(p.xp_next));
  setPct("xp-bar-fill", xpPct);

  // Rank progress
  const rankPct = getRankProgressPct(p);
  setPct("rank-bar-fill", rankPct * 100);
  const nextRank = getNextRank(p.rank);
  set("rank-progress-text", `Rank ${p.rank} → ${nextRank}`);

  // Streak
  set("dash-streak", dt.current_streak || 0);
  set("dash-total-days", dt.total_days || 0);
  set("dash-best-streak", dt.best_streak || 0);

  // Attribute points
  const attrPointsBar = document.getElementById("attr-points-bar");
  if (p.attribute_points > 0) {
    attrPointsBar.style.display = "flex";
    set("attr-points-text", `${p.attribute_points} pontos de atributo disponíveis`);
  } else {
    attrPointsBar.style.display = "none";
  }

  // Atributos (grid pequena)
  renderAttributesGrid(attrs, "attributes-grid", false);

  // Missões rápidas
  loadQuickMissions();
}

function renderAttributesGrid(attrs, containerId, showSpend = false) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = "";
  const attrKeys = Object.keys(ATTR_NAMES_BR);
  attrKeys.forEach(key => {
    const val = Math.round((attrs[key] || 0) * 10) / 10;
    const pct = Math.min(100, val);
    const color = ATTR_COLORS[key] || "#00d4ff";
    const card = document.createElement("div");
    card.className = "attr-bar-card";
    card.innerHTML = `
      <div class="attr-header">
        <span class="attr-name">${ATTR_ICONS[key]} ${ATTR_NAMES_BR[key].toUpperCase()}</span>
        <span class="attr-value">${val.toFixed(1)}</span>
      </div>
      <div class="attr-fill-bar">
        <div class="attr-fill-inner" style="width:${pct}%;background:${color};"></div>
      </div>
    `;
    container.appendChild(card);
  });
}

async function loadQuickMissions() {
  try {
    const res = await fetch(`${API}/missions?type=daily`);
    const missions = await res.json();
    const completed = (playerData.missions || {}).daily_completed_today || [];
    const container = document.getElementById("quick-missions-list");
    if (!container) return;
    container.innerHTML = "";
    const toShow = missions.slice(0, 5);
    toShow.forEach(m => {
      const isDone = completed.includes(m.id);
      container.appendChild(buildMissionCard(m, isDone, true));
    });
    allMissions["daily"] = missions;
    updateMissionBadge();
  } catch {}
}

function buildMissionCard(m, isDone, compact = false) {
  const catIcons = { physical: "⚔️", study: "📚", selfcare: "🌿", mental: "🧠" };
  const card = document.createElement("div");
  card.className = `mission-card${isDone ? " completed" : ""}`;
  card.dataset.id = m.id;
  const diffClass = `diff-${m.difficulty}`;
  card.innerHTML = `
    <span class="mission-icon">${catIcons[m.category] || "◆"}</span>
    <div class="mission-body">
      <div class="mission-title">${m.title}</div>
      <div class="mission-desc">${m.description}</div>
    </div>
    <div class="mission-rewards">
      <span class="difficulty-badge ${diffClass}">${m.difficulty.toUpperCase()}</span>
      <span class="reward-xp">+${m.xp_reward} XP</span>
      <span class="reward-gold">💰${m.gold_reward}</span>
      ${isDone
        ? `<span style="color:var(--neon-green);font-size:0.85rem;">✓</span>`
        : `<button class="btn-complete" onclick="completeMission('${m.id}', this)">COMPLETAR</button>`
      }
    </div>
  `;
  return card;
}

async function completeMission(missionId, btn) {
  if (btn) {
    btn.textContent = "...";
    btn.disabled = true;
  }
  try {
    const res = await fetch(`${API}/missions/complete`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mission_id: missionId }),
    });
    const data = await res.json();
    if (data.error) { showToast(`[ERRO] ${data.error}`, "red"); return; }

    playerData = data.player;
    renderDashboard();

    showToast(`✅ Missão concluída! +${data.xp_gained} XP`, "green");

    if (data.level_ups && data.level_ups.length > 0) {
      setTimeout(() => showLevelUpModal(data.level_ups[data.level_ups.length - 1]), 800);
    }
    if (data.new_rank) {
      setTimeout(() => showRankUpModal(data.new_rank), 1600);
    }
    if (data.new_achievements && data.new_achievements.length > 0) {
      setTimeout(() => showAchievementModal(data.new_achievements[0]), 2400);
    }
    if (data.new_titles && data.new_titles.length > 0) {
      data.new_titles.forEach(t => showToast(`👑 Título: "${t}" desbloqueado!`, "gold"));
    }

    // Atualizar card
    const card = document.querySelector(`[data-id="${missionId}"]`);
    if (card) {
      card.classList.add("completed");
      const b = card.querySelector(".btn-complete");
      if (b) b.replaceWith(Object.assign(document.createElement("span"), {
        style: "color:var(--neon-green);font-size:0.85rem;", textContent: "✓"
      }));
    }
    updateMissionBadge();
  } catch {
    showToast("[ERRO] Não foi possível completar a missão.", "red");
    if (btn) { btn.textContent = "COMPLETAR"; btn.disabled = false; }
  }
}

function updateMissionBadge() {
  const badge = document.getElementById("badge-missions");
  if (!badge || !playerData) return;
  const total = (allMissions["daily"] || []).length;
  const done = ((playerData.missions || {}).daily_completed_today || []).length;
  const remaining = Math.max(0, total - done);
  badge.textContent = remaining;
  badge.style.display = remaining > 0 ? "inline-block" : "none";
}

// ── MISSÕES (SEÇÃO COMPLETA) ──────────────────────
async function loadMissions(type) {
  currentMissTab = type;
  try {
    if (!allMissions[type]) {
      const res = await fetch(`${API}/missions?type=${type}`);
      allMissions[type] = await res.json();
    }
    const completed = (playerData?.missions || {}).daily_completed_today || [];
    const container = document.getElementById("missions-container");
    if (!container) return;
    container.innerHTML = "";
    const missions = allMissions[type] || [];
    if (missions.length === 0) {
      container.innerHTML = `<div class="system-msg">Nenhuma missão disponível nesta categoria.</div>`;
      return;
    }
    missions.forEach(m => {
      const isDone = type === "daily" && completed.includes(m.id);
      container.appendChild(buildMissionCard(m, isDone, false));
    });
  } catch {
    showToast("[ERRO] Erro ao carregar missões.", "red");
  }
}

function switchMissionTab(type, btn) {
  document.querySelectorAll(".mission-tab").forEach(t => t.classList.remove("active"));
  btn.classList.add("active");
  loadMissions(type);
}

// ── CONQUISTAS ────────────────────────────────────
async function loadAchievements() {
  try {
    const res = await fetch(`${API}/achievements`);
    allAchievements = await res.json();
    renderAchievements(allAchievements);
    buildAchCategories();
  } catch {}
}

function buildAchCategories() {
  const cats = ["Todas", ...new Set(allAchievements.filter(a => !a.secret || a.unlocked).map(a => a.category))];
  const container = document.getElementById("ach-categories");
  if (!container) return;
  container.innerHTML = "";
  cats.forEach(cat => {
    const btn = document.createElement("button");
    btn.className = `ach-cat-btn${cat === currentAchCat ? " active" : ""}`;
    btn.textContent = cat;
    btn.onclick = () => {
      currentAchCat = cat;
      document.querySelectorAll(".ach-cat-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const filtered = cat === "Todas" ? allAchievements : allAchievements.filter(a => a.category === cat);
      renderAchievements(filtered);
    };
    container.appendChild(btn);
  });
}

function renderAchievements(list) {
  const grid = document.getElementById("achievements-grid");
  const countEl = document.getElementById("ach-count");
  if (!grid) return;
  grid.innerHTML = "";
  const unlocked = list.filter(a => a.unlocked).length;
  if (countEl) countEl.textContent = `${unlocked} / ${list.length}`;
  list.forEach(a => {
    const card = document.createElement("div");
    card.className = `ach-card ${a.unlocked ? "unlocked" : "locked"}`;
    const isSecret = a.secret && !a.unlocked;
    card.innerHTML = `
      <span class="ach-icon">${isSecret ? "🔒" : a.icon}</span>
      <div class="ach-name">${isSecret ? "???" : a.name}</div>
      <div class="ach-desc">${isSecret ? "Conquista secreta." : a.description}</div>
      ${a.unlocked ? `<div class="ach-reward">+${a.xp_reward} XP · ${a.gold_reward}💰</div>` : ""}
    `;
    grid.appendChild(card);
  });
}

// ── RANKINGS ──────────────────────────────────────
async function loadRankings() {
  try {
    const res = await fetch(`${API}/rankings/info`);
    const ranks = await res.json();
    const grid = document.getElementById("rankings-grid");
    if (!grid) return;
    grid.innerHTML = "";
    ranks.forEach(r => {
      const isCurrent = playerData && playerData.rank === r.rank;
      const card = document.createElement("div");
      card.className = `rank-card${isCurrent ? " current-rank" : ""}`;
      card.style.border = `1px solid ${r.color}22`;
      if (isCurrent) card.style.boxShadow = `0 0 20px ${r.color}33`;
      let badge = "";
      if (r.special) badge = `<span class="rank-type-badge rank-special">ESPECIAL</span>`;
      else if (r.secret) badge = `<span class="rank-type-badge rank-secret">SECRETO</span>`;
      else badge = `<span class="rank-type-badge rank-normal">${isCurrent ? "ATUAL" : "PADRÃO"}</span>`;
      card.innerHTML = `
        <div class="rank-label-big" style="color:${r.color};text-shadow:0 0 15px ${r.color}66">
          ${r.secret && !isCurrent ? "???" : r.rank}
        </div>
        <div class="rank-xp-req">${r.xp_required > 0 ? formatNum(r.xp_required) + " XP" : "INICIAL"}</div>
        ${badge}
      `;
      grid.appendChild(card);
    });
  } catch {}
}

// ── LEGADO ────────────────────────────────────────
async function loadLegacy() {
  try {
    const res = await fetch(`${API}/legacy`);
    const legacy = await res.json();
    const container = document.getElementById("legacy-content");
    if (!container) return;
    const p = playerData || {};
    const dt = p.day_tracker || {};
    const m = p.missions || {};
    const attrs = p.attributes || {};

    container.innerHTML = `
      <div class="legacy-card">
        <div class="legacy-card-title">[JORNADA]</div>
        ${legacyRow("Data de Início", formatDate(dt.creation_date || legacy.creation_date))}
        ${legacyRow("Dias Totais", formatNum(dt.total_days || legacy.total_days || 0))}
        ${legacyRow("Melhor Sequência", `${dt.best_streak || legacy.best_streak || 0} dias`)}
        ${legacyRow("Nível Atual", p.level || legacy.final_level || 1)}
        ${legacyRow("Rank Atual", p.rank || legacy.final_rank || "D")}
      </div>
      <div class="legacy-card">
        <div class="legacy-card-title">[PROGRESSO]</div>
        ${legacyRow("Missões Concluídas", formatNum(m.total || 0))}
        ${legacyRow("Treinos Realizados", formatNum(dt.workouts_done || 0))}
        ${legacyRow("Horas de Estudo", `${(dt.study_hours || 0).toFixed(1)}h`)}
        ${legacyRow("Ouro Acumulado", formatNum(p.gold || 0))}
        ${legacyRow("Conquistas", (p.achievements || []).length)}
      </div>
      <div class="legacy-card">
        <div class="legacy-card-title">[ATRIBUTOS ATUAIS]</div>
        ${Object.entries(attrs).map(([k, v]) =>
          legacyRow(`${ATTR_ICONS[k]} ${ATTR_NAMES_BR[k]}`, `${Math.round(v * 10) / 10} / 100`)
        ).join("")}
      </div>
      <div class="legacy-card">
        <div class="legacy-card-title">[TÍTULOS DESBLOQUEADOS]</div>
        ${(p.unlocked_titles || []).map(tid => {
          const name = getTitleName(tid);
          return `<div class="legacy-stat-row"><span class="legacy-stat-label">👑 ${name}</span></div>`;
        }).join("") || "<div class='legacy-stat-row'><span class='legacy-stat-label' style='color:var(--text-muted)'>Nenhum ainda.</span></div>"}
      </div>
      <div class="legacy-card">
        <div class="legacy-card-title">[HISTÓRICO DE RANKS]</div>
        ${(p.rank_history || []).slice(-8).reverse().map(r =>
          legacyRow(formatDate(r.date), `${r.from} → ${r.rank}`)
        ).join("") || `<div class='legacy-stat-row'><span class='legacy-stat-label' style='color:var(--text-muted)'>Rank D inicial.</span></div>`}
      </div>
    `;
  } catch {}
}

function legacyRow(label, val) {
  return `<div class="legacy-stat-row">
    <span class="legacy-stat-label">${label}</span>
    <span class="legacy-stat-val">${val}</span>
  </div>`;
}

// ── PERFIL ────────────────────────────────────────
async function renderProfile() {
  if (!playerData) return;
  const p = playerData;
  const attrs = p.attributes || {};

  set("profile-rank", p.rank);
  set("profile-initial", (p.name || "?")[0].toUpperCase());
  set("profile-name", p.name);
  set("profile-title-display", p.title || "Iniciante");
  set("profile-level-display", `Nível ${p.level}`);
  set("profile-points-available", p.attribute_points > 0
    ? `${p.attribute_points} pts disponíveis` : "");

  // Atributos completos
  renderAttributesFull(attrs, p.attribute_points || 0);

  // Títulos
  try {
    const res = await fetch(`${API}/titles`);
    const titles = await res.json();
    renderProfileTitles(titles, p.title, p.unlocked_titles || []);
  } catch {}
}

function renderAttributesFull(attrs, points) {
  const container = document.getElementById("attributes-full-list");
  if (!container) return;
  container.innerHTML = "";
  Object.entries(ATTR_NAMES_BR).forEach(([key, name]) => {
    const val = Math.round((attrs[key] || 0) * 10) / 10;
    const pct = Math.min(100, val);
    const color = ATTR_COLORS[key] || "#00d4ff";
    const row = document.createElement("div");
    row.className = "attr-full-row";
    row.innerHTML = `
      <span class="attr-full-icon">${ATTR_ICONS[key]}</span>
      <span class="attr-full-name">${name.toUpperCase()}</span>
      <div class="attr-full-bar">
        <div class="attr-full-fill" style="width:${pct}%;background:${color};"></div>
      </div>
      <span class="attr-full-val">${val.toFixed(0)}</span>
      ${points > 0
        ? `<button class="attr-spend-btn" onclick="spendPoint('${key}')">+2</button>`
        : ""}
    `;
    container.appendChild(row);
  });
}

async function spendPoint(attr) {
  try {
    const res = await fetch(`${API}/player/spend_points`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ attribute: attr, amount: 1 }),
    });
    const data = await res.json();
    if (data.success) {
      playerData = data.player;
      renderProfile();
      renderDashboard();
      showToast(`⬆️ ${ATTR_NAMES_BR[attr]} aumentado!`, "blue");
    }
  } catch {}
}

function renderProfileTitles(titles, currentTitle, unlockedIds) {
  const container = document.getElementById("profile-titles-list");
  if (!container) return;
  container.innerHTML = "";
  const unlocked = titles.filter(t => unlockedIds.includes(t.id));
  if (unlocked.length === 0) {
    container.innerHTML = `<div style="color:var(--text-muted);font-size:0.8rem;padding:12px 0;">Nenhum título desbloqueado ainda.</div>`;
    return;
  }
  unlocked.forEach(t => {
    const isActive = t.name === currentTitle;
    const row = document.createElement("div");
    row.className = `title-row${isActive ? " active-title" : ""}`;
    row.innerHTML = `
      <span class="title-name${t.secret ? " title-secret-name" : ""}">${t.name}</span>
      ${isActive
        ? `<span class="title-select-btn">✓ ATIVO</span>`
        : `<button class="title-select-btn" onclick="setTitle('${t.id}')">USAR</button>`
      }
    `;
    container.appendChild(row);
  });
}

async function setTitle(titleId) {
  try {
    const res = await fetch(`${API}/player/set_title`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title_id: titleId }),
    });
    const data = await res.json();
    if (data.success) {
      playerData.title = data.title;
      renderProfile();
      renderDashboard();
      showToast(`👑 Título "${data.title}" ativado!`, "gold");
    }
  } catch {}
}

// ── NO FAP ────────────────────────────────────────
function renderNoFap() {
  if (!playerData) return;
  const nf = playerData.nofap || {};
  const container = document.getElementById("nofap-content");
  if (!container) return;

  const history = (nf.history || []).slice(-10).reverse();
  container.innerHTML = `
    <div class="nofap-counter-card">
      <div class="nofap-days-big">${nf.clean_days || 0}</div>
      <div class="nofap-days-label">DIAS LIMPOS</div>
      <div class="nofap-record">🏆 Recorde Pessoal: ${nf.record || 0} dias</div>
      <div class="nofap-buttons">
        ${nf.active
          ? `<button class="btn-nofap-fall" onclick="nofapFall()">⚠️ /comunicar_queda</button>
             <button class="btn-nofap-checkin" onclick="nofapCheckin()">✓ REGISTRAR DIA</button>`
          : `<button class="btn-nofap-checkin" style="width:100%" onclick="nofapStart()">⚡ ATIVAR MÓDULO NO FAP</button>`
        }
      </div>
    </div>
    <div class="nofap-history">
      <div class="nofap-history-title">[HISTÓRICO DE RECAÍDAS]</div>
      ${history.length === 0
        ? `<div class="nofap-history-item" style="color:var(--neon-green)">Nenhuma recaída registrada.</div>`
        : history.map(h => `
            <div class="nofap-history-item">
              📅 ${formatDate(h.date)} — ${h.days_reached} dias alcançados
            </div>
          `).join("")
      }
    </div>
  `;
}

async function nofapStart() {
  try {
    await fetch(`${API}/nofap/start`, { method: "POST" });
    await loadAndShowMain();
    showSection("nofap");
    showToast("[SISTEMA] Módulo NO FAP ativado. Vamos nessa.", "green");
  } catch {}
}

async function nofapCheckin() {
  try {
    const res = await fetch(`${API}/nofap/checkin`, { method: "POST" });
    const data = await res.json();
    playerData = data.player || playerData;
    if (playerData.nofap) playerData.nofap.clean_days = data.clean_days;
    renderNoFap();
    showToast(data.message || "[SISTEMA] Dia registrado.", "green");
    if (data.new_achievements && data.new_achievements.length > 0) {
      setTimeout(() => showAchievementModal(data.new_achievements[0]), 800);
    }
  } catch {}
}

async function nofapFall() {
  if (!confirm("Registrar queda? Seu contador será resetado, mas XP e Rank serão mantidos.")) return;
  try {
    const res = await fetch(`${API}/nofap/fall`, { method: "POST" });
    const data = await res.json();
    playerData = data.player || playerData;
    renderNoFap();
    showToast(data.message, "red");
  } catch {}
}

// ── RELATÓRIOS ────────────────────────────────────
async function loadReport(period, btn) {
  if (btn) {
    document.querySelectorAll(".report-tab").forEach(t => t.classList.remove("active"));
    btn.classList.add("active");
  }
  try {
    const res = await fetch(`${API}/reports/${period}`);
    const report = await res.json();
    renderReport(report);
  } catch {}
}

function renderReport(report) {
  const container = document.getElementById("report-content");
  if (!container) return;
  const attrs = report.attributes_snapshot || {};
  container.innerHTML = `
    <div class="report-card">
      <div class="report-card-title">[VISÃO GERAL]</div>
      ${reportRow("Jogador", report.player_name)}
      ${reportRow("Nível", report.level)}
      ${reportRow("Rank", report.rank)}
      ${reportRow("XP Total", formatNum(report.xp_total))}
      ${reportRow("Missões Total", formatNum(report.missions_total))}
      ${reportRow("Sequência", `${report.current_streak} dias`)}
    </div>
    <div class="report-card">
      <div class="report-card-title">[ATRIBUTOS]</div>
      ${Object.entries(attrs).map(([k, v]) =>
        reportRow(`${ATTR_ICONS[k]} ${ATTR_NAMES_BR[k]}`, `${(v || 0).toFixed(1)}`)
      ).join("")}
    </div>
    <div class="report-card">
      <div class="report-card-title">[DESTAQUES]</div>
      ${report.highlights && report.highlights.length > 0
        ? report.highlights.map(h => `<div class="report-highlight">✅ ${h}</div>`).join("")
        : `<div class="report-highlight" style="color:var(--text-muted)">Sem destaques ainda.</div>`}
    </div>
    <div class="report-card">
      <div class="report-card-title">[ALERTAS DO SISTEMA]</div>
      ${report.warnings && report.warnings.length > 0
        ? report.warnings.map(w => `<div class="report-warning">⚠️ ${w}</div>`).join("")
        : `<div class="report-highlight">Nenhum alerta. Continue assim!</div>`}
    </div>
  `;
}

function reportRow(label, val) {
  return `<div class="report-row">
    <span class="report-row-label">${label}</span>
    <span class="report-row-val">${val}</span>
  </div>`;
}

// ── MENSAGENS DO SISTEMA ──────────────────────────
async function loadSystemMessages() {
  try {
    const res = await fetch(`${API}/system/message`);
    const data = await res.json();
    const msgs = data.messages || [data.message];
    const container = document.getElementById("system-messages-list");
    if (!container) return;
    container.innerHTML = "";
    msgs.forEach(msg => {
      const el = document.createElement("div");
      const isWarning = msg.includes("ALERTA") || msg.includes("caiu") || msg.includes("queda");
      const isGold = msg.includes("dias") && !isWarning;
      el.className = `system-msg${isWarning ? " warning" : isGold ? " gold" : ""}`;
      el.textContent = msg;
      container.appendChild(el);
    });
  } catch {}
}

// ── NOTIFICAÇÕES (POLLING) ────────────────────────
async function pollNotifications() {
  try {
    const res = await fetch(`${API}/notifications`);
    const data = await res.json();
    (data.notifications || []).forEach(msg => showToast(msg, detectToastColor(msg)));
  } catch {}
}

function detectToastColor(msg) {
  if (msg.includes("LEVEL") || msg.includes("CONQUISTA") || msg.includes("XP")) return "blue";
  if (msg.includes("RANK"))      return "purple";
  if (msg.includes("ALERTA") || msg.includes("caiu")) return "red";
  if (msg.includes("título") || msg.includes("Título") || msg.includes("Ouro")) return "gold";
  if (msg.includes("dias"))      return "green";
  return "blue";
}

// ── MODAIS ────────────────────────────────────────
function showLevelUpModal(level) {
  set("levelup-level", `Nível ${level}`);
  set("levelup-reward", `+3 Pontos de Atributo | +${level * 50} Ouro`);
  openModal("levelup-modal");
}

function showRankUpModal(rank) {
  set("rankup-rank", rank);
  set("rankup-desc", "Nova classificação registrada no Sistema.");
  openModal("rankup-modal");
}

function showAchievementModal(name) {
  set("ach-modal-name", name);
  set("ach-modal-icon", "🏅");
  openModal("achievement-modal");
}

function openModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.add("active");
}

function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.remove("active");
}

// ── TOASTS ────────────────────────────────────────
function showToast(msg, color = "blue") {
  const container = document.getElementById("notification-container");
  if (!container) return;
  const toast = document.createElement("div");
  toast.className = `notification-toast ${color}`;
  toast.textContent = msg;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add("fade-out");
    setTimeout(() => toast.remove(), 500);
  }, 4000);
}

// ── HELPERS ───────────────────────────────────────
function set(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

function setPct(id, pct) {
  const el = document.getElementById(id);
  if (el) el.style.width = `${Math.min(100, Math.max(0, pct))}%`;
}

function formatNum(n) {
  return Number(n || 0).toLocaleString("pt-BR");
}

function formatDate(iso) {
  if (!iso) return "—";
  try {
    return new Date(iso).toLocaleDateString("pt-BR");
  } catch { return iso; }
}

function getTitleName(tid) {
  const map = {
    iniciante:"Iniciante",pioneiro:"Pioneiro",aprendiz:"Aprendiz",
    persistente:"Persistente",disciplinado:"Disciplinado",estudioso:"Estudioso",
    focado:"Focado",organizado:"Organizado",lutador:"Lutador",guerreiro:"Guerreiro",
    sobrevivente:"Sobrevivente",determinado:"Determinado",estrategista:"Estrategista",
    guardiao:"Guardião",conquistador:"Conquistador",mestre_disciplina:"Mestre da Disciplina",
    mestre_mente:"Mestre da Mente",mestre_corpo:"Mestre do Corpo",lenda_viva:"Lenda Viva",
    ascendente:"Ascendente",imperador:"Imperador da Disciplina",atleta:"Atleta",
    academico:"Acadêmico",saudavel:"Saudável",energizado:"Energizado",
    carismatico:"Carismático",belo:"Belo",incansavel:"Incansável",
    inabalavel:"Inabalável",monolito:"Monólito",eterno:"Eterno",
    vencedor:"Vencedor",veterano:"Veterano",elite:"Elite",lendario:"Lendário",
    monarca:"Monarca",soberano:"Soberano",ultimo_heroi:"Último Herói",
    filho_evolucao:"Filho da Evolução",ascendido:"Ascendido",
    portador_destino:"Portador do Destino",rei_constancia:"Rei da Constância",
    alem_limite:"Além do Limite",sombra_eterna:"Sombra Eterna",despertar:"O Despertar",
    titan:"Titã",sabio:"Sábio",lider:"Líder",imparavel:"Imparável",
    resiliente:"Resiliente",crescente:"Crescente",consistente:"Consistente",
    madrugador:"Madrugador",noturno:"Noturno",perfeicionista:"Perfeccionista",
    harmonioso:"Harmonioso",completo:"Ser Completo",treinador:"Treinador",
    scholar:"Scholar",monge:"Monge",cuidador:"Cuidador",
  };
  return map[tid] || tid;
}

function getRankProgressPct(p) {
  const RANK_THRESHOLDS = {
    "D":0,"D+":500,"C-":1200,"C":2500,"C+":4500,"B-":7000,"B":10000,"B+":14000,
    "A-":19000,"A":25000,"A+":33000,"S-":43000,"S":55000,"S+":70000,
    "SS":90000,"SS+":115000,"SSS":150000,"Z":200000,"Z+":275000,"Z++":375000,
    "EX":500000,"Ω":750000,
  };
  const RANKS = Object.keys(RANK_THRESHOLDS);
  const idx = RANKS.indexOf(p.rank);
  if (idx < 0 || idx >= RANKS.length - 1) return 1.0;
  const cur = RANK_THRESHOLDS[p.rank] || 0;
  const nxt = RANK_THRESHOLDS[RANKS[idx + 1]] || cur + 1;
  return Math.max(0, Math.min(1, (p.xp - cur) / (nxt - cur)));
}

function getNextRank(rank) {
  const RANKS = ["D","D+","C-","C","C+","B-","B","B+","A-","A","A+","S-","S","S+","SS","SS+","SSS","Z","Z+","Z++","EX","Ω"];
  const idx = RANKS.indexOf(rank);
  return idx < RANKS.length - 1 ? RANKS[idx + 1] : "MAX";
}
