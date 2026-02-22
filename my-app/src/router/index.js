import { createRouter, createWebHistory } from "vue-router";
import { jwtDecode } from "jwt-decode"; // ← named import に修正

import LoginView from "../views/LoginView.vue";
import MainView from "../views/MainView.vue";
import AdminView from "../views/AdminView.vue";

const routes = [
  { path: "/", component: LoginView },
  { path: "/home", component: MainView },
  { path: "/memos/:id", component: MainView },
  { path: "/admin", component: AdminView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ルートガード
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");

  // 未ログイン → ログイン画面へ
  if (!token && to.path !== "/") return next("/");

  // ログイン済みで login に来たら home
  if (token && to.path === "/") return next("/home");

  if (token) {
    try {
      const decoded = jwtDecode(token); // named import に変更済み
      const role = decoded.role || "user";

      // admin ルート制御
      if (to.path === "/admin" && role !== "admin") {
        alert("管理者権限が必要です");
        return next("/home");
      }
    } catch (e) {
      console.error("JWT decode error:", e);
      localStorage.removeItem("access_token");
      return next("/");
    }
  }

  next();
});

export default router;
