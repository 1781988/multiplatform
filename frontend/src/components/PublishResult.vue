<template>
  <section v-if="results.length" class="result-panel">
    <h3>{{ ui.t("sections.results") }}</h3>
    <div class="result-grid">
      <article v-for="result in results" :key="result.platform" class="result-card">
        <div class="result-header">
          <span class="result-title">{{ labelFor(result.platform) }}</span>
          <span class="pill" :class="result.status">{{ statusLabel(result.status) }}</span>
        </div>
        <p class="result-message">{{ messageFor(result) }}</p>
        <p class="result-time">{{ result.publish_time }}</p>
      </article>
    </div>
  </section>
</template>

<script setup>
import { inject } from "vue";

const ui = inject("ui");

const props = defineProps({
  results: {
    type: Array,
    default: () => []
  }
});

const statusLabel = (status) => ui.t(`status.${status}`) || status;
const labelFor = (platform) => ui.t(`platforms.${platform}`) || platform;

const messageFor = (result) => {
  if (ui.locale.value === "zh") {
    return result.message;
  }
  if (result.status === "success") {
    return ui.t("messages.publishSuccess");
  }
  return ui.t("messages.publishFailed");
};
</script>
