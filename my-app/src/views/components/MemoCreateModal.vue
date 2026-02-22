<template>
  <!-- モーダル表示 -->
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h2>新規メモ</h2>

      <!-- タイトル -->
      <input v-model="localForm.title" placeholder="タイトル" required />

      <!-- 内容 -->
      <textarea v-model="localForm.content" placeholder="内容"></textarea>

      <!-- カテゴリ選択 -->
      <label>カテゴリ</label>
      <select v-model="localForm.category_id">
        <option disabled value="">選択してください</option>
        <option v-for="c in categories" :key="c.id" :value="c.id">
          {{ c.name }}
        </option>
      </select>

      <!-- 重要度 -->
      <label>重要度</label>
      <select v-model="localForm.important">
        <option :value="1">低</option>
        <option :value="2">中</option>
        <option :value="3">高</option>
      </select>

      <!-- タグ入力 -->
      <label>タグ</label>
      <div class="tag-input">
        <select v-model="tagInput">
          <option v-for="t in tags" :key="t.id" :value="t.id">
            {{ t.name }}
          </option>
        </select>
        <button type="button" @click="addTag">追加</button>
      </div>

      <!-- タグ一覧 -->
      <div class="tag-list">
        <span v-for="t in localForm.tags" :key="t.id" class="tag-item">
          {{ t.name }}
        </span>
      </div>

      <!-- 添付ファイル -->
      <label>添付ファイルパス</label>
      <div class="tag-input">
        <input v-model="fileInput" placeholder="ファイルパスを入力" />
        <button type="button" @click="addFile">追加</button>
      </div>
      <ul>
        <li v-for="(f, i) in localForm.file_paths" :key="i">{{ f }}</li>
      </ul>

      <!-- URL入力 -->
      <label>関連URL</label>
      <div class="tag-input">
        <input v-model="urlInput" placeholder="https://example.com" />
        <button type="button" @click="addUrl">追加</button>
      </div>
      <ul>
        <li v-for="(u, i) in localForm.urls" :key="i">{{ u }}</li>
      </ul>

      <!-- ボタン -->
      <div class="modal-buttons">
        <button type="button" @click="createMemo" class="btn-save">保存</button>
        <button type="button" @click="$emit('close')" class="btn-close">閉じる</button>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref } from "vue";

export default {
  name: "MemoCreateModal",

  props: {
    tags: { type: Array, required: true },         // [{id, name}]
    categories: { type: Array, required: true }    // [{id, name}]
  },

  emits: ["create", "close"],

  setup(props, { emit }) {
    const localForm = reactive({
      title: "",
      content: "",
      category_id: "",
      important: 1,
      tags: [],           // ← tag_ids ではなく tags 配列
      file_paths: [],
      urls: []
    });

    const tagInput = ref("");
    const fileInput = ref("");
    const urlInput = ref("");

    const addTag = () => {
      const tagId = tagInput.value;
      if (!tagId) return;

      const tagObj = props.tags.find(t => t.id === tagId);
      if (tagObj && !localForm.tags.some(t => t.id === tagObj.id)) {
        localForm.tags.push(tagObj);
      }
      tagInput.value = "";
    };

    const addFile = () => {
      const f = fileInput.value.trim();
      if (f) localForm.file_paths.push(f);
      fileInput.value = "";
    };

    const addUrl = () => {
      const u = urlInput.value.trim();
      if (u) localForm.urls.push(u);
      urlInput.value = "";
    };

const createMemo = () => {
  if (!localForm.title) {
    alert("タイトルは必須です");
    return;
  }

  // tags 配列 → tag_ids 配列に変換
  const payload = {
    title: localForm.title,
    content: localForm.content,
    category_id: localForm.category_id || null,
    important: localForm.important,
    file_paths: localForm.file_paths,
    urls: localForm.urls,
    tag_ids: localForm.tags.map(t => t.id)   // ← ここ
  };

  emit("create", payload);

  // リセット
  localForm.title = "";
  localForm.content = "";
  localForm.category_id = "";
  localForm.important = 1;
  localForm.tags = [];
  localForm.file_paths = [];
  localForm.urls = [];
};


    return {
      localForm,
      tagInput,
      addTag,
      fileInput,
      addFile,
      urlInput,
      addUrl,
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
  display: inline-block;
  background-color: #d1d5db;
  color: #111;
  padding: 0.25rem 0.5rem;
  margin: 0.125rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
}

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
</style>
