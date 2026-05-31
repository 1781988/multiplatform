<template>
  <section v-if="isAuthPage" class="auth-page">
    <div class="auth-card">
      <img src="/figures/聚发舟.png" alt="聚舟" />
      <h1>{{ route.path === "/login" ? "登录聚舟" : "注册聚舟" }}</h1>
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
        <img class="brand-logo" src="/figures/聚发舟.png" alt="聚舟" />
        <div>
          <strong>聚舟</strong>
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
        <div class="top-popover-wrap">
          <button class="icon-btn theme-trigger" type="button" title="主题" @click="toggleThemeMenu">
            <span>☼</span>
          </button>
          <div v-if="themeMenuVisible" class="top-popover theme-popover">
            <button
              v-for="item in themeOptions"
              :key="item.value"
              type="button"
              :class="{ active: themeMode === item.value }"
              @click="setThemeMode(item.value)"
            >
              <span>{{ item.icon }}</span>
              <strong>{{ item.label }}</strong>
            </button>
          </div>
        </div>
        <div class="top-popover-wrap">
          <button class="icon-btn bell" type="button" title="通知" aria-label="通知" @click="toggleNotificationPanel">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9" />
              <path d="M13.7 21a2 2 0 0 1-3.4 0" />
            </svg>
            <i v-if="unreadNotifications">{{ unreadNotifications }}</i>
          </button>
          <div v-if="notificationPanelVisible" class="top-popover notification-popover">
            <div class="notification-head">
              <strong>通知中心</strong>
              <button v-if="notifications.length" type="button" @click="markAllNotificationsRead">全部已读</button>
            </div>
            <div v-if="!notifications.length" class="notification-empty">暂无新通知</div>
            <button
              v-for="item in notifications"
              :key="item.id"
              class="notification-item"
              :class="[item.type, { unread: !item.read }]"
              type="button"
              @click="markNotificationRead(item.id)"
            >
              <b>{{ item.type === "failed" ? "!" : "✓" }}</b>
              <span>{{ item.title }}</span>
              <p>{{ item.message }}</p>
              <small>{{ item.time }}</small>
            </button>
          </div>
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

    <div v-if="sampleDialogVisible" class="dialog-mask" @click.self="sampleDialogVisible = false">
      <section class="sample-dialog">
        <button class="dialog-close" type="button" @click="sampleDialogVisible = false">×</button>
        <div class="sample-dialog-head">
          <h2>选择样例内容</h2>
          <p>选择一组样例后，将填充标题、正文和标签。</p>
        </div>
        <div class="sample-grid">
          <button
            v-for="sample in contentSamples"
            :key="sample.id"
            class="sample-card"
            type="button"
            @click="selectSample(sample)"
          >
            <strong>{{ sample.title }}</strong>
            <span>{{ sample.summary }}</span>
            <small>{{ sample.tags.join(" / ") }}</small>
          </button>
        </div>
      </section>
    </div>

    <div v-if="recordDetailVisible" class="drawer-mask" @click.self="recordDetailVisible = false">
      <section class="record-drawer">
        <button class="dialog-close" type="button" @click="recordDetailVisible = false">×</button>
        <h2>发布详情</h2>
        <div class="detail-meta">
          <span><b>任务标题</b>{{ selectedRecord?.task_title || "-" }}</span>
          <span><b>发布平台</b>{{ detailPlatformNames(selectedRecord).join("、") || "-" }}</span>
          <span><b>发布时间</b>{{ formatPublishTime(selectedRecord?.publish_time) }}</span>
          <span><b>状态</b>{{ detailStatusLabel(selectedRecord?.status) }}</span>
          <span><b>模拟发布ID</b>{{ selectedRecord?.mock_publish_id || "-" }}</span>
        </div>
        <section class="detail-section">
          <h3>帖子标题</h3>
          <strong class="detail-post-title">{{ detailPrimaryContent(selectedRecord)?.title || selectedRecord?.task_title || "-" }}</strong>
        </section>
        <section class="detail-section">
          <h3>正文</h3>
          <p class="source-text">{{ detailPrimaryContent(selectedRecord)?.content || detailPrimaryContent(selectedRecord)?.description || selectedRecord?.source_content || "-" }}</p>
        </section>
        <section class="detail-section">
          <h3>标签</h3>
          <div class="preview-tags detail-tags">
            <span v-for="tag in detailTags(selectedRecord)" :key="tag">#{{ tag }}</span>
            <small v-if="!detailTags(selectedRecord).length">暂无标签</small>
          </div>
        </section>
        <section class="detail-section">
          <h3>素材列表</h3>
          <div v-if="detailMaterials(selectedRecord).length" class="detail-materials">
            <a v-for="item in detailMaterials(selectedRecord)" :key="item.key" :href="item.url" target="_blank" rel="noreferrer">
              <span>{{ item.type }}</span>
              <strong>{{ item.name }}</strong>
            </a>
          </div>
          <div v-else class="detail-empty">暂无素材</div>
        </section>
      </section>
    </div>

    <div v-if="deleteConfirmVisible" class="dialog-mask" @click.self="closeDeleteConfirm">
      <section class="confirm-dialog">
        <button class="dialog-close" type="button" @click="closeDeleteConfirm">×</button>
        <div class="confirm-icon">!</div>
        <h2>删除发布记录</h2>
        <p>确认删除这条发布记录吗？当前是模拟发布，只会删除本地系统记录，不涉及真实平台帖子。</p>
        <strong>{{ pendingDeleteRecord?.title || pendingDeleteRecord?.task_title || "未命名发布记录" }}</strong>
        <div class="confirm-actions">
          <button class="ghost-btn" type="button" @click="closeDeleteConfirm">取消</button>
          <button class="danger-confirm-btn" type="button" @click="confirmDeletePublishRecord">确认删除</button>
        </div>
      </section>
    </div>

    <div v-if="aiConfigVisible" class="dialog-mask" @click.self="closeAiConfig">
      <section class="ai-config-dialog">
        <button class="dialog-close" type="button" @click="closeAiConfig">×</button>
        <div class="sample-dialog-head">
          <h2>{{ currentProvider?.label || "模型配置" }}</h2>
          <p>配置会保存到后端数据库，内容创作页会读取当前默认模型生成多平台内容。</p>
        </div>
        <div class="settings-grid">
          <label v-if="currentProvider?.needsKey" class="setting-field">
            <span>API Key</span>
            <input v-model="aiSettings[providerField(configProvider, 'key')]" type="password" placeholder="请输入 API Key" />
          </label>
          <label v-if="currentProvider?.hasBaseUrl" class="setting-field">
            <span>Base URL</span>
            <input v-model="aiSettings[providerField(configProvider, 'baseUrl')]" placeholder="请输入 Base URL" />
          </label>
          <label class="setting-field">
            <span>模型名</span>
            <input v-model="aiSettings[providerField(configProvider, 'model')]" placeholder="请输入模型名" />
          </label>
          <label class="setting-field">
            <span>创作随机度</span>
            <input v-model.number="aiSettings[providerField(configProvider, 'temperature')]" type="number" min="0" max="2" step="0.1" />
            <small>越低越稳定，越高越有创意，推荐 0.7。</small>
          </label>
          <label class="setting-field">
            <span>最大输出长度</span>
            <input v-model.number="aiSettings[providerField(configProvider, 'maxTokens')]" type="number" min="1" step="1" />
            <small>控制单次生成内容长度，推荐 2000。</small>
          </label>
        </div>
        <div class="settings-actions">
          <button class="ghost-btn" type="button" @click="setDefaultProvider(configProvider)">设为默认模型</button>
          <button class="ghost-btn" type="button" :disabled="loading.settings" @click="testModelConnection(configProvider)">
            {{ loading.settings ? "测试中..." : "测试连接" }}
          </button>
          <button class="primary-btn" type="button" :disabled="loading.settings" @click="saveAiSettings">
            保存配置
          </button>
        </div>
      </section>
    </div>

    <div v-if="authDialogVisible" class="dialog-mask" @click.self="closeOfficialAuth">
      <section class="official-auth-dialog">
        <button class="dialog-close" type="button" @click="closeOfficialAuth">×</button>
        <div class="sample-dialog-head">
          <h2>{{ platformName(authPlatformId) }} 官方授权</h2>
          <p>当前为授权流程预留入口，可扫码或输入账号密码模拟登录真实平台账号。</p>
        </div>
        <div class="auth-dialog-body">
          <div class="mock-qr">
            <span></span>
            <strong>模拟二维码</strong>
            <small>请使用对应平台 App 扫码</small>
          </div>
          <div class="auth-form">
            <label>
              账号
              <input v-model="platformLoginForm.account" placeholder="请输入平台账号" />
            </label>
            <label>
              密码
              <input v-model="platformLoginForm.password" type="password" placeholder="请输入平台密码" />
            </label>
            <button class="primary-btn" type="button" @click="submitOfficialAuth">模拟登录真实账号</button>
          </div>
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
const deleteConfirmVisible = ref(false);
const pendingDeleteRecord = ref(null);
const themeMode = ref(localStorage.getItem("themeMode") || "system");
const themeMenuVisible = ref(false);
const notificationPanelVisible = ref(false);
const notifications = ref(JSON.parse(localStorage.getItem("notifications") || "[]"));
const aiConfigVisible = ref(false);
const configProvider = ref("openai");
const authDialogVisible = ref(false);
const authPlatformId = ref("wechat");
const platformLoginForm = reactive({ account: "", password: "" });

const authForm = reactive({ name: "", account: "", password: "", confirm: "" });
const authError = ref("");
const username = ref(localStorage.getItem("username") || "");
const isPro = ref(localStorage.getItem("isPro") === "true");
const vipStart = ref(localStorage.getItem("vipStart") || "");
const vipEnd = ref(localStorage.getItem("vipEnd") || "");
const upgradeDialogVisible = ref(false);
const sampleDialogVisible = ref(false);
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
const materials = ref([]);
const history = ref([]);
const coverPlaceholder = "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80";

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
  localKey: "local",
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
  wechat: { loggedIn: false, accountName: "", authType: "未授权", expireAt: "-" },
  zhihu: { loggedIn: false, accountName: "", authType: "未授权", expireAt: "-" },
  bilibili: { loggedIn: false, accountName: "", authType: "未授权", expireAt: "-" },
  xiaohongshu: { loggedIn: false, accountName: "", authType: "未授权", expireAt: "-" }
});

const form = reactive({
  title: "",
  content: "",
  tagsText: "",
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
  { value: "openai", label: "OpenAI", description: "OpenAI 官方与兼容接口", hasBaseUrl: true, needsKey: true },
  { value: "qwen", label: "Qwen", description: "阿里云百炼 OpenAI Compatible", hasBaseUrl: true, needsKey: true },
  { value: "gemini", label: "Gemini", description: "Google Gemini 模型", hasBaseUrl: false, needsKey: true },
  { value: "deepseek", label: "DeepSeek", description: "DeepSeek OpenAI Compatible", hasBaseUrl: true, needsKey: true },
  { value: "ollama", label: "Ollama", description: "本地 Ollama 服务", hasBaseUrl: true, needsKey: false },
  { value: "local", label: "Local", description: "本地 OpenAI Compatible 服务", hasBaseUrl: true, needsKey: false }
];

const themeOptions = [
  { value: "light", label: "亮色模式", icon: "☼" },
  { value: "dark", label: "深色模式", icon: "●" },
  { value: "system", label: "跟随系统", icon: "◐" }
];

const rewriteModes = [
  { value: "conservative", label: "保守" },
  { value: "balanced", label: "平衡" },
  { value: "creative", label: "创意" }
];

const contentSamples = [
  {
    id: "ai-learning",
    title: "AI学习效率",
    summary: "适合生成公众号、知乎和小红书学习方法类内容。",
    content:
      "随着AI工具的快速发展，大学生和职场新人可以利用AI辅助完成资料整理、论文阅读、知识总结、代码调试和复习规划等任务。合理使用AI工具不仅可以节省时间，还可以帮助使用者建立更加清晰的知识结构。\n\n本文将从学习计划制定、课堂笔记整理、论文阅读辅助、代码学习和考试复习五个方面，介绍AI工具在学习效率提升中的实际应用方法，并强调在使用过程中保持独立思考和信息核验的重要性。",
    tags: ["AI学习", "效率提升", "学习方法", "人工智能"]
  },
  {
    id: "ai-office-video",
    title: "AI办公视频",
    summary: "适合生成B站、短视频简介和办公效率教程内容。",
    content:
      "AI办公工具正在改变日常工作方式。从会议纪要、邮件草稿、表格分析到PPT大纲生成，AI可以帮助团队减少重复劳动，把更多时间投入到判断、沟通和创造性任务中。\n\n本期视频将用三个真实办公场景演示AI工具的使用流程：快速整理会议重点、把零散需求转成项目计划、根据数据生成汇报提纲。视频也会提醒大家注意隐私保护、数据脱敏和结果复核。",
    tags: ["AI办公", "效率工具", "职场技能", "视频教程"]
  },
  {
    id: "smart-product-review",
    title: "智能产品测评",
    summary: "适合生成产品测评、种草笔记和平台对比内容。",
    content:
      "这款智能产品主打便携、自动化和多设备联动，适合对效率、体验和智能场景有要求的用户。实际体验中，它的优势主要体现在上手简单、响应速度快、日常任务自动化程度高。\n\n测评将从外观设计、核心功能、连接稳定性、续航表现、使用门槛和适用人群六个维度展开，同时也会说明它的不足，例如高阶功能需要学习成本、部分场景依赖网络环境。最终给出适合购买的人群建议。",
    tags: ["智能产品", "产品测评", "数码好物", "使用体验"]
  }
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
const unreadNotifications = computed(() => notifications.value.filter((item) => !item.read).length);
const defaultProvider = computed(() => providers.find((provider) => provider.value === aiSettings.provider) || providers[0]);
const currentProvider = computed(() => providers.find((provider) => provider.value === configProvider.value) || providers[0]);
const filteredMaterials = computed(() => (materialFilter.value === "all" ? materials.value : materials.value.filter((item) => item.type === materialFilter.value)));
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
    h("div", { class: "dashboard-copy" }, [
      h("span", "MultiPost AI"),
      h("h2", "工作台"),
      h("p", "集中查看发布、素材、模型和平台账号状态，快速进入下一步创作。")
    ]),
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
  h("article", { class: "panel dashboard-records" }, [
    h("div", { class: "panel-head compact" }, [h("div", [h("h2", "最近发布记录"), h("p", "点击记录可查看完整帖子内容。")])]),
    history.value.length
      ? h("div", { class: "record-list" }, history.value.slice(0, 5).map((record) => recordRow(record)))
      : h("div", { class: "dashboard-empty" }, [
          h("strong", "暂无发布记录"),
          h("p", "完成一次模拟发布后，这里会展示最新发布动态。"),
          h("button", { class: "primary-outline", onClick: () => router.push("/content") }, "去内容创作")
        ])
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
      ? h("div", { class: "record-table-wrap" }, [
          h("table", { class: "record-table" }, [
            h("thead", [
              h("tr", [
                h("th", "发布时间"),
                h("th", "任务标题"),
                h("th", "发布平台"),
                h("th", "状态"),
                h("th", "操作")
              ])
            ]),
            h("tbody", history.value.map((record) => recordRow(record, true)))
          ])
        ])
      : h("div", { class: "records-empty" }, [
          h("strong", "暂无发布记录"),
          h("p", "完成一次模拟发布后，发布记录会显示在这里。"),
          h("button", { class: "primary-outline", type: "button", onClick: () => router.push("/content") }, "去内容创作")
        ])
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
          h("button", { class: "ghost-btn small", onClick: () => openOfficialAuth(platform.id) }, "官方授权预留")
        ])
      ]);
    }))
  ])
]);

const MaterialsView = page(() => [
  h("article", { class: "panel" }, [
    h("div", { class: "panel-head" }, [
      h("div", [h("h2", "全局素材库"), h("p", "管理历史上传素材，可筛选、删除、复制链接或加入当前创作。")]),
      h("button", { class: "ghost-btn", onClick: loadMaterials }, "刷新素材")
    ]),
    h("div", { class: "material-stats" }, [
      metric("图片", `${materialStats.value.image} 张`, "jpg/png/webp"),
      metric("视频", `${materialStats.value.video} 个`, "mp4/mov/avi/mkv"),
      metric("封面", `${materialStats.value.cover} 张`, "推荐 16:9 或 3:4"),
      metric("总占用", materialStats.value.size, "本地/后端素材")
    ]),
    h("div", { class: "filter-tabs" }, ["all", "image", "video", "cover"].map((type) =>
      h("button", { class: { active: materialFilter.value === type }, onClick: () => (materialFilter.value = type) }, materialFilterLabel(type))
    )),
    filteredMaterials.value.length
      ? h("div", { class: "material-grid" }, filteredMaterials.value.map((item) => materialCard(item)))
      : h("div", { class: "empty-state" }, "暂无素材，请在内容创作页上传图片、视频或封面。")
  ])
]);

const SettingsView = page(() => [
  h("article", { class: "panel settings-panel" }, [
    h("div", { class: "panel-head" }, [h("div", [h("h2", "AI 设置中心"), h("p", "管理多模型配置，内容创作页会优先读取当前默认模型。")])]),
    h("section", { class: "default-model-card" }, [
      h("span", "当前默认模型"),
      h("strong", `${defaultProvider.value.label} / ${aiSettings[providerField(defaultProvider.value.value, "model")] || "-"}`),
      h("small", providerConnectionText(defaultProvider.value.value))
    ]),
    h("div", { class: "ai-provider-grid" }, providers.map((provider) => providerCard(provider))),
    h("section", { class: "settings-preferences" }, [
      h("div", [
        h("h3", "全局偏好"),
        h("p", "用于内容创作页的一键生成默认参数。")
      ]),
      h("div", { class: "settings-preference-fields" }, [
        settingSelect("默认语言", "defaultLang", [{ value: "zh", label: "中文" }, { value: "en", label: "English" }]),
        settingSelect("默认改写强度", "defaultIntensity", rewriteModes),
        h("button", { class: "primary-btn", onClick: saveAiSettings }, "保存全局设置")
      ])
    ]),
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
  return h("div", { class: "metric-card" }, [h("i", metricIcon(label)), h("span", label), h("strong", value), h("small", hint)]);
}

function metricIcon(label) {
  if (label.includes("发布")) return "↗";
  if (label.includes("素材")) return "▧";
  if (label.includes("AI")) return "✦";
  if (label.includes("账号")) return "♙";
  return "•";
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
  return h("div", { class: "media-grid" }, [
    uploadCard("图片", `${form.images.length}/9`, "支持 jpg/png/webp，单张不超过 10MB，最多 9 张。推荐：公众号 900x500，知乎 1200x675，小红书 1080x1440。", form.images, "images", () => imageInput.value?.click()),
    uploadCard("视频", `${form.videos.length}/3`, "支持 mp4/mov/avi/mkv，单个不超过 500MB，最多 3 个。推荐：B站 1920x1080，小红书 1080x1920。", form.videos, "videos", () => videoInput.value?.click()),
    h("div", { class: "media-card cover-card" }, [
      h("strong", "封面图"),
      h("p", { class: "media-hint" }, "支持 jpg/png/webp，不超过 10MB。推荐：B站 1920x1080，公众号 900x383，小红书 1080x1440。"),
      h("div", { class: "cover-preview" }, h("img", { src: form.cover?.url || coverPlaceholder, alt: "封面图" })),
      h("button", { class: "ghost-btn small", onClick: () => coverInput.value?.click() }, "更换封面")
    ])
  ]);
}

function uploadCard(title, count, hint, list, type, onAdd) {
  return h("div", { class: "media-card" }, [
    h("strong", [title, h("span", ` (${count})`)]),
    h("p", { class: "media-hint" }, hint),
    h("div", { class: "media-list" }, [
      ...list.map((item, index) =>
        h("div", { class: ["thumb", type === "videos" ? "video-thumb" : "image-thumb"] }, [
          type === "videos" ? h("span", "▷") : h("img", { src: item.url, alt: item.name }),
          h("small", item.name),
          h("button", { class: "delete-media", onClick: () => removeMedia(type, index) }, "×")
        ])
      ),
      list.length < (type === "videos" ? 3 : 9) ? h("button", { class: "add-thumb", onClick: onAdd }, "+") : null
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
    return h("tr", { class: "record-tr", onClick: open }, [
      h("td", { class: "record-time" }, formatPublishTime(record.publish_time)),
      h("td", [h("strong", { class: "record-title", title: record.title || form.title }, record.title || form.title || "-")]),
      h("td", [h("span", { class: "platform-tag" }, platformName(record.platform || record.id))]),
      h("td", [h("span", { class: "record-status" }, publishStatusTags(record))]),
      h("td", [
        h("span", { class: "record-action" }, [
          h("button", { class: "table-action-btn", onClick: (event) => { event.stopPropagation(); open(); } }, "详情"),
          h("button", { class: "table-action-btn danger", onClick: (event) => { event.stopPropagation(); openDeleteConfirm(record); } }, "删除")
        ])
      ])
    ]);
  }
  return h("div", { class: "record-row", onClick: open }, [
    h("strong", record.title || form.title),
    h("span", platformName(record.platform || record.id)),
    h("span", { class: "record-status" }, publishStatusTags(record)),
    h("small", formatPublishTime(record.publish_time))
  ]);
}

function materialCard(item) {
  return h("section", { class: "material-card" }, [
    h("div", { class: "material-preview" }, item.type === "video" ? h("span", "视频") : h("img", { src: item.url, alt: item.name })),
    h("strong", item.name),
    h("span", `${materialFilterLabel(item.type)} · ${formatSize(item.size)}`),
    h("small", `上传时间：${item.created_at || "本地预览"} · 使用 ${item.usage_count || 0} 次`),
    h("div", { class: "card-actions" }, [
      h("button", { class: "ghost-btn small", onClick: () => copyText(item.url) }, "复制链接"),
      h("button", { class: "ghost-btn small", onClick: () => addMaterialToCurrentTask(item) }, "加入创作"),
      h("button", { class: "ghost-btn small", onClick: () => removeMaterial(item) }, "删除")
    ])
  ]);
}

function providerField(provider, field) {
  return `${provider}${field[0].toUpperCase()}${field.slice(1)}`;
}

function providerConnectionText(provider) {
  const model = aiSettings[providerField(provider, "model")] || "未配置模型";
  const baseUrl = aiSettings[providerField(provider, "baseUrl")];
  const key = aiSettings[providerField(provider, "key")];
  if (["ollama", "local"].includes(provider)) return baseUrl ? `本地服务：${baseUrl}` : model;
  return key ? "API Key 已填写" : "API Key 未填写";
}

function accountStorageKey() {
  return `platformAccounts:${username.value || "guest"}`;
}

function saveLocalAccounts() {
  localStorage.setItem(accountStorageKey(), JSON.stringify(accounts));
}

function resetAccounts() {
  Object.values(accounts).forEach((account) => {
    account.loggedIn = false;
    account.accountName = "";
    account.authType = "未授权";
    account.expireAt = "-";
  });
}

function loadLocalAccounts() {
  resetAccounts();
  const saved = localStorage.getItem(accountStorageKey());
  if (!saved) return;
  try {
    const data = JSON.parse(saved);
    Object.entries(data).forEach(([platform, account]) => {
      if (!accounts[platform]) return;
      Object.assign(accounts[platform], account);
    });
  } catch (error) {
    resetAccounts();
  }
}

function openAiConfig(provider) {
  configProvider.value = provider;
  aiConfigVisible.value = true;
}

function closeAiConfig() {
  aiConfigVisible.value = false;
}

function setDefaultProvider(provider) {
  aiSettings.provider = provider;
  form.llmProvider = provider;
  notice.value = `已设为默认模型：${providerLabel(provider)}`;
}

function providerCard(provider) {
  const isDefault = aiSettings.provider === provider.value;
  return h("section", { class: ["ai-provider-card", { active: isDefault }] }, [
    h("div", { class: "ai-provider-head" }, [
      h("div", [
        h("h3", provider.label),
        h("p", provider.description)
      ]),
      isDefault ? h("span", "默认") : null
    ]),
    h("dl", [
      h("dt", "模型"),
      h("dd", aiSettings[providerField(provider.value, "model")] || "-"),
      h("dt", "Base URL"),
      h("dd", provider.hasBaseUrl ? aiSettings[providerField(provider.value, "baseUrl")] || "-" : "官方 SDK"),
      h("dt", "参数"),
      h("dd", `随机度 ${aiSettings[providerField(provider.value, "temperature")] ?? 0.7} / 输出 ${aiSettings[providerField(provider.value, "maxTokens")] || 2000}`)
    ]),
    h("div", { class: "card-actions" }, [
      h("button", { class: "ghost-btn small", onClick: () => openAiConfig(provider.value) }, "配置"),
      h("button", { class: "ghost-btn small", onClick: () => setDefaultProvider(provider.value) }, "设为默认"),
      h("button", { class: "ghost-btn small", disabled: loading.settings, onClick: () => testModelConnection(provider.value) }, "测试连接")
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
  history.value = [];
  materials.value = [];
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

function effectiveTheme(mode = themeMode.value) {
  if (mode === "system") {
    return window.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  return mode;
}

function applyTheme() {
  document.documentElement.dataset.theme = effectiveTheme();
}

function toggleThemeMenu() {
  themeMenuVisible.value = !themeMenuVisible.value;
  notificationPanelVisible.value = false;
}

function setThemeMode(mode) {
  themeMode.value = mode;
  localStorage.setItem("themeMode", mode);
  applyTheme();
  themeMenuVisible.value = false;
}

function toggleNotificationPanel() {
  notificationPanelVisible.value = !notificationPanelVisible.value;
  themeMenuVisible.value = false;
}

function saveNotifications() {
  localStorage.setItem("notifications", JSON.stringify(notifications.value.slice(0, 30)));
}

function addNotification(type, title, message) {
  notifications.value = [
    {
      id: Date.now() + Math.random(),
      type,
      title,
      message,
      time: formatPublishTime(new Date()),
      read: false
    },
    ...notifications.value
  ].slice(0, 30);
  saveNotifications();
}

function markNotificationRead(id) {
  const item = notifications.value.find((notification) => notification.id === id);
  if (item) item.read = true;
  saveNotifications();
}

function markAllNotificationsRead() {
  notifications.value.forEach((item) => {
    item.read = true;
  });
  saveNotifications();
}

function applySample() {
  sampleDialogVisible.value = true;
}

function selectSample(sample) {
  form.title = sample.title;
  form.content = sample.content;
  form.tagsText = sample.tags.join(",");
  sampleDialogVisible.value = false;
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

function detailPrimaryContent(record) {
  const contents = record?.platform_contents || [];
  if (!contents.length) return null;
  return contents.find((item) => item.platform === record?.platform) || contents[0];
}

function detailPlatformNames(record) {
  const ids = record?.platform
    ? [record.platform]
    : record?.platforms || (record?.platform_contents || []).map((item) => item.platform);
  return [...new Set((ids || []).filter(Boolean))].map(platformName);
}

function detailStatusLabel(status) {
  return status === "failed" ? "失败" : "成功";
}

function detailTags(record) {
  return normalizeTags(detailPrimaryContent(record)?.tags || []);
}

function materialFileName(url) {
  if (!url) return "-";
  return String(url).split("/").filter(Boolean).pop() || String(url);
}

function detailMaterials(record) {
  const content = detailPrimaryContent(record) || {};
  const items = [];
  (content.images || []).forEach((url, index) => {
    items.push({ key: `image-${index}-${url}`, type: "图片", name: materialFileName(url), url });
  });
  (content.videos || []).forEach((url, index) => {
    items.push({ key: `video-${index}-${url}`, type: "视频", name: materialFileName(url), url });
  });
  if (content.cover) {
    items.push({ key: `cover-${content.cover}`, type: "封面", name: materialFileName(content.cover), url: content.cover });
  }
  return items;
}

function providerLabel(id) {
  return providers.find((provider) => provider.value === id)?.label || id;
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

function formatPublishTime(value) {
  const time = parsePublishTime(value);
  if (!time) return "-";
  const date = new Date(time);
  const pad = (number) => String(number).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

function publishStatusTags(record) {
  const status = record.status === "failed" ? "failed" : "success";
  return [
    h("span", { class: ["status-tag", status] }, status === "failed" ? "失败" : "成功"),
    h("span", { class: ["status-tag", "mock"] }, "模拟发布")
  ];
}

function formatSize(size = 0) {
  if (size >= 1024 * 1024) return `${(size / 1024 / 1024).toFixed(1)}MB`;
  if (size >= 1024) return `${(size / 1024).toFixed(1)}KB`;
  return `${size || 0}B`;
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
  }
}

async function handleImageUpload(event) {
  const files = Array.from(event.target.files || []);
  for (const file of files) {
    if (form.images.length >= 9) {
      notice.value = "最多只能上传 9 张图片。";
      break;
    }
    if (!["image/png", "image/jpeg", "image/jpg", "image/webp"].includes(file.type)) {
      notice.value = "只能上传 jpg/png/jpeg/webp 图片。";
      continue;
    }
    if (file.size > 10 * 1024 * 1024) {
      notice.value = "单张图片不能超过 10MB。";
      continue;
    }
    form.images.push(await addLocalFile(file, "image"));
  }
  event.target.value = "";
}

async function handleVideoUpload(event) {
  const files = Array.from(event.target.files || []);
  for (const file of files) {
    if (form.videos.length >= 3) {
      notice.value = "最多只能上传 3 个视频。";
      break;
    }
    if (!file.type.startsWith("video/")) {
      notice.value = "只能上传视频文件。";
      continue;
    }
    if (file.size > 500 * 1024 * 1024) {
      notice.value = "单个视频不能超过 500MB。";
      continue;
    }
    form.videos.push(await addLocalFile(file, "video"));
  }
  event.target.value = "";
}

async function handleCoverUpload(event) {
  const file = event.target.files?.[0];
  if (!file) return;
  if (!["image/png", "image/jpeg", "image/jpg", "image/webp"].includes(file.type)) {
    notice.value = "封面必须是 jpg/png/jpeg/webp 图片。";
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    notice.value = "封面不能超过 10MB。";
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

function removeMaterial(item) {
  materials.value = materials.value.filter((material) => material.id !== item.id && material.url !== item.url);
  if (!String(item.id || "").startsWith("local-")) {
    apiRequest(`/api/materials/${item.id}`, { method: "DELETE" }).catch(() => {});
  }
}

function addMaterialToCurrentTask(item) {
  const target = item.type === "video" ? form.videos : item.type === "cover" ? null : form.images;
  if (item.type === "cover") {
    form.cover = item;
  } else if (target && !target.some((existing) => existing.url === item.url)) {
    target.push(item);
  }
  item.usage_count = (item.usage_count || 0) + 1;
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
      timeout: 45000,
      body: JSON.stringify({
        title: form.title,
        content: form.content,
        tags: parsedTags.value,
        author: username.value || null,
        platforms: form.platforms,
        use_ai: form.useAi,
        llm_provider: form.useAi ? form.llmProvider : null,
        media_files: {
          images: form.images.map((item) => item.url),
          videos: form.videos.map((item) => item.url),
          cover: form.cover?.url || null
        }
      })
    });
    taskId.value = response?.task_id || Date.now();
    Object.assign(adapted, response?.code === 200 && response.data ? response.data : buildLocalPreview());
    if (response?.ai_fallback) {
      notice.value = response.message || "大模型调用失败，已使用本地规则模板生成预览。";
      addNotification("failed", "AI 已降级", notice.value);
    } else if (response?.code !== 200) {
      notice.value = response?.message || "后端未返回有效结果，已使用本地规则生成预览。";
      addNotification("failed", "AI 调用失败", notice.value);
    } else {
      addNotification("success", "AI 生成成功", `已生成 ${form.platforms.length} 个平台版本。`);
    }
  } catch (error) {
    taskId.value = Date.now();
    Object.assign(adapted, buildLocalPreview());
    notice.value = error?.name === "AbortError" ? "AI 生成超时，已使用本地规则模板生成预览。" : "未连接到后端服务，已使用本地演示数据生成预览。";
    addNotification("failed", "AI 调用失败", notice.value);
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
    const response = await apiRequest("/api/account/mock-login", {
      method: "POST",
      body: JSON.stringify({ platform: platformId, account_name: accounts[platformId].accountName })
    });
    if (response?.code === 200) {
      saveLocalAccounts();
    } else {
      notice.value = response?.message || "后端账号登录保存失败，已保留本地登录状态。";
      saveLocalAccounts();
    }
  } catch (error) {
    // 离线演示允许模拟登录成功。
    saveLocalAccounts();
  }
}

function logoutPlatform(platformId) {
  accounts[platformId].loggedIn = false;
  accounts[platformId].authType = "未授权";
  accounts[platformId].accountName = "";
  accounts[platformId].expireAt = "-";
  saveLocalAccounts();
  apiRequest("/api/account/logout", {
    method: "POST",
    body: JSON.stringify({ platform: platformId })
  }).catch(() => {});
}

function openOfficialAuth(platformId) {
  authPlatformId.value = platformId;
  platformLoginForm.account = accounts[platformId].accountName || "";
  platformLoginForm.password = "";
  authDialogVisible.value = true;
}

function closeOfficialAuth() {
  authDialogVisible.value = false;
}

async function submitOfficialAuth() {
  const platform = platforms.find((item) => item.id === authPlatformId.value);
  accounts[authPlatformId.value].loggedIn = true;
  accounts[authPlatformId.value].accountName = platformLoginForm.account || `${platform?.name || authPlatformId.value}账号`;
  accounts[authPlatformId.value].authType = "Official OAuth";
  accounts[authPlatformId.value].expireAt = "2026-12-31";
  try {
    const response = await apiRequest("/api/account/mock-login", {
      method: "POST",
      body: JSON.stringify({ platform: authPlatformId.value, account_name: accounts[authPlatformId.value].accountName })
    });
    if (response?.code !== 200) {
      notice.value = response?.message || "后端账号授权保存失败，已保留本地授权状态。";
    }
  } catch (error) {
    // 保留前端模拟授权状态。
  }
  saveLocalAccounts();
  closeOfficialAuth();
}

async function publishAll() {
  notice.value = "";
  if (!previewList.value.length) {
    notice.value = "请先生成各平台预览内容。";
    return;
  }
  const offlinePlatforms = selectedPlatforms.value.filter((platform) => !accounts[platform.id]?.loggedIn);
  if (offlinePlatforms.length) {
    notice.value = `以下平台未登录，无法发布：${offlinePlatforms.map((platform) => platform.name).join("、")}`;
    addNotification("failed", "发布失败", notice.value);
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
    publishResults.value = response?.code === 200 ? response.data || [] : [];
    if (response?.code === 200) {
      addNotification("success", "模拟发布成功", `已生成 ${publishResults.value.length || form.platforms.length} 条发布记录。`);
    } else {
      addNotification("failed", "发布失败", response?.message || "模拟发布未成功。");
    }
  } catch (error) {
    publishResults.value = [];
    notice.value = "模拟发布失败，未生成发布记录。";
    addNotification("failed", "发布失败", "模拟发布失败，未生成发布记录。");
  } finally {
    await loadRecords();
    loading.publish = false;
    router.push("/records");
  }
}

function buildLocalRecordDetail(record) {
  return {
    id: record?.id || Date.now(),
    platform: record?.platform,
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

function openDeleteConfirm(record) {
  pendingDeleteRecord.value = record;
  deleteConfirmVisible.value = true;
}

function closeDeleteConfirm() {
  deleteConfirmVisible.value = false;
  pendingDeleteRecord.value = null;
}

async function confirmDeletePublishRecord() {
  const record = pendingDeleteRecord.value;
  if (!record) return;
  const recordId = Number(record.id);
  if (!Number.isInteger(recordId)) {
    history.value = history.value.filter((item) => item.id !== record.id);
    closeDeleteConfirm();
    return;
  }
  try {
    const response = await apiRequest(`/api/records/${recordId}`, { method: "DELETE" });
    if (response?.code !== 200) {
      notice.value = response?.message || "删除发布记录失败。";
      return;
    }
    if (selectedRecord.value?.id === recordId) {
      recordDetailVisible.value = false;
      selectedRecord.value = null;
    }
    closeDeleteConfirm();
    await loadRecords();
  } catch (error) {
    notice.value = "删除发布记录失败，请检查后端服务。";
  }
}

async function loadRecords() {
  loading.records = true;
  try {
    const response = await apiRequest("/api/records?limit=50");
    history.value = response?.code === 200 ? response.data || [] : [];
  } catch (error) {
    history.value = [];
  } finally {
    loading.records = false;
  }
}

async function loadMaterials() {
  loading.materials = true;
  try {
    const response = await apiRequest("/api/materials");
    if (response?.code === 200) {
      materials.value = response.data || [];
    }
  } catch (error) {
    materials.value = [];
  } finally {
    loading.materials = false;
  }
}

async function loadAccounts() {
  loadLocalAccounts();
  try {
    const response = await apiRequest("/api/account/list");
    if (response?.code === 200) {
      resetAccounts();
      response.data.forEach((item) => {
        if (!accounts[item.platform]) return;
        accounts[item.platform].loggedIn = item.login_status === "logged_in";
        accounts[item.platform].accountName = item.login_status === "logged_in" ? item.account_name || accounts[item.platform].accountName : "";
        accounts[item.platform].authType = item.auth_type === "mock" ? "Mock Token" : item.auth_type;
        accounts[item.platform].expireAt = item.token_expire_time || "-";
      });
      saveLocalAccounts();
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
    closeAiConfig();
  } catch (error) {
    notice.value = "后端不可用，AI 设置已保存到本地。";
    closeAiConfig();
  } finally {
    loading.settings = false;
  }
}

async function testModelConnection(provider = aiSettings.provider) {
  loading.settings = true;
  try {
    let response = await apiRequest("/api/settings/llm/test", {
      method: "POST",
      timeout: 30000,
      body: JSON.stringify({ provider, settings: aiSettings })
    });
    if (response?.code === 404) {
      response = await apiRequest("/api/settings/llm-test", {
        method: "POST",
        timeout: 30000,
        body: JSON.stringify({ provider, settings: aiSettings })
      });
    }
    notice.value = response?.message || "模型连接测试完成。";
    if (response?.code === 200) {
      addNotification("success", "模型连接成功", `${providerLabel(provider)} 测试通过。`);
    } else if (response?.code === 0 || response?.code === 408) {
      notice.value = response.message;
      addNotification("failed", "模型连接失败", response.message);
    } else {
      addNotification("failed", "模型连接失败", response?.message || `${providerLabel(provider)} 测试失败。`);
    }
  } catch (error) {
    notice.value = error?.message || "模型连接测试失败，请检查后端服务。";
    addNotification("failed", "模型连接失败", notice.value);
  } finally {
    loading.settings = false;
  }
}

onMounted(() => {
  applyTheme();
  window.matchMedia?.("(prefers-color-scheme: dark)").addEventListener?.("change", () => {
    if (themeMode.value === "system") applyTheme();
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
  --shadow: 0 12px 34px rgba(25, 34, 61, 0.07);
  --sidebar: 260px;
  --topbar: 74px;
}

:root[data-theme="dark"] {
  --accent: #ff8357;
  --accent-soft: #39261f;
  --blue: #77a7ff;
  --red: #ff6f80;
  --green: #45cf86;
  --purple: #a18cff;
  --ink: #eef3ff;
  --muted: #9aa8c0;
  --line: #2b3548;
  --panel: #151d2c;
  --page: #0d1420;
  --shadow: 0 18px 42px rgba(0, 0, 0, 0.28);
}

* { box-sizing: border-box; }
html { min-height: 100%; background: var(--page); }
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
.top-popover-wrap { position: relative; display: grid; place-items: center; width: 38px; height: 38px; }
.icon-btn { position: relative; width: 38px; height: 38px; display: grid; place-items: center; padding: 0; border: 0; border-radius: 50%; background: transparent; color: #4f5972; font-size: 0; line-height: 1; }
.theme-trigger span { display: grid; place-items: center; width: 22px; height: 22px; font-size: 22px; line-height: 1; transform: translateY(-1px); }
.icon-btn:hover { background: #f3f6fb; color: var(--accent); }
.icon-btn i { position: absolute; top: -2px; right: -2px; min-width: 18px; height: 18px; display: grid; place-items: center; padding: 0 5px; border: 2px solid var(--panel); border-radius: 999px; background: var(--red); color: #fff; font-size: 10px; font-style: normal; font-weight: 900; }
.bell svg { display: block; width: 22px; height: 22px; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.top-popover { position: absolute; top: 48px; right: 0; z-index: 40; width: 260px; padding: 10px; border: 1px solid var(--line); border-radius: 12px; background: var(--panel); box-shadow: 0 18px 46px rgba(25, 34, 61, 0.18); }
.theme-popover { width: 190px; display: grid; gap: 6px; }
.theme-popover button { display: flex; align-items: center; gap: 10px; min-height: 38px; padding: 0 10px; border: 0; border-radius: 8px; background: transparent; color: var(--ink); text-align: left; }
.theme-popover button:hover, .theme-popover button.active { background: var(--accent-soft); color: var(--accent); }
.theme-popover span { width: 20px; text-align: center; }
.notification-popover { width: 360px; max-height: 460px; overflow: auto; padding: 12px; }
.notification-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 4px 4px 12px; border-bottom: 1px solid var(--line); }
.notification-head button { border: 0; background: transparent; color: var(--blue); font-size: 12px; font-weight: 900; }
.notification-empty { padding: 30px 12px; color: var(--muted); text-align: center; font-weight: 800; }
.notification-item { position: relative; width: 100%; display: grid; grid-template-columns: 34px minmax(0, 1fr) auto; gap: 3px 10px; align-items: start; margin-top: 10px; padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; color: var(--ink); text-align: left; }
.notification-item.unread { border-color: #ffd0c0; background: linear-gradient(135deg, #fff7f3, #fbfcff); }
.notification-item.unread::after { content: ""; position: absolute; top: 12px; right: 12px; width: 7px; height: 7px; border-radius: 50%; background: var(--accent); }
.notification-item b { grid-row: 1 / 4; width: 30px; height: 30px; display: grid; place-items: center; border-radius: 50%; background: #edf8f2; color: var(--green); font-size: 15px; }
.notification-item.failed b { background: #fff0f1; color: var(--red); }
.notification-item span { font-weight: 900; }
.notification-item.success span { color: #15824a; }
.notification-item.failed span { color: #d33b4d; }
.notification-item p { grid-column: 2 / 4; margin: 0; color: #596276; line-height: 1.5; }
.notification-item small { grid-column: 2 / 4; color: #8a94aa; }
.profile { padding-left: 18px; border-left: 1px solid var(--line); }
.avatar { width: 42px; height: 42px; display: grid; place-items: center; border-radius: 50%; background: linear-gradient(135deg, #f8b28d, #5a87c8); color: #fff; font-weight: 900; }
.profile strong, .profile span { display: block; }
.profile strong { font-size: 14px; }
.profile div span { width: max-content; margin-top: 3px; padding: 2px 8px; border-radius: 99px; background: #fff2cc; color: #b88910; font-size: 11px; font-weight: 800; }
.logout-btn { border: 0; background: transparent; color: #7a849a; font-weight: 800; }

.workspace { display: grid; grid-template-columns: minmax(0, 1fr) 430px; gap: 22px; max-width: 1660px; margin: 0 auto; padding: 22px 28px 34px; }
.workspace.wide { grid-template-columns: minmax(0, 1fr); }
.main-column, .side-column { display: grid; align-content: start; gap: 20px; }
.panel { padding: 22px; }
.panel-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; margin-bottom: 20px; }
.panel-head.compact { margin-bottom: 16px; }
.panel h2, .panel-head h2 { margin: 0; font-size: 20px; line-height: 1.2; }
.panel-head p { margin: 8px 0 0; color: var(--muted); font-size: 14px; }
.dashboard-hero { position: relative; overflow: hidden; display: flex; align-items: center; justify-content: space-between; gap: 20px; min-height: 138px; padding: 26px 28px; background: linear-gradient(135deg, #fff7f2 0%, #eef4ff 100%); }
.dashboard-hero::after { content: ""; position: absolute; right: 28%; top: -40px; width: 220px; height: 220px; border-radius: 50%; background: rgba(255, 107, 53, 0.1); }
.dashboard-copy { position: relative; z-index: 1; display: grid; gap: 8px; }
.dashboard-copy span { color: var(--accent); font-size: 12px; font-weight: 900; text-transform: uppercase; }
.dashboard-copy h2, .dashboard-copy p { margin: 0; }
.dashboard-copy h2 { font-size: 28px; }
.dashboard-copy p { color: #526079; font-weight: 700; }
.quick-actions, .card-actions, .settings-actions { display: flex; gap: 10px; flex-wrap: wrap; }
.metric-grid, .material-stats { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; }
.metric-card { position: relative; display: grid; gap: 8px; min-height: 132px; padding: 18px; border: 1px solid var(--line); border-radius: 8px; background: #fff; box-shadow: var(--shadow); }
.metric-card i { position: absolute; top: 16px; right: 16px; width: 32px; height: 32px; display: grid; place-items: center; border-radius: 8px; background: var(--accent-soft); color: var(--accent); font-style: normal; font-weight: 900; }
.metric-card span { color: #68728b; font-weight: 800; }
.metric-card strong { font-size: 24px; }
.metric-card small { color: #8b94a8; }
.dashboard-records { box-shadow: 0 18px 46px rgba(25, 34, 61, 0.08); }
.dashboard-empty { display: grid; justify-items: center; gap: 8px; padding: 30px; border: 1px dashed #d8deea; border-radius: 8px; background: #fbfcff; text-align: center; }
.dashboard-empty strong { font-size: 17px; }
.dashboard-empty p { margin: 0; color: var(--muted); font-weight: 800; }

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

.media-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
.media-card { min-width: 0; padding: 14px; border: 1px solid var(--line); border-radius: 8px; }
.media-card strong { display: block; margin-bottom: 8px; font-size: 14px; }
.media-card strong span, .media-hint { color: #7b8498; }
.media-hint { min-height: 54px; margin: 0 0 10px; font-size: 12px; line-height: 1.5; }
.media-list { display: flex; gap: 10px; max-width: 100%; overflow-x: auto; padding: 2px 2px 8px; }
.thumb, .add-thumb, .cover-preview { border-radius: 8px; border: 1px solid var(--line); background: #f8fafc; overflow: hidden; }
.thumb, .add-thumb { position: relative; width: 88px; height: 88px; flex: 0 0 88px; }
.thumb img, .cover-preview img { width: 100%; height: 100%; object-fit: cover; }
.image-thumb small { position: absolute; left: 4px; right: 4px; bottom: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: #fff; font-size: 10px; text-shadow: 0 1px 4px #111; }
.video-thumb { display: grid; place-items: center; padding: 8px; color: #fff; background: linear-gradient(135deg, #17203a, #31517a); }
.video-thumb span { width: 30px; height: 30px; display: grid; place-items: center; border: 1px solid rgba(255, 255, 255, 0.75); border-radius: 50%; }
.video-thumb small { width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; text-align: center; font-size: 11px; }
.delete-media { position: absolute; top: 4px; right: 4px; width: 22px; height: 22px; border: 0; border-radius: 50%; background: rgba(24, 33, 58, 0.75); color: #fff; font-weight: 900; }
.add-thumb { border-style: dashed; color: #48536d; font-size: 28px; }
.cover-card { display: grid; grid-template-columns: 1fr auto; align-items: end; gap: 10px; }
.cover-card strong, .cover-card .media-hint { grid-column: 1 / -1; }
.cover-preview { width: 150px; height: 88px; }

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
.primary-btn, .primary-outline, .ghost-btn { height: 42px; border-radius: 8px; font-weight: 900; }
.primary-btn { border: 0; padding: 0 16px; background: linear-gradient(135deg, #ff4f83, #5e82ff); color: #fff; box-shadow: 0 12px 24px rgba(92, 118, 255, 0.24); }
.primary-btn:disabled, .primary-outline:disabled { cursor: not-allowed; opacity: 0.58; }
.primary-outline, .ghost-btn { padding: 0 16px; border: 1px solid var(--line); background: #fff; color: #45506a; }
.ghost-btn.small { height: 32px; padding: 0 10px; font-size: 12px; }
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
.records-empty { display: grid; justify-items: center; gap: 10px; padding: 40px 18px; border: 1px dashed #d8deea; border-radius: 8px; background: #fbfcff; color: #69738a; text-align: center; }
.records-empty strong { color: var(--ink); font-size: 18px; }
.records-empty p { margin: 0; font-weight: 700; }
.records-empty .primary-outline { margin-top: 4px; }
.record-list { display: grid; gap: 10px; }
.record-table-wrap { width: 100%; overflow-x: auto; border: 1px solid var(--line); border-radius: 8px; background: #fff; }
.record-table { width: 100%; min-width: 920px; border-collapse: collapse; table-layout: fixed; }
.record-table th,
.record-table td { height: 56px; padding: 0 16px; border-bottom: 1px solid var(--line); vertical-align: middle; text-align: left; }
.record-table th { height: 42px; background: #f6f8fc; color: #7b8498; font-size: 13px; font-weight: 900; }
.record-table th:nth-child(1), .record-table td:nth-child(1) { width: 168px; }
.record-table th:nth-child(3), .record-table td:nth-child(3) { width: 140px; }
.record-table th:nth-child(4), .record-table td:nth-child(4) { width: 178px; }
.record-table th:nth-child(5), .record-table td:nth-child(5) { width: 132px; text-align: right; }
.record-table tbody tr:last-child td { border-bottom: 0; }
.record-tr { cursor: pointer; }
.record-tr:hover td { background: #f7f9fd; }
.record-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 120px 170px 180px;
  gap: 12px;
  align-items: center;
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #fbfcff;
  cursor: pointer;
}
.record-row:hover { background: #f7f9fd; }
.record-row span, .record-row small { color: #6e788e; }
.record-time { color: #5f6b82; white-space: nowrap; font-variant-numeric: tabular-nums; }
.record-title {
  display: block;
  min-width: 0;
  overflow: hidden;
  color: var(--ink);
  text-overflow: ellipsis;
  white-space: nowrap;
}
.record-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
}
.record-action {
  display: inline-flex;
  justify-content: flex-end;
  gap: 0;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #fff;
}
.table-action-btn { height: 30px; padding: 0 10px; border: 0; border-right: 1px solid var(--line); background: transparent; color: #4d5871; font-size: 12px; font-weight: 900; }
.table-action-btn:last-child { border-right: 0; }
.table-action-btn:hover { background: #f3f6fb; color: var(--blue); }
.table-action-btn.danger { color: #c93648; }
.table-action-btn.danger:hover { background: #fff5f6; color: #b52b3d; }
.platform-tag {
  display: inline-flex;
  align-items: center;
  max-width: 100%;
  height: 26px;
  padding: 0 10px;
  overflow: hidden;
  border-radius: 999px;
  background: #f2f6ff;
  color: #3867d6;
  font-size: 12px;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.status-tag {
  display: inline-flex;
  align-items: center;
  height: 24px;
  padding: 0 9px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 900;
  line-height: 1;
}
.status-tag.success { background: #eaf8f0; color: #16834a; }
.status-tag.failed { background: #fff0f1; color: #c93648; }
.status-tag.mock { background: #eef4ff; color: #3867d6; }

.account-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.account-card { display: grid; gap: 14px; padding: 16px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; }
.account-card dl { display: grid; grid-template-columns: 88px 1fr; gap: 8px 12px; margin: 0; font-size: 14px; }
.account-card dt { color: #7b8498; }
.account-card dd { margin: 0; font-weight: 800; }
.filter-tabs { display: flex; gap: 8px; margin: 18px 0; }
.filter-tabs button { height: 34px; padding: 0 14px; border: 1px solid var(--line); border-radius: 999px; background: #fff; color: #5d6680; font-weight: 800; }
.filter-tabs button.active { border-color: var(--accent); background: var(--accent-soft); color: var(--accent); }
.material-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 14px; }
.material-card { display: grid; gap: 9px; padding: 14px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; }
.material-preview { height: 128px; display: grid; place-items: center; overflow: hidden; border-radius: 8px; background: #edf2f8; color: #50607a; font-weight: 900; }
.material-preview img { width: 100%; height: 100%; object-fit: cover; }
.material-card span, .material-card small { color: #6e788e; }
.settings-panel { display: grid; gap: 18px; }
.settings-panel .panel-head { margin-bottom: 0; }
.settings-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.default-model-card { display: grid; gap: 8px; padding: 18px 20px; border: 1px solid var(--line); border-radius: 8px; background: linear-gradient(135deg, #fff7f2, #eef4ff); }
.default-model-card span { color: var(--muted); font-size: 13px; font-weight: 900; }
.default-model-card strong { color: var(--ink); font-size: 24px; line-height: 1.2; }
.default-model-card small { color: #5f6b82; font-weight: 800; }
.ai-provider-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.ai-provider-card { min-height: 210px; display: grid; grid-template-rows: auto 1fr auto; gap: 14px; padding: 16px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; }
.ai-provider-card.active { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }
.ai-provider-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
.ai-provider-head h3, .ai-provider-head p { margin: 0; }
.ai-provider-head h3 { font-size: 17px; }
.ai-provider-head p { margin-top: 6px; color: var(--muted); font-size: 13px; line-height: 1.5; }
.ai-provider-head span { flex: 0 0 auto; padding: 4px 9px; border-radius: 999px; background: var(--accent-soft); color: var(--accent); font-size: 12px; font-weight: 900; }
.ai-provider-card dl { display: grid; grid-template-columns: 74px minmax(0, 1fr); gap: 8px 10px; margin: 0; font-size: 13px; }
.ai-provider-card dt { color: var(--muted); font-weight: 800; }
.ai-provider-card dd { min-width: 0; margin: 0; overflow: hidden; color: var(--ink); font-weight: 800; text-overflow: ellipsis; white-space: nowrap; }
.settings-preferences { display: grid; grid-template-columns: minmax(180px, 0.8fr) minmax(0, 1.4fr); align-items: end; gap: 18px; padding: 18px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; }
.settings-preferences h3, .settings-preferences p { margin: 0; }
.settings-preferences h3 { font-size: 16px; }
.settings-preferences p { margin-top: 6px; color: var(--muted); font-size: 13px; }
.settings-preference-fields { display: grid; grid-template-columns: minmax(130px, 1fr) minmax(130px, 1fr) auto; align-items: end; gap: 12px; }
.settings-preference-fields .setting-field { min-width: 0; }
.ai-config-dialog { position: relative; width: min(760px, 100%); display: grid; gap: 18px; padding: 28px; border: 1px solid var(--line); border-radius: 12px; background: #fff; box-shadow: 0 24px 80px rgba(0, 0, 0, 0.18); }
.official-auth-dialog { position: relative; width: min(720px, 100%); display: grid; gap: 18px; padding: 28px; border: 1px solid var(--line); border-radius: 12px; background: #fff; box-shadow: 0 24px 80px rgba(0, 0, 0, 0.18); }
.auth-dialog-body { display: grid; grid-template-columns: 240px minmax(0, 1fr); gap: 18px; align-items: stretch; }
.mock-qr { display: grid; place-items: center; align-content: center; gap: 10px; min-height: 240px; border: 1px dashed #cfd6e4; border-radius: 8px; background: #fbfcff; text-align: center; }
.mock-qr span { width: 118px; height: 118px; border: 8px solid #fff; background: repeating-linear-gradient(45deg, #18213a 0 8px, #fff 8px 16px); box-shadow: 0 0 0 1px #dfe5ef; }
.mock-qr strong { font-size: 16px; }
.mock-qr small { color: var(--muted); font-weight: 800; }
.auth-form { display: grid; align-content: center; gap: 14px; }
.auth-form label { display: grid; gap: 8px; color: var(--ink); font-weight: 900; }
.auth-form input { height: 42px; padding: 0 12px; border: 1px solid #dfe5ef; border-radius: 8px; outline: 0; }

.dialog-mask, .drawer-mask { position: fixed; inset: 0; z-index: 30; display: grid; place-items: center; padding: 24px; background: rgba(18, 27, 47, 0.42); }
.upgrade-dialog { position: relative; width: min(460px, 100%); display: grid; gap: 14px; padding: 26px; border-radius: 12px; background: #fff; box-shadow: 0 24px 80px rgba(0, 0, 0, 0.18); }
.upgrade-dialog h2, .upgrade-dialog p { margin: 0; }
.upgrade-dialog p { color: var(--muted); }
.dialog-close { position: absolute; top: 10px; right: 10px; width: 34px; height: 34px; border: 0; border-radius: 50%; background: #f2f4f8; color: #566176; font-size: 22px; }
.confirm-dialog { position: relative; width: min(440px, 100%); display: grid; justify-items: start; gap: 12px; padding: 28px; border: 1px solid var(--line); border-radius: 12px; background: #fff; box-shadow: 0 24px 80px rgba(0, 0, 0, 0.18); }
.confirm-icon { width: 42px; height: 42px; display: grid; place-items: center; border-radius: 50%; background: #fff0f1; color: #c93648; font-size: 22px; font-weight: 900; }
.confirm-dialog h2 { margin: 0; color: var(--ink); font-size: 20px; }
.confirm-dialog p { margin: 0; color: #596276; line-height: 1.7; }
.confirm-dialog strong { max-width: 100%; padding: 9px 12px; overflow: hidden; border-radius: 8px; background: #f7f9fc; color: var(--ink); font-size: 13px; text-overflow: ellipsis; white-space: nowrap; }
.confirm-actions { width: 100%; display: flex; justify-content: flex-end; gap: 10px; margin-top: 4px; }
.danger-confirm-btn { height: 42px; padding: 0 16px; border: 0; border-radius: 8px; background: #c93648; color: #fff; font-weight: 900; box-shadow: 0 12px 24px rgba(201, 54, 72, 0.22); }
.danger-confirm-btn:hover { background: #b52b3d; }
.sample-dialog { position: relative; width: min(760px, 100%); display: grid; gap: 18px; padding: 28px; border: 1px solid var(--line); border-radius: 12px; background: #fff; box-shadow: 0 24px 80px rgba(0, 0, 0, 0.18); }
.sample-dialog-head h2, .sample-dialog-head p { margin: 0; }
.sample-dialog-head p { margin-top: 8px; color: var(--muted); }
.sample-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.sample-card { min-height: 172px; display: grid; align-content: start; gap: 10px; padding: 16px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; color: var(--ink); text-align: left; }
.sample-card:hover { border-color: var(--accent); background: var(--accent-soft); }
.sample-card strong { font-size: 16px; }
.sample-card span { color: #58637a; font-size: 13px; line-height: 1.6; }
.sample-card small { color: var(--accent); font-size: 12px; font-weight: 900; line-height: 1.5; }
.pay-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.pay-grid div { display: grid; place-items: center; gap: 8px; min-height: 130px; border: 1px dashed #cfd6e4; border-radius: 8px; background: #fbfcff; color: #53607a; font-weight: 800; }
.pay-grid b { width: 74px; height: 74px; display: grid; place-items: center; background: repeating-linear-gradient(45deg, #111 0 6px, #fff 6px 12px); color: var(--accent); border: 8px solid #fff; box-shadow: 0 0 0 1px #dfe5ef; }
.record-drawer { position: relative; width: min(980px, 100%); max-height: 88vh; overflow: auto; display: grid; gap: 16px; padding: 28px; border-radius: 12px; background: #fff; box-shadow: 0 24px 80px rgba(0, 0, 0, 0.18); }
.record-drawer h2 { margin: 0; }
.detail-meta { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; color: #65708a; font-weight: 800; font-size: 13px; }
.detail-meta span { min-width: 0; display: grid; gap: 4px; padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; color: var(--ink); overflow-wrap: anywhere; }
.detail-meta b { color: #7b8498; font-size: 12px; }
.source-text { margin: 0; padding: 14px; border-radius: 8px; background: #f7f9fc; color: #4e5a74; line-height: 1.7; white-space: pre-wrap; }
.detail-section { display: grid; gap: 10px; }
.detail-section h3 { margin: 0; color: var(--ink); font-size: 15px; }
.detail-post-title { min-width: 0; padding: 12px 14px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; color: var(--ink); overflow-wrap: anywhere; }
.detail-tags small { color: #7b8498; font-weight: 800; }
.detail-materials { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 10px; }
.detail-materials a { min-width: 0; display: grid; gap: 6px; padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; color: var(--ink); text-decoration: none; }
.detail-materials span { color: var(--accent); font-size: 12px; font-weight: 900; }
.detail-materials strong { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.detail-empty { padding: 12px 14px; border: 1px dashed #d8deea; border-radius: 8px; background: #fbfcff; color: #7b8498; font-weight: 800; }
.detail-platforms { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.detail-card { display: grid; gap: 10px; padding: 16px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcff; }
.detail-card h3, .detail-card p { margin: 0; }
.detail-card p { color: #4e5a74; line-height: 1.7; white-space: pre-wrap; }

:root[data-theme="dark"] .auth-card,
:root[data-theme="dark"] body,
:root[data-theme="dark"] .app-shell,
:root[data-theme="dark"] .workspace,
:root[data-theme="dark"] .sidebar,
:root[data-theme="dark"] .topbar,
:root[data-theme="dark"] .panel,
:root[data-theme="dark"] .metric-card,
:root[data-theme="dark"] .platform-card,
:root[data-theme="dark"] .preview-card,
:root[data-theme="dark"] .record-table-wrap,
:root[data-theme="dark"] .record-action,
:root[data-theme="dark"] .table-action-btn,
:root[data-theme="dark"] .account-card,
:root[data-theme="dark"] .material-card,
:root[data-theme="dark"] .ai-provider-card,
:root[data-theme="dark"] .ai-config-dialog,
:root[data-theme="dark"] .official-auth-dialog,
:root[data-theme="dark"] .settings-preferences,
:root[data-theme="dark"] .dashboard-hero,
:root[data-theme="dark"] .dashboard-empty,
:root[data-theme="dark"] .mock-qr,
:root[data-theme="dark"] .more-platforms button,
:root[data-theme="dark"] .filter-tabs button,
:root[data-theme="dark"] .confirm-dialog strong,
:root[data-theme="dark"] .pay-grid div,
:root[data-theme="dark"] .detail-card,
:root[data-theme="dark"] .upgrade-dialog,
:root[data-theme="dark"] .sample-dialog,
:root[data-theme="dark"] .confirm-dialog,
:root[data-theme="dark"] .record-drawer,
:root[data-theme="dark"] .top-popover { background: var(--panel); }
:root[data-theme="dark"] { color-scheme: dark; }
html[data-theme="dark"],
:root[data-theme="dark"] body { background: var(--page); }
:root[data-theme="dark"] .topbar { background: rgba(21, 29, 44, 0.94); }
:root[data-theme="dark"] .auth-page { background: var(--page); }
:root[data-theme="dark"] .default-model-card { background: #101827; }
:root[data-theme="dark"] .dashboard-copy p { color: var(--muted); }
:root[data-theme="dark"] .upgrade-card { background: #1d2435; color: var(--purple); }
:root[data-theme="dark"] .upgrade-card.pro { background: #14291f; color: var(--green); }
:root[data-theme="dark"] input,
:root[data-theme="dark"] textarea,
:root[data-theme="dark"] select,
:root[data-theme="dark"] .input-wrap,
:root[data-theme="dark"] .tag-editor,
:root[data-theme="dark"] .rich-editor,
:root[data-theme="dark"] .segmented,
:root[data-theme="dark"] .sample-card,
:root[data-theme="dark"] .records-empty,
:root[data-theme="dark"] .empty-state,
:root[data-theme="dark"] .record-table th,
:root[data-theme="dark"] .record-row,
:root[data-theme="dark"] .detail-meta span,
:root[data-theme="dark"] .source-text,
:root[data-theme="dark"] .detail-post-title,
:root[data-theme="dark"] .detail-materials a,
:root[data-theme="dark"] .detail-empty,
:root[data-theme="dark"] .notification-item,
:root[data-theme="dark"] .material-preview,
:root[data-theme="dark"] .tag-editor span,
:root[data-theme="dark"] .thumb,
:root[data-theme="dark"] .add-thumb,
:root[data-theme="dark"] .cover-preview { background: #101827; color: var(--ink); border-color: var(--line); }
:root[data-theme="dark"] .primary-outline,
:root[data-theme="dark"] .ghost-btn { background: #f8fafc; color: #18213a; border-color: #d9e0ec; }
:root[data-theme="dark"] .topbar .ghost-btn { background: #f8fafc; color: #18213a; }
:root[data-theme="dark"] .notification-item.unread { background: #241c1d; border-color: #61313b; }
:root[data-theme="dark"] .platform-card.selected.wechat,
:root[data-theme="dark"] .platform-card.selected.zhihu,
:root[data-theme="dark"] .platform-card.selected.bilibili,
:root[data-theme="dark"] .platform-card.selected.xiaohongshu,
:root[data-theme="dark"] .theme-popover button:hover,
:root[data-theme="dark"] .theme-popover button.active { background: var(--accent-soft); }
:root[data-theme="dark"] .icon-btn { color: #c5cee0; }
:root[data-theme="dark"] .icon-btn:hover { background: #202a3c; }
:root[data-theme="dark"] .record-tr:hover td { background: #172132; }
:root[data-theme="dark"] .record-table td { background: var(--panel); }
:root[data-theme="dark"] .platform-tag { background: #172643; color: #8fb5ff; }
:root[data-theme="dark"] .status-tag.success { background: #133124; color: #70e0a2; }
:root[data-theme="dark"] .status-tag.failed { background: #3a1820; color: #ff8796; }
:root[data-theme="dark"] .status-tag.mock { background: #172643; color: #8fb5ff; }
:root[data-theme="dark"] .publish-overview-item { border-bottom-color: var(--line); color: var(--muted); }
:root[data-theme="dark"] .profile div span { background: #352b17; color: #ffd36a; }
:root[data-theme="dark"] .preview-card input,
:root[data-theme="dark"] .preview-card textarea { background: #101827; color: var(--ink); border-color: var(--line); }
:root[data-theme="dark"] .panel-head p,
:root[data-theme="dark"] .field > span,
:root[data-theme="dark"] .ai-panel label > span,
:root[data-theme="dark"] .setting-field span,
:root[data-theme="dark"] .notification-item p,
:root[data-theme="dark"] .detail-card p { color: var(--muted); }

@media (max-width: 1320px) {
  .workspace { grid-template-columns: 1fr; }
  .side-column { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .platform-panel { grid-column: 1 / -1; }
  .ai-panel, .settings-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 900px) {
  :root { --sidebar: 0px; --topbar: 64px; }
  .sidebar { display: none; }
  .topbar { left: 0; padding: 0 14px; }
  .stepper { overflow-x: auto; gap: 12px; }
  .top-actions { display: none; }
  .workspace { padding: 14px; }
  .media-grid, .side-column, .preview-grid, .platform-grid, .metric-grid, .material-stats, .account-grid, .settings-grid, .sample-grid, .detail-platforms, .detail-meta { grid-template-columns: 1fr; }
  .ai-panel { grid-template-columns: 1fr; }
  .record-row:not(.table) { grid-template-columns: 1fr; }
  .dashboard-hero { display: grid; }
}
</style>
