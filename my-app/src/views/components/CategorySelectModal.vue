<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <h3>カテゴリ選択</h3>

      <input
        v-model="searchText"
        class="search-box"
        placeholder="カテゴリ検索"
      />

      <div class="category-list">
        <div
          v-for="category in filteredCategories"
          :key="category.id"
          class="category-row"
          :class="{ selected: tempCategoryId === category.id }"
          @click="tempCategoryId = category.id"
        >
          {{ category.name }}
        </div>
      </div>

      <div class="modal-buttons">
        <button class="btn-cancel" @click="$emit('close')">
          キャンセル
        </button>

        <button class="btn-select" @click="applySelection">
          選択
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CategorySelectModal",

  props: {
    categories: {
      type: Array,
      required: true
    },
    selectedCategoryId: {
      type: Number,
      default: null
    }
  },

  data() {
    return {
      searchText: "",
      tempCategoryId: this.selectedCategoryId
    };
  },

  computed: {
    filteredCategories() {
      const keyword = this.searchText.toLowerCase();

      return this.categories.filter(category =>
        category.name.toLowerCase().includes(keyword)
      );
    }
  },

  methods: {
    applySelection() {
      this.$emit("select", this.tempCategoryId);
      this.$emit("close");
    }
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 3000;
}

.modal {
  width: 500px;
  max-width: 90vw;
  background: white;
  border-radius: 12px;
  padding: 1rem;
}

h3 {
  margin-top: 0;
}

.search-box {
  width: 100%;
  box-sizing: border-box;
  padding: 0.6rem;
  margin-bottom: 1rem;
}

.category-list {
  height: 350px;
  overflow-y: auto;
  border: 1px solid #d1d5db;
  border-radius: 8px;
}

.category-row {
  padding: 0.75rem;
  cursor: pointer;
  border-bottom: 1px solid #e5e7eb;
}

.category-row:hover {
  background: #f3f4f6;
}

.category-row.selected {
  background: #dbeafe;
  font-weight: bold;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn-select {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}

.btn-cancel {
  background: #6b7280;
  color: white;
  border: none;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}
</style>