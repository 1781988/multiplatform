import { createRouter, createWebHistory } from "vue-router";

const Page = { template: "<div />" };

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/dashboard" },
    { path: "/login", component: Page, meta: { public: true, title: "登录" } },
    { path: "/register", component: Page, meta: { public: true, title: "注册" } },
    { path: "/dashboard", component: Page, meta: { title: "工作台" } },
    { path: "/content", component: Page, meta: { title: "内容创作" } },
    { path: "/preview", component: Page, meta: { title: "平台预览" } },
    { path: "/records", component: Page, meta: { title: "发布记录" } },
    { path: "/accounts", component: Page, meta: { title: "账号管理" } },
    { path: "/materials", component: Page, meta: { title: "素材管理" } },
    { path: "/settings", component: Page, meta: { title: "AI 设置" } },
    { path: "/help", component: Page, meta: { title: "帮助中心" } },
    { path: "/:pathMatch(.*)*", redirect: "/dashboard" }
  ]
});

router.beforeEach((to) => {
  const token = localStorage.getItem("token");
  if (!to.meta.public && !token) return "/login";
  if ((to.path === "/login" || to.path === "/register") && token) return "/dashboard";
  return true;
});

router.afterEach((to) => {
  document.title = `${to.meta.title || "工作台"} - 聚舟 MultiPost AI`;
});

export default router;
