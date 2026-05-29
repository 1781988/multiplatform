<template>
  <div class="media-card">
    <div class="card-head">
      <div>
        <h3 class="card-title">{{ ui.t("cards.mediaTitle") }}</h3>
        <p class="card-sub">{{ ui.t("cards.mediaSub") }}</p>
      </div>
    </div>
    <div class="media-columns">
      <div class="media-col">
        <div class="media-col-head">
          <span class="col-icon">&#128444;</span>
          <span class="col-label">{{ ui.t("media.images") }}</span>
        </div>
        <div class="media-dropzone" @click="triggerUpload('image')">
          <div v-if="images.length" class="thumb-grid">
            <div v-for="item in images.slice(0, 4)" :key="item" class="thumb-item">
              <span class="thumb-name">{{ fileName(item) }}</span>
              <button class="thumb-remove" @click.stop="removeImage(item)">&times;</button>
            </div>
          </div>
          <div v-else class="dropzone-empty">
            <span class="dropzone-plus">+</span>
            <span class="dropzone-hint">{{ ui.t("media.uploadImage") }}</span>
          </div>
        </div>
        <p class="media-hint">{{ ui.t("media.imageHint") }}</p>
        <input
          type="file"
          class="sr-only"
          :ref="el => fileInputs.image = el"
          accept=".jpg,.jpeg,.png,.webp"
          multiple
          @change="handleUpload($event, 'image')"
        />
      </div>

      <div class="media-col">
        <div class="media-col-head">
          <span class="col-icon">&#127910;</span>
          <span class="col-label">{{ ui.t("media.videos") }}</span>
        </div>
        <div class="media-dropzone" @click="triggerUpload('video')">
          <div v-if="videos.length" class="thumb-grid">
            <div v-for="item in videos.slice(0, 2)" :key="item" class="thumb-item video-thumb">
              <span class="play-icon">&#9654;</span>
              <span class="thumb-name">{{ fileName(item) }}</span>
              <button class="thumb-remove" @click.stop="removeVideo(item)">&times;</button>
            </div>
          </div>
          <div v-else class="dropzone-empty">
            <span class="dropzone-plus">+</span>
            <span class="dropzone-hint">{{ ui.t("media.uploadVideo") }}</span>
          </div>
        </div>
        <p class="media-hint">{{ ui.t("media.videoHint") }}</p>
        <input
          type="file"
          class="sr-only"
          :ref="el => fileInputs.video = el"
          accept=".mp4,.mov,.avi,.mkv"
          multiple
          @change="handleUpload($event, 'video')"
        />
      </div>

      <div class="media-col">
        <div class="media-col-head">
          <span class="col-icon">&#128247;</span>
          <span class="col-label">{{ ui.t("media.cover") }}</span>
        </div>
        <div class="media-dropzone" @click="triggerUpload('cover')">
          <div v-if="cover" class="thumb-item cover-thumb">
            <span class="thumb-name">{{ fileName(cover) }}</span>
            <button class="cover-change-btn">{{ ui.t("media.changeCover") }}</button>
            <button class="thumb-remove" @click.stop="emitUpdate('cover', '')">&times;</button>
          </div>
          <div v-else class="dropzone-empty">
            <span class="dropzone-plus">+</span>
            <span class="dropzone-hint">{{ ui.t("media.uploadCover") }}</span>
          </div>
        </div>
        <p class="media-hint">{{ ui.t("media.coverHint") }}</p>
        <input
          type="file"
          class="sr-only"
          :ref="el => fileInputs.cover = el"
          accept=".jpg,.jpeg,.png,.webp"
          @change="handleUpload($event, 'cover')"
        />
      </div>
    </div>
    <p v-if="notice" class="notice">{{ notice }}</p>
  </div>
</template>

<script setup>
import { inject, reactive, ref } from "vue";
import { apiRequest } from "../api/request.js";

const ui = inject("ui");

const props = defineProps({
  images: { type: Array, default: () => [] },
  videos: { type: Array, default: () => [] },
  cover: { type: String, default: "" }
});

const emit = defineEmits(["update:images", "update:videos", "update:cover"]);

const notice = ref("");
const fileInputs = reactive({ image: null, video: null, cover: null });

const emitUpdate = (field, value) => {
  emit(`update:${field}`, value);
};

const fileName = (path) => {
  if (!path) return "";
  return path.split("/").pop() || path;
};

const removeImage = (item) => {
  emitUpdate("images", props.images.filter((i) => i !== item));
};

const removeVideo = (item) => {
  emitUpdate("videos", props.videos.filter((v) => v !== item));
};

const triggerUpload = (type) => {
  if (fileInputs[type]) fileInputs[type].click();
};

const uploadFile = async (file, type) => {
  notice.value = "";
  const formData = new FormData();
  formData.append("file", file);
  const pathMap = {
    image: "/api/upload/image",
    video: "/api/upload/video",
    cover: "/api/upload/cover"
  };
  const response = await apiRequest(pathMap[type], {
    method: "POST",
    body: formData
  });
  if (!response || response.code !== 200) {
    notice.value = ui.t("media.uploadFailed");
    return null;
  }
  return response.data?.file_url || "";
};

const handleUpload = async (event, type) => {
  const files = Array.from(event.target.files || []);
  if (!files.length) return;
  const uploads = [];
  for (const file of files) {
    const fileUrl = await uploadFile(file, type);
    if (fileUrl) uploads.push(fileUrl);
  }
  if (!uploads.length) return;
  if (type === "cover") {
    emitUpdate("cover", uploads[0]);
  } else if (type === "image") {
    emitUpdate("images", [...props.images, ...uploads]);
  } else if (type === "video") {
    emitUpdate("videos", [...props.videos, ...uploads]);
  }
  event.target.value = "";
};
</script>

<style scoped>
.media-card {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #edf0f5;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
  padding: 20px 24px 24px;
}

.card-head {
  margin-bottom: 16px;
}

.card-title { margin: 0 0 4px; font-size: 1.15rem; font-weight: 700; }
.card-sub { margin: 0; font-size: 0.82rem; color: #8c8c8c; }

.media-columns {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}

.media-col {
  display: flex;
  flex-direction: column;
}

.media-col-head {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
  font-weight: 600;
  font-size: 0.88rem;
}

.col-icon { font-size: 1rem; }
.col-label { color: #374151; }

.media-dropzone {
  flex: 1;
  min-height: 100px;
  border: 2px dashed #e5e7eb;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.2s;
  padding: 8px;
}

.media-dropzone:hover { border-color: #ff7b4a; }

.dropzone-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  color: #9ca3af;
}

.dropzone-plus { font-size: 1.5rem; font-weight: 300; }
.dropzone-hint { font-size: 0.78rem; }

.thumb-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  width: 100%;
}

.thumb-item {
  position: relative;
  background: #fafbfc;
  border: 1px solid #edf0f5;
  border-radius: 8px;
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  font-size: 0.72rem;
}

.video-thumb { background: #f8f4f0; }
.cover-thumb { grid-column: 1 / -1; }

.play-icon {
  font-size: 1.2rem;
  color: #ff7b4a;
}

.thumb-name {
  color: #374151;
  word-break: break-all;
  text-align: center;
  line-height: 1.3;
}

.thumb-remove {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: none;
  background: #fee2e2;
  color: #dc2626;
  font-size: 0.7rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-change-btn {
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid #edf0f5;
  background: #fff;
  font-size: 0.7rem;
  color: #6b7280;
  cursor: pointer;
}

.media-hint {
  margin: 4px 0 0;
  font-size: 0.7rem;
  color: #b0b8c1;
  line-height: 1.4;
}

.notice { margin: 10px 0 0; color: #dc2626; font-weight: 600; font-size: 0.85rem; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }

@media (max-width: 720px) {
  .media-columns { grid-template-columns: 1fr; }
}
</style>
