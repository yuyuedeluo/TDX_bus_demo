<script setup>
import axios from "axios";
import { computed, reactive } from "vue";

const apiBase = import.meta.env.VITE_API_BASE || "http://localhost:8000";
const defaultCity = import.meta.env.VITE_DEFAULT_CITY || "Taipei";

const state = reactive({
  route: "",
  city: defaultCity,
  loading: false,
  error: "",
  directions: [],
  selectedDirection: 0,
  lastUpdated: "",
});

const hasData = computed(() => state.directions.length > 0);
const selectedBucket = computed(() =>
  state.directions.find((d) => d.direction === state.selectedDirection) || state.directions[0]
);

const sortedDirections = computed(() =>
  [...state.directions].sort((a, b) => (a.direction || 0) - (b.direction || 0))
);

function etaLabel(stop) {
  const s = stop.stop_status;
  if (s === 1) return "尚未發車";
  if (s === 2) return "交管不停靠";
  if (s === 3) return "末班已過";
  if (s === 4) return "未營運";

  const secs = stop.estimate_seconds;
  if (secs === null || secs === undefined) return "—";
  if (secs <= 30) return "進站";
  if (secs < 90) return "1 分";
  const mins = Math.round(secs / 60);
  return `${mins} 分`;
}

function badgeTone(stop) {
  const status = stop.stop_status;
  if (status === 2 || status === 4) return "badge muted";
  if (status === 3) return "badge warning";
  const secs = stop.estimate_seconds;
  if (secs !== null && secs <= 90) return "badge active";
  return "badge";
}

function directionLabel(d) {
  if (d === 0) return "去程"; //0
  if (d === 1) return "返程"; //1
  return `方向 ${d ?? "-"}`;
}

async function fetchData() {
  state.error = "";
  if (!state.route.trim()) {
    state.error = "請輸入路線號碼";
    return;
  }

  state.loading = true;
  try {
    const resp = await axios.get(
      `${apiBase}/api/routes/${encodeURIComponent(state.route.trim())}/stop-etas`,
      {
        params: { city: state.city },
      }
    );
    state.directions = resp.data?.directions || [];
    state.lastUpdated = resp.data?.updated_at || "";
    if (state.directions.length) {
      state.selectedDirection = state.directions[0].direction ?? 0;
    }
    if (!state.directions.length) {
      state.error = "查無資料，請確認路線與城市";
    }
  } catch (err) {
    state.error = err?.response?.data?.detail || "查詢失敗，請稍後再試";
  } finally {
    state.loading = false;
  }
}
</script>

<template>
  <div class="hero">
    <div>
      <p class="eyebrow">TDX • Bus ETA</p>
      <h1>查詢公車即時到站</h1>
      <p class="lead">
        輸入路線（如 307、236區、綠1），即時查看去程 / 回程每站預估到站時間。資料來源：
        /v2/Bus/EstimatedTimeOfArrival 與 /v2/Bus/StopOfRoute。
      </p>
      <div class="actions">
        <input
          v-model="state.route"
          class="input route-input"
          placeholder="輸入路線號碼"
          inputmode="numeric"
        />
        <select v-model="state.city" class="input city-select">
          <option value="Taipei">Taipei (台北市)</option>
          <option value="NewTaipei">NewTaipei (新北市)</option>
          <option value="Taoyuan">Taoyuan (桃園市)</option>
          <option value="Taichung">Taichung (台中市)</option>
          <option value="Tainan">Tainan (台南市)</option>
          <option value="Kaohsiung">Kaohsiung (高雄市)</option>
        </select>
        <button class="primary" :disabled="state.loading" @click="fetchData">
          {{ state.loading ? "查詢中..." : "查詢" }}
        </button>
      </div>
      <p class="hint">城市預設為 {{ defaultCity }}，可依 TDX City 代碼調整。</p>
    </div>
  </div>

  <div class="card content">
    <div class="content-head">
      <div>
        <p class="eyebrow">路線</p>
        <h2 class="route-title">
          {{ state.route || "" }}
          <span class="city">{{ state.city }}</span>
        </h2>
        <p class="timestamp" v-if="state.lastUpdated">更新：{{ state.lastUpdated }}</p>
      </div>
      <div class="direction-tabs" v-if="sortedDirections.length">
        <button
          v-for="dir in sortedDirections"
          :key="dir.direction ?? -1"
          :class="['tab', state.selectedDirection === dir.direction ? 'active' : '']"
          @click="state.selectedDirection = dir.direction"
        >
          {{ directionLabel(dir.direction) }}
        </button>
      </div>
    </div>

    <div v-if="state.error" class="alert">{{ state.error }}</div>
    <div v-else-if="state.loading" class="loading">讀取中…</div>
    <div v-else-if="hasData && selectedBucket">
      <div class="stop-list">
        <div v-for="stop in selectedBucket.stops" :key="stop.stop_uid" class="stop-row">
          <div :class="badgeTone(stop)">{{ etaLabel(stop) }}</div>
          <div class="timeline">
            <div class="dot"></div>
            <div class="line"></div>
          </div>
          <div class="stop-info">
            <div class="name-zh">{{ stop.name?.zh }}</div>
            <div class="name-en">{{ stop.name?.en }}</div>
            <div class="meta">
              Seq {{ stop.stop_sequence || "-" }} · UID {{ stop.stop_uid || "-" }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="empty">請輸入路線並點擊查詢。</div>
  </div>
</template>

<style scoped>
.hero {
  display: flex;
  gap: 28px;
  padding: 8px 12px 28px;
}

.eyebrow {
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-size: 12px;
  color: #5c6f91;
  margin: 0 0 4px;
}

h1 {
  margin: 0;
  font-size: 34px;
  color: #0d1a2d;
}

.lead {
  color: #42526b;
  line-height: 1.6;
  max-width: 720px;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 14px;
}

.input {
  border: 1px solid #d8deeb;
  border-radius: 12px;
  padding: 12px 14px;
  font-size: 16px;
  min-width: 200px;
  background: #fff;
  transition: border 0.2s, box-shadow 0.2s;
}

.input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.18);
}

.route-input {
  flex: 1;
}

.city-select {
  width: 200px;
}

.primary {
  background: linear-gradient(135deg, #2563eb, #38bdf8);
  border: none;
  color: #fff;
  border-radius: 12px;
  padding: 12px 18px;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 12px 30px rgba(37, 99, 235, 0.25);
  transition: transform 0.15s ease, box-shadow 0.2s ease;
}

.primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}

.primary:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 16px 36px rgba(37, 99, 235, 0.32);
}

.hint {
  color: #6b7a99;
  margin-top: 6px;
  font-size: 13px;
}

.card.content {
  margin-top: 10px;
  padding: 20px 18px;
}

.content-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.route-title {
  margin: 6px 0 6px;
  font-size: 26px;
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.city {
  font-size: 16px;
  color: #607089;
}

.timestamp {
  margin: 0;
  color: #607089;
}

.direction-tabs {
  display: flex;
  gap: 8px;
}

.tab {
  border: 1px solid #d8deeb;
  border-radius: 12px;
  padding: 10px 14px;
  background: #f6f8fc;
  color: #294057;
  font-weight: 600;
  min-width: 120px;
}

.tab.active {
  background: linear-gradient(135deg, #2563eb, #38bdf8);
  color: white;
  border-color: transparent;
  box-shadow: 0 12px 28px rgba(37, 99, 235, 0.24);
}

.alert {
  background: #fff6f2;
  color: #b54708;
  border: 1px solid #ffd4bd;
  padding: 12px 14px;
  border-radius: 12px;
}

.loading,
.empty {
  color: #5c6f91;
  padding: 12px 0;
}

.stop-list {
  margin-top: 12px;
  display: grid;
  gap: 12px;
}

.stop-row {
  display: grid;
  grid-template-columns: 110px 26px 1fr;
  align-items: center;
  gap: 14px;
  padding: 14px 12px;
  border: 1px solid #e6ecf5;
  border-radius: 14px;
  background: linear-gradient(135deg, #fff, #f9fbff);
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  padding: 6px 12px;
  background: #e8edf7;
  color: #1c2c46;
  font-weight: 700;
  min-width: 72px;
}

.badge.active {
  background: #22c55e1a;
  color: #0f9d46;
}

.badge.warning {
  background: #fef2c0;
  color: #915103;
}

.badge.muted {
  background: #ececf1;
  color: #6f7285;
}

.timeline {
  display: flex;
  align-items: center;
  gap: 6px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #2563eb;
}

.line {
  height: 1px;
  flex: 1;
  background: #cbd5e1;
}

.stop-info .name-zh {
  font-weight: 700;
  color: #0f172a;
}

.stop-info .name-en {
  color: #5c6f91;
  font-size: 13px;
}

.stop-info .meta {
  color: #7b879e;
  font-size: 12px;
  margin-top: 2px;
}

@media (max-width: 700px) {
  .stop-row {
    grid-template-columns: 1fr;
    align-items: start;
  }

  .timeline {
    display: none;
  }

  .route-title {
    font-size: 22px;
  }
}
</style>
