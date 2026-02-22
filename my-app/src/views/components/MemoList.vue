<template>
  <div class="memo-container-wrapper">
    <h2>メモ管理</h2>

    <div class="memo-container">
      <div
        v-for="memo in memos"
        :key="memo.id"
        class="memo-card"
        :class="'imp-card-' + memo.important"
        @click="$emit('open-detail', memo.id)"
      >
        <h3 class="memo-title">{{ memo.title }}</h3>

        <p class="memo-category">
          カテゴリ: {{ memo.categoryName || "未分類" }}
        </p>

        <div class="memo-tags">
          <span
            v-for="tag in memo.tags"
            :key="tag.name"
            class="tag"
            :style="{ backgroundColor: tag.color }"
          >
            {{ tag.name }}
          </span>
        </div>

        <p class="memo-importance">
          重要度:
          <span :class="'imp imp-' + memo.important">{{ importanceLabel(memo.important) }}</span>
        </p>

        <p class="memo-date">日付: {{ formatDate(memo.created_at) }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MemoList",
  props: { memos: Array },
  emits: ["open-detail"],
  methods: {
    importanceLabel(i) {
      return i === 3 ? "高" : i === 2 ? "中" : "低";
    },
    formatDate(dt) {
      return dt ? dt.toString().substring(0, 10) : "";
    },
  },
};
</script>

<style scoped>
.memo-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
  width: 80%;
  margin: 0 auto;
}

/* カードスタイル */
.memo-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 1rem;
  width: 300px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.1s;
}

.memo-card:hover {
  transform: scale(1.02);
}

/* 重要度ごとの背景色 */
.imp-card-1 { background-color: #d0f0ff; }  /* 低:薄い水色 */
.imp-card-2 { background-color: #fff9c4; }  /* 中:薄い黄色 */
.imp-card-3 { background-color: #ffd6d6; }  /* 高:薄い赤 */

.memo-title { font-size: 1.2rem; margin-bottom: 0.5rem; }
.memo-tags { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-bottom: 0.5rem; }

.tag {
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

@media (max-width: 600px) {
  .memo-card { width: 80%; }
  .memo-container { width: 100%; gap: 0.5rem; }
}
</style>
