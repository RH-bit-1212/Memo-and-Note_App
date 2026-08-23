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
        <button
          class="btn-view"
          :class="{ active: viewMode }"
          @click="viewMode = !viewMode"
        >
          {{ viewMode ? "閲覧ON" : "閲覧OFF" }}
        </button>
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

      <MemoList :memos="filteredMemos" @open-detail="handleMemoClick" />

      <MemoCreateModal
        v-if="showCreate"
        :tags="tags"
        :categories="categories"
        @close="showCreate = false"
        @create="createMemo"
      />

      <MemoDetailModal
        v-if="selectedMemo && !viewMode"
        :memo="selectedMemo"
        :tags="tags"
        :categories="categories"
        @close="closeDetail"
        @update="updateMemoData"
        @delete="deleteMemoData"
      />

      <MemoViewModal
        v-if="selectedMemo && viewMode"
        :memo="selectedMemo"
        :tags="tags"
        :categories="categories"
        @close="closeDetail"
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
import { ref, onMounted, watch, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { jwtDecode } from "jwt-decode";

import MemoFilter from "./components/MemoFilter.vue";
import MemoList from "./components/MemoList.vue";
import MemoCreateModal from "./components/MemoCreateModal.vue";
import MemoDetailModal from "./components/MemoDetailModal.vue";
import CategoryManager from "./components/CategoryManager.vue";
import TagManager from "./components/TagManager.vue";
import MemoViewModal from "./components/MemoViewModal.vue";

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
const viewMode = ref(false); // false=編集モード / true=閲覧モード

const filterCondition = ref({
  keyword: "",
  category_id: "",
  tag_ids: [],
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
// loading
// ---------------------------
const isLoading = ref(false);

// ---------------------------
// API load（完全API駆動）
// ---------------------------
const loadAllData = async () => {
  isLoading.value = true;

  try {
    const params = {
      ...filterCondition.value,
      tag_ids: filterCondition.value.tag_ids || [],
    };

    const [memoRes, catRes, tagRes] = await Promise.all([
      fetchMemos(params),
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
const filteredMemos = computed(() =>
  memos.value.map(enhanceMemo)
);

// ---------------------------
// 閲覧モード
// ---------------------------
const handleMemoClick = (id) => {
  selectedMemo.value =
    memos.value.find(m => m.id === id) || null;

  router.push(`/memos/${id}`);
};

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

// ---------------------------
// filter watch（debounce化）
// ---------------------------
let timer = null;

watch(filterCondition, () => {
  clearTimeout(timer);

  timer = setTimeout(() => {
    loadAllData();
  }, 300);
}, { deep: true });

// 初期化
onMounted(() => {
  initAuth();
  loadAllData();
});
</script>



<style scoped>
/* 全体コンテナ */
.main-container {
  min-height: 100vh;
  background-image: url("../assets/backgrounds/haikei.jpg");

  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

/* =========================
   ヘッダー（ログイン情報＋ログアウト）
========================= */
.header {
  display: flex;
  justify-content: flex-end;
  align-items: center;

  gap: 0.5rem;

  width: 100%;

  margin-bottom: 0.5rem;
}

.login-info {
  padding: 0.2rem 0.5rem;

  font-size: 0.8rem;

  border-radius: 4px;

  background: rgba(0,0,0,0.6);
  color: white;
}

.btn-logout {
  padding: 0.2rem 0.6rem;

  font-size: 0.8rem;

  border: none;
  border-radius: 4px;

  background-color: #ef4444;
  color: white;

  cursor: pointer;
}

/* =========================
   メニュー（メモ・カテゴリ・タグ）
========================= */
.top-menu {
  display: flex;

  border-bottom: 2px solid rgba(255,255,255,0.3);

  background: rgba(255,255,255,0.35);
  backdrop-filter: blur(6px);
}

.top-menu button {
  flex: 1;

  border: none;

  background: transparent;

  padding: 12px;

  color: #374151;

  cursor: pointer;

  transition: background-color 0.2s;
}

.top-menu button:hover {
  background: rgba(255,255,255,0.25);
}

.top-menu button.active {
  background: rgba(59,130,246,0.12);

  border-bottom: 3px solid #3b82f6;

  color: #2563eb;
  font-weight: bold;
}

/* =========================
   メモ画面のボタン（フィルター・新規作成）
========================= */
.memo-controls {
  display: grid;
  grid-template-columns: repeat(3, 1fr);

  width: 100%;
  margin-bottom: 1rem;

  border: 1px solid #cbd5e1;

  background: rgba(255,255,255,0.55);
  backdrop-filter: blur(6px);
}

/* 共通ボタン */
.btn-view,
.btn-filter,
.btn-create {
  padding: 0.8rem;

  border: none;
  background: rgba(255,255,255,0.15);

  color: #111827;
  cursor: pointer;

  transition: 0.2s;
}

/* 区切り線（横並びの境界） */
.btn-view {
  border-right: 1px solid #cbd5e1;
}

.btn-filter {
  border-right: 1px solid #cbd5e1;
}

.btn-create {
  border-right: none;
}

/* hover */
.btn-view:hover,
.btn-filter:hover,
.btn-create:hover {
  background: rgba(255,255,255,0.3);
}

/* active */
.btn-view.active {
  background: rgba(59,130,246,0.15);
  color: #2563eb;
  font-weight: 600;
}

</style>