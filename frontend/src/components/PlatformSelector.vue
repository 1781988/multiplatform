<template>
  <div class="platform-card">
    <div class="card-head">
      <div>
        <h3 class="card-title">{{ ui.t("cards.platformTitle") }}</h3>
        <p class="card-sub">{{ ui.t("cards.platformSub") }}</p>
      </div>
    </div>
    <div class="platform-grid">
      <button
        v-for="option in options"
        :key="option.id"
        class="platform-item"
        :class="[option.id, { active: selected.includes(option.id) }]"
        type="button"
        @click="toggle(option.id)"
      >
        <span class="platform-check" v-if="selected.includes(option.id)">&#10003;</span>
        <span class="platform-icon" v-html="platformIcon(option.id)"></span>
        <span class="platform-name">{{ option.label }}</span>
        <span class="platform-type">{{ option.tone }}</span>
      </button>
    </div>
    <div class="more-platforms">
      <span class="more-label">{{ ui.t("platforms.more") }}</span>
      <div class="more-tags">
        <span class="more-tag">微博</span>
        <span class="more-tag">抖音</span>
        <span class="more-tag">头条</span>
        <span class="more-tag">快手</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject } from "vue";

const ui = inject("ui");

const props = defineProps({
  options: { type: Array, default: () => [] },
  selected: { type: Array, default: () => [] }
});

const emit = defineEmits(["update:selected"]);

const toggle = (id) => {
  const next = new Set(props.selected);
  if (next.has(id)) next.delete(id);
  else next.add(id);
  emit("update:selected", Array.from(next));
};

const platformIcon = (id) => {
  const icons = {
    wechat: "&#128172;",
    zhihu: "&#10068;",
    bilibili: "&#127916;",
    xiaohongshu: "&#128149;"
  };
  return icons[id] || "&#9679;";
};
</script>

<style scoped>
.platform-card {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #edf0f5;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
  padding: 20px 24px 24px;
}

.card-head { margin-bottom: 16px; }
.card-title { margin: 0 0 4px; font-size: 1.15rem; font-weight: 700; }
.card-sub { margin: 0; font-size: 0.82rem; color: #8c8c8c; }

.platform-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.platform-item {
  position: relative;
  padding: 14px 12px;
  border-radius: 14px;
  border: 2px solid transparent;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  transition: transform 0.2s, box-shadow 0.2s, border 0.2s;
  text-align: center;
}

.platform-item.wechat { background: rgba(7, 193, 96, 0.06); }
.platform-item.zhihu { background: rgba(0, 102, 255, 0.06); }
.platform-item.bilibili { background: rgba(251, 114, 153, 0.06); }
.platform-item.xiaohongshu { background: rgba(255, 36, 66, 0.06); }

.platform-item.active {
  border-color: #ff7b4a;
  box-shadow: 0 4px 16px rgba(255, 123, 74, 0.16);
  transform: translateY(-2px);
}

.platform-item.wechat.active { border-color: #07c160; box-shadow: 0 4px 16px rgba(7, 193, 96, 0.18); }
.platform-item.zhihu.active { border-color: #0066ff; box-shadow: 0 4px 16px rgba(0, 102, 255, 0.18); }
.platform-item.bilibili.active { border-color: #fb7299; box-shadow: 0 4px 16px rgba(251, 114, 153, 0.18); }
.platform-item.xiaohongshu.active { border-color: #ff2442; box-shadow: 0 4px 16px rgba(255, 36, 66, 0.18); }

.platform-check {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ff7b4a;
  color: #fff;
  font-size: 0.65rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.platform-item.wechat .platform-check { background: #07c160; }
.platform-item.zhihu .platform-check { background: #0066ff; }
.platform-item.bilibili .platform-check { background: #fb7299; }
.platform-item.xiaohongshu .platform-check { background: #ff2442; }

.platform-icon { font-size: 1.4rem; }
.platform-name { font-weight: 700; font-size: 0.88rem; color: #1c1c1c; }
.platform-type { font-size: 0.7rem; color: #8c8c8c; line-height: 1.3; }

.more-platforms {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid #f0f2f5;
}

.more-label {
  font-size: 0.75rem;
  color: #9ca3af;
  display: block;
  margin-bottom: 8px;
}

.more-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.more-tag {
  padding: 4px 10px;
  border-radius: 6px;
  background: #f0f2f5;
  color: #9ca3af;
  font-size: 0.7rem;
  font-weight: 500;
}
</style>
