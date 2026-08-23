<template>
  <div class="memo-container-wrapper">

    <div class="memo-table-wrapper">
      <div class="memo-table-scroll">

        <table class="memo-table">
          <thead>
            <tr>
              <th class="col-title">タイトル</th>
              <th class="col-category">カテゴリ</th>
              <th class="col-tags">タグ</th>
              <th class="col-important">重要度</th>
              <th class="col-date">作成日</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="memo in memos"
              :key="memo.id"
              :class="'imp-row-' + memo.important"
              @click="$emit('open-detail', memo.id)"
            >
              <td class="title-cell">
                {{ memo.title }}
              </td>

              <td>
                {{ memo.categoryName || "未分類" }}
              </td>

              <td>
                <div class="memo-tags">
                  <span
                    v-for="tag in (memo.tags || [])"
                    :key="tag.id"
                    class="tag"
                    :style="{ backgroundColor: tag.color || '#999' }"
                  >
                    {{ tag.name }}
                  </span>
                </div>
              </td>

              <td>
                <span
                  class="importance-badge"
                  :class="'imp-' + memo.important"
                >
                  {{ importanceLabel(memo.important) }}
                </span>
              </td>

              <td>
                {{ formatDate(memo.created_at) }}
              </td>
            </tr>

            <tr v-if="memos.length === 0">
              <td colspan="5" class="empty-row">
                メモがありません
              </td>
            </tr>
          </tbody>

        </table>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MemoList",

  props: {
    memos: {
      type: Array,
      default: () => []
    }
  },

  emits: ["open-detail"],

  methods: {
    importanceLabel(i) {
      return i === 3 ? "高" : i === 2 ? "中" : "低";
    },

    formatDate(dt) {
      return dt
        ? String(dt).substring(0, 10)
        : "";
    }
  }
};
</script>

<style scoped>

.tag-manager-container {
  display: flex;
  flex-direction: column;
  align-items: center;

  padding: 1rem;

  overflow: hidden;

  background: rgba(236, 236, 236, 0.99); /* 半透明白 */
  border-radius: 12px;
  backdrop-filter: blur(4px);

  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
}

/* =======================
   テーブル全体
======================= */

.memo-table-wrapper {
  width: 95%;
  margin: 0 auto;

  background: rgba(255,255,255,0.35);
  backdrop-filter: blur(6px);

  border-radius: 12px;
  padding: 1rem;

  box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}

/* 横・縦スクロール */

.memo-table-scroll {
  max-height: 75vh; /* ここでテーブル全体の高さ調整 */

  overflow-x: auto;
  overflow-y: auto;
}

/* =======================
   テーブル
======================= */

.memo-table {
  width: 100%;
  min-width: 1200px;
  table-layout: fixed; /* 列幅を固定 */
}

.col-title {
  width: 330px;
}

.col-category {
  width: 90px;
}

.col-tags {
  width: 250px;
}

.col-important {
  width: 50px;
}

.col-date {
  width: 90px;
}

/* ヘッダー固定 */

.memo-table thead th {
  position: sticky;
  top: 0;
  z-index: 10;

  background: rgba(40, 40, 40, 0.9);
  color: white;

  padding: 12px;
  text-align: center;
}

.memo-table tbody tr {
  height: 70px;
}

.memo-table td {
  vertical-align: middle;
}

.memo-table tbody tr:hover {
  background-color: rgba(255,255,255,0.8);
}

/* =======================
   重要度色
======================= */

.imp-row-1 {
  background-color: rgba(208,240,255,0.55);
}

.imp-row-2 {
  background-color: rgba(255,249,196,0.55);
}

.imp-row-3 {
  background-color: rgba(255,214,214,0.55);
}

/* =======================
   タイトル
======================= */

.title-cell {
  font-weight: 600;
  min-width: 250px;
}

/* =======================
   タグ
======================= */

.memo-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
}

.tag {
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  white-space: nowrap;
}

/* =======================
   重要度
======================= */

.importance-badge {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: bold;
}

.imp-1 {
  background: rgba(0,120,255,0.15);
}

.imp-2 {
  background: rgba(255,180,0,0.18);
}

.imp-3 {
  background: rgba(255,0,0,0.15);
}

/* =======================
   空データ
======================= */

.empty-row {
  text-align: center;
  padding: 2rem;
  color: #666;
}

/* =======================
   スマホ
======================= */

@media (max-width: 600px) {

  .memo-table-wrapper {
    width: 95%;
    padding: 0.5rem;
  }

  .memo-table {
    min-width: 800px;
  }

}

</style>