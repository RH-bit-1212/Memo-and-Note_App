<template>
  <div
    class="modal-overlay"
  >
    <div class="modal-content">
      <h2>新規メモ</h2>

      <!-- タイトル -->
      <input
        v-model="localForm.title"
        placeholder="タイトル"
        required
      />

      <!-- 内容 -->
      <textarea
        v-model="localForm.content"
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

          <select v-model.number="localForm.important">
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
            v-for="tag in localForm.tags"
            :key="tag.id"
            class="tag-item"
            :style="{ backgroundColor: tag.color }"
          >
            {{ tag.name }}

            <button
              type="button"
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
            v-for="(file, index) in localForm.file_paths"
            :key="index"
            class="tag-item"
          >
            {{ file }}

            <button
              type="button"
              class="mini-del"
              @click="removeFile(index)"
            >
              ×
            </button>
          </span>
        </div>

        <!-- 関連URL -->
        <div class="form-row">
          <label>関連URL</label>

          <div class="inline-input">
            <input
              v-model="urlInput"
              placeholder="https://example.com"
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
            v-for="(url, index) in localForm.urls"
            :key="index"
            class="tag-item"
          >
            {{ url }}

            <button
              type="button"
              class="mini-del"
              @click="removeUrl(index)"
            >
              ×
            </button>
          </span>
        </div>

      </div>

      <!-- 操作ボタン -->
      <div class="modal-buttons">
        <button
          type="button"
          @click="createMemo"
          class="btn-save"
        >
          保存
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
      :selected-category-id="localForm.category_id"
      @select="onCategorySelected"
      @close="showCategoryModal = false"
    />

    <!-- タグ選択モーダル -->
    <TagSelectModal
      v-if="showTagModal"
      :tags="tags"
      :selected-tags="localForm.tags"
      @select="onTagsSelected"
      @close="showTagModal = false"
    />
  </div>
</template>

<script>
import { reactive, ref, computed } from "vue";

import CategorySelectModal from "./CategorySelectModal.vue";
import TagSelectModal from "./TagSelectModal.vue";

export default {
  name: "MemoCreateModal",

  components: {
    CategorySelectModal,
    TagSelectModal
  },

  props: {
    tags: {
      type: Array,
      required: true
    },
    categories: {
      type: Array,
      required: true
    }
  },

  emits: ["create", "close"],

  setup(props, { emit }) {
    const localForm = reactive({
      title: "",
      content: "",
      category_id: null,
      important: 1,
      tags: [],
      file_paths: [],
      urls: []
    });

    const fileInput = ref("");
    const urlInput = ref("");

    const showCategoryModal = ref(false);
    const showTagModal = ref(false);

    const selectedCategoryName = computed(() => {
      const category = props.categories.find(
        c => c.id === localForm.category_id
      );

      return category
        ? category.name
        : "カテゴリを選択";
    });

    const selectedTagSummary = computed(() => {
      if (!localForm.tags.length) {
        return "タグを選択";
      }

      if (localForm.tags.length <= 3) {
        return localForm.tags
          .map(tag => tag.name)
          .join(", ");
      }

      return `${localForm.tags.length}件選択中`;
    });

    const onCategorySelected = (categoryId) => {
      localForm.category_id = categoryId;
    };

    const onTagsSelected = (selectedTags) => {
      localForm.tags = selectedTags;
    };

    const addFile = () => {
      const file = fileInput.value.trim();

      if (
        file &&
        !localForm.file_paths.includes(file)
      ) {
        localForm.file_paths.push(file);
      }

      fileInput.value = "";
    };

    const removeFile = (index) => {
      localForm.file_paths.splice(index, 1);
    };

    const addUrl = () => {
      const url = urlInput.value.trim();

      if (
        url &&
        !localForm.urls.includes(url)
      ) {
        localForm.urls.push(url);
      }

      urlInput.value = "";
    };

    const removeUrl = (index) => {
      localForm.urls.splice(index, 1);
    };

    const removeTag = (tagId) => {
      localForm.tags =
        localForm.tags.filter(
          tag => tag.id !== tagId
        );
    };

    const createMemo = () => {
      if (!localForm.title.trim()) {
        alert("タイトルは必須です");
        return;
      }

      const payload = {
        title: localForm.title,
        content: localForm.content,

        category_id:
          localForm.category_id || null,

        important:
          localForm.important,

        file_paths:
          [...localForm.file_paths],

        urls:
          [...localForm.urls],

        tag_ids:
          localForm.tags.map(
            tag => tag.id
          )
      };

      emit("create", payload);

      localForm.title = "";
      localForm.content = "";
      localForm.category_id = null;
      localForm.important = 1;
      localForm.tags = [];
      localForm.file_paths = [];
      localForm.urls = [];

      fileInput.value = "";
      urlInput.value = "";
    };

    return {
      localForm,

      fileInput,
      urlInput,

      showCategoryModal,
      showTagModal,

      selectedCategoryName,
      selectedTagSummary,

      onCategorySelected,
      onTagsSelected,

      addFile,
      removeFile,

      addUrl,
      removeUrl,

      removeTag,

      createMemo
    };
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

.modal-content {
  background: #fff;
  width: 80vw;
  height: 80vh;
  padding: 1rem;
  border-radius: 0.5rem;
  display: flex;
  flex-direction: column;
}

.modal-body {
  flex: 1 1 auto;
  overflow-y: auto;
  padding-right: 0.5rem;
  min-height: 300px;
}

/* =========================
   入力欄
========================= */

input,
select,
textarea {
  box-sizing: border-box;
}

.modal-content > input {
  width: 97%;
  margin-bottom: 0.75rem;

  padding: 0.5rem;

  border: 1px solid #d1d5db;
  border-radius: 0.25rem;
}

textarea {
  width: 97%;
  height: 350px;

  margin-bottom: 1rem;

  padding: 0.5rem;

  border: 1px solid #d1d5db;
  border-radius: 0.25rem;

  resize: vertical;
  overflow-y: auto;
}

/* =========================
   行レイアウト
========================= */

.form-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.form-row label {
  width: 50px;
  min-width: 100px;
  font-weight: 600;
  margin: 0;
}

.form-row select,
.form-row .select-box {
  flex: 1;
  width: auto;
  margin: 0;
}

.select-box {
  background: white;
  cursor: pointer;
}

/* =========================
   ファイルパス・URL
========================= */

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

  padding: 0.5rem;

  border: 1px solid #d1d5db;
  border-radius: 0.25rem;
}

.inline-input button {
  width: 80px;
  flex-shrink: 0;
}

/* =========================
   タグ一覧
========================= */

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

.mini-del:hover {
  color: #b91c1c;
}

/* =========================
   ボタン
========================= */

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

.btn-save:hover {
  background-color: #2563eb;
}

.btn-close {
  padding: 0.5rem 1rem;

  background-color: #6b7280;
  color: white;

  border: none;
  border-radius: 0.375rem;

  cursor: pointer;
}

.btn-close:hover {
  background-color: #4b5563;
}

/* =========================
   スマホ対応
========================= */

@media (max-width: 550px) {

  .modal-content {
    width: 95vw;
    height: 90vh;
  }

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

  .modal-content > input,
  textarea {
    width: 100%;
  }
}
</style>