<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">

      <h2 class="modal-title">フィルター</h2>

      <!-- キーワード -->
      <div class="filter-row">
        <label>キーワード：</label>
        <input
          type="text"
          v-model="localKeyword"
          placeholder="タイトル / 内容検索"
        />
      </div>

      <!-- タグ（モーダル呼び出し） -->
      <div class="filter-row">
        <label>タグ：</label>
        <button class="select-btn" @click="showTagModal = true">
          {{ localTagIds.length ? `${localTagIds.length}件選択中` : "選択" }}
        </button>
      </div>

      <!-- カテゴリ（モーダル呼び出し） -->
      <div class="filter-row">
        <label>カテゴリ：</label>
        <button class="select-btn" @click="showCategoryModal = true">
          {{ selectedCategoryLabel }}
        </button>
      </div>

      <!-- 重要度 -->
      <div class="filter-row">
        <label>重要度：</label>
        <select v-model.number="localImportant">
          <option :value="null">全て</option>
          <option :value="1">低</option>
          <option :value="2">中</option>
          <option :value="3">高</option>
        </select>
      </div>

      <!-- ソート -->
      <div class="filter-row">
        <label>日時：</label>
        <select v-model="localSort">
          <option value="created_desc">新しい順</option>
          <option value="created_asc">古い順</option>
          <option value="important_desc">重要度 高→低</option>
          <option value="important_asc">重要度 低→高</option>
        </select>
      </div>

      <div class="modal-buttons">
        <button class="btn-clear" @click="clearFilter">クリア</button>
      </div>
    </div>

    <!-- =========================
         TAG MODAL
    ========================== -->
    <div v-if="showTagModal" class="inner-modal" @click.self="showTagModal = false">
      <div class="inner-box">
        <h3>タグ選択</h3>

        <div class="scroll-area">
          <label v-for="t in tags" :key="t.id" class="check-item">
            <input type="checkbox" :value="t.id" v-model="localTagIds" />
            {{ t.name }}
          </label>
        </div>

        <button @click="showTagModal = false">閉じる</button>
      </div>
    </div>

    <!-- =========================
         CATEGORY MODAL
    ========================== -->
    <div v-if="showCategoryModal" class="inner-modal" @click.self="showCategoryModal = false">
      <div class="inner-box">
        <h3>カテゴリ選択</h3>

        <div class="scroll-area">
          <label class="check-item">
            <input type="radio" :value="null" v-model="localCategoryId" />
            全て
          </label>

          <label
            v-for="c in categories"
            :key="c.id"
            class="check-item"
          >
            <input type="radio" :value="c.id" v-model="localCategoryId" />
            {{ c.name }}
          </label>
        </div>

        <button @click="showCategoryModal = false">閉じる</button>
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
      localTagIds: this.modelValue.tag_ids || [],
      localCategoryId: this.modelValue.category_id ?? null,
      localImportant: this.modelValue.important ?? null,
      localSort: this.modelValue.sort || "created_desc",

      showTagModal: false,
      showCategoryModal: false,
    };
  },

  computed: {
    selectedCategoryLabel() {
      if (!this.localCategoryId) return "全て";
      const c = this.categories.find(c => c.id === this.localCategoryId);
      return c ? c.name : "全て";
    },
  },

  watch: {
    localKeyword: "emitFilter",
    localTagIds: "emitFilter",
    localCategoryId: "emitFilter",
    localImportant: "emitFilter",
    localSort: "emitFilter",

    modelValue: {
      handler(val) {
        this.localKeyword = val.keyword || "";
        this.localTagIds = val.tag_ids || [];
        this.localCategoryId = val.category_id ?? null;
        this.localImportant = val.important ?? null;
        this.localSort = val.sort || "created_desc";
      },
      deep: true,
    },
  },

  methods: {
    emitFilter() {
      this.$emit("update:modelValue", {
        keyword: this.localKeyword.trim(),
        tag_ids: this.localTagIds,
        category_id: this.localCategoryId,
        important: this.localImportant,
        sort: this.localSort,
      });
    },

    clearFilter() {
      this.localKeyword = "";
      this.localTagIds = [];
      this.localCategoryId = null;
      this.localImportant = null;
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

/* ボタンは右寄せ維持（必要ならそのまま） */
.modal-buttons {
  display: flex;
  justify-content: flex-end;
}

.btn-clear {
  background: #e5e7eb;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
}

.inner-modal {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 3000;
}

.inner-box {
  background: white;
  width: 300px;
  padding: 1rem;
  border-radius: 8px;
  text-align: left;
}

.scroll-area {
  max-height: 250px;
  overflow-y: auto;
  margin: 10px 0;
  border: 1px solid #ddd;
  padding: 8px;
}

.check-item {
  display: block;
  margin: 4px 0;
}

.select-btn {
  padding: 6px 10px;
  border: 1px solid #ccc;
  background: #f5f5f5;
  border-radius: 4px;
}


</style>
