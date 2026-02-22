<template>
  <div class="admin-container">
    <!-- ヘッダー -->
    <div class="header">
      <h2>管理者画面</h2>
      <div class="user-info">
        <span>ログイン中: {{ username }}</span>
        <button @click="logout" class="logout-btn">ログアウト</button>
      </div>
    </div>

    <!-- 新規ユーザー作成フォーム -->
    <div class="create-user">
      <input v-model="newUsername" placeholder="ユーザー名" />
      <input type="password" v-model="newPassword" placeholder="パスワード" />
      <select v-model="newRole">
        <option value="user">user</option>
        <option value="admin">admin</option>
      </select>
      <button @click="addUser" :disabled="isProcessing">作成</button>
    </div>

    <!-- ユーザー一覧 -->
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>ユーザー名</th>
            <th>新パスワード</th>
            <th>役割</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>
              <input v-model="user.username" />
            </td>
            <td>
              <input
                type="password"
                v-model="user.newPassword"
                placeholder="変更する場合のみ入力"
              />
            </td>
            <td>{{ user.role }}</td>
            <td>
              <button @click="updateUser(user)" :disabled="isProcessing">
                編集
              </button>
              <button @click="deleteUser(user)" :disabled="isProcessing">
                削除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { jwtDecode } from 'jwt-decode';
import {
  fetchUsers,
  updateUser as apiUpdateUser,
  deleteUser as apiDeleteUser,
  createUser
} from '../api/api.js';

const router = useRouter();

const users = ref([]);
const username = ref('');
const newUsername = ref('');
const newPassword = ref('');
const newRole = ref('user');
const error = ref('');
const isProcessing = ref(false);

/* -------------------------
   共通
-------------------------- */
const logout = () => {
  localStorage.clear();
  router.push('/');
};

const loadUsers = async () => {
  const data = await fetchUsers();
  users.value = data.map(u => ({ ...u, newPassword: '' }));
};

/* -------------------------
   更新
-------------------------- */
const updateUser = async (user) => {
  if (isProcessing.value) return;

  if (!confirm('このユーザーを更新しますか？')) return;

  isProcessing.value = true;
  try {
    const payload = { username: user.username };
    if (user.newPassword) payload.password = user.newPassword;

    await apiUpdateUser(user.id, payload);
    loadUsers();
  } catch (e) {
    console.error(e);
    error.value = '更新に失敗しました';
  } finally {
    isProcessing.value = false;
  }
};

/* -------------------------
   削除
-------------------------- */
const deleteUser = async (user) => {
  if (isProcessing.value) return;

  // 自分自身の削除禁止
  if (user.username === username.value) {
    error.value = '自分自身は削除できません';
    return;
  }

  if (!confirm('本当に削除しますか？')) return;

  isProcessing.value = true;
  try {
    await apiDeleteUser(user.id);
    loadUsers();
  } catch (e) {
    console.error(e);
    error.value = '削除に失敗しました';
  } finally {
    isProcessing.value = false;
  }
};

/* -------------------------
   作成
-------------------------- */
const addUser = async () => {
  if (isProcessing.value) return;

  // 入力チェック
  if (!/^[a-zA-Z0-9_]{4,20}$/.test(newUsername.value)) {
    error.value = 'ユーザー名形式が不正です';
    return;
  }

  if (newPassword.value.length < 8) {
    error.value = 'パスワードは8文字以上です';
    return;
  }

  if (!['user', 'admin'].includes(newRole.value)) {
    error.value = '不正な権限です';
    return;
  }

  isProcessing.value = true;
  try {
    await createUser({
      username: newUsername.value,
      password: newPassword.value,
      role: newRole.value
    });

    newUsername.value = '';
    newPassword.value = '';
    newRole.value = 'user';
    loadUsers();
  } catch (e) {
    console.error(e);
    error.value = '作成に失敗しました';
  } finally {
    isProcessing.value = false;
  }
};

/* -------------------------
   初期処理（①②）
-------------------------- */
onMounted(() => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) throw new Error();

    const decoded = jwtDecode(token);

    // 管理者チェック
    if (decoded.role !== 'admin') throw new Error();

    // 有効期限チェック
    const now = Math.floor(Date.now() / 1000);
    if (decoded.exp && decoded.exp < now) throw new Error();

    username.value = decoded.sub;
    loadUsers();
  } catch {
    logout();
  }
});
</script>



<style scoped>
.admin-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  overflow: hidden; /* メイン画面は固定 */
}

/* ヘッダー */
.header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.header h2 {
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logout-btn {
  padding: 0.3rem 0.6rem;
  border: none;
  border-radius: 4px;
  background-color: #f87171;
  color: white;
  cursor: pointer;
}

/* 新規ユーザー作成フォーム */
.create-user {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
  justify-content: center;
  width: 80%;
  max-width: 100%;
  box-sizing: border-box;
}

.create-user input,
.create-user select,
.create-user button {
  padding: 0.4rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  flex: 1 1 150px; /* PC: 均等に伸縮 */
  min-height: 2rem; /* 高さを固定して大きくなりすぎない */
}


/* テーブルラッパー */
.table-wrapper {
  width: 80%;
  max-height: 400px; /* 縦スクロール高さ */
  overflow-y: auto;
  border: 1px solid #ccc;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 0.5rem;
  border: 1px solid #ccc;
  text-align: left;
}

input {
  width: 100%;
  box-sizing: border-box;
}

/* エラー表示 */
.error {
  color: red;
  margin-top: 0.5rem;
}

/* レスポンシブ対応 */
@media (max-width: 600px) {
  .table-wrapper {
    width: 100%;
  }
  .create-user {
    flex-direction: column;
    align-items: stretch;
  }
  .user-info {
    width: 100%;
    justify-content: flex-end;
  }
}

/* スマホ対応：2行2列 */
@media (max-width: 600px) {
  .create-user {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto auto;
    gap: 0.5rem;
  }

  .create-user input,
  .create-user select,
  .create-user button {
    flex: none;
    width: 100%;
  }

  /* 配置調整：入力/選択/ボタン順に対応 */
  .create-user input:nth-child(1) { grid-column: 1; grid-row: 1; } /* ユーザー名 */
  .create-user input:nth-child(2) { grid-column: 2; grid-row: 1; } /* パスワード */
  .create-user select { grid-column: 1; grid-row: 2; }               /* 選択肢 */
  .create-user button { grid-column: 2; grid-row: 2; }               /* 作成ボタン */
}

</style>