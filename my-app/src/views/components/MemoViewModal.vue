<template>
  <div
    v-if="memo"
    class="modal-overlay"
  >
    <div class="modal-content">

      <div class="modal-body">

        <!-- タイトル -->
        <div class="view-section">
          <div class="section-value title-value">
            {{ memo.title }}
          </div>
        </div>

        <!-- 内容 -->
        <div class="view-section">
          <div class="content-box">
            {{ memo.content || "内容なし" }}
          </div>
        </div>

        <!-- メタ情報 -->
        <div class="meta-row">

            <div class="meta-item">
                <span class="meta-label">カテゴリ：</span>
                <span>{{ categoryName }}</span>
            </div>

            <div class="meta-item">
                <span class="meta-label">重要度：</span>

                <span
                    class="importance-badge"
                    :class="'imp-' + memo.important"
                >
                    {{ importanceLabel(memo.important) }}
                </span>
            </div>

            <div class="meta-item">
                <span class="meta-label">作成日：</span>
                <span>{{ formatDate(memo.created_at) }}</span>
            </div>

        </div>

        <!-- タグ -->
        <div class="view-section">
          <div class="section-label">タグ</div>

          <div class="tag-list">
            <span
              v-for="tag in (memo.tags || [])"
              :key="tag.id"
              class="tag-item"
            >
              {{ tag.name }}
            </span>

            <span
              v-if="!memo.tags || memo.tags.length === 0"
            >
              タグなし
            </span>
          </div>
        </div>

        <!-- 添付ファイル -->
        <div class="view-section">
          <div class="section-label">添付ファイル</div>

          <div
            v-if="memo.file_paths?.length"
            class="link-list"
          >
            <div
              v-for="(file, index) in memo.file_paths"
              :key="index"
              class="link-item"
            >
              {{ file }}
            </div>
          </div>

          <div v-else>
            添付ファイルなし
          </div>
        </div>

        <!-- URL -->
        <div class="view-section">
          <div class="section-label">関連URL</div>

          <div
            v-if="memo.urls?.length"
            class="link-list"
          >
            <a
              v-for="(url, index) in memo.urls"
              :key="index"
              :href="url"
              target="_blank"
              rel="noopener noreferrer"
              class="url-link"
            >
              {{ url }}
            </a>
          </div>

          <div v-else>
            URLなし
          </div>
        </div>

      </div>

      <div class="modal-buttons">
        <button
          class="btn-close"
          @click="$emit('close')"
        >
          閉じる
        </button>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "MemoViewModal",

  props: {
    memo: {
      type: Object,
      required: true
    },

    tags: {
      type: Array,
      default: () => []
    },

    categories: {
      type: Array,
      default: () => []
    }
  },

  computed: {
    categoryName() {
      const category = this.categories.find(
        c => c.id === this.memo.category_id
      );

      return category
        ? category.name
        : "未分類";
    }
  },

  methods: {
    importanceLabel(i) {
      return i === 3
        ? "高"
        : i === 2
          ? "中"
          : "低";
    },

    formatDate(dt) {
      if (!dt) return "";

      return new Date(dt).toLocaleString("ja-JP");
    }
  }
};
</script>

<style scoped>

.modal-overlay {
  position: fixed;
  inset: 0;

  background: rgba(0,0,0,0.5);

  display: flex;
  justify-content: center;
  align-items: center;

  z-index: 3000;
}

.modal-content {
  width: 80vw;
  height: 80vh;

  background: rgba(255,255,255,0.75);
  backdrop-filter: blur(12px);

  border-radius: 10px;

  padding: 1rem;

  display: flex;
  flex-direction: column;
}

.modal-body {
  flex: 1;

  overflow-y: auto;

  padding-right: 8px;
}

.view-section {
  margin-bottom: 1rem;
  padding: 0.75rem;

  border: 1px solid rgba(255, 255, 255, 0.25);
  background: rgba(255, 255, 255, 0.35);
  backdrop-filter: blur(6px);

  border-radius: 8px;

  text-align: left; /* 左揃え */
}

/* 見出し */
.section-label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #111827;
}

.section-value {
  color: #111827;
}

.title-value {
  font-size: 1.3rem;
  font-weight: 600;
}

.content-box {
  white-space: pre-wrap;

  text-align: left;

  min-height: 200px;

  border: 1px solid #d1d5db;

  border-radius: 6px;

  background: rgba(255,255,255,0.6);

  padding: 0.8rem;
}

/* タグ */
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

/* タグ要素 */
.tag-item {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;

  background: rgba(209, 213, 219, 0.7);
  color: #111;

  font-size: 0.85rem;
}

/* ファイル・URL共通リスト */
.link-list {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

/* ファイル表示 */
.link-item {
  padding: 0.25rem 0.5rem;
  background: rgba(243, 244, 246, 0.6);
  border-radius: 6px;
}

/* URLリンク */
.url-link {
  color: #2563eb;
  text-decoration: none;

  padding: 0.25rem 0.5rem;
  background: rgba(219, 234, 254, 0.5);
  border-radius: 6px;

  display: inline-block;
}

.url-link:hover {
  text-decoration: underline;
}

.importance-badge {
  display: inline-block;

  padding: 0.3rem 0.8rem;

  border-radius: 999px;

  font-weight: 600;
}

.imp-1 {
  background: rgba(208,240,255,0.8);
}

.imp-2 {
  background: rgba(255,249,196,0.8);
}

.imp-3 {
  background: rgba(255,214,214,0.8);
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;

  margin-top: 1rem;
}

.btn-close {
  padding: 0.6rem 1.2rem;

  border: none;

  border-radius: 6px;

  background: #6b7280;

  color: white;

  cursor: pointer;
}

.btn-close:hover {
  background: #4b5563;
}

.meta-row {
  display: flex;
  flex-wrap: wrap;

  gap: 1.5rem;

  margin-bottom: 1rem;

  padding: 0.75rem;

  border: 1px solid rgb(255, 255, 255);

  border-radius: 6px;

  background: rgba(255,255,255,1);
}

.meta-item {
  display: flex;
  align-items: center;

  gap: 0.5rem;
}

.meta-label {
  font-weight: 600;
  color: #000000;
}
</style>