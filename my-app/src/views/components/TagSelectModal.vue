<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <h3>タグ選択</h3>

      <input
        v-model="searchText"
        class="search-box"
        placeholder="タグ検索"
      />

      <div class="tag-list">
        <label
          v-for="tag in filteredTags"
          :key="tag.id"
          class="tag-row"
        >
          <input
            type="checkbox"
            :value="tag.id"
            v-model="selectedTagIds"
          />

          <span
            class="tag-color"
            :style="{ backgroundColor: tag.color }"
          ></span>

          <span>{{ tag.name }}</span>
        </label>
      </div>

      <div class="modal-buttons">
        <button class="btn-cancel" @click="$emit('close')">
          キャンセル
        </button>

        <button class="btn-select" @click="applySelection">
          適用
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TagSelectModal",

  props: {
    tags: {
      type: Array,
      required: true
    },
    selectedTags: {
      type: Array,
      default: () => []
    }
  },

  data() {
    return {
      searchText: "",
      selectedTagIds: this.selectedTags.map(tag => tag.id)
    };
  },

  computed: {
    filteredTags() {
      const keyword = this.searchText.toLowerCase();

      return this.tags.filter(tag =>
        tag.name.toLowerCase().includes(keyword)
      );
    }
  },

  methods: {
    applySelection() {
      const selectedTags = this.tags.filter(tag =>
        this.selectedTagIds.includes(tag.id)
      );

      this.$emit("select", selectedTags);
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
  width: 550px;
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

.tag-list {
  height: 350px;
  overflow-y: auto;
  border: 1px solid #d1d5db;
  border-radius: 8px;
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;

  padding: 0.75rem;
  cursor: pointer;

  border-bottom: 1px solid #e5e7eb;
}

.tag-row:hover {
  background: #f8fafc;
}

.tag-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: 1px solid #d1d5db;
  flex-shrink: 0;
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