<template>
  <!-- モーダル背景 -->
  <div class="modal-overlay" @click.self="$emit('close')">
    <!-- モーダル本体 -->
    <div class="modal">
      <h2 class="modal-title">フィルター</h2>

      <!-- キーワード検索 -->
      <div class="filter-row">
        <label>キーワード：</label>
        <input
          type="text"
          v-model="localKeyword"
          placeholder="タイトル / 内容検索"
        />
      </div>

      <!-- タグフィルター -->
      <div class="filter-row">
        <label>タグ：</label>
        <select v-model="localTagId">
          <option value="">全て</option>
          <option v-for="t in tags" :key="t.id" :value="t.id">
            {{ t.name }}
          </option>
        </select>
      </div>

      <!-- カテゴリフィルター -->
      <div class="filter-row">
        <label>カテゴリ：</label>
        <select v-model="localCategoryId">
          <option value="">全て</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">
            {{ c.name }}
          </option>
        </select>
      </div>

      <!-- 重要度 -->
      <div class="filter-row">
        <label>重要度：</label>
        <select v-model="localImportant">
          <option value="">全て</option>
          <option value="1">低</option>
          <option value="2">中</option>
          <option value="3">高</option>
        </select>
      </div>

      <!-- 日時ソート -->
      <div class="filter-row">
        <label>日時：</label>
        <select v-model="localSort">
          <option value="created_desc">新しい順</option>
          <option value="created_asc">古い順</option>
          <option value="important_desc">重要度 高→低</option>
          <option value="important_asc">重要度 低→高</option>
        </select>
      </div>

      <!-- ボタン -->
      <div class="modal-buttons">
        <button class="btn-clear" @click="clearFilter">クリア</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MemoFilter",

  props: {
    modelValue: { type: Object, default: () => ({}) },
    tags: { type: Array, required: true },
    categories: { type: Array, required: true },
  },

  data() {
    return {
      localKeyword: this.modelValue.keyword || "",
      localTagId: this.modelValue.tag_id || "",
      localCategoryId: this.modelValue.category_id || "",
      localImportant: this.modelValue.important || "",
      localSort: this.modelValue.sort || "created_desc",
    };
  },

  watch: {
    localKeyword: "emitFilter",
    localTagId: "emitFilter",
    localCategoryId: "emitFilter",
    localImportant: "emitFilter",
    localSort: "emitFilter",

    // 外部から更新された場合もローカルに反映
    modelValue: {
      handler(val) {
        this.localKeyword = val.keyword || "";
        this.localTagId = val.tag_id || "";
        this.localCategoryId = val.category_id || "";
        this.localImportant = val.important || "";
        this.localSort = val.sort || "created_desc";
      },
      deep: true,
    },
  },

  methods: {
    emitFilter() {
      this.$emit("update:modelValue", {
        keyword: this.localKeyword.trim(),
        tag_id: this.localTagId,
        category_id: this.localCategoryId,
        important: this.localImportant,
        sort: this.localSort,
      });
    },

    clearFilter() {
      this.localKeyword = "";
      this.localTagId = "";
      this.localCategoryId = "";
      this.localImportant = "";
      this.localSort = "created_desc";
      this.emitFilter();
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal {
  background: white;
  padding: 1.5rem;
  width: 350px;
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(0,0,0,0.2);
}

.modal-title {
  font-size: 1.25rem;
  margin-bottom: 1rem;
  font-weight: bold;
}

.filter-row {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}

input,
select {
  padding: 0.4rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.btn-clear {
  background: #e5e7eb;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
}
</style>
