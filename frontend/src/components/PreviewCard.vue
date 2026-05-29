<template>
  <article class="preview-card" :style="style">
    <header class="preview-head">
      <div>
        <h3>{{ platform.label }}</h3>
        <p>{{ platform.tone }}</p>
      </div>
      <button class="btn ghost small" type="button" @click="copyContent">
        {{ ui.t("actions.copy") }}
      </button>
    </header>
    <img
      v-if="content.cover"
      class="preview-cover"
      :src="content.cover"
      :alt="ui.t('fields.cover')"
    />
    <label class="field">
      <span>{{ ui.t("fields.title") }}</span>
      <input v-model="content.title" type="text" />
    </label>
    <label class="field">
      <span>{{ mainLabel }}</span>
      <textarea v-model="content[mainField]" rows="5"></textarea>
    </label>
    <label v-if="content.summary" class="field">
      <span>{{ ui.t("fields.summary") }}</span>
      <textarea v-model="content.summary" rows="2"></textarea>
    </label>
    <label v-if="content.category" class="field">
      <span>{{ ui.t("fields.category") }}</span>
      <input v-model="content.category" type="text" />
    </label>
    <label v-if="hasVideo" class="field">
      <span>{{ ui.t("fields.video") }}</span>
      <input :value="videoText" type="text" @input="updateVideo($event.target.value)" />
    </label>
    <label v-if="hasImages" class="field">
      <span>{{ ui.t("fields.images") }}</span>
      <input :value="imagesText" type="text" @input="updateImages($event.target.value)" />
    </label>
    <label class="field">
      <span>{{ ui.t("fields.tags") }}</span>
      <input :value="tagText" type="text" @input="updateTags($event.target.value)" />
    </label>
  </article>
</template>

<script setup>
import { computed, inject } from "vue";

const ui = inject("ui");

const props = defineProps({
  platform: {
    type: Object,
    required: true
  },
  content: {
    type: Object,
    required: true
  },
  style: {
    type: Object,
    default: () => ({})
  }
});

const mainField = computed(() => {
  if (Object.prototype.hasOwnProperty.call(props.content, "description")) {
    return "description";
  }
  return "content";
});

const mainLabel = computed(() => {
  return mainField.value === "description"
    ? ui.t("fields.description")
    : ui.t("fields.content");
});

const tagText = computed(() => {
  return (props.content.tags || []).join(", ");
});

const updateTags = (value) => {
  props.content.tags = value
    .split(/[，,]/)
    .map((tag) => tag.trim())
    .filter(Boolean);
};

const hasImages = computed(() => Array.isArray(props.content.images));
const hasVideo = computed(
  () => typeof props.content.video !== "undefined" || Array.isArray(props.content.videos)
);

const imagesText = computed(() => {
  return (props.content.images || []).join(", ");
});

const videoText = computed(() => {
  if (props.content.video) {
    return props.content.video;
  }
  return (props.content.videos || [""])[0] || "";
});

const updateImages = (value) => {
  props.content.images = value
    .split(/[，,]/)
    .map((item) => item.trim())
    .filter(Boolean);
};

const updateVideo = (value) => {
  const cleaned = value.trim();
  props.content.video = cleaned;
  props.content.videos = cleaned ? [cleaned] : [];
};

const copyContent = async () => {
  const parts = [
    `${ui.t("fields.title")}: ${props.content.title || ""}`,
    `${mainLabel.value}: ${props.content[mainField.value] || ""}`,
    `${ui.t("fields.tags")}: ${tagText.value}`
  ];
  if (props.content.summary) {
    parts.push(`${ui.t("fields.summary")}: ${props.content.summary}`);
  }
  const payload = parts.join("\n");
  if (navigator.clipboard) {
    await navigator.clipboard.writeText(payload);
  }
};
</script>
