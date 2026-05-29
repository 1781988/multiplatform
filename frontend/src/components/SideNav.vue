<template>
  <aside class="sidenav">
    <div class="sidenav-brand">
      <div class="brand-icon">M</div>
      <div class="brand-text">
        <span class="brand-zh">{{ ui.t("nav.brand") }}</span>
        <span class="brand-en">MultiPost AI</span>
      </div>
    </div>

    <nav class="sidenav-menu">
      <button
        v-for="item in menuItems"
        :key="item.key"
        class="menu-item"
        :class="{ active: activeMenu === item.key }"
        @click="$emit('update:activeMenu', item.key)"
      >
        <span class="menu-icon" v-html="item.icon"></span>
        <span class="menu-label">{{ item.label }}</span>
        <span v-if="item.badge" class="menu-badge">{{ item.badge }}</span>
      </button>
    </nav>

    <div class="sidenav-stats">
      <div class="stats-header">{{ ui.t("nav.statsTitle") }}</div>
      <div class="stats-row">
        <span class="stats-count">{{ publishedToday }} / {{ dailyLimit }}</span>
      </div>
      <div class="stats-bar">
        <div class="stats-fill" :style="{ width: statsPercent + '%' }"></div>
      </div>
      <div class="stats-detail">
        {{ ui.t("nav.publishedToday", { count: publishedToday }) }}
      </div>
      <div class="stats-detail">
        {{ ui.t("nav.remainingToday", { count: dailyLimit - publishedToday }) }}
      </div>
    </div>

    <div class="sidenav-upgrade">
      <div class="upgrade-title">{{ ui.t("nav.upgradeTitle") }}</div>
      <div class="upgrade-desc">{{ ui.t("nav.upgradeDesc") }}</div>
      <button class="upgrade-btn">{{ ui.t("nav.upgradeBtn") }}</button>
    </div>
  </aside>
</template>

<script setup>
import { computed, inject } from "vue";

const ui = inject("ui");

const props = defineProps({
  activeMenu: { type: String, default: "create" },
  publishedToday: { type: Number, default: 0 },
  dailyLimit: { type: Number, default: 10 }
});

defineEmits(["update:activeMenu"]);

const statsPercent = computed(() =>
  Math.min(100, Math.round((props.publishedToday / props.dailyLimit) * 100))
);

const menuItems = computed(() => [
  { key: "create", icon: "&#9998;", label: ui.t("nav.create") },
  { key: "preview", icon: "&#9744;", label: ui.t("nav.preview") },
  { key: "history", icon: "&#128196;", label: ui.t("nav.history") },
  { key: "accounts", icon: "&#128100;", label: ui.t("nav.accounts") },
  { key: "media", icon: "&#128444;", label: ui.t("nav.media") },
  { key: "aiSettings", icon: "&#9881;", label: ui.t("nav.aiSettings") },
  { key: "help", icon: "&#63;", label: ui.t("nav.help") }
]);
</script>

<style scoped>
.sidenav {
  width: 220px;
  min-width: 220px;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  background: #fff;
  border-right: 1px solid #edf0f5;
  display: flex;
  flex-direction: column;
  padding: 20px 14px;
  overflow-y: auto;
  z-index: 50;
}

.sidenav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 6px 20px;
  border-bottom: 1px solid #f0f2f5;
  margin-bottom: 16px;
}

.brand-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, #ff7b4a, #f26430);
  color: #fff;
  font-weight: 800;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-zh {
  font-weight: 700;
  font-size: 1.05rem;
  color: #1c1c1c;
  line-height: 1.3;
}

.brand-en {
  font-size: 0.7rem;
  color: #8c8c8c;
  font-weight: 500;
  letter-spacing: 0.04em;
}

.sidenav-menu {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 12px;
  border-radius: 10px;
  border: none;
  background: transparent;
  color: #4a4a4a;
  font-size: 0.88rem;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  text-align: left;
}

.menu-item:hover {
  background: #f8f4f0;
}

.menu-item.active {
  background: rgba(255, 123, 74, 0.1);
  color: #f26430;
  font-weight: 600;
}

.menu-icon {
  width: 20px;
  text-align: center;
  font-size: 0.95rem;
}

.menu-label {
  flex: 1;
}

.menu-badge {
  background: #ff7b4a;
  color: #fff;
  font-size: 0.65rem;
  padding: 2px 7px;
  border-radius: 999px;
  font-weight: 600;
}

.sidenav-stats {
  margin-top: 16px;
  padding: 14px;
  border-radius: 12px;
  background: #fafbfc;
  border: 1px solid #edf0f5;
}

.stats-header {
  font-weight: 600;
  font-size: 0.78rem;
  color: #6b7280;
  margin-bottom: 8px;
}

.stats-row {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1c1c1c;
}

.stats-bar {
  height: 4px;
  background: #e5e7eb;
  border-radius: 4px;
  margin: 8px 0;
  overflow: hidden;
}

.stats-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff7b4a, #f26430);
  border-radius: 4px;
  transition: width 0.4s ease;
}

.stats-detail {
  font-size: 0.72rem;
  color: #9ca3af;
  line-height: 1.5;
}

.sidenav-upgrade {
  margin-top: 12px;
  padding: 14px;
  border-radius: 12px;
  background: linear-gradient(135deg, #f8f4f0 0%, #fdf2ec 100%);
  border: 1px solid rgba(255, 123, 74, 0.15);
}

.upgrade-title {
  font-weight: 700;
  font-size: 0.85rem;
  color: #1c1c1c;
  margin-bottom: 4px;
}

.upgrade-desc {
  font-size: 0.72rem;
  color: #8c8c8c;
  margin-bottom: 10px;
  line-height: 1.4;
}

.upgrade-btn {
  width: 100%;
  padding: 7px 0;
  border-radius: 8px;
  border: none;
  background: linear-gradient(135deg, #ff7b4a, #f26430);
  color: #fff;
  font-weight: 600;
  font-size: 0.78rem;
  cursor: pointer;
  transition: opacity 0.2s;
}

.upgrade-btn:hover {
  opacity: 0.9;
}
</style>
