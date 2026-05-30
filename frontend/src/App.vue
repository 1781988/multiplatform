<template>
  <section v-if="isAuthPage" class="auth-page">
    <div class="auth-card">
      <img src="/figures/聚发舟.png" alt="聚发舟" />
      <h1>{{ route.path === "/login" ? "登录聚发舟" : "注册聚发舟" }}</h1>
      <p>MultiPost AI 多平台内容发布工作台</p>

      <label v-if="route.path === '/register'">
        用户名
        <input v-model="authForm.name" placeholder="请输入用户名" />
      </label>
      <label>
        账号
        <input v-model="authForm.account" placeholder="请输入账号" />
      </label>
      <label>
        密码
        <input v-model="authForm.password" type="password" placeholder="请输入密码" />
      </label>
      <label v-if="route.path === '/register'">
        确认密码
        <input v-model="authForm.confirm" type="password" placeholder="请再次输入密码" />
      </label>

      <p v-if="authError" class="error-text">{{ authError }}</p>
      <button class="primary-btn" type="button" @click="route.path === '/login' ? login() : register()">
        {{ route.path === "/login" ? "登录" : "注册" }}
      </button>
      <router-link class="auth-link" :to="route.path === '/login' ? '/register' : '/login'">
        {{ route.path === "/login" ? "没有账号？去注册" : "已有账号？去登录" }}
      </router-link>
    </div>
  </section>

  <div v-else class="app-shell">
    <aside class="sidebar">
      <div class="brand">
        <img class="brand-logo" src="/figures/聚发舟.png" alt="聚发舟" />
        <div>
          <strong>聚发舟</strong>
          <span>MultiPost AI</span>
        </div>
      </div>

      <nav class="nav-list" aria-label="主导航">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          class="nav-item"
          :class="{ active: route.path === item.path }"
          :to="item.path"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </router-link>
      </nav>

      <div class="publish-overview-card">
        <p>发布概览</p>
        <div class="publish-overview-grid">
          <div class="publish-overview-item">
            <span>今日发布</span>
            <strong>{{ publishOverview.today }} 篇</strong>
          </div>
          <div class="publish-overview-item">
            <span>本周发布</span>
            <strong>{{ publishOverview.week }} 篇</strong>
          </div>
          <div class="publish-overview-item">
            <span>累计发布</span>
            <strong>{{ publishOverview.total }} 篇</strong>
          </div>
          <div class="publish-overview-item">
            <span>发布成功率</span>
            <strong>{{ publishOverview.successRate }}%</strong>
          </div>
        </div>
      </div>

      <div class="upgrade-card" :class="{ pro: isPro }">
        <template v-if="isPro">
          <strong>专业版已开通</strong>
          <span>有效期：{{ vipStart }} 至 {{ vipEnd }}</span>
        </template>
        <template v-else>
          <strong>升级专业版</strong>
          <span>解锁更多高级功能</span>
          <button type="button" @click="upgradeDialogVisible = true">立即升级</button>
        </template>
      </div>
    </aside>

    <header class="topbar">
      <div class="stepper">
        <div
          v-for="step in steps"
          :key="step.id"
          class="step"
          :class="{ active: activeStep === step.id, done: activeStep > step.id }"
        >
          <span>{{ step.id }}</span>
          <strong>{{ step.label }}</strong>
        </div>
      </div>
      <div class="top-actions">
        <div class="theme-wrap">
          <button class="icon-btn" type="button" title="主题" @click="themeMenuOpen = !themeMenuOpen">{{ themeIcon }}</button>
          <section v-if="themeMenuOpen" class="theme-menu">
            <button
              v-for="item in themeOptions"
              :key="item.value"
              type="button"
              :class="{ active: themeMode === item.value }"
              @click="selectTheme(item.value)"
            >
              <span>{{ item.icon }}</span>
              {{ item.label }}
            </button>
          </section>
        </div>
        <div class="notification-wrap">
          <button class="icon-btn bell" type="button" title="通知" aria-label="通知" @click="notificationPanelOpen = !notificationPanelOpen">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9" />
              <path d="M13.7 21a2 2 0 0 1-3.4 0" />
            </svg>
            <b v-if="unreadNotifications.length">{{ unreadNotifications.length > 9 ? "9+" : unreadNotifications.length }}</b>
          </button>
          <section v-if="notificationPanelOpen" class="notification-panel">
            <div class="notification-head">
              <strong>通知中心</strong>
              <button v-if="unreadNotifications.length" type="button" @click="markAllNotificationsRead">全部已读</button>
            </div>
            <div v-if="notifications.length" class="notification-list">
              <article v-for="item in notifications" :key="item.id" class="notification-item" :class="{ unread: !item.read, [item.type]: true }">
                <div>
                  <strong>{{ item.title }}</strong>
                  <p>{{ item.message }}</p>
                  <small>{{ item.time }}</small>
                </div>
                <button v-if="!item.read" type="button" @click="markNotificationRead(item.id)">已读</button>
              </article>
            </div>
            <div v-else class="notification-empty">暂无新通知</div>
          </section>
        </div>
        <div class="profile">
          <div class="avatar">{{ username.slice(0, 1) || "明" }}</div>
          <div>
            <strong>{{ username || "创作者小明" }}</strong>
            <span>{{ isPro ? "专业版" : "普通版" }}</span>
          </div>
          <button class="logout-btn" type="button" @click="logout">退出</button>
        </div>
      </div>
    </header>

    <main class="workspace" :class="{ wide: isWidePage }">
      <section class="main-column">
        <DashboardView v-if="route.path === '/dashboard'" />
        <ContentView v-else-if="route.path === '/content'" />
        <PreviewView v-else-if="route.path === '/preview'" />
        <RecordsView v-else-if="route.path === '/records'" />
        <AccountsView v-else-if="route.path === '/accounts'" />
        <MaterialsView v-else-if="route.path === '/materials'" />
        <SettingsView v-else-if="route.path === '/settings'" />
        <HelpView v-else-if="route.path === '/help'" />
      </section>

      <aside v-if="showSideColumn" class="side-column">
        <PlatformPanel />
        <OverviewPanel />
        <TipsPanel />
      </aside>
    </main>

    <div v-if="upgradeDialogVisible" class="dialog-mask" @click.self="upgradeDialogVisible = false">
      <section class="upgrade-dialog">
        <button class="dialog-close" type="button" @click="upgradeDialogVisible = false">×</button>
        <h2>升级专业版</h2>
        <p>输入会员码完成 mock 升级，或扫码模拟支付。</p>
        <label>
          会员码
          <input v-model.trim="memberCode" placeholder="例如 JUFZ2026" @keydown.enter="handleUpgradeByCode" />
        </label>
        <p v-if="upgradeError" class="error-text">{{ upgradeError }}</p>
        <button class="primary-btn" type="button" @click="handleUpgradeByCode">验证会员码</button>
        <div class="pay-grid">
          <div>
            <span>微信支付</span>
            <b>WX</b>
          </div>
          <div>
            <span>支付宝</span>
            <b>ALI</b>
          </div>
        </div>
      </section>
    </div>

    <div v-if="deleteDialogVisible" class="dialog-mask" @click.self="cancelDeleteRecord">
      <section class="delete-dialog">
        <button class="dialog-close" type="button" :disabled="deletingRecord" @click="cancelDeleteRecord">×</button>
        <div class="delete-dialog-icon">!</div>
        <div>
          <h2>删除发布记录</h2>
          <p>确认删除这条发布记录吗？当前是模拟发布，只会删除本地系统记录，不会影响真实平台帖子。</p>
        </div>
        <div class="delete-record-preview">
          <span>任务标题</span>
          <strong>{{ pendingDeleteRecord?.title || form.title || "-" }}</strong>
          <span>发布平台</span>
          <strong>{{ platformName(pendingDeleteRecord?.platform || pendingDeleteRecord?.id) }}</strong>
        </div>
        <div class="delete-dialog-actions">
          <button class="ghost-btn" type="button" :disabled="deletingRecord" @click="cancelDeleteRecord">取消</button>
          <button class="danger-primary-btn" type="button" :disabled="deletingRecord" @click="confirmDeleteRecord">
            {{ deletingRecord ? "删除中..." : "确认删除" }}
          </button>
        </div>
      </section>
    </div>

    <div v-if="aiConfigDialogVisible" class="dialog-mask" @click.self="closeAiConfigDialog">
      <section class="ai-config-dialog">
        <button class="dialog-close" type="button" :disabled="loading.settings" @click="closeAiConfigDialog">×</button>
        <div class="ai-config-title">
          <span :class="['provider-mark', currentEditingProvider?.tone]">{{ currentEditingProvider?.label?.slice(0, 1) }}</span>
          <div>
            <h2>{{ currentEditingProvider?.label }} 配置</h2>
            <p>{{ currentEditingProvider?.description }}</p>
          </div>
        </div>
        <div class="ai-config-form">
          <label v-if="currentEditingProvider?.requiresKey">
            <span>API Key</span>
            <input v-model.trim="aiConfigDraft.key" type="password" placeholder="请输入 API Key" />
          </label>
          <label>
            <span>Base URL</span>
            <input v-model.trim="aiConfigDraft.baseUrl" placeholder="例如 https://api.openai.com/v1" />
          </label>
          <label>
            <span>模型名</span>
            <input v-model.trim="aiConfigDraft.model" placeholder="例如 gpt-4o-mini" />
          </label>
          <label>
            <span>Temperature</span>
            <input v-model.number="aiConfigDraft.temperature" type="number" min="0" max="2" step="0.1" />
          </label>
          <label>
            <span>Max Tokens</span>
            <input v-model.number="aiConfigDraft.maxTokens" type="number" min="256" step="256" />
          </label>
          <label class="switch set-default-switch">
            <input v-model="aiConfigDraft.setDefault" type="checkbox" />
            <span></span>
            设为默认模型
          </label>
        </div>
        <div class="ai-config-actions">
          <button class="ghost-btn" type="button" :disabled="loading.settings" @click="testCurrentProvider">
            {{ testingProvider === editingProvider ? "测试中..." : "测试连接" }}
          </button>
          <button class="primary-btn" type="button" :disabled="loading.settings" @click="saveAiProviderConfig">
            {{ loading.settings ? "保存中..." : "保存配置" }}
          </button>
        </div>
      </section>
    </div>

    <div v-if="recordDetailVisible" class="drawer-mask" @click.self="recordDetailVisible = false">
      <section class="record-drawer">
        <button class="dialog-close" type="button" @click="recordDetailVisible = false">×</button>
        <h2>{{ selectedRecord?.task_title || "发布详情" }}</h2>
        <div class="detail-meta">
          <span>发布时间：{{ selectedRecord?.publish_time || "-" }}</span>
          <span>发布模式：{{ selectedRecord?.publish_mode || "mock" }}</span>
          <span>模拟发布ID：{{ selectedRecord?.mock_publish_id || "-" }}</span>
          <span>状态：{{ selectedRecord?.status || "success" }}</span>
          <span>平台数：{{ selectedRecord?.platform_contents?.length || 0 }}</span>
        </div>
        <p class="source-text">{{ selectedRecord?.source_content || form.content }}</p>
        <div class="detail-platforms">
          <article v-for="item in selectedRecord?.platform_contents || []" :key="item.platform" class="detail-card">
            <h3>{{ platformName(item.platform) }}</h3>
            <strong>{{ item.title }}</strong>
            <p>{{ item.content || item.description }}</p>
            <div class="preview-tags">
              <span v-for="tag in normalizeTags(item.tags)" :key="tag">#{{ tag }}</span>
            </div>
            <small>状态：{{ item.status || selectedRecord?.status || "success" }}</small>
          </article>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, defineComponent, h, onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { apiRequest } from "./api/request.js";

const route = useRoute();
const router = useRouter();

const imageInput = ref(null);
const videoInput = ref(null);
const coverInput = ref(null);
const materialFilter = ref("all");
const recordDetailVisible = ref(false);
const selectedRecord = ref(null);
const deleteDialogVisible = ref(false);
const pendingDeleteRecord = ref(null);
const deletingRecord = ref(false);
const aiConfigDialogVisible = ref(false);
const editingProvider = ref(null);
const aiConfigDraft = reactive({});
const testingProvider = ref("");

const authForm = reactive({ name: "", account: "", password: "", confirm: "" });
const authError = ref("");
const username = ref(localStorage.getItem("username") || "");
const isPro = ref(localStorage.getItem("isPro") === "true");
const vipStart = ref(localStorage.getItem("vipStart") || "");
const vipEnd = ref(localStorage.getItem("vipEnd") || "");
const upgradeDialogVisible = ref(false);
const memberCode = ref("");
const upgradeError = ref("");

const aiIntensity = ref(localStorage.getItem("aiIntensity") || "balanced");
const outputLang = ref(localStorage.getItem("outputLang") || "zh");
const tagDraft = ref("");
const notice = ref("");
const taskId = ref(null);
const loading = reactive({ adapt: false, publish: false, records: false, materials: false, settings: false });
const publishResults = ref([]);
const adapted = reactive({});
const materials = ref(sanitizeMaterials(JSON.parse(localStorage.getItem(`materials:${username.value || "guest"}`) || "[]")));
const history = ref(JSON.parse(localStorage.getItem(`records:${username.value || "guest"}`) || "[]"));
const notifications = ref(JSON.parse(localStorage.getItem(`notifications:${username.value || "guest"}`) || "[]"));
const notificationPanelOpen = ref(false);
const themeMode = ref(localStorage.getItem("themeMode") || "light");
const themeMenuOpen = ref(false);
const IMAGE_MAX_COUNT = 9;
const VIDEO_MAX_COUNT = 3;
const COVER_MAX_COUNT = 1;
const IMAGE_MAX_SIZE = 10 * 1024 * 1024;
const VIDEO_MAX_SIZE = 500 * 1024 * 1024;
const IMAGE_TYPES = ["image/png", "image/jpeg", "image/jpg", "image/webp"];
const VIDEO_TYPES = ["video/mp4", "video/quicktime", "video/x-msvideo", "video/x-matroska"];
const VIDEO_EXTS = [".mp4", ".mov", ".avi", ".mkv"];

const aiSettings = reactive({
  provider: "openai",
  openaiKey: "",
  openaiBaseUrl: "https://api.openai.com/v1",
  openaiModel: "gpt-4o-mini",
  openaiTemperature: 0.7,
  openaiMaxTokens: 2000,
  qwenKey: "",
  qwenBaseUrl: "https://dashscope.aliyuncs.com/compatible-mode/v1",
  qwenModel: "qwen-plus",
  qwenTemperature: 0.7,
  qwenMaxTokens: 2000,
  geminiKey: "",
  geminiBaseUrl: "",
  geminiModel: "gemini-1.5-flash",
  geminiTemperature: 0.7,
  geminiMaxTokens: 2000,
  deepseekKey: "",
  deepseekBaseUrl: "https://api.deepseek.com",
  deepseekModel: "deepseek-chat",
  deepseekTemperature: 0.7,
  deepseekMaxTokens: 2000,
  ollamaBaseUrl: "http://localhost:11434",
  ollamaModel: "qwen2.5:7b",
  ollamaTemperature: 0.7,
  ollamaMaxTokens: 2000,
  localKey: "",
  localBaseUrl: "http://127.0.0.1:8000/v1",
  localModel: "local-model",
  localTemperature: 0.7,
  localMaxTokens: 2000,
  defaultLang: outputLang.value,
  defaultIntensity: aiIntensity.value
});

const platforms = [
  { id: "wechat", name: "微信公众号", type: "图文消息", icon: "/figures/公众号.png", permission: "图文草稿、封面、群发模拟" },
  { id: "zhihu", name: "知乎", type: "问答文章", icon: "/figures/知乎.png", permission: "回答、文章、专栏模拟" },
  { id: "bilibili", name: "B站", type: "视频投稿", icon: "/figures/b站.png", permission: "视频投稿、封面、分区模拟" },
  { id: "xiaohongshu", name: "小红书", type: "图文笔记", icon: "/figures/小红书.png", permission: "图文笔记、话题标签模拟" }
];

const accounts = reactive({
  wechat: { loggedIn: true, accountName: "测试公众号账号", authType: "Mock Token", expireAt: "2026-12-31" },
  zhihu: { loggedIn: true, accountName: "知乎创作者", authType: "Mock Token", expireAt: "2026-12-31" },
  bilibili: { loggedIn: false, accountName: "", authType: "未授权", expireAt: "-" },
  xiaohongshu: { loggedIn: false, accountName: "", authType: "未授权", expireAt: "-" }
});

const form = reactive({
  title: "如何用AI工具提升大学生学习效率",
  content:
    "随着AI工具的快速发展，大学生在学习过程中可以利用AI辅助完成资料整理、论文阅读、知识总结、代码调试和复习规划等任务。合理使用AI工具不仅可以节省时间，还可以帮助学生建立更加清晰的知识结构。\n\n本文将从学习计划制定、课堂笔记整理、论文阅读辅助、代码学习和考试复习五个方面，介绍AI工具在学习效率提升中的实际应用方法。",
  tagsText: "AI学习,大学生,效率提升,学习方法,人工智能",
  platforms: platforms.map((platform) => platform.id),
  useAi: true,
  llmProvider: aiSettings.provider,
  publishMode: "simulate",
  images: [],
  videos: [],
  cover: null
});

const navItems = [
  { path: "/dashboard", label: "工作台", icon: "▦" },
  { path: "/content", label: "内容创作", icon: "⌂" },
  { path: "/preview", label: "平台预览", icon: "▣" },
  { path: "/records", label: "发布记录", icon: "▤" },
  { path: "/accounts", label: "账号管理", icon: "♙" },
  { path: "/materials", label: "素材管理", icon: "▧" },
  { path: "/settings", label: "AI 设置", icon: "⚙" },
  { path: "/help", label: "帮助中心", icon: "?" }
];

const steps = [
  { id: 1, label: "内容创作" },
  { id: 2, label: "平台适配" },
  { id: 3, label: "预览编辑" },
  { id: 4, label: "一键发布" }
];

const morePlatforms = [
  { name: "微博", icon: "◎" },
  { name: "抖音", icon: "♪" },
  { name: "头条", icon: "T" },
  { name: "快手", icon: "K" }
];

const providers = [
  { value: "openai", label: "OpenAI", tone: "blue", description: "OpenAI 官方或兼容接口", requiresKey: true },
  { value: "qwen", label: "Qwen", tone: "green", description: "通义千问 DashScope 兼容接口", requiresKey: true },
  { value: "gemini", label: "Gemini", tone: "purple", description: "Google Gemini 模型服务", requiresKey: true },
  { value: "deepseek", label: "DeepSeek", tone: "pink", description: "DeepSeek Chat / Coder 服务", requiresKey: true },
  { value: "ollama", label: "Ollama", tone: "orange", description: "本机 Ollama 模型服务", requiresKey: false },
  { value: "local", label: "Local", tone: "gray", description: "私有化 OpenAI 兼容服务", requiresKey: false }
];

const rewriteModes = [
  { value: "conservative", label: "保守" },
  { value: "balanced", label: "平衡" },
  { value: "creative", label: "创意" }
];

const isAuthPage = computed(() => route.path === "/login" || route.path === "/register");
const isWidePage = computed(() => ["/dashboard", "/records", "/accounts", "/materials", "/settings", "/help"].includes(route.path));
const showSideColumn = computed(() => ["/content", "/preview"].includes(route.path));
const publishOverview = computed(() => {
  const now = new Date();
  const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();
  const day = now.getDay() || 7;
  const startOfWeek = new Date(now.getFullYear(), now.getMonth(), now.getDate() - day + 1).getTime();
  let today = 0;
  let week = 0;
  let success = 0;
  let failed = 0;

  history.value.forEach((record) => {
    const time = parsePublishTime(record.publish_time);
    if (time >= startOfToday) today += 1;
    if (time >= startOfWeek) week += 1;
    if (record.status === "success") success += 1;
    if (record.status === "failed") failed += 1;
  });

  const counted = success + failed;
  return {
    today,
    week,
    total: history.value.length,
    successRate: counted ? Math.round((success / counted) * 100) : 0
  };
});
const parsedTags = computed(() =>
  form.tagsText
    .split(/[,，、\s]+/)
    .map((tag) => tag.trim())
    .filter(Boolean)
    .slice(0, 10)
);
const selectedPlatforms = computed(() => platforms.filter((platform) => form.platforms.includes(platform.id)));
const previewList = computed(() => selectedPlatforms.value.map((platform) => ({ ...platform, content: adapted[platform.id] })).filter((item) => item.content));
const unreadNotifications = computed(() => notifications.value.filter((item) => !item.read));
const filteredMaterials = computed(() => (materialFilter.value === "all" ? materials.value : materials.value.filter((item) => item.type === materialFilter.value)));
const themeOptions = [
  { value: "light", label: "亮色模式", icon: "☼" },
  { value: "dark", label: "深色模式", icon: "●" },
  { value: "system", label: "跟随系统", icon: "◐" }
];
const themeIcon = computed(() => themeOptions.find((item) => item.value === themeMode.value)?.icon || "☼");
const materialStats = computed(() => {
  const totalSize = materials.value.reduce((sum, item) => sum + (item.size || 0), 0);
  return {
    image: materials.value.filter((item) => item.type === "image").length,
    video: materials.value.filter((item) => item.type === "video").length,
    cover: materials.value.filter((item) => item.type === "cover").length,
    size: formatSize(totalSize)
  };
});
const activeStep = computed(() => {
  if (publishResults.value.length || route.path === "/records") return 4;
  if (previewList.value.length || route.path === "/preview") return 3;
  if (form.title.trim() && form.content.trim() && form.platforms.length) return 2;
  return 1;
});

function page(render) {
  return defineComponent({ setup: () => () => h("div", render()) });
}

const DashboardView = page(() => [
  h("article", { class: "panel dashboard-hero" }, [
    h("div", [h("h2", "工作台"), h("p", "查看发布、素材、模型和平台账号的整体状态。")]),
    h("div", { class: "quick-actions" }, [
      h("button", { class: "primary-btn", onClick: () => router.push("/content") }, "新建创作"),
      h("button", { class: "ghost-btn", onClick: () => router.push("/records") }, "查看记录"),
      h("button", { class: "ghost-btn", onClick: () => router.push("/accounts") }, "管理账号")
    ])
  ]),
  h("div", { class: "metric-grid" }, [
    metric("今日发布", `${publishOverview.value.today} 篇`, "按当前用户统计"),
    metric("素材容量", materialStats.value.size, `${materials.value.length} 个素材`),
    metric("AI 模型", providerLabel(form.llmProvider), "当前默认生成模型"),
    metric("账号状态", `${Object.values(accounts).filter((item) => item.loggedIn).length}/4`, "已模拟登录平台")
  ]),
  h("article", { class: "panel" }, [
    h("div", { class: "panel-head compact" }, [h("div", [h("h2", "最近发布记录"), h("p", "点击记录可查看完整帖子内容。")])]),
    history.value.length
      ? h("div", { class: "record-list" }, history.value.slice(0, 5).map((record) => recordRow(record)))
      : h("div", { class: "empty-state" }, "暂无发布记录。")
  ])
]);

const ContentView = page(() => [
  h("article", { class: "panel editor-panel" }, [
    h("div", { class: "panel-head" }, [
      h("div", [h("h2", "创作内容"), h("p", "当前任务的内容输入、素材选择和 AI 生成。")]),
      h("button", { class: "ghost-btn", onClick: applySample }, "填充样例内容")
    ]),
    fieldInput("标题", true),
    fieldEditor(),
    fieldTags()
  ]),
  h("article", { class: "panel media-panel" }, [
    h("div", { class: "panel-head compact" }, [h("div", [h("h2", "当前任务素材"), h("p", "上传素材会写入素材库，也可仅作为本地预览。")])]),
    hiddenInputs(),
    mediaUploadGrid()
  ]),
  aiGeneratePanel(),
  notice.value ? h("p", { class: "notice" }, notice.value) : null
]);

const PreviewView = page(() => [
  h("article", { class: "panel preview-panel" }, [
    h("div", { class: "panel-head" }, [
      h("div", [h("h2", "平台预览"), h("p", "展示并编辑当前生成的多平台内容。")]),
      h("button", { class: "primary-outline", disabled: loading.publish || !previewList.value.length, onClick: publishAll }, loading.publish ? "发布中..." : "一键模拟发布")
    ]),
    previewList.value.length
      ? h("div", { class: "preview-grid" }, previewList.value.map((item) => previewCard(item)))
      : h("div", { class: "empty-state" }, [h("span", "暂无平台预览，请先生成内容。"), h("a", { onClick: () => router.push("/content") }, "去生成")])
  ])
]);

const RecordsView = page(() => [
  h("article", { class: "panel records-panel" }, [
    h("div", { class: "panel-head" }, [
      h("div", [h("h2", "发布记录"), h("p", "历史发布任务和帖子详情。")]),
      h("button", { class: "ghost-btn", onClick: loadRecords }, "刷新")
    ]),
    history.value.length
      ? h("div", { class: "record-table" }, [
          h("div", { class: "record-head" }, [h("span", "发布时间"), h("span", "任务标题"), h("span", "发布平台"), h("span", "状态"), h("span", "操作")]),
          ...history.value.map((record) => recordRow(record, true))
        ])
      : h("div", { class: "empty-state" }, "暂无发布记录。")
  ])
]);

const AccountsView = page(() => [
  h("article", { class: "panel" }, [
    h("div", { class: "panel-head" }, [h("div", [h("h2", "平台账号中心"), h("p", "管理各平台授权状态、账号名称、Token 有效期和预留官方授权入口。")])]),
    h("div", { class: "account-grid" }, platforms.map((platform) => {
      const account = accounts[platform.id];
      return h("section", { class: "account-card" }, [
        h("div", { class: "account-title" }, [h("img", { src: platform.icon, alt: platform.name }), h("div", [h("h3", platform.name), h("span", platform.permission)])]),
        h("dl", [
          h("dt", "状态"), h("dd", account.loggedIn ? "已登录" : "未登录"),
          h("dt", "授权方式"), h("dd", account.authType),
          h("dt", "账号名称"), h("dd", account.accountName || "未设置"),
          h("dt", "授权有效期"), h("dd", account.expireAt)
        ]),
        h("div", { class: "card-actions" }, [
          h("button", { class: "ghost-btn small", onClick: () => mockLogin(platform.id) }, account.loggedIn ? "重新登录" : "模拟登录"),
          h("button", { class: "ghost-btn small", onClick: () => logoutPlatform(platform.id) }, "退出登录"),
          h("button", { class: "ghost-btn small" }, "官方授权预留")
        ])
      ]);
    }))
  ])
]);

const MaterialsView = page(() => [
  h("article", { class: "panel material-library" }, [
    h("div", { class: "panel-head" }, [
      h("div", [h("h2", "全局素材库"), h("p", "集中管理历史上传的图片、视频和封面素材，可筛选、删除并加入当前创作任务。")]),
      h("button", { class: "ghost-btn", disabled: loading.materials, onClick: loadMaterials }, loading.materials ? "刷新中..." : "刷新素材")
    ]),
    h("div", { class: "material-stats" }, [
      metric("图片", `${materialStats.value.image} 张`, "jpg/png/webp"),
      metric("视频", `${materialStats.value.video} 个`, "mp4/mov/avi/mkv"),
      metric("封面", `${materialStats.value.cover} 张`, "推荐 16:9 或 3:4"),
      metric("总占用", materialStats.value.size, "本地/后端素材")
    ]),
    h("div", { class: "library-toolbar" }, [
      h("div", { class: "filter-tabs" }, ["all", "image", "video", "cover"].map((type) =>
        h("button", { class: { active: materialFilter.value === type }, onClick: () => (materialFilter.value = type) }, `${materialFilterLabel(type)} ${materialFilterCount(type)}`)
      )),
      h("span", `${filteredMaterials.value.length} 个素材`)
    ]),
    filteredMaterials.value.length
      ? h("div", { class: "material-grid" }, filteredMaterials.value.map((item) => materialCard(item)))
      : h("div", { class: "empty-state" }, "暂无匹配素材，请在内容创作页上传图片、视频或封面。")
  ])
]);

const SettingsView = page(() => [
  h("article", { class: "panel settings-panel" }, [
    h("div", { class: "panel-head" }, [h("div", [h("h2", "AI 设置中心"), h("p", "管理模型服务、默认模型和后续真实 API 接入参数。")])]),
    h("section", { class: "ai-default-card" }, [
      h("div", [
        h("span", "当前默认模型"),
        h("h3", `${providerLabel(aiSettings.provider)} · ${providerModel(aiSettings.provider) || "未配置模型"}`),
        h("p", `默认语言：${aiSettings.defaultLang === "en" ? "English" : "中文"} / 改写强度：${rewriteModeLabel(aiSettings.defaultIntensity)}`)
      ]),
      h("button", { class: "primary-outline", onClick: () => openAiConfigDialog(aiSettings.provider) }, "配置默认模型")
    ]),
    h("div", { class: "ai-provider-grid" }, providers.map((provider) => aiProviderCard(provider))),
    notice.value ? h("p", { class: "notice" }, notice.value) : null
  ])
]);

const HelpView = page(() => [
  h("article", { class: "panel help-panel" }, [
    h("h2", "帮助中心"),
    h("p", "建议流程：登录/注册 -> 工作台 -> 内容创作 -> 生成预览 -> 编辑各平台内容 -> 模拟发布 -> 查看发布详情。"),
    h("ul", [
      h("li", "素材上传支持图片、视频、封面，并显示格式、大小和推荐尺寸。"),
      h("li", "发布记录可以点击查看完整帖子内容、标签、素材和状态。"),
      h("li", "AI 设置中心用于保存全局 API 配置，内容创作页只负责本次生成参数。"),
      h("li", "会员码测试值：JUFZ2026、MULTIPOSTAI、VIP888。")
    ])
  ])
]);

const PlatformPanel = page(() => [
  h("article", { class: "panel platform-panel" }, [
    h("div", { class: "panel-head compact" }, [h("div", [h("h2", "目标平台"), h("p", "选择要发布的平台（可多选）")])]),
    h("div", { class: "platform-grid" }, platforms.map((platform) =>
      h("button", { class: ["platform-card", platform.id, { selected: form.platforms.includes(platform.id) }], type: "button", onClick: () => togglePlatform(platform.id) }, [
        h("img", { src: platform.icon, alt: platform.name }),
        h("span", [h("strong", platform.name), h("small", platform.type)]),
        h("b", form.platforms.includes(platform.id) ? "✓" : "")
      ])
    )),
    h("div", { class: "more-platforms" }, [h("p", "更多平台（开发中）"), ...morePlatforms.map((item) => h("button", [h("span", item.icon), item.name]))])
  ])
]);

const OverviewPanel = page(() => [
  h("article", { class: "panel overview-panel" }, [
    h("h2", "内容概览"),
    overviewRow("预计生成内容", `${form.platforms.length} 篇`),
    overviewRow("预计消耗积分", `${form.platforms.length * (form.useAi ? 5 : 1)} 积分`),
    overviewRow("预计生成时间", "约 30 秒")
  ])
]);

const TipsPanel = page(() => [
  h("article", { class: "panel tips-panel" }, [
    h("h2", "创作小贴士"),
    h("ul", [
      h("li", "建议标题包含核心关键词，提升各平台推荐效果"),
      h("li", "正文内容越详细，AI 适配效果越好"),
      h("li", "上传相关图片和视频，可提升内容吸引力"),
      h("li", "可在预览编辑阶段进一步优化各平台内容")
    ])
  ])
]);

function metric(label, value, hint) {
  return h("div", { class: "metric-card" }, [h("span", label), h("strong", value), h("small", hint)]);
}

function overviewRow(label, value) {
  return h("div", { class: "overview-row" }, [h("span", label), h("strong", value)]);
}

function fieldInput(label, required) {
  return h("label", { class: "field" }, [
    h("span", [label, required ? h("em", " *") : null]),
    h("div", { class: "input-wrap" }, [
      h("input", {
        value: form.title,
        maxlength: 100,
        placeholder: "请输入内容标题",
        onInput: (event) => (form.title = event.target.value)
      }),
      h("small", `${form.title.length}/100`)
    ])
  ]);
}

function fieldEditor() {
  return h("label", { class: "field" }, [
    h("span", ["正文 ", h("em", "*")]),
    h("div", { class: "rich-editor" }, [
      h("div", { class: "toolbar" }, [
        h("button", "B"),
        h("button", h("i", "I")),
        h("button", "H"),
        h("button", h("u", "U")),
        h("button", "≡"),
        h("button", "”"),
        h("button", "∞"),
        h("button", "▧"),
        h("button", { class: "rewrite-btn", onClick: () => (form.useAi = true) }, "智能改写")
      ]),
      h("textarea", {
        value: form.content,
        maxlength: 5000,
        placeholder: "请输入核心内容",
        onInput: (event) => (form.content = event.target.value)
      }),
      h("small", `${form.content.length}/5000`)
    ])
  ]);
}

function fieldTags() {
  return h("label", { class: "field" }, [
    h("span", "标签"),
    h("div", { class: "tag-editor" }, [
      ...parsedTags.value.map((tag) => h("span", [tag, h("button", { onClick: () => removeTag(tag) }, "×")])),
      h("input", {
        value: tagDraft.value,
        placeholder: "+ 添加标签",
        onInput: (event) => (tagDraft.value = event.target.value),
        onKeydown: (event) => {
          if (event.key === "Enter" || event.key === ",") {
            event.preventDefault();
            addTag();
          }
        }
      }),
      h("small", `${parsedTags.value.length}/10`)
    ])
  ]);
}

function hiddenInputs() {
  return [
    h("input", { ref: imageInput, hidden: true, type: "file", accept: "image/png,image/jpeg,image/jpg,image/webp", multiple: true, onChange: handleImageUpload }),
    h("input", { ref: videoInput, hidden: true, type: "file", accept: "video/mp4,video/quicktime,video/x-msvideo,video/x-matroska", multiple: true, onChange: handleVideoUpload }),
    h("input", { ref: coverInput, hidden: true, type: "file", accept: "image/png,image/jpeg,image/jpg,image/webp", onChange: handleCoverUpload })
  ];
}

function mediaUploadGrid() {
  const imageHints = ["格式：JPG / PNG / WEBP", "大小：单张不超过 10MB，最多 9 张", "推荐：公众号 900x500，知乎 1200x675，小红书 1080x1440"];
  const videoHints = ["格式：MP4 / MOV / AVI / MKV", "大小：单个不超过 500MB，最多 3 个", "推荐：B站 1920x1080，小红书 1080x1920"];
  const coverHints = ["格式：JPG / PNG / WEBP", "大小：1 张，不超过 10MB", "推荐：B站 1920x1080，公众号 900x383，小红书 1080x1440"];
  return h("div", { class: "media-grid" }, [
    uploadCard("图片", `${form.images.length}/${IMAGE_MAX_COUNT}`, imageHints, form.images, "images", () => imageInput.value?.click()),
    uploadCard("视频", `${form.videos.length}/${VIDEO_MAX_COUNT}`, videoHints, form.videos, "videos", () => videoInput.value?.click()),
    h("div", { class: "media-card cover-card" }, [
      h("strong", ["封面图", h("span", ` (${form.cover ? COVER_MAX_COUNT : 0}/${COVER_MAX_COUNT})`)]),
      h("ul", { class: "media-hint-list" }, coverHints.map((hint) => h("li", hint))),
      h("div", { class: "cover-preview-wrap" }, [
        h("div", { class: ["cover-preview", { empty: !form.cover }] }, form.cover ? h("img", { src: form.cover.url, alt: "封面图" }) : h("span", "未上传")),
        form.cover ? h("div", { class: "media-meta" }, [
          h("strong", form.cover.name || "封面图"),
          h("span", formatSize(form.cover.size))
        ]) : h("p", { class: "media-empty" }, "尚未上传封面")
      ]),
      h("div", { class: "cover-actions" }, [
        h("button", { class: "ghost-btn small", onClick: () => coverInput.value?.click() }, form.cover ? "更换封面" : "上传封面"),
        form.cover ? h("button", { class: "danger-btn small", onClick: removeCover }, "删除") : null
      ])
    ])
  ]);
}

function uploadCard(title, count, hint, list, type, onAdd) {
  const maxCount = type === "videos" ? VIDEO_MAX_COUNT : IMAGE_MAX_COUNT;
  return h("div", { class: "media-card" }, [
    h("strong", [title, h("span", ` (${count})`)]),
    h("ul", { class: "media-hint-list" }, hint.map((item) => h("li", item))),
    h("div", { class: "media-list" }, [
      ...list.map((item, index) =>
        h("div", { class: ["thumb", type === "videos" ? "video-thumb" : "image-thumb"] }, [
          type === "videos" ? h("span", "▷") : h("img", { src: item.url, alt: item.name }),
          h("small", item.name),
          h("em", formatSize(item.size)),
          h("button", { class: "delete-media", title: "删除素材", onClick: () => removeMedia(type, index) }, "×")
        ])
      ),
      list.length < maxCount ? h("button", { class: "add-thumb", onClick: onAdd }, "+") : null
    ])
  ]);
}

function aiGeneratePanel() {
  return h("article", { class: "panel ai-panel" }, [
    h("label", [h("span", "AI 模型"), h("select", { value: form.llmProvider, disabled: !form.useAi, onChange: (event) => (form.llmProvider = event.target.value) }, providers.map((provider) => h("option", { value: provider.value }, provider.label)))]),
    h("label", [h("span", "改写强度"), h("div", { class: "segmented" }, rewriteModes.map((mode) => h("button", { class: { active: aiIntensity.value === mode.value }, onClick: () => (aiIntensity.value = mode.value) }, mode.label)))]),
    h("label", [h("span", "输出语言"), h("select", { value: outputLang.value, onChange: (event) => (outputLang.value = event.target.value) }, [h("option", { value: "zh" }, "中文"), h("option", { value: "en" }, "English")])]),
    h("label", { class: "switch" }, [h("input", { type: "checkbox", checked: form.useAi, onChange: (event) => (form.useAi = event.target.checked) }), h("span"), "启用 AI"]),
    h("button", { class: "primary-btn", disabled: loading.adapt, onClick: generateContent }, loading.adapt ? "正在生成..." : "一键生成内容")
  ]);
}

function previewCard(item) {
  return h("section", { class: "preview-card" }, [
    h("div", { class: "preview-title" }, [h("img", { src: item.icon, alt: item.name }), h("div", [h("h3", item.name), h("span", item.type)])]),
    h("input", { value: item.content.title, onInput: (event) => (item.content.title = event.target.value) }),
    h("textarea", { value: item.content.content || item.content.description, onInput: (event) => (item.content.content = event.target.value) }),
    h("div", { class: "preview-tags" }, normalizeTags(item.content.tags).map((tag) => h("span", `#${tag}`)))
  ]);
}

function recordRow(record, table = false) {
  const open = () => openRecordDetail(record);
  if (table) {
    return h("div", { class: "record-row table", onClick: open }, [
      h("span", record.publish_time || "刚刚"),
      h("strong", record.title || form.title),
      h("span", platformName(record.platform || record.id)),
      h("b", record.status === "failed" ? "失败" : "成功"),
      h("div", { class: "record-actions" }, [
        h("button", { class: "ghost-btn small", onClick: (event) => { event.stopPropagation(); open(); } }, "查看详情"),
        h("button", { class: "danger-btn small", onClick: (event) => { event.stopPropagation(); askDeleteRecord(record); } }, "删除")
      ])
    ]);
  }
  return h("div", { class: "record-row", onClick: open }, [
    h("strong", record.title || form.title),
    h("span", platformName(record.platform || record.id)),
    h("b", record.status === "failed" ? "失败" : "成功"),
    h("small", record.publish_time || "刚刚")
  ]);
}

function materialCard(item) {
  return h("section", { class: "material-card" }, [
    h("div", { class: ["material-preview", item.type] }, item.type === "video" ? h("span", "视频") : h("img", { src: item.url, alt: item.name })),
    h("div", { class: "material-info" }, [
      h("strong", item.name || "未命名素材"),
      h("dl", [
        h("dt", "类型"), h("dd", materialFilterLabel(item.type)),
        h("dt", "大小"), h("dd", formatSize(item.size)),
        h("dt", "格式"), h("dd", materialFormat(item)),
        h("dt", "上传时间"), h("dd", formatMaterialTime(item.created_at)),
      ])
    ]),
    h("div", { class: "card-actions" }, [
      h("button", { class: "ghost-btn small", onClick: () => addMaterialToCurrentTask(item) }, "加入创作"),
      h("button", { class: "ghost-btn small", onClick: () => copyText(item.url) }, "复制链接"),
      h("button", { class: "danger-btn small", onClick: () => removeMaterial(item) }, "删除")
    ])
  ]);
}

function aiProviderCard(provider) {
  const isDefault = aiSettings.provider === provider.value;
  const configured = isProviderConfigured(provider.value);
  return h("section", { class: ["ai-provider-card", provider.tone, { active: isDefault }] }, [
    h("div", { class: "ai-provider-top" }, [
      h("span", { class: ["provider-mark", provider.tone] }, provider.label.slice(0, 1)),
      h("div", [
        h("h3", provider.label),
        h("p", provider.description)
      ])
    ]),
    h("div", { class: "ai-provider-meta" }, [
      h("span", [h("b", "模型"), providerModel(provider.value) || "未配置"]),
      h("span", [h("b", "状态"), configured ? "已配置" : "待配置"]),
      h("span", [h("b", "默认"), isDefault ? "是" : "否"])
    ]),
    h("div", { class: "card-actions" }, [
      h("button", { class: "ghost-btn small", onClick: () => openAiConfigDialog(provider.value) }, "配置"),
      h("button", { class: "ghost-btn small", disabled: testingProvider.value === provider.value, onClick: () => testProvider(provider.value) }, testingProvider.value === provider.value ? "测试中..." : "测试连接"),
      h("button", { class: isDefault ? "primary-outline small" : "primary-btn small", disabled: isDefault || loading.settings, onClick: () => setDefaultProvider(provider.value) }, isDefault ? "默认模型" : "设为默认")
    ])
  ]);
}

function settingInput(label, key, password = false) {
  return h("label", { class: "setting-field" }, [
    h("span", label),
    h("input", { type: password ? "password" : "text", value: aiSettings[key], onInput: (event) => (aiSettings[key] = event.target.value) })
  ]);
}

function settingSelect(label, key, options) {
  return h("label", { class: "setting-field" }, [
    h("span", label),
    h("select", { value: aiSettings[key], onChange: (event) => (aiSettings[key] = event.target.value) }, options.map((option) => h("option", { value: option.value }, option.label)))
  ]);
}

async function login() {
  authError.value = "";
  if (!authForm.account || !authForm.password) {
    authError.value = "请输入账号和密码。";
    return;
  }
  try {
    const response = await apiRequest("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ account: authForm.account, password: authForm.password })
    });
    if (response?.code !== 200) throw new Error(response?.message || "登录失败");
    applyLogin(response.data);
  } catch (error) {
    localStorage.setItem("token", "mock_user_token");
    localStorage.setItem("username", authForm.account);
    username.value = authForm.account;
    authError.value = "";
  }
  await afterAuth();
}

async function register() {
  authError.value = "";
  if (!authForm.name || !authForm.account || !authForm.password) {
    authError.value = "请完整填写注册信息。";
    return;
  }
  if (authForm.password !== authForm.confirm) {
    authError.value = "两次输入的密码不一致。";
    return;
  }
  try {
    const response = await apiRequest("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ username: authForm.name, account: authForm.account, password: authForm.password })
    });
    if (response?.code !== 200) throw new Error(response?.message || "注册失败");
    applyLogin(response.data);
  } catch (error) {
    localStorage.setItem("token", "mock_user_token");
    localStorage.setItem("username", authForm.account);
    username.value = authForm.account;
  }
  await afterAuth();
}

function applyLogin(data) {
  localStorage.setItem("token", data.token || "mock_user_token");
  localStorage.setItem("username", data.username || data.account || authForm.account);
  username.value = data.username || data.account || authForm.account;
}

async function afterAuth() {
  history.value = JSON.parse(localStorage.getItem(`records:${username.value}`) || "[]");
  materials.value = sanitizeMaterials(JSON.parse(localStorage.getItem(`materials:${username.value}`) || "[]"));
  notifications.value = JSON.parse(localStorage.getItem(notificationStorageKey()) || "[]");
  await Promise.all([loadRecords(), loadMaterials(), loadAiSettings(), loadAccounts()]);
  router.push("/dashboard");
}

function logout() {
  localStorage.removeItem("token");
  router.push("/login");
}

function handleUpgradeByCode() {
  const validCodes = ["JUFZ2026", "MULTIPOSTAI", "VIP888"];
  if (!validCodes.includes(memberCode.value.toUpperCase())) {
    upgradeError.value = "会员码无效，请重新输入或选择扫码支付。";
    return;
  }
  isPro.value = true;
  vipStart.value = "2026-05-29";
  vipEnd.value = "2027-05-29";
  localStorage.setItem("isPro", "true");
  localStorage.setItem("vipStart", vipStart.value);
  localStorage.setItem("vipEnd", vipEnd.value);
  upgradeDialogVisible.value = false;
  upgradeError.value = "";
}

function clearAdapted() {
  Object.keys(adapted).forEach((key) => delete adapted[key]);
}

function addTag() {
  const value = tagDraft.value.replace(/[,，]/g, "").trim();
  if (!value || parsedTags.value.includes(value) || parsedTags.value.length >= 10) {
    tagDraft.value = "";
    return;
  }
  form.tagsText = [...parsedTags.value, value].join(",");
  tagDraft.value = "";
}

function removeTag(tag) {
  form.tagsText = parsedTags.value.filter((item) => item !== tag).join(",");
}

function togglePlatform(id) {
  form.platforms = form.platforms.includes(id) ? form.platforms.filter((item) => item !== id) : [...form.platforms, id];
}

function applySample() {
  form.title = "如何用AI工具提升大学生学习效率";
  form.content =
    "随着AI工具的快速发展，大学生在学习过程中可以利用AI辅助完成资料整理、论文阅读、知识总结、代码调试和复习规划等任务。合理使用AI工具不仅可以节省时间，还可以帮助学生建立更加清晰的知识结构。\n\n本文将从学习计划制定、课堂笔记整理、论文阅读辅助、代码学习和考试复习五个方面，介绍AI工具在学习效率提升中的实际应用方法。";
  form.tagsText = "AI学习,大学生,效率提升,学习方法,人工智能";
  form.platforms = platforms.map((platform) => platform.id);
  form.useAi = true;
  notice.value = "";
  publishResults.value = [];
  clearAdapted();
}

function normalizeTags(tags) {
  if (Array.isArray(tags)) return tags;
  if (typeof tags === "string") return tags.split(/[,，、\s]+/).filter(Boolean);
  return parsedTags.value;
}

function platformName(id) {
  return platforms.find((platform) => platform.id === id)?.name || id;
}

function providerLabel(id) {
  return providers.find((provider) => provider.value === id)?.label || id;
}

const currentEditingProvider = computed(() => providers.find((provider) => provider.value === editingProvider.value));

function rewriteModeLabel(value) {
  return rewriteModes.find((mode) => mode.value === value)?.label || value || "balanced";
}

function providerKey(provider, field) {
  return `${provider}${field[0].toUpperCase()}${field.slice(1)}`;
}

function providerModel(provider) {
  return aiSettings[providerKey(provider, "model")];
}

function isProviderConfigured(provider) {
  const meta = providers.find((item) => item.value === provider);
  const hasModel = Boolean(aiSettings[providerKey(provider, "model")]);
  const hasBaseUrl = provider === "gemini" || Boolean(aiSettings[providerKey(provider, "baseUrl")]);
  const hasKey = !meta?.requiresKey || Boolean(aiSettings[providerKey(provider, "key")]);
  return hasModel && hasBaseUrl && hasKey;
}

function openAiConfigDialog(provider) {
  editingProvider.value = provider;
  aiConfigDraft.key = aiSettings[providerKey(provider, "key")] || "";
  aiConfigDraft.baseUrl = aiSettings[providerKey(provider, "baseUrl")] || "";
  aiConfigDraft.model = aiSettings[providerKey(provider, "model")] || "";
  aiConfigDraft.temperature = Number(aiSettings[providerKey(provider, "temperature")] ?? 0.7);
  aiConfigDraft.maxTokens = Number(aiSettings[providerKey(provider, "maxTokens")] ?? 2000);
  aiConfigDraft.setDefault = aiSettings.provider === provider;
  aiConfigDialogVisible.value = true;
}

function closeAiConfigDialog() {
  if (loading.settings) return;
  aiConfigDialogVisible.value = false;
  editingProvider.value = null;
}

function applyDraftToSettings() {
  const provider = editingProvider.value;
  if (!provider) return;
  aiSettings[providerKey(provider, "key")] = aiConfigDraft.key || "";
  aiSettings[providerKey(provider, "baseUrl")] = aiConfigDraft.baseUrl || "";
  aiSettings[providerKey(provider, "model")] = aiConfigDraft.model || "";
  aiSettings[providerKey(provider, "temperature")] = Number(aiConfigDraft.temperature ?? 0.7);
  aiSettings[providerKey(provider, "maxTokens")] = Number(aiConfigDraft.maxTokens ?? 2000);
  if (aiConfigDraft.setDefault) aiSettings.provider = provider;
}

async function saveAiProviderConfig() {
  applyDraftToSettings();
  await saveAiSettings();
  if (!loading.settings) closeAiConfigDialog();
}

async function setDefaultProvider(provider) {
  aiSettings.provider = provider;
  await saveAiSettings();
}

async function testCurrentProvider() {
  applyDraftToSettings();
  await testProvider(editingProvider.value);
}

function materialFilterLabel(type) {
  return { all: "全部", image: "图片", video: "视频", cover: "封面" }[type] || type;
}

function parsePublishTime(value) {
  if (!value) return 0;
  const normalized = typeof value === "string" ? value.replace(" ", "T") : value;
  const time = new Date(normalized).getTime();
  return Number.isNaN(time) ? 0 : time;
}

function formatSize(size = 0) {
  if (size >= 1024 * 1024) return `${(size / 1024 / 1024).toFixed(1)}MB`;
  if (size >= 1024) return `${(size / 1024).toFixed(1)}KB`;
  return `${size || 0}B`;
}

function isLegacySampleMaterial(item) {
  const sampleUrls = ["/uploads/images/cover.jpg", "/uploads/videos/demo.mp4", "/uploads/covers/cover.jpg"];
  return sampleUrls.includes(item?.url) && !(item?.size > 0);
}

function sanitizeMaterials(list = []) {
  return list.filter((item) => !isLegacySampleMaterial(item));
}

function materialFilterCount(type) {
  if (type === "all") return materials.value.length;
  return materials.value.filter((item) => item.type === type).length;
}

function materialFormat(item) {
  const fromApi = item.format || "";
  if (fromApi) return fromApi.toUpperCase();
  const name = item.name || item.url || "";
  const ext = name.includes(".") ? name.split(".").pop() : "";
  return ext ? ext.toUpperCase() : "-";
}

function formatMaterialTime(value) {
  if (!value) return "本地预览";
  const date = new Date(String(value).replace(" ", "T"));
  if (Number.isNaN(date.getTime())) return value;
  const pad = (number) => String(number).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

function notificationStorageKey() {
  return `notifications:${username.value || "guest"}`;
}

function persistNotifications() {
  localStorage.setItem(notificationStorageKey(), JSON.stringify(notifications.value));
}

function addNotification(type, title, message) {
  notifications.value = [
    {
      id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
      type,
      title,
      message,
      time: new Date().toLocaleString(),
      read: false
    },
    ...notifications.value
  ].slice(0, 50);
  persistNotifications();
}

function markNotificationRead(id) {
  const item = notifications.value.find((notification) => notification.id === id);
  if (!item) return;
  item.read = true;
  persistNotifications();
}

function markAllNotificationsRead() {
  notifications.value.forEach((notification) => {
    notification.read = true;
  });
  persistNotifications();
}

function resolvedTheme(mode = themeMode.value) {
  if (mode !== "system") return mode;
  return window.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function applyTheme(mode = themeMode.value) {
  const resolved = resolvedTheme(mode);
  document.documentElement.dataset.theme = resolved;
  document.documentElement.dataset.themeMode = mode;
}

function selectTheme(mode) {
  themeMode.value = mode;
  localStorage.setItem("themeMode", mode);
  applyTheme(mode);
  themeMenuOpen.value = false;
}

function fileExt(file) {
  const name = file?.name || "";
  const index = name.lastIndexOf(".");
  return index >= 0 ? name.slice(index).toLowerCase() : "";
}

function isAllowedVideo(file) {
  return VIDEO_TYPES.includes(file.type) || VIDEO_EXTS.includes(fileExt(file));
}

function validateUploadFile(file, type) {
  if (type === "image") {
    if (!IMAGE_TYPES.includes(file.type)) return "只能上传 JPG / PNG / WEBP 图片。";
    if (file.size > IMAGE_MAX_SIZE) return "单张图片不能超过 10MB。";
  }
  if (type === "video") {
    if (!isAllowedVideo(file)) return "只能上传 MP4 / MOV / AVI / MKV 视频。";
    if (file.size > VIDEO_MAX_SIZE) return "单个视频不能超过 500MB。";
  }
  if (type === "cover") {
    if (!IMAGE_TYPES.includes(file.type)) return "封面必须是 JPG / PNG / WEBP 图片。";
    if (file.size > IMAGE_MAX_SIZE) return "封面不能超过 10MB。";
  }
  return "";
}

async function uploadFile(file, type) {
  const body = new FormData();
  body.append("file", file);
  return apiRequest(`/api/upload/${type}`, { method: "POST", body });
}

async function addLocalFile(file, type) {
  const item = {
    id: `local-${Date.now()}-${Math.random()}`,
    file,
    name: file.name,
    url: URL.createObjectURL(file),
    type: type === "image" ? "image" : type === "video" ? "video" : "cover",
    size: file.size,
    created_at: new Date().toLocaleString(),
    usage_count: 0,
    localOnly: true
  };
  try {
    const response = await uploadFile(file, type);
    if (response?.code === 200 && response.data?.file_url) {
      item.url = response.data.file_url;
      item.name = response.data.file_name || item.name;
      item.size = response.data.size || item.size;
      item.localOnly = false;
    }
  } catch (error) {
    notice.value = "未连接后端上传服务，当前仅本地预览。";
  }
  upsertMaterial(item);
  return item;
}

function upsertMaterial(item) {
  const exists = materials.value.some((material) => material.url === item.url);
  if (!exists) {
    materials.value.unshift({ ...item });
    localStorage.setItem(`materials:${username.value || "guest"}`, JSON.stringify(materials.value));
  }
}

async function handleImageUpload(event) {
  const files = Array.from(event.target.files || []);
  for (const file of files) {
    if (form.images.length >= IMAGE_MAX_COUNT) {
      notice.value = "图片最多只能上传 9 张。";
      break;
    }
    const error = validateUploadFile(file, "image");
    if (error) {
      notice.value = error;
      continue;
    }
    form.images.push(await addLocalFile(file, "image"));
  }
  event.target.value = "";
}

async function handleVideoUpload(event) {
  const files = Array.from(event.target.files || []);
  for (const file of files) {
    if (form.videos.length >= VIDEO_MAX_COUNT) {
      notice.value = "视频最多只能上传 3 个。";
      break;
    }
    const error = validateUploadFile(file, "video");
    if (error) {
      notice.value = error;
      continue;
    }
    form.videos.push(await addLocalFile(file, "video"));
  }
  event.target.value = "";
}

async function handleCoverUpload(event) {
  const file = event.target.files?.[0];
  if (!file) return;
  const error = validateUploadFile(file, "cover");
  if (error) {
    notice.value = error;
    event.target.value = "";
    return;
  }
  form.cover = await addLocalFile(file, "cover");
  event.target.value = "";
}

function removeMedia(type, index) {
  const item = form[type][index];
  if (item?.url?.startsWith("blob:")) URL.revokeObjectURL(item.url);
  form[type].splice(index, 1);
}

function removeCover() {
  if (form.cover?.url?.startsWith("blob:")) URL.revokeObjectURL(form.cover.url);
  form.cover = null;
}

async function removeMaterial(item) {
  const isBackendMaterial = Number.isInteger(Number(item.id)) && !item.localOnly;
  if (isBackendMaterial) {
    try {
      await apiRequest(`/api/materials/${item.id}`, { method: "DELETE" });
    } catch (error) {
      notice.value = "后端删除失败，已先从当前列表移除。";
    }
  }
  materials.value = materials.value.filter((material) => material.id !== item.id && material.url !== item.url);
  form.images = form.images.filter((material) => material.url !== item.url);
  form.videos = form.videos.filter((material) => material.url !== item.url);
  if (form.cover?.url === item.url) form.cover = null;
  localStorage.setItem(`materials:${username.value || "guest"}`, JSON.stringify(materials.value));
}

function addMaterialToCurrentTask(item) {
  const target = item.type === "video" ? form.videos : item.type === "cover" ? null : form.images;
  if (item.type === "cover") {
    form.cover = item;
  } else if (target && !target.some((existing) => existing.url === item.url)) {
    if (item.type === "image" && target.length >= IMAGE_MAX_COUNT) {
      notice.value = "图片最多只能添加 9 张。";
      return;
    }
    if (item.type === "video" && target.length >= VIDEO_MAX_COUNT) {
      notice.value = "视频最多只能添加 3 个。";
      return;
    }
    target.push(item);
  }
  item.usage_count = (item.usage_count || 0) + 1;
  localStorage.setItem(`materials:${username.value || "guest"}`, JSON.stringify(materials.value));
  notice.value = "素材已加入当前创作任务。";
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    notice.value = "素材链接已复制。";
  } catch (error) {
    notice.value = text;
  }
}

function buildLocalPreview() {
  const suffix = aiIntensity.value === "creative" ? "，让学习更轻松" : "";
  return Object.fromEntries(
    selectedPlatforms.value.map((platform) => {
      const base = { title: form.title, content: form.content, tags: parsedTags.value };
      if (platform.id === "wechat") {
        base.title = `${form.title}：一份可执行指南`;
        base.content = `导语：${form.content}\n\n适合拆成计划、执行、复盘三个部分发布，突出结构化方法。`;
      }
      if (platform.id === "zhihu") {
        base.title = `${form.title}？`;
        base.content = `${form.content}\n\n结论先行：AI 的价值不是替代思考，而是帮助学生更快形成可验证的学习路径。`;
      }
      if (platform.id === "bilibili") {
        base.title = `大学生必看：${form.title}${suffix}`;
        base.description = "视频简介：围绕学习计划、论文阅读、代码调试和复习规划拆解 AI 工具用法。";
        base.content = base.description;
        base.video = form.videos[0]?.url || "";
      }
      if (platform.id === "xiaohongshu") {
        base.title = "AI学习效率提升方法｜大学生亲测";
        base.content = `${form.content.slice(0, 130)}...\n\n适合收藏的学习工作流，搭配真实案例更容易种草。`;
      }
      base.images = form.images.map((item) => item.url);
      base.videos = form.videos.map((item) => item.url);
      base.cover = form.cover?.url || null;
      return [platform.id, base];
    })
  );
}

function validatePublishBeforeSubmit() {
  if (!form.title.trim()) return "发布前请先填写标题。";
  if (!form.content.trim()) return "发布前请先填写正文。";
  if (!form.platforms.length) return "发布前请至少选择一个目标平台。";
  if (!previewList.value.length) return "请先生成各平台预览内容。";

  for (const platform of selectedPlatforms.value) {
    const content = adapted[platform.id];
    if (!content) return `${platform.name} 缺少待发布内容。`;
    if (!String(content.title || "").trim()) return `${platform.name} 缺少标题。`;
    const body = platform.id === "bilibili" ? content.description || content.content : content.content;
    if (!String(body || "").trim()) return `${platform.name} 缺少正文内容。`;
    if (platform.id === "bilibili") {
      const video = content.video || content.videos?.[0] || form.videos[0]?.url;
      if (!video) return "B站模拟发布需要至少上传 1 个视频素材。";
    }
  }
  return "";
}

async function generateContent() {
  notice.value = "";
  if (!form.title.trim()) {
    notice.value = "标题不能为空，请先输入内容标题。";
    return;
  }
  if (!form.content.trim()) {
    notice.value = "正文不能为空，请先输入核心内容。";
    return;
  }
  if (!form.platforms.length) {
    notice.value = "请至少选择一个目标平台。";
    return;
  }
  loading.adapt = true;
  publishResults.value = [];
  clearAdapted();
  try {
    const response = await apiRequest("/api/content/generate", {
      method: "POST",
      body: JSON.stringify({
        title: form.title,
        content: form.content,
        tags: parsedTags.value,
        author: username.value || null,
        platforms: form.platforms,
        use_ai: form.useAi,
        llm_provider: form.useAi ? aiSettings.provider || form.llmProvider : null,
        media_files: {
          images: form.images.map((item) => item.url),
          videos: form.videos.map((item) => item.url),
          cover: form.cover?.url || null
        }
      })
    });
    taskId.value = response?.task_id || Date.now();
    Object.assign(adapted, response?.code === 200 && response.data ? response.data : buildLocalPreview());
    if (response?.code === 200) {
      addNotification("success", "AI生成成功", `已生成 ${Object.keys(adapted).length} 个平台内容。`);
    } else {
      notice.value = "后端未返回有效结果，已使用本地规则生成预览。";
    }
  } catch (error) {
    taskId.value = Date.now();
    Object.assign(adapted, buildLocalPreview());
    notice.value = "未连接到后端服务，已使用本地演示数据生成预览。";
  } finally {
    loading.adapt = false;
    router.push("/preview");
  }
}

async function mockLogin(platformId) {
  const platform = platforms.find((item) => item.id === platformId);
  accounts[platformId].loggedIn = true;
  accounts[platformId].accountName = accounts[platformId].accountName || `${platform?.name || platformId}测试账号`;
  accounts[platformId].authType = "Mock Token";
  accounts[platformId].expireAt = "2026-12-31";
  try {
    await apiRequest("/api/account/mock-login", {
      method: "POST",
      body: JSON.stringify({ platform: platformId, account_name: accounts[platformId].accountName })
    });
  } catch (error) {
    // 离线演示允许模拟登录成功。
  }
}

function logoutPlatform(platformId) {
  accounts[platformId].loggedIn = false;
  accounts[platformId].authType = "未授权";
  accounts[platformId].expireAt = "-";
}

async function publishAll() {
  notice.value = "";
  const validationError = validatePublishBeforeSubmit();
  if (validationError) {
    notice.value = validationError;
    return;
  }
  loading.publish = true;
  try {
    const response = await apiRequest("/api/publish", {
      method: "POST",
      body: JSON.stringify({
        task_id: taskId.value || Date.now(),
        platforms: form.platforms,
        contents: adapted,
        publish_mode: form.publishMode
      })
    });
    if (response?.code !== 200) {
      throw new Error(response?.message || "模拟发布失败");
    }
    publishResults.value = response.data || [];
  } catch (error) {
    publishResults.value = selectedPlatforms.value.map((platform, index) => ({
      id: `${Date.now()}-${index}`,
      title: form.title,
      platform: platform.id,
      status: "failed",
      message: error?.message || "模拟发布失败",
      publish_time: new Date().toLocaleString(),
      detail: buildLocalRecordDetail()
    }));
    notice.value = error?.message || "模拟发布失败，请检查后端服务。";
  } finally {
    const failedCount = publishResults.value.filter((item) => item.status === "failed").length;
    const successCount = publishResults.value.length - failedCount;
    if (successCount > 0) addNotification("success", "模拟发布成功", `${successCount} 个平台已完成模拟发布。`);
    if (failedCount > 0) addNotification("danger", "发布失败", `${failedCount} 个平台发布失败，请查看发布记录。`);
    if (successCount > 0) {
      await loadRecords();
    } else {
      history.value = [...publishResults.value, ...history.value].slice(0, 30);
      localStorage.setItem(`records:${username.value || "guest"}`, JSON.stringify(history.value));
    }
    loading.publish = false;
    router.push("/records");
  }
}

function buildLocalRecordDetail(record) {
  return {
    id: record?.id || Date.now(),
    task_title: form.title,
    source_content: form.content,
    publish_time: record?.publish_time || new Date().toLocaleString(),
    publish_mode: "mock",
    status: record?.status || "success",
    mock_publish_id: record?.mock_publish_id || null,
    platform_contents: selectedPlatforms.value.map((platform) => ({
      platform: platform.id,
      ...(adapted[platform.id] || {}),
      status: "success"
    }))
  };
}

async function openRecordDetail(record) {
  selectedRecord.value = record.detail || buildLocalRecordDetail(record);
  recordDetailVisible.value = true;
  if (!Number.isInteger(Number(record.id))) return;
  try {
    const response = await apiRequest(`/api/records/${record.id}`);
    if (response?.code === 200) selectedRecord.value = response.data;
  } catch (error) {
    // 保留本地详情。
  }
}

function askDeleteRecord(record) {
  pendingDeleteRecord.value = record;
  deleteDialogVisible.value = true;
}

function cancelDeleteRecord() {
  if (deletingRecord.value) return;
  deleteDialogVisible.value = false;
  pendingDeleteRecord.value = null;
}

async function confirmDeleteRecord() {
  const record = pendingDeleteRecord.value;
  if (!record) return;
  deletingRecord.value = true;

  const recordId = record.id;
  const isBackendRecord = Number.isInteger(Number(recordId));

  try {
    if (isBackendRecord) {
      try {
        await apiRequest(`/api/records/${recordId}`, { method: "DELETE" });
      } catch (error) {
        // 后端不可用时仍删除本地缓存中的模拟记录。
      }
    }

    history.value = history.value.filter((item) => item.id !== recordId);
    localStorage.setItem(`records:${username.value || "guest"}`, JSON.stringify(history.value));
    if (selectedRecord.value?.id === recordId) {
      recordDetailVisible.value = false;
      selectedRecord.value = null;
    }

    await loadRecords();
    deleteDialogVisible.value = false;
    pendingDeleteRecord.value = null;
  } finally {
    deletingRecord.value = false;
  }
}

async function loadRecords() {
  loading.records = true;
  try {
    const response = await apiRequest("/api/records?limit=50");
    if (response?.code === 200 && response.data?.length) history.value = response.data;
  } catch (error) {
    history.value = JSON.parse(localStorage.getItem(`records:${username.value || "guest"}`) || "[]");
  } finally {
    loading.records = false;
  }
}

async function loadMaterials() {
  loading.materials = true;
  try {
    const response = await apiRequest("/api/materials");
    if (response?.code === 200) {
      const localItems = sanitizeMaterials(JSON.parse(localStorage.getItem(`materials:${username.value || "guest"}`) || "[]"));
      materials.value = sanitizeMaterials([...response.data, ...localItems.filter((item) => item.localOnly)]);
    }
  } catch (error) {
    materials.value = sanitizeMaterials(JSON.parse(localStorage.getItem(`materials:${username.value || "guest"}`) || "[]"));
  } finally {
    loading.materials = false;
  }
}

async function loadAccounts() {
  try {
    const response = await apiRequest("/api/account/list");
    if (response?.code === 200) {
      response.data.forEach((item) => {
        if (!accounts[item.platform]) return;
        accounts[item.platform].loggedIn = item.login_status === "logged_in";
        accounts[item.platform].accountName = item.account_name || accounts[item.platform].accountName;
        accounts[item.platform].authType = item.auth_type === "mock" ? "Mock Token" : item.auth_type;
        accounts[item.platform].expireAt = item.token_expire_time || "-";
      });
    }
  } catch (error) {
    // 保留本地账号状态。
  }
}

async function loadAiSettings() {
  try {
    const response = await apiRequest("/api/settings/llm");
    if (response?.code === 200 && response.data && Object.keys(response.data).length) {
      Object.assign(aiSettings, response.data);
      form.llmProvider = aiSettings.provider || form.llmProvider;
      outputLang.value = aiSettings.defaultLang || outputLang.value;
      aiIntensity.value = aiSettings.defaultIntensity || aiIntensity.value;
    }
  } catch (error) {
    const saved = localStorage.getItem(`aiSettings:${username.value || "guest"}`);
    if (saved) Object.assign(aiSettings, JSON.parse(saved));
  }
}

async function saveAiSettings() {
  loading.settings = true;
  aiSettings.provider = aiSettings.provider || form.llmProvider;
  form.llmProvider = aiSettings.provider;
  outputLang.value = aiSettings.defaultLang;
  aiIntensity.value = aiSettings.defaultIntensity;
  localStorage.setItem("outputLang", outputLang.value);
  localStorage.setItem("aiIntensity", aiIntensity.value);
  localStorage.setItem(`aiSettings:${username.value || "guest"}`, JSON.stringify(aiSettings));
  try {
    await apiRequest("/api/settings/llm", {
      method: "POST",
      body: JSON.stringify({ provider: aiSettings.provider, settings: aiSettings })
    });
    notice.value = "AI 设置已保存到后端。";
  } catch (error) {
    notice.value = "后端不可用，AI 设置已保存到本地。";
  } finally {
    loading.settings = false;
  }
}

async function testProvider(provider = aiSettings.provider) {
  if (!provider) return;
  testingProvider.value = provider;
  try {
    const response = await apiRequest("/api/settings/llm/test", {
      method: "POST",
      body: JSON.stringify({ provider, settings: aiSettings })
    });
    notice.value = response?.message || `${providerLabel(provider)} 连接测试已完成。`;
    if (response?.code !== 200) {
      addNotification("danger", "模型连接失败", `${providerLabel(provider)} 连接测试失败，请检查 API Key、Base URL 和模型名。`);
    }
  } catch (error) {
    notice.value = `${providerLabel(provider)} 连接测试失败，请检查配置。`;
    addNotification("danger", "模型连接失败", `${providerLabel(provider)} 连接测试失败，请检查 API Key、Base URL 和模型名。`);
  } finally {
    testingProvider.value = "";
  }
}

function testModelConnection() {
  return testProvider(aiSettings.provider);
}

onMounted(() => {
  applyTheme();
  window.matchMedia?.("(prefers-color-scheme: dark)").addEventListener("change", () => {
    if (themeMode.value === "system") applyTheme("system");
  });
  if (!isAuthPage.value) {
    loadRecords();
    loadMaterials();
    loadAiSettings();
    loadAccounts();
  }
});
</script>

<style>
:root {
  --accent: #ff6b35;
  --accent-soft: #fff1eb;
  --blue: #4d8cff;
  --red: #f2556a;
  --green: #31b46d;
  --purple: #7657ff;
  --ink: #18213a;
  --muted: #778098;
  --line: #e9edf5;
  --panel: #ffffff;
  --page: #f6f8fc;
  --bg: #f6f8fc;
  --surface: #ffffff;
  --shadow: 0 12px 34px rgba(25, 34, 61, 0.07);
  --sidebar: 260px;
  --topbar: 74px;
}

:root[data-theme="dark"] {
  color-scheme: dark;
  --accent: #ff8a5c;
  --accent-soft: #3b241d;
  --blue: #78a8ff;
  --red: #ff7385;
  --green: #45d084;
  --purple: #9b86ff;
  --ink: #eef3ff;
  --muted: #9da8bd;
  --line: #2b3548;
  --panel: #151c2b;
  --page: #0d1320;
  --bg: #0d1320;
  --surface: #151c2b;
  --shadow: 0 14px 40px rgba(0, 0, 0, 0.34);
}

* { box-sizing: border-box; }
html, body, #app { min-height: 100%; background: var(--page); }
body { margin: 0; min-width: 320px; min-height: 100vh; background: var(--page); color: var(--ink); font-family: "Inter", "PingFang SC", "Microsoft YaHei", Arial, sans-serif; }
button, input, textarea, select { font: inherit; }
button { cursor: pointer; }
a { color: inherit; text-decoration: none; }

.auth-page { min-height: 100vh; display: grid; place-items: center; padding: 24px; background: linear-gradient(135deg, #fff7f2, #eef4ff); }
.auth-card { width: min(420px, 100%); display: grid; gap: 14px; padding: 34px; border: 1px solid var(--line); border-radius: 12px; background: #fff; box-shadow: var(--shadow); }
.auth-card img { width: 76px; height: 76px; object-fit: contain; margin: 0 auto; }
.auth-card h1, .auth-card p { margin: 0; text-align: center; }
.auth-card p { color: var(--muted); }
.auth-card label, .upgrade-dialog label { display: grid; gap: 8px; font-weight: 800; }
.auth-card input, .upgrade-dialog input, .setting-field input { height: 44px; padding: 0 12px; border: 1px solid #dfe5ef; border-radius: 8px; outline: 0; }
.error-text { margin: 0; color: #c63f2d; font-weight: 800; }
.auth-link { text-align: center; color: var(--blue); font-weight: 800; }

.app-shell { min-height: 100vh; padding: var(--topbar) 0 0 var(--sidebar); background: var(--page); }
.sidebar { position: fixed; inset: 0 auto 0 0; z-index: 10; width: var(--sidebar); display: flex; flex-direction: column; gap: 22px; padding: 22px; background: #fff; border-right: 1px solid var(--line); }
.brand { display: flex; align-items: center; gap: 12px; min-height: 50px; }
.brand-logo { width: 54px; height: 54px; object-fit: contain; }
.brand strong { display: block; font-size: 23px; letter-spacing: 0; }
.brand span { display: block; margin-top: 2px; color: #53607a; font-size: 13px; font-weight: 700; }
.nav-list { display: grid; gap: 7px; }
.nav-item { position: relative; display: flex; align-items: center; gap: 14px; min-height: 48px; padding: 0 16px; border-radius: 8px; color: #5d6680; font-weight: 700; }
.nav-item.active { background: var(--accent-soft); color: var(--accent); }
.nav-item.active::before { content: ""; position: absolute; left: -22px; width: 4px; height: 28px; border-radius: 0 4px 4px 0; background: var(--accent); }
.nav-icon { width: 24px; text-align: center; font-size: 18px; }

.publish-overview-card, .upgrade-card, .panel { border: 1px solid var(--line); border-radius: 8px; background: var(--panel); box-shadow: var(--shadow); }
.publish-overview-card { margin-top: auto; padding: 18px; }
.publish-overview-card p { margin: 0 0 14px; font-weight: 800; font-size: 14px; }
.publish-overview-grid { display: grid; gap: 10px; }
.publish-overview-item { display: flex; align-items: center; justify-content: space-between; gap: 10px; min-height: 34px; padding-bottom: 9px; border-bottom: 1px solid #f0f2f7; color: #68728b; font-size: 13px; }
.publish-overview-item:last-child { border-bottom: 0; padding-bottom: 0; }
.publish-overview-item strong { color: var(--ink); font-size: 16px; white-space: nowrap; }
.upgrade-card { display: grid; gap: 8px; padding: 18px; background: linear-gradient(145deg, #f0edff, #fff6fb); color: var(--purple); }
.upgrade-card.pro { background: #f1fff8; color: #138452; }
.upgrade-card span { font-size: 13px; }
.upgrade-card button { height: 40px; border: 0; border-radius: 8px; background: linear-gradient(135deg, #6b6cff, #9b45ff); color: #fff; font-weight: 800; }

.topbar { position: fixed; top: 0; right: 0; left: var(--sidebar); z-index: 9; height: var(--topbar); display: flex; align-items: center; justify-content: space-between; gap: 20px; padding: 0 28px; background: rgba(255, 255, 255, 0.95); border-bottom: 1px solid var(--line); backdrop-filter: blur(16px); }
.stepper { display: flex; align-items: center; gap: 24px; min-width: 0; }
.step { display: flex; align-items: center; gap: 10px; color: #9aa1b4; white-space: nowrap; }
.step:not(:last-child)::after { content: ">"; margin-left: 14px; color: #c4cad7; font-size: 18px; }
.step span { width: 28px; height: 28px; display: grid; place-items: center; border-radius: 50%; background: #d7dbe4; color: #fff; font-weight: 800; font-size: 13px; }
.step strong { font-size: 14px; }
.step.active { color: var(--ink); }
.step.active span, .step.done span { background: var(--accent); }
.top-actions, .profile { display: flex; align-items: center; gap: 14px; }
.icon-btn { width: 38px; height: 38px; border: 0; border-radius: 50%; background: transparent; color: #4f5972; font-size: 22px; }
.bell svg { width: 22px; height: 22px; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.notification-wrap { position: relative; }
.bell { position: relative; display: grid; place-items: center; }
.bell b { position: absolute; top: -4px; right: -3px; min-width: 18px; height: 18px; display: grid; place-items: center; padding: 0 5px; border: 2px solid #fff; border-radius: 99px; background: #ff4f6d; color: #fff; font-size: 10px; line-height: 1; }
.notification-panel { position: absolute; top: 50px; right: 0; z-index: 40; width: min(380px, calc(100vw - 32px)); display: grid; gap: 10px; padding: 14px; border: 1px solid var(--line); border-radius: 12px; background: #fff; box-shadow: 0 20px 60px rgba(18, 27, 47, 0.16); }
.notification-head { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.notification-head strong { font-size: 15px; }
.notification-head button, .notification-item button { border: 0; background: transparent; color: var(--blue); font-size: 12px; font-weight: 900; }
.notification-list { display: grid; gap: 8px; max-height: 360px; overflow: auto; }
.notification-item { display: flex; justify-content: space-between; gap: 10px; padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; }
.notification-item.unread { border-color: #b9cdfa; background: #f5f8ff; }
.notification-item.success { border-left: 4px solid var(--green); }
.notification-item.danger { border-left: 4px solid #e5485d; }
.notification-item strong, .notification-item p, .notification-item small { display: block; margin: 0; }
.notification-item p { margin-top: 5px; color: #596276; font-size: 13px; line-height: 1.5; }
.notification-item small { margin-top: 6px; color: #8a94a8; font-size: 12px; }
.notification-empty { padding: 22px; border: 1px dashed #d8deea; border-radius: 8px; background: #fbfcff; color: #7b8498; text-align: center; font-weight: 800; }
.profile { padding-left: 18px; border-left: 1px solid var(--line); }
.avatar { width: 42px; height: 42px; display: grid; place-items: center; border-radius: 50%; background: linear-gradient(135deg, #f8b28d, #5a87c8); color: #fff; font-weight: 900; }
.profile strong, .profile span { display: block; }
.profile strong { font-size: 14px; }
.profile div span { width: max-content; margin-top: 3px; padding: 2px 8px; border-radius: 99px; background: #fff2cc; color: #b88910; font-size: 11px; font-weight: 800; }
.logout-btn { border: 0; background: transparent; color: #7a849a; font-weight: 800; }

.theme-wrap { position: relative; }
.theme-menu { position: absolute; top: 50px; right: 0; z-index: 40; width: 160px; display: grid; gap: 6px; padding: 8px; border: 1px solid var(--line); border-radius: 12px; background: var(--panel); box-shadow: 0 20px 60px rgba(18, 27, 47, 0.16); }
.theme-menu button { display: flex; align-items: center; gap: 9px; height: 38px; padding: 0 10px; border: 0; border-radius: 8px; background: transparent; color: var(--ink); font-weight: 800; text-align: left; }
.theme-menu button:hover, .theme-menu button.active { background: var(--accent-soft); color: var(--accent); }
.theme-menu span { width: 18px; text-align: center; }

:root[data-theme="dark"] .auth-card,
:root[data-theme="dark"] .sidebar,
:root[data-theme="dark"] .topbar,
:root[data-theme="dark"] .panel,
:root[data-theme="dark"] .metric-card,
:root[data-theme="dark"] .publish-overview-card,
:root[data-theme="dark"] .profile,
:root[data-theme="dark"] .notification-panel,
:root[data-theme="dark"] .upgrade-dialog,
:root[data-theme="dark"] .delete-dialog,
:root[data-theme="dark"] .ai-config-dialog,
:root[data-theme="dark"] .record-drawer,
:root[data-theme="dark"] .preview-card,
:root[data-theme="dark"] .account-card,
:root[data-theme="dark"] .material-card,
:root[data-theme="dark"] .media-card,
:root[data-theme="dark"] .ai-provider-card,
:root[data-theme="dark"] .platform-card,
:root[data-theme="dark"] .record-row,
:root[data-theme="dark"] .detail-card {
  background: var(--panel);
  border-color: var(--line);
  color: var(--ink);
}
:root[data-theme="dark"] body,
:root[data-theme="dark"] #app,
:root[data-theme="dark"] .app-shell,
:root[data-theme="dark"] .workspace {
  background: var(--page);
}
:root[data-theme="dark"] .topbar { background: rgba(21, 28, 43, 0.96); }
:root[data-theme="dark"] .upgrade-card { background: linear-gradient(145deg, #211f36, #241b2f); color: #d7ccff; }
:root[data-theme="dark"] .upgrade-card.pro { background: #102b21; color: #73e4aa; }
:root[data-theme="dark"] .icon-btn,
:root[data-theme="dark"] .ghost-btn,
:root[data-theme="dark"] .primary-outline,
:root[data-theme="dark"] input,
:root[data-theme="dark"] textarea,
:root[data-theme="dark"] select {
  background: #101827;
  border-color: var(--line);
  color: var(--ink);
}
:root[data-theme="dark"] .empty-state,
:root[data-theme="dark"] .notification-empty,
:root[data-theme="dark"] .notification-item,
:root[data-theme="dark"] .notification-item.unread,
:root[data-theme="dark"] .media-hint-list,
:root[data-theme="dark"] .material-preview,
:root[data-theme="dark"] .material-preview.cover,
:root[data-theme="dark"] .ai-provider-meta,
:root[data-theme="dark"] .delete-record-preview,
:root[data-theme="dark"] .source-text,
:root[data-theme="dark"] .input-wrap,
:root[data-theme="dark"] .tag-editor,
:root[data-theme="dark"] .rich-editor,
:root[data-theme="dark"] .more-platforms button,
:root[data-theme="dark"] .pay-grid div,
:root[data-theme="dark"] .thumb,
:root[data-theme="dark"] .add-thumb,
:root[data-theme="dark"] .cover-preview {
  background: #101827;
  border-color: var(--line);
}
:root[data-theme="dark"] .field > span,
:root[data-theme="dark"] .ai-panel label > span,
:root[data-theme="dark"] .setting-field span,
:root[data-theme="dark"] .ai-config-form label,
:root[data-theme="dark"] .toolbar button,
:root[data-theme="dark"] .toolbar .rewrite-btn,
:root[data-theme="dark"] .material-info dd,
:root[data-theme="dark"] .ai-provider-meta b,
:root[data-theme="dark"] .profile strong,
:root[data-theme="dark"] .metric-card strong {
  color: var(--ink);
}
:root[data-theme="dark"] .brand span,
:root[data-theme="dark"] .nav-item,
:root[data-theme="dark"] .metric-card span,
:root[data-theme="dark"] .metric-card small,
:root[data-theme="dark"] .media-card strong span,
:root[data-theme="dark"] .media-empty,
:root[data-theme="dark"] .material-info dt,
:root[data-theme="dark"] .library-toolbar > span,
:root[data-theme="dark"] .overview-row,
:root[data-theme="dark"] .tips-panel ul,
:root[data-theme="dark"] .help-panel ul,
:root[data-theme="dark"] .record-row span,
:root[data-theme="dark"] .record-row small,
:root[data-theme="dark"] .detail-meta,
:root[data-theme="dark"] .detail-card p,
:root[data-theme="dark"] .source-text,
:root[data-theme="dark"] .notification-item p {
  color: var(--muted);
}
:root[data-theme="dark"] .filter-tabs button,
:root[data-theme="dark"] .segmented,
:root[data-theme="dark"] .segmented button.active,
:root[data-theme="dark"] .preview-tags span,
:root[data-theme="dark"] .tag-editor span {
  background: #101827;
  border-color: var(--line);
  color: var(--ink);
}
:root[data-theme="dark"] .platform-card.selected.wechat,
:root[data-theme="dark"] .platform-card.selected.zhihu,
:root[data-theme="dark"] .platform-card.selected.bilibili,
:root[data-theme="dark"] .platform-card.selected.xiaohongshu {
  background: #1b2638;
  border-color: var(--accent);
}
:root[data-theme="dark"] .ai-default-card {
  background: linear-gradient(135deg, #151f33, #201a2d);
  border-color: var(--line);
}
:root[data-theme="dark"] .danger-btn { background: #2a1620; border-color: #6b2d3a; color: #ff95a4; }
:root[data-theme="dark"] .danger-btn:hover { background: #351a25; }
:root[data-theme="dark"] .notice { background: #2c2115; border-color: #725233; color: #ffd0aa; }

.workspace { display: grid; grid-template-columns: minmax(0, 1fr) 430px; gap: 22px; max-width: 1660px; margin: 0 auto; padding: 22px 28px 34px; }
.workspace.wide { grid-template-columns: minmax(0, 1fr); }
.main-column, .side-column { display: grid; align-content: start; gap: 20px; }
.panel { padding: 22px; }
.panel-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; margin-bottom: 20px; }
.panel-head.compact { margin-bottom: 16px; }
.panel h2, .panel-head h2 { margin: 0; font-size: 20px; line-height: 1.2; }
.panel-head p { margin: 8px 0 0; color: var(--muted); font-size: 14px; }
.dashboard-hero { display: flex; align-items: center; justify-content: space-between; gap: 20px; }
.quick-actions, .card-actions, .settings-actions { display: flex; gap: 10px; flex-wrap: wrap; }
.metric-grid, .material-stats { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; }
.metric-card { display: grid; gap: 8px; padding: 18px; border: 1px solid var(--line); border-radius: 8px; background: #fff; box-shadow: var(--shadow); }
.metric-card span { color: #68728b; font-weight: 800; }
.metric-card strong { font-size: 24px; }
.metric-card small { color: #8b94a8; }

.field { display: grid; gap: 10px; margin-top: 18px; }
.field > span, .ai-panel label > span, .setting-field span { color: #17203a; font-size: 14px; font-weight: 800; }
.field em { color: var(--red); font-style: normal; }
.input-wrap, .tag-editor, .rich-editor { border: 1px solid #dfe5ef; border-radius: 8px; background: #fff; }
.input-wrap { display: flex; align-items: center; gap: 10px; padding: 0 12px; }
.input-wrap input { flex: 1; min-width: 0; height: 46px; border: 0; outline: 0; color: var(--ink); }
.input-wrap small, .rich-editor small, .tag-editor small { color: #929bae; font-size: 12px; }
.toolbar { display: flex; align-items: center; gap: 8px; height: 46px; padding: 0 12px; border-bottom: 1px solid var(--line); }
.toolbar button { min-width: 26px; height: 28px; border: 0; border-radius: 6px; background: transparent; color: #3d465e; font-weight: 800; }
.toolbar .rewrite-btn { margin-left: auto; padding: 0 14px; border: 1px solid var(--line); background: #fff; color: #49546f; font-weight: 800; }
.rich-editor textarea { width: 100%; min-height: 164px; resize: vertical; border: 0; outline: 0; padding: 18px; color: #283149; line-height: 1.8; }
.rich-editor small { display: block; padding: 0 14px 12px; text-align: right; }
.tag-editor { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; min-height: 48px; padding: 8px 10px; }
.tag-editor span { display: inline-flex; align-items: center; gap: 8px; height: 30px; padding: 0 10px; border-radius: 6px; background: #f3f6fb; color: #596276; font-size: 13px; font-weight: 700; }
.tag-editor button { border: 0; background: transparent; color: #98a1b3; }
.tag-editor input { flex: 1; min-width: 120px; border: 0; outline: 0; }

.media-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.media-card { min-width: 0; max-width: 100%; padding: 14px; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }
.media-card strong { display: block; margin-bottom: 8px; font-size: 14px; }
.media-card strong span, .media-hint { color: #7b8498; }
.media-hint-list { min-height: 72px; margin: 0 0 10px; padding: 10px 12px 10px 26px; border: 1px solid #edf1f7; border-radius: 8px; background: #fbfcff; color: #69738a; font-size: 12px; line-height: 1.55; }
.media-list { display: flex; gap: 10px; width: 100%; max-width: 100%; overflow-x: auto; overflow-y: hidden; padding: 2px 2px 8px; overscroll-behavior-inline: contain; }
.thumb, .add-thumb, .cover-preview { border-radius: 8px; border: 1px solid var(--line); background: #f8fafc; overflow: hidden; }
.thumb, .add-thumb { position: relative; width: 88px; height: 88px; flex: 0 0 88px; }
.thumb img, .cover-preview img { width: 100%; height: 100%; object-fit: cover; }
.image-thumb small { position: absolute; left: 4px; right: 4px; bottom: 17px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: #fff; font-size: 10px; text-shadow: 0 1px 4px #111; }
.thumb em { position: absolute; left: 4px; right: 4px; bottom: 4px; overflow: hidden; color: rgba(255, 255, 255, 0.9); font-size: 10px; font-style: normal; text-align: center; text-overflow: ellipsis; white-space: nowrap; text-shadow: 0 1px 4px #111; }
.video-thumb { display: grid; place-items: center; padding: 8px; color: #fff; background: linear-gradient(135deg, #17203a, #31517a); }
.video-thumb span { width: 30px; height: 30px; display: grid; place-items: center; border: 1px solid rgba(255, 255, 255, 0.75); border-radius: 50%; }
.video-thumb small { width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; text-align: center; font-size: 11px; }
.delete-media { position: absolute; top: 4px; right: 4px; width: 22px; height: 22px; border: 0; border-radius: 50%; background: rgba(24, 33, 58, 0.75); color: #fff; font-weight: 900; }
.add-thumb { border-style: dashed; color: #48536d; font-size: 28px; }
.cover-card { display: grid; grid-template-columns: minmax(0, 1fr); align-items: start; gap: 10px; }
.cover-preview-wrap { display: grid; grid-template-columns: 150px minmax(0, 1fr); align-items: center; gap: 12px; min-width: 0; }
.cover-preview { width: 150px; height: 88px; }
.cover-preview.empty { display: grid; place-items: center; border-style: dashed; color: #8a94a8; font-size: 12px; font-weight: 800; }
.media-meta { min-width: 0; }
.media-meta strong { overflow: hidden; margin: 0 0 6px; text-overflow: ellipsis; white-space: nowrap; }
.media-meta span, .media-empty { margin: 0; color: #7b8498; font-size: 12px; font-weight: 700; }
.cover-actions { display: flex; gap: 8px; flex-wrap: wrap; }

.ai-panel { display: grid; grid-template-columns: minmax(180px, 1fr) minmax(220px, 1fr) minmax(140px, 0.7fr) auto minmax(190px, 0.9fr); align-items: end; gap: 18px; }
.ai-panel label, .setting-field { display: grid; gap: 8px; }
select { width: 100%; height: 42px; padding: 0 12px; border: 1px solid #dfe5ef; border-radius: 8px; background: #fff; color: var(--ink); outline: 0; }
.segmented { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; padding: 4px; border-radius: 8px; background: #f4f6fa; }
.segmented button { height: 34px; border: 0; border-radius: 7px; background: transparent; color: #6c7488; font-weight: 800; }
.segmented button.active { background: #fff; color: var(--blue); box-shadow: 0 0 0 1px #9ec1ff inset; }
.switch { display: flex !important; align-items: center; grid-template-columns: none !important; gap: 8px !important; height: 42px; color: #596276; font-weight: 800; white-space: nowrap; }
.switch input { position: absolute; opacity: 0; }
.switch span { width: 40px; height: 22px; border-radius: 99px; background: #d5dae5; transition: 0.2s; }
.switch span::after { content: ""; display: block; width: 18px; height: 18px; margin: 2px; border-radius: 50%; background: #fff; transition: 0.2s; }
.switch input:checked + span { background: var(--accent); }
.switch input:checked + span::after { transform: translateX(18px); }
.primary-btn, .primary-outline, .ghost-btn, .danger-btn, .danger-primary-btn { height: 42px; border-radius: 8px; font-weight: 900; }
.primary-btn { border: 0; padding: 0 16px; background: linear-gradient(135deg, #ff4f83, #5e82ff); color: #fff; box-shadow: 0 12px 24px rgba(92, 118, 255, 0.24); }
.primary-btn:disabled, .primary-outline:disabled, .ghost-btn:disabled, .danger-btn:disabled, .danger-primary-btn:disabled { cursor: not-allowed; opacity: 0.58; }
.primary-outline, .ghost-btn { padding: 0 16px; border: 1px solid var(--line); background: #fff; color: #45506a; }
.primary-btn.small, .primary-outline.small, .ghost-btn.small { height: 32px; padding: 0 10px; font-size: 12px; box-shadow: none; }
.danger-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 42px;
  padding: 0 16px;
  border: 1px solid #f3c0c8;
  border-radius: 8px;
  background: #fff;
  color: #c93648;
  font-weight: 900;
  transition: background 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
}
.danger-btn:hover {
  border-color: #ec8d9b;
  background: #fff5f6;
  box-shadow: 0 8px 18px rgba(201, 54, 72, 0.12);
  transform: translateY(-1px);
}
.danger-btn.small { height: 32px; padding: 0 11px; font-size: 12px; }
.danger-primary-btn {
  padding: 0 18px;
  border: 0;
  background: linear-gradient(135deg, #ff5b72, #d9344c);
  color: #fff;
  box-shadow: 0 12px 24px rgba(217, 52, 76, 0.22);
}
.notice { margin: 0; padding: 12px 14px; border: 1px solid #ffd5c7; border-radius: 8px; background: #fff5f0; color: #b94b26; font-weight: 800; }

.platform-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.platform-card { position: relative; display: flex; align-items: center; gap: 12px; min-height: 82px; padding: 14px; border: 1px solid var(--line); border-radius: 8px; background: #fff; text-align: left; }
.platform-card.selected.wechat { border-color: #8adbb5; background: #f2fff8; }
.platform-card.selected.zhihu { border-color: #99c0ff; background: #f5f9ff; }
.platform-card.selected.bilibili { border-color: #ffb5c0; background: #fff6f8; }
.platform-card.selected.xiaohongshu { border-color: #ffb8a8; background: #fff7f2; }
.platform-card img { width: 40px; height: 40px; object-fit: contain; }
.platform-card strong, .platform-card small { display: block; }
.platform-card strong { font-size: 15px; }
.platform-card small { margin-top: 4px; color: #7b8498; font-size: 12px; font-weight: 700; }
.platform-card b { position: absolute; top: 9px; right: 10px; width: 18px; height: 18px; display: grid; place-items: center; border-radius: 50%; background: var(--green); color: #fff; font-size: 12px; }
.more-platforms { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; margin-top: 18px; padding-top: 16px; border-top: 1px solid var(--line); }
.more-platforms p { grid-column: 1 / -1; margin: 0 0 4px; color: #4d5871; font-weight: 900; }
.more-platforms button { display: grid; place-items: center; gap: 6px; height: 58px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; color: #505b74; font-weight: 800; }
.more-platforms span { color: var(--accent); font-size: 19px; }
.overview-panel, .tips-panel { display: grid; gap: 16px; }
.overview-row { display: flex; justify-content: space-between; align-items: center; min-height: 34px; color: #667089; font-size: 14px; }
.overview-row strong { color: var(--ink); }
.tips-panel ul, .help-panel ul { margin: 0; padding-left: 18px; color: #667089; font-size: 14px; line-height: 1.9; }

.ai-default-card { display: flex; justify-content: space-between; align-items: center; gap: 18px; margin-bottom: 18px; padding: 18px; border: 1px solid #dce6ff; border-radius: 12px; background: linear-gradient(135deg, #f7faff, #fff7fb); }
.ai-default-card span { color: #65708a; font-size: 13px; font-weight: 900; }
.ai-default-card h3 { margin: 6px 0; font-size: 22px; }
.ai-default-card p { margin: 0; color: #65708a; font-weight: 700; }
.ai-provider-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.ai-provider-card { display: grid; gap: 14px; padding: 16px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; }
.ai-provider-card.active { border-color: #9ebcff; box-shadow: 0 10px 26px rgba(94, 130, 255, 0.12); }
.ai-provider-top { display: flex; align-items: center; gap: 12px; }
.provider-mark { width: 42px; height: 42px; flex: 0 0 auto; display: grid; place-items: center; border-radius: 10px; background: #eef4ff; color: #4e71df; font-size: 18px; font-weight: 950; }
.provider-mark.green { background: #ebfff5; color: #1c9a5c; }
.provider-mark.purple { background: #f5efff; color: #7a55d9; }
.provider-mark.pink { background: #fff1f5; color: #d43f62; }
.provider-mark.orange { background: #fff5e8; color: #c06a14; }
.provider-mark.gray { background: #eef1f6; color: #596276; }
.ai-provider-top h3 { margin: 0; font-size: 16px; }
.ai-provider-top p { margin: 4px 0 0; color: #738098; font-size: 12px; font-weight: 700; }
.ai-provider-meta { display: grid; gap: 8px; padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: #fff; }
.ai-provider-meta span { display: flex; justify-content: space-between; gap: 10px; color: #596276; font-size: 13px; min-width: 0; }
.ai-provider-meta b { color: #17203a; }
.ai-provider-meta span:not(:last-child) { padding-bottom: 8px; border-bottom: 1px solid #eef2f7; }

.preview-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.preview-card { display: grid; gap: 12px; padding: 16px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; }
.preview-title, .account-title { display: flex; align-items: center; gap: 10px; }
.preview-title img, .account-title img { width: 34px; height: 34px; object-fit: contain; }
.preview-title h3, .account-title h3 { margin: 0; font-size: 15px; }
.preview-title span, .account-title span { display: block; margin-top: 3px; color: #7b8498; font-size: 12px; }
.preview-card input, .preview-card textarea { width: 100%; border: 1px solid #dde3ee; border-radius: 8px; background: #fff; color: var(--ink); outline: 0; }
.preview-card input { height: 40px; padding: 0 12px; font-weight: 800; }
.preview-card textarea { min-height: 120px; resize: vertical; padding: 12px; line-height: 1.7; }
.preview-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.preview-tags span { padding: 4px 8px; border-radius: 99px; background: #eef4ff; color: #4970ca; font-size: 12px; font-weight: 800; }
.empty-state { padding: 18px; border: 1px dashed #d8deea; border-radius: 8px; background: #fbfcff; color: #69738a; font-weight: 700; }
.empty-state a { color: var(--blue); margin-left: 8px; cursor: pointer; }
.record-list, .record-table { display: grid; gap: 10px; }
.record-head, .record-row.table { display: grid; grid-template-columns: 180px 1fr 140px 80px 100px; gap: 12px; align-items: center; }
.record-head { padding: 0 14px; color: #7b8498; font-size: 13px; font-weight: 900; }
.record-row { display: grid; grid-template-columns: 1fr 120px 70px 180px; gap: 12px; align-items: center; padding: 14px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; cursor: pointer; }
.record-row.table { grid-template-columns: 180px 1fr 140px 80px 100px; }
.record-row span, .record-row small { color: #6e788e; }
.record-row b { color: var(--green); }
.record-actions { display: flex; align-items: center; justify-content: flex-end; gap: 8px; }

.account-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.account-card { display: grid; gap: 14px; padding: 16px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; }
.account-card dl { display: grid; grid-template-columns: 88px 1fr; gap: 8px 12px; margin: 0; font-size: 14px; }
.account-card dt { color: #7b8498; }
.account-card dd { margin: 0; font-weight: 800; }
.filter-tabs { display: flex; gap: 8px; margin: 18px 0; }
.filter-tabs button { height: 34px; padding: 0 14px; border: 1px solid var(--line); border-radius: 999px; background: #fff; color: #5d6680; font-weight: 800; }
.filter-tabs button.active { border-color: var(--accent); background: var(--accent-soft); color: var(--accent); }
.library-toolbar { display: flex; justify-content: space-between; align-items: center; gap: 14px; margin: 18px 0; }
.library-toolbar .filter-tabs { margin: 0; flex-wrap: wrap; }
.library-toolbar > span { color: #6e788e; font-size: 13px; font-weight: 800; white-space: nowrap; }
.material-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(270px, 1fr)); gap: 14px; }
.material-card { min-width: 0; display: grid; gap: 12px; padding: 14px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; }
.material-preview { aspect-ratio: 16 / 9; display: grid; place-items: center; overflow: hidden; border-radius: 8px; background: #edf2f8; color: #50607a; font-weight: 900; }
.material-preview.video { background: linear-gradient(135deg, #17203a, #31517a); color: #fff; }
.material-preview.cover { background: #fff7fb; }
.material-preview img { width: 100%; height: 100%; object-fit: cover; }
.material-info { min-width: 0; }
.material-info > strong { display: block; overflow: hidden; margin-bottom: 10px; color: var(--ink); text-overflow: ellipsis; white-space: nowrap; }
.material-info dl { display: grid; grid-template-columns: 72px minmax(0, 1fr); gap: 7px 10px; margin: 0; font-size: 13px; }
.material-info dt { color: #7b8498; font-weight: 800; }
.material-info dd { min-width: 0; margin: 0; overflow: hidden; color: #3f4a63; font-weight: 800; text-overflow: ellipsis; white-space: nowrap; }
.settings-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }

.dialog-mask, .drawer-mask { position: fixed; inset: 0; z-index: 30; display: grid; place-items: center; padding: 24px; background: rgba(18, 27, 47, 0.42); }
.upgrade-dialog { position: relative; width: min(460px, 100%); display: grid; gap: 14px; padding: 26px; border-radius: 12px; background: #fff; box-shadow: 0 24px 80px rgba(0, 0, 0, 0.18); }
.upgrade-dialog h2, .upgrade-dialog p { margin: 0; }
.upgrade-dialog p { color: var(--muted); }
.dialog-close { position: absolute; top: 10px; right: 10px; width: 34px; height: 34px; border: 0; border-radius: 50%; background: #f2f4f8; color: #566176; font-size: 22px; }
.delete-dialog { position: relative; width: min(440px, 100%); display: grid; gap: 16px; padding: 26px; border: 1px solid #f1d8dc; border-radius: 12px; background: #fff; box-shadow: 0 24px 80px rgba(0, 0, 0, 0.18); }
.delete-dialog-icon { width: 44px; height: 44px; display: grid; place-items: center; border-radius: 50%; background: #fff1f3; color: #c93648; font-size: 24px; font-weight: 900; }
.delete-dialog h2 { margin: 0; font-size: 20px; }
.delete-dialog p { margin: 6px 0 0; color: #667089; line-height: 1.7; }
.delete-record-preview { display: grid; grid-template-columns: 72px minmax(0, 1fr); gap: 8px 12px; padding: 14px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; }
.delete-record-preview span { color: #7b8498; font-size: 13px; font-weight: 800; }
.delete-record-preview strong { min-width: 0; overflow: hidden; color: var(--ink); font-size: 13px; text-overflow: ellipsis; white-space: nowrap; }
.delete-dialog-actions { display: flex; justify-content: flex-end; gap: 10px; }
.delete-dialog-actions .ghost-btn, .delete-dialog-actions .danger-primary-btn { min-width: 96px; }
.ai-config-dialog { position: relative; width: min(620px, 100%); display: grid; gap: 18px; padding: 28px; border: 1px solid var(--line); border-radius: 12px; background: #fff; box-shadow: 0 24px 80px rgba(0, 0, 0, 0.18); }
.ai-config-title { display: flex; align-items: center; gap: 14px; padding-right: 34px; }
.ai-config-title h2 { margin: 0; font-size: 21px; }
.ai-config-title p { margin: 5px 0 0; color: #65708a; font-weight: 700; }
.ai-config-form { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.ai-config-form label { display: grid; gap: 8px; color: #17203a; font-size: 14px; font-weight: 800; }
.ai-config-form label:nth-child(1), .ai-config-form label:nth-child(2), .ai-config-form label:nth-child(3), .set-default-switch { grid-column: 1 / -1; }
.set-default-switch { justify-content: start; }
.ai-config-actions { display: flex; justify-content: flex-end; gap: 10px; }
.pay-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.pay-grid div { display: grid; place-items: center; gap: 8px; min-height: 130px; border: 1px dashed #cfd6e4; border-radius: 8px; background: #fbfcff; color: #53607a; font-weight: 800; }
.pay-grid b { width: 74px; height: 74px; display: grid; place-items: center; background: repeating-linear-gradient(45deg, #111 0 6px, #fff 6px 12px); color: var(--accent); border: 8px solid #fff; box-shadow: 0 0 0 1px #dfe5ef; }
.record-drawer { position: relative; width: min(980px, 100%); max-height: 88vh; overflow: auto; display: grid; gap: 16px; padding: 28px; border-radius: 12px; background: #fff; box-shadow: 0 24px 80px rgba(0, 0, 0, 0.18); }
.record-drawer h2 { margin: 0; }
.detail-meta { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; color: #65708a; font-weight: 800; font-size: 13px; }
.source-text { margin: 0; padding: 14px; border-radius: 8px; background: #f7f9fc; color: #4e5a74; line-height: 1.7; white-space: pre-wrap; }
.detail-platforms { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.detail-card { display: grid; gap: 10px; padding: 16px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; }
.detail-card h3, .detail-card p { margin: 0; }
.detail-card p { color: #4e5a74; line-height: 1.7; white-space: pre-wrap; }

@media (max-width: 1320px) {
  .workspace { grid-template-columns: 1fr; }
  .side-column { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .platform-panel { grid-column: 1 / -1; }
  .ai-panel, .settings-grid, .ai-provider-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 900px) {
  :root { --sidebar: 0px; --topbar: 64px; }
  .sidebar { display: none; }
  .topbar { left: 0; padding: 0 14px; }
  .stepper { overflow-x: auto; gap: 12px; }
  .top-actions { display: none; }
  .workspace { padding: 14px; }
  .media-grid, .side-column, .preview-grid, .platform-grid, .metric-grid, .material-stats, .account-grid, .settings-grid, .ai-provider-grid, .ai-config-form, .detail-platforms, .detail-meta { grid-template-columns: 1fr; }
  .cover-preview-wrap { grid-template-columns: 1fr; }
  .cover-preview { width: 100%; max-width: 260px; }
  .ai-default-card { align-items: stretch; flex-direction: column; }
  .ai-panel { grid-template-columns: 1fr; }
  .record-row, .record-row.table, .record-head { grid-template-columns: 1fr; }
  .dashboard-hero { display: grid; }
}
</style>
