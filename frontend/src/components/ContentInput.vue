<template>
  <div class="editor-card">
    <div class="card-head">
      <div>
        <h3 class="card-title">{{ ui.t("cards.createTitle") }}</h3>
        <p class="card-sub">{{ ui.t("cards.createSub") }}</p>
      </div>
      <button class="smart-btn" :disabled="!useAi" @click="$emit('smartRewrite')">
        <span class="smart-icon">&#9889;</span>
        {{ ui.t("actions.smartRewrite") }}
      </button>
    </div>

    <div class="editor-body">
      <div class="field-group">
        <div class="field-header">
          <span class="field-label">{{ ui.t("fields.title") }}</span>
          <span class="field-count">{{ title.length }} / 100</span>
        </div>
        <input
          class="title-input"
          :value="title"
          type="text"
          :placeholder="ui.t('placeholders.title')"
          maxlength="100"
          @input="emitUpdate('title', $event.target.value)"
        />
      </div>

      <div class="field-group">
        <div class="field-header">
          <span class="field-label">{{ ui.t("fields.content") }}</span>
          <span class="field-count">{{ content.length }} / 5000</span>
        </div>
        <div class="toolbar">
          <button
            v-for="tool in tools"
            :key="tool.key"
            class="tool-btn"
            :title="tool.label"
            type="button"
            @click="applyFormat(tool.key)"
            v-html="tool.icon"
          ></button>
          <span class="toolbar-divider"></span>
          <button class="tool-btn" type="button" title="图片" @click="applyFormat('image')">&#128444;</button>
          <button class="tool-btn" type="button" title="视频" @click="applyFormat('video')">&#127910;</button>
        </div>
        <textarea
          ref="editorRef"
          class="content-textarea"
          :value="content"
          rows="10"
          :placeholder="ui.t('placeholders.content')"
          maxlength="5000"
          @input="emitUpdate('content', $event.target.value)"
        ></textarea>
      </div>

      <div class="field-row">
        <div class="field-group flex-1">
          <div class="field-header">
            <span class="field-label">{{ ui.t("fields.tags") }}</span>
          </div>
          <input
            :value="tags"
            type="text"
            :placeholder="ui.t('placeholders.tags')"
            @input="emitUpdate('tags', $event.target.value)"
          />
        </div>
        <div class="field-group flex-1">
          <div class="field-header">
            <span class="field-label">{{ ui.t("fields.author") }}</span>
          </div>
          <input
            :value="author"
            type="text"
            :placeholder="ui.t('placeholders.author')"
            @input="emitUpdate('author', $event.target.value)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject, ref } from "vue";

const ui = inject("ui");

const props = defineProps({
  title: { type: String, default: "" },
  content: { type: String, default: "" },
  tags: { type: String, default: "" },
  author: { type: String, default: "" },
  useAi: { type: Boolean, default: false },
  llmProvider: { type: String, default: "" },
  providerOptions: { type: Array, default: () => [] },
  publishMode: { type: String, default: "" },
  publishModes: { type: Array, default: () => [] }
});

const emit = defineEmits([
  "update:title", "update:content", "update:tags", "update:author",
  "update:useAi", "update:llmProvider", "update:publishMode",
  "smartRewrite"
]);

const editorRef = ref(null);

const emitUpdate = (field, value) => {
  emit(`update:${field}`, value);
};

const tools = [
  { key: "bold", label: "加粗", icon: "<b>B</b>" },
  { key: "italic", label: "斜体", icon: "<i>I</i>" },
  { key: "heading", label: "标题", icon: "<b>H</b>" },
  { key: "underline", label: "下划线", icon: "<u>U</u>" },
  { key: "list", label: "列表", icon: "&#9776;" },
  { key: "quote", label: "引用", icon: "&#8220;" },
  { key: "link", label: "链接", icon: "&#128279;" }
];

const applyFormat = (key) => {
  const el = editorRef.value;
  if (!el) return;
  const start = el.selectionStart;
  const end = el.selectionEnd;
  const selected = props.content.substring(start, end);
  let replacement = "";

  switch (key) {
    case "bold": replacement = `**${selected || "加粗文本"}**`; break;
    case "italic": replacement = `*${selected || "斜体文本"}*`; break;
    case "heading": replacement = `\n## ${selected || "标题"}\n`; break;
    case "underline": replacement = `<u>${selected || "下划线文本"}</u>`; break;
    case "list": replacement = `\n- ${selected || "列表项"}\n`; break;
    case "quote": replacement = `\n> ${selected || "引用内容"}\n`; break;
    case "link": replacement = `[${selected || "链接文字"}](url)`; break;
    case "image": replacement = `![图片描述](url)`; break;
    case "video": replacement = `[视频](url)`; break;
    default: return;
  }

  const newContent = props.content.substring(0, start) + replacement + props.content.substring(end);
  emitUpdate("content", newContent);
};
</script>

<style scoped>
.editor-card {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #edf0f5;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
  overflow: hidden;
}

.card-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px 24px 0;
}

.card-title {
  margin: 0 0 4px;
  font-size: 1.15rem;
  font-weight: 700;
}

.card-sub {
  margin: 0;
  font-size: 0.82rem;
  color: #8c8c8c;
}

.smart-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 999px;
  border: 1px solid #edf0f5;
  background: #fff;
  color: #f26430;
  font-weight: 600;
  font-size: 0.82rem;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s;
}

.smart-btn:hover {
  background: rgba(255, 123, 74, 0.06);
}

.smart-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.smart-icon {
  font-size: 0.9rem;
}

.editor-body {
  padding: 20px 24px 24px;
  display: grid;
  gap: 18px;
}

.field-group {
  display: grid;
  gap: 8px;
}

.field-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.field-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #374151;
}

.field-count {
  font-size: 0.72rem;
  color: #9ca3af;
}

.title-input {
  border-radius: 12px;
  border: 1px solid #edf0f5;
  padding: 12px 16px;
  font-size: 1rem;
  background: #fafbfc;
  color: #1c1c1c;
  transition: border 0.2s;
}

.title-input:focus {
  outline: none;
  border-color: #ff7b4a;
  background: #fff;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 6px 8px;
  border: 1px solid #edf0f5;
  border-radius: 12px 12px 0 0;
  background: #fafbfc;
  flex-wrap: wrap;
}

.tool-btn {
  width: 30px;
  height: 30px;
  border-radius: 6px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 0.78rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: background 0.15s;
}

.tool-btn:hover {
  background: #e5e7eb;
}

.toolbar-divider {
  width: 1px;
  height: 18px;
  background: #e5e7eb;
  margin: 0 4px;
}

.content-textarea {
  border-radius: 0 0 12px 12px;
  border: 1px solid #edf0f5;
  border-top: none;
  padding: 14px 16px;
  font-size: 0.93rem;
  background: #fff;
  color: #1c1c1c;
  resize: vertical;
  min-height: 200px;
  line-height: 1.7;
  transition: border 0.2s;
}

.content-textarea:focus {
  outline: none;
  border-color: #ff7b4a;
}

.field-group input {
  border-radius: 12px;
  border: 1px solid #edf0f5;
  padding: 11px 14px;
  font-size: 0.9rem;
  background: #fafbfc;
  color: #1c1c1c;
  transition: border 0.2s;
}

.field-group input:focus {
  outline: none;
  border-color: #ff7b4a;
  background: #fff;
}

.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.flex-1 {
  flex: 1;
}

@media (max-width: 640px) {
  .field-row {
    grid-template-columns: 1fr;
  }
}
</style>
