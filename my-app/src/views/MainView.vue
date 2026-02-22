<template>
  <div class="main-container">

    <!-- ========================= -->
    <!-- ヘッダー（ログイン・ログアウト） -->
    <!-- ========================= -->
    <div class="header">
      <div class="login-info">
        ログイン中: <strong>{{ username }}</strong>
      </div>
      <button class="btn-logout" @click="logout">ログアウト</button>
    </div>

    <!-- ========================= -->
    <!-- メニュー（メモ・カテゴリ・タグ） -->
    <!-- ========================= -->
    <div class="top-menu">
      <button :class="{ active: currentView === 'memo' }" @click="currentView = 'memo'">メモ</button>
      <button :class="{ active: currentView === 'category' }" @click="currentView = 'category'">カテゴリ管理</button>
      <button :class="{ active: currentView === 'tag' }" @click="currentView = 'tag'">タグ管理</button>
    </div>

    <!-- ========================= -->
    <!-- メモ管理画面 -->
    <!-- ========================= -->
    <div v-if="currentView === 'memo'" class="main-view">
      <div class="memo-controls">
        <button class="btn-filter" @click="showFilter = true">🔍 フィルター</button>
        <button class="btn-create" @click="showCreate = true">＋ 新規メモ</button>
      </div>

      <MemoFilter
        v-if="showFilter"
        v-model="filterCondition"
        :tags="tags"
        :categories="categories"
        @close="showFilter = false"
      />

      <MemoList :memos="filteredMemos" @open-detail="openDetail" />

      <MemoCreateModal
        v-if="showCreate"
        :tags="tags"
        :categories="categories"
        @close="showCreate = false"
        @create="createMemo"
      />

      <MemoDetailModal
        v-if="selectedMemo"
        :memo="selectedMemo"
        :tags="tags"
        :categories="categories"
        @close="closeDetail"
        @update="updateMemoData"
        @delete="deleteMemoData"
      />
    </div>

    <!-- ========================= -->
    <!-- カテゴリ管理画面 -->
    <!-- ========================= -->
    <div v-if="currentView === 'category'" class="admin-view">
      <CategoryManager :model-value="categories" @reload="loadAllData" />
    </div>

    <!-- ========================= -->
    <!-- タグ管理画面 -->
    <!-- ========================= -->
    <div v-if="currentView === 'tag'" class="admin-view">
      <TagManager :model-value="tags" @reload="loadAllData" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { jwtDecode } from "jwt-decode";

import MemoFilter from "./components/MemoFilter.vue";
import MemoList from "./components/MemoList.vue";
import MemoCreateModal from "./components/MemoCreateModal.vue";
import MemoDetailModal from "./components/MemoDetailModal.vue";
import CategoryManager from "./components/CategoryManager.vue";
import TagManager from "./components/TagManager.vue";

import {
  fetchMemos,
  addMemo,
  updateMemo,
  deleteMemo,
  fetchCategories,
  fetchTags,
} from "../api/api";

// ---------------------------
// 認証情報
// ---------------------------
const username = ref("");
const router = useRouter();
const route = useRoute();

// ---------------------------
// データ
// ---------------------------
const memos = ref([]);
const tags = ref([]);
const categories = ref([]);

const currentView = ref("memo");
const showCreate = ref(false);
const selectedMemo = ref(null);
const showFilter = ref(false);

const filterCondition = ref({
  keyword: "",
  category_id: "",
  tag_id: "",
  important: "",
  sort: "created_desc",
});


// ---------------------------
// ログアウト
// ---------------------------
const logout = () => {
  localStorage.clear();
  router.push("/");
};

// ---------------------------
// 共通エラーハンドラ
// ---------------------------
const handleApiError = (err) => {
  console.error(err);

  const status = err?.response?.status;

  if (status === 401 || status === 403) {
    alert("セッションが切れました。再ログインしてください。");
    logout();
    return;
  }

  alert("エラーが発生しました。再度お試しください。");
};


// ---------------------------
// JWT 検証 + ユーザー取得
// ---------------------------
const initAuth = () => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("token not found");

    const decoded = jwtDecode(token);

    // 有効期限チェック
    if (decoded.exp * 1200 < Date.now()) {
      throw new Error("token expired");
    }

    username.value = decoded.sub;
  } catch (e) {
    console.warn("Auth failed:", e);
    logout();
  }
};


// ---------------------------
// APIロード（※ user 制約は backend 側）
// ---------------------------
const isLoading = ref(false);

const loadAllData = async () => {
  isLoading.value = true;
  try {
    const [memoRes, catRes, tagRes] = await Promise.all([
      fetchMemos(),
      fetchCategories(),
      fetchTags(),
    ]);

    memos.value = memoRes;
    categories.value = catRes;
    tags.value = tagRes;

    const memoId = Number(route.params.id);
    if (memoId) openDetail(memoId, false);

  } catch (err) {
    handleApiError(err);
  } finally {
    isLoading.value = false;
  }
};


// ---------------------------
// JOIN 表示用
// ---------------------------
const enhanceMemo = (memo) => {
  const category = categories.value.find(c => c.id === memo.category_id);
  return {
    ...memo,
    categoryName: category ? category.name : "未分類",
    tagNames: memo.tags?.map(t => t.name) || [],
  };
};

// ---------------------------
// フィルタ
// ---------------------------
const filteredMemos = computed(() => {
  let result = memos.value.map(enhanceMemo);
  const cond = filterCondition.value;

  if (cond.keyword) {
    const kw = cond.keyword.toLowerCase();
    result = result.filter(m =>
      m.title?.toLowerCase().includes(kw) ||
      m.content?.toLowerCase().includes(kw)
    );
  }

  if (cond.category_id) {
    result = result.filter(m => m.category_id == cond.category_id);
  }

  if (cond.tag_id) {
    result = result.filter(m => m.tags?.some(t => t.id == cond.tag_id));
  }

  if (cond.important) {
    result = result.filter(m => m.important == cond.important);
  }

  return result;
});

// ---------------------------
// CRUD
// ---------------------------

// メモの新規作成
const createMemo = async (memo) => {
  try {
    await addMemo(memo);
    await loadAllData();
    showCreate.value = false;
  } catch (err) {
    handleApiError(err);
  }
};

// メモの詳細表示(オープン)
const openDetail = (id, pushUrl = true) => {
  selectedMemo.value = memos.value.find(m => m.id === id) || null;
  if (pushUrl) router.push(`/memos/${id}`);
};

// メモの詳細表示(クローズ)
const closeDetail = () => {
  selectedMemo.value = null;
  router.push("/home");
};

// メモの編集
const updateMemoData = async (id, data) => {
  try {
    await updateMemo(id, data);
    await loadAllData();
    closeDetail();
  } catch (err) {
    handleApiError(err);
  }
};

// メモの削除
const deleteMemoData = async (id) => {
  if (!confirm("削除しますか？")) return;

  try {
    await deleteMemo(id);
    await loadAllData();
    closeDetail();
  } catch (err) {
    handleApiError(err);
  }
};

// URL直アクセス
watch(route, (r) => {
  if (r.params.id) openDetail(Number(r.params.id), false);
  else selectedMemo.value = null;
});

// 初期化
onMounted(() => {
  initAuth();
  loadAllData();
});
</script>

<style scoped>
/* 全体コンテナ */
.main-container {
  display: flex;
  flex-direction: column;
  padding: 1rem;
}



/* =========================
   ヘッダー（ログイン情報＋ログアウト）
========================= */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%; /* PC画面幅の80% */
  margin-bottom: 1rem;
}

.login-info {
  padding: 0.4rem 0.8rem;

  background-color: #700000ff;
  color: white;
}

.btn-logout {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  background-color: #f87171;
  color: white;
  cursor: pointer;
}

/* =========================
   メニュー（メモ・カテゴリ・タグ）
========================= */
.top-menu {
  display: flex;
  justify-content: space-between;
  width: 100%; /* PC画面幅の80% */
  margin-bottom: 1rem;
}

.top-menu button {
  flex: 1;
  margin: 0 0.25rem;
  padding: 0.5rem 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #e5e7eb;
}

.top-menu button.active {
  background-color: #3b82f6;
  color: white;
}

/* =========================
   メモ画面のボタン（フィルター・新規作成）
========================= */
.memo-controls {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
  width: 100%;
}

.btn-filter,
.btn-create {
  flex: 1;
  padding: 0.6rem 0;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  color: white;
}

.btn-filter {
  background-color: #3b82f6;
}

.btn-create {
  background-color: #10b981;
}

/* =========================
   スマホ対応
========================= */
@media (max-width: 600px) {
  .header,
  .top-menu,
  .memo-controls {
    width: 100%; /* スマホでは100% */
  }

  .top-menu {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr; /* 3分割 */
    gap: 0.5rem;
  }

  .memo-controls {
    display: grid;
    grid-template-columns: 1fr 1fr; /* フィルター・新規作成横並び */
    gap: 0.5rem;
  }
}
</style>