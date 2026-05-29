<template>
  <header class="topbar">
    <div class="topbar-steps">
      <div
        v-for="(step, index) in steps"
        :key="step.key"
        class="step-item"
        :class="{
          active: index + 1 === activeStep,
          done: index + 1 < activeStep
        }"
      >
        <div class="step-dot">
          <span v-if="index + 1 < activeStep">&#10003;</span>
          <span v-else>{{ index + 1 }}</span>
        </div>
        <span class="step-label">{{ step.label }}</span>
        <span v-if="index < steps.length - 1" class="step-line"></span>
      </div>
    </div>

    <div class="topbar-actions">
      <button class="action-btn" :title="ui.t('topbar.theme')">&#9788;</button>
      <button class="action-btn notify-btn" :title="ui.t('topbar.notifications')">
        &#128276;
        <span v-if="notifyCount" class="notify-badge">{{ notifyCount }}</span>
      </button>
      <div class="user-info">
        <div class="user-avatar">{{ userInitial }}</div>
        <div class="user-meta">
          <span class="user-name">{{ userName || ui.t('topbar.defaultUser') }}</span>
          <span class="user-plan">{{ ui.t('topbar.plan') }}</span>
        </div>
        <span class="user-arrow">&#9662;</span>
      </div>
      <div class="lang-toggle">
        <button
          class="lang-btn"
          :class="{ active: ui.locale.value === 'zh' }"
          @click="ui.locale.value = 'zh'; saveLocale('zh')"
        >中</button>
        <button
          class="lang-btn"
          :class="{ active: ui.locale.value === 'en' }"
          @click="ui.locale.value = 'en'; saveLocale('en')"
        >EN</button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, inject } from "vue";

const ui = inject("ui");

const props = defineProps({
  activeStep: { type: Number, default: 1 },
  userName: { type: String, default: "" },
  notifyCount: { type: Number, default: 0 }
});

const steps = computed(() => [
  { key: "create", label: ui.t("topbar.step1") },
  { key: "adapt", label: ui.t("topbar.step2") },
  { key: "preview", label: ui.t("topbar.step3") },
  { key: "publish", label: ui.t("topbar.step4") }
]);

const userInitial = computed(() =>
  (props.userName || ui.t("topbar.defaultUser")).charAt(0)
);

const saveLocale = (value) => {
  if (typeof localStorage !== "undefined") {
    localStorage.setItem("locale", value);
  }
};
</script>

<style scoped>
.topbar {
  position: fixed;
  top: 0;
  left: 220px;
  right: 0;
  height: 56px;
  background: #fff;
  border-bottom: 1px solid #edf0f5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 40;
}

.topbar-steps {
  display: flex;
  align-items: center;
  gap: 0;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  font-size: 0.82rem;
  color: #b0b8c1;
  white-space: nowrap;
}

.step-item.active {
  color: #f26430;
}

.step-item.done {
  color: #1a9aa6;
}

.step-dot {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #f0f2f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  flex-shrink: 0;
}

.step-item.active .step-dot {
  background: #ff7b4a;
  color: #fff;
}

.step-item.done .step-dot {
  background: #1a9aa6;
  color: #fff;
}

.step-line {
  width: 32px;
  height: 2px;
  background: #e5e7eb;
  margin: 0 8px;
  flex-shrink: 0;
}

.step-item.done .step-line {
  background: #1a9aa6;
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.action-btn {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  border: 1px solid #edf0f5;
  background: #fff;
  cursor: pointer;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
}

.action-btn:hover {
  background: #f8f4f0;
}

.notify-btn {
  position: relative;
}

.notify-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #ff7b4a;
  color: #fff;
  font-size: 0.6rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px 4px 4px;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.15s;
}

.user-info:hover {
  background: #f8f4f0;
}

.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  font-weight: 700;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-meta {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.user-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: #1c1c1c;
}

.user-plan {
  font-size: 0.65rem;
  color: #f26430;
  font-weight: 500;
}

.user-arrow {
  font-size: 0.6rem;
  color: #9ca3af;
}

.lang-toggle {
  display: flex;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #edf0f5;
}

.lang-btn {
  padding: 5px 10px;
  border: none;
  background: #fff;
  font-size: 0.75rem;
  font-weight: 600;
  color: #b0b8c1;
  cursor: pointer;
  transition: all 0.15s;
}

.lang-btn.active {
  background: #ff7b4a;
  color: #fff;
}

.lang-btn + .lang-btn {
  border-left: 1px solid #edf0f5;
}
</style>
