<template>
  <div
    v-if="localMemo"
    class="modal-overlay"
  >
    <div class="modal-content">
      <h2>メモ詳細</h2>

      <!-- タイトル -->
      <input
        v-model="localMemo.title"
        placeholder="タイトル"
      />

      <!-- 内容 -->
      <textarea
        v-model="localMemo.content"
        placeholder="内容"
      ></textarea>

      <div class="modal-body">

        <!-- カテゴリ -->
        <div class="form-row">
          <label>カテゴリ</label>

          <input
            readonly
            class="select-box"
            :value="selectedCategoryName"
            @click="showCategoryModal = true"
          />
        </div>

        <!-- 重要度 -->
        <div class="form-row">
          <label>重要度</label>

          <select v-model.number="localMemo.important">
            <option :value="1">低</option>
            <option :value="2">中</option>
            <option :value="3">高</option>
          </select>
        </div>

        <!-- タグ -->
        <div class="form-row">
          <label>タグ</label>

          <input
            readonly
            class="select-box"
            :value="selectedTagSummary"
            @click="showTagModal = true"
          />
        </div>

        <div class="tag-list">
          <span
            v-for="tag in localMemo.tags"
            :key="tag.id"
            class="tag-item"
            :style="{ backgroundColor: tag.color }"
          >
            {{ tag.name }}

            <button
              class="mini-del"
              @click="removeTag(tag.id)"
            >
              ×
            </button>
          </span>
        </div>

        <!-- ファイルパス -->
        <div class="form-row">
          <label>ファイルパス</label>

          <div class="inline-input">
            <input
              v-model="fileInput"
              placeholder="ファイルパスを入力"
            />

            <button
              type="button"
              @click="addFile"
            >
              追加
            </button>
          </div>
        </div>

        <div class="tag-list">
          <span
            v-for="(file, index) in localMemo.file_paths"
            :key="index"
            class="tag-item"
          >
            {{ file }}

            <button
              class="mini-del"
              @click="removeFile(index)"
            >
              ×
            </button>
          </span>
        </div>

        <!-- URL -->
        <div class="form-row">
          <label>関連URL</label>

          <div class="inline-input">
            <input
              v-model="urlInput"
              placeholder="URLを入力"
            />

            <button
              type="button"
              @click="addUrl"
            >
              追加
            </button>
          </div>
        </div>

        <div class="tag-list">
          <span
            v-for="(url, index) in localMemo.urls"
            :key="index"
            class="tag-item"
          >
            {{ url }}

            <button
              class="mini-del"
              @click="removeUrl(index)"
            >
              ×
            </button>
          </span>
        </div>

      </div>

      <!-- ボタン -->
      <div class="modal-buttons">
        <button
          type="button"
          @click="save"
          class="btn-save"
        >
          保存
        </button>

        <button
          type="button"
          @click="deleteMemo"
          class="btn-delete"
        >
          削除
        </button>

        <button
          type="button"
          @click="$emit('close')"
          class="btn-close"
        >
          閉じる
        </button>
      </div>
    </div>

    <!-- カテゴリ選択モーダル -->
    <CategorySelectModal
      v-if="showCategoryModal"
      :categories="categories"
      :selected-category-id="localMemo.category_id"
      @select="onCategorySelected"
      @close="showCategoryModal = false"
    />

    <!-- タグ選択モーダル -->
    <TagSelectModal
      v-if="showTagModal"
      :tags="tags"
      :selected-tags="localMemo.tags"
      @select="onTagsSelected"
      @close="showTagModal = false"
    />
  </div>
</template>

<script>
import CategorySelectModal from "./CategorySelectModal.vue";
import TagSelectModal from "./TagSelectModal.vue";

export default {
  name: "MemoDetailModal",

  components: {
    CategorySelectModal,
    TagSelectModal
  },

  props: {
    memo: {
      type: Object,
      required: true
    },
    tags: {
      type: Array,
      required: true
    },
    categories: {
      type: Array,
      required: true
    }
  },

  data() {
    return {
      localMemo: null,

      urlInput: "",
      fileInput: "",

      showCategoryModal: false,
      showTagModal: false
    };
  },

  computed: {
    selectedCategoryName() {
      if (!this.localMemo) return "";

      const category = this.categories.find(
        c => c.id === this.localMemo.category_id
      );

      return category ? category.name : "カテゴリを選択";
    },

    selectedTagSummary() {
      if (!this.localMemo?.tags?.length) {
        return "タグを選択";
      }

      if (this.localMemo.tags.length <= 3) {
        return this.localMemo.tags
          .map(tag => tag.name)
          .join(", ");
      }

      return `${this.localMemo.tags.length}件選択中`;
    }
  },

  watch: {
    memo: {
      immediate: true,
      handler(newVal) {
        this.localMemo = newVal
          ? {
              ...newVal,

              urls: [...(newVal.urls || [])],

              file_paths: [...(newVal.file_paths || [])],

              tags: [...(newVal.tags || [])],

              important: newVal.important ?? 1,

              category_id: newVal.category_id ?? null
            }
          : null;
      }
    }
  },

  methods: {
    onCategorySelected(categoryId) {
      this.localMemo.category_id = categoryId;
    },

    onTagsSelected(selectedTags) {
      this.localMemo.tags = selectedTags;
    },

    removeTag(tagId) {
      this.localMemo.tags =
        this.localMemo.tags.filter(
          tag => tag.id !== tagId
        );
    },

    addUrl() {
      const url = this.urlInput.trim();

      if (
        url &&
        !this.localMemo.urls.includes(url)
      ) {
        this.localMemo.urls.push(url);
      }

      this.urlInput = "";
    },

    removeUrl(index) {
      this.localMemo.urls.splice(index, 1);
    },

    addFile() {
      const file = this.fileInput.trim();

      if (
        file &&
        !this.localMemo.file_paths.includes(file)
      ) {
        this.localMemo.file_paths.push(file);
      }

      this.fileInput = "";
    },

    removeFile(index) {
      this.localMemo.file_paths.splice(index, 1);
    },

    save() {
      if (!this.localMemo.title?.trim()) {
        alert("タイトルは必須です");
        return;
      }

      const payload = {
        title: this.localMemo.title,
        content: this.localMemo.content,

        category_id:
          this.localMemo.category_id || null,

        important:
          this.localMemo.important,

        file_paths:
          this.localMemo.file_paths,

        urls:
          this.localMemo.urls,

        tag_ids:
          this.localMemo.tags.map(
            tag => tag.id
          )
      };

      this.$emit(
        "update",
        this.localMemo.id,
        payload
      );
    },

    deleteMemo() {
      if (
        !confirm(
          "本当にこのメモを削除しますか？"
        )
      ) {
        return;
      }

      this.$emit(
        "delete",
        this.localMemo.id
      );

      this.$emit("close");
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
}

/* ★ モーダル全体：画面の 80% */
.modal-content {
  background: #fff;
  width: 80vw;
  height: 80vh;
  padding: 1rem;
  border-radius: 0.5rem;
  display: flex;
  flex-direction: column;
}

/* ★ メモ内容のスクロールエリア */
.modal-body {
  flex: 1 1 auto;
  overflow-y: auto;
  padding-right: 0.5rem;
  min-height: 300px;
}

input, select {
  width: 95%;
  margin-top: 0.25rem;
  margin-bottom: 0.5rem;
  padding: 0.25rem 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.25rem;
}

textarea {
  width: 95%;
  height: 200px;            /* 初期高さを確保（好みに応じて変更可） */
  margin-top: 0.25rem;
  margin-bottom: 0.5rem;
  padding: 0.25rem 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.25rem;

  resize: vertical;         /* 高さのみ変更可能 */
  overflow-y: auto;         /* 必要な時に縦スクロール */
}

.tag-input {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.tag-list {
  margin-bottom: 1rem;
}

.tag-item {
  display: inline-flex;
  align-items: center;
  background-color: #d1d5db;
  color: #111;
  padding: 0.25rem 0.5rem;
  margin: 0.125rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
}

.mini-del {
  margin-left: 0.4rem;
  background: transparent;
  border: none;
  color: #374151;
  cursor: pointer;
  font-weight: bold;
  line-height: 1;
}
.mini-del:hover { color: #b91c1c; }

.modal-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.btn-save {
  padding: 0.5rem 1rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
}
.btn-save:hover { background-color: #2563eb; }

.btn-delete {
  background-color: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
}
.btn-delete:hover { background-color: #dc2626; }

.btn-close {
  padding: 0.5rem 1rem;
  background-color: #6b7280;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
}
.btn-close:hover { background-color: #4b5563; }

/* ===== 項目行 ===== */

.form-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.form-row label {
  width: 120px;
  min-width: 120px;
  font-weight: 600;
  margin: 0;
}

/* カテゴリ・タグ・重要度 */

.form-row select,
.form-row .select-box {
  flex: 1;
  width: auto;
  margin: 0;
}

/* クリック用入力欄 */

.select-box {
  background: white;
  cursor: pointer;
}

/* ===== ファイルパス・URL ===== */

.inline-input {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.inline-input input {
  flex: 1;
  width: auto;
  margin: 0;
}

.inline-input button {
  width: 80px;
  flex-shrink: 0;
}

.modal-content > input {
  width: 95%;
  margin-bottom: 0.75rem;
}

textarea {
  width: 95%;
  height: 300px;

  margin-bottom: 1rem;

  padding: 0.5rem;

  border: 1px solid #d1d5db;
  border-radius: 0.25rem;

  resize: vertical;
  overflow-y: auto;
}


@media (max-width: 768px) {

  .form-row {
    flex-direction: column;
    align-items: stretch;
  }

  .form-row label {
    width: auto;
    min-width: auto;
  }

  .inline-input {
    width: 100%;
  }
}

</style>
