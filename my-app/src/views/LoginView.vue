<template>
  <div class="login-container">
    <h1 class="app-title">メモアプリ</h1>
    <h2>ログイン</h2>

    <form @submit.prevent="loginUser" class="login-form">
      <input
        v-model="username"
        type="text"
        placeholder="ユーザー名"
        required
      />

      <input
        v-model="password"
        type="password"
        placeholder="パスワード"
        required
      />

      <button type="submit">ログイン</button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { jwtDecode } from "jwt-decode";

import { login } from "../api/api.js";

const username = ref("");
const password = ref("");
const error = ref("");

const router = useRouter();

const loginUser = async () => {
  error.value = "";

  try {
    const data = await login(username.value, password.value);

    const decoded = jwtDecode(data.access_token); // 正常に decode 可能

    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("username", decoded.sub);
    localStorage.setItem("role", decoded.role || "user");

    if ((decoded.role || "user") === "admin") {
      await router.push("/admin");
    } else {
      await router.push("/home");
    }
  } catch (e) {
    console.error("ログインエラー:", e);
    error.value = "ユーザー名またはパスワードが違います";
  }
};
</script>

<style scoped>
/* コンテナ */
.login-container {
  max-width: 400px;
  margin: 60px auto;
  padding: 24px;
  border: 1px solid #ccc;
  border-radius: 12px;
  background: #f9f9f9;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* タイトル */
.app-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #3b82f6;
}

/* サブタイトル */
h2 {
  margin-bottom: 24px;
  font-weight: normal;
  color: #333;
}

/* 入力フォーム */
.login-form input {
  width: 100%;
  padding: 10px;
  margin-bottom: 16px;
  border-radius: 6px;
  border: 1px solid #ccc;
  box-sizing: border-box;
  font-size: 1rem;
}

/* ボタン */
.login-form button {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: none;
  background-color: #3b82f6;
  color: white;
  font-size: 1rem;
  cursor: pointer;
}

.login-form button:hover {
  background-color: #2563eb;
}

/* エラー表示 */
.error {
  margin-top: 12px;
  color: red;
  font-size: 0.9rem;
}

/* スマホ対応 */
@media (max-width: 480px) {
  .login-container {
    margin: 40px 16px;
    padding: 20px;
  }

  .app-title {
    font-size: 1.5rem;
  }

  .login-form input,
  .login-form button {
    padding: 8px;
    font-size: 0.95rem;
  }
}
</style>