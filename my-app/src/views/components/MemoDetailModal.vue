<template>
  <div v-if="localMemo" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h2>メモ詳細</h2>

      <!-- タイトル -->
      <input v-model="localMemo.title" placeholder="タイトル" />

      <!-- 内容 -->
      <textarea v-model="localMemo.content" placeholder="内容"></textarea>

      <!-- カテゴリ選択 -->
      <label>カテゴリ</label>
      <select v-model="localMemo.category_id">
        <option v-for="c in categories" :key="c.id" :value="c.id">
          {{ c.name }}
        </option>
      </select>

      <!-- 重要度 -->
      <label>重要度</label>
      <select v-model.number="localMemo.important">
        <option :value="1">低</option>
        <option :value="2">中</option>
        <option :value="3">高</option>
      </select>

      <!-- タグ -->
      <label>タグ</label>
      <div class="tag-input">
        <select v-model="tagInput">
          <option :value="null">選択してください</option>
          <option v-for="t in tags" :key="t.id" :value="t.id">
            {{ t.name }}
          </option>
        </select>
        <button type="button" @click="addTag">追加</button>
      </div>

      <div class="tag-list">
        <span v-for="t in localMemo.tags" :key="t.id" class="tag-item">
          {{ t.name }}
          <button class="mini-del" @click="removeTag(t.id)">×</button>
        </span>
      </div>

      <!-- ファイル -->
      <label>添付ファイルパス</label>
      <div class="tag-input">
        <input v-model="fileInput" placeholder="ファイルパスを入力" />
        <button type="button" @click="addFile">追加</button>
      </div>

      <div class="tag-list">
        <span v-for="(f,i) in localMemo.file_paths" :key="i" class="tag-item">
          {{ f }}
          <button class="mini-del" @click="removeFile(i)">×</button>
        </span>
      </div>

      <!-- URL -->
      <label>関連URL</label>
      <div class="tag-input">
        <input v-model="urlInput" placeholder="URL を入力" />
        <button type="button" @click="addUrl">追加</button>
      </div>

      <div class="tag-list">
        <span v-for="(u,i) in localMemo.urls" :key="i" class="tag-item">
          {{ u }}
          <button class="mini-del" @click="removeUrl(i)">×</button>
        </span>
      </div>

      <!-- 操作ボタン -->
      <div class="modal-buttons">
        <button type="button" @click="save" class="btn-save">保存</button>
        <button type="button" @click="deleteMemo" class="btn-delete">削除</button>
        <button type="button" @click="$emit('close')" class="btn-close">閉じる</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MemoDetailModal",

  props: {
    memo: { type: Object, required: true },
    tags: { type: Array, required: true },        // [{id, name}]
    categories: { type: Array, required: true }   // [{id, name}]
  },

  data() {
    return {
      localMemo: null,
      tagInput: null,
      urlInput: "",
      fileInput: ""
    };
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
              tags: [...(newVal.tags || [])],  // ← tag_ids → tags
              important: newVal.important ?? 1,
              category_id: newVal.category_id ?? null
            }
          : null;
      }
    }
  },

  methods: {
    addTag() {
      if (!this.tagInput) return;

      const tagObj = this.tags.find(t => t.id === this.tagInput);
      if (tagObj && !this.localMemo.tags.some(t => t.id === tagObj.id)) {
        this.localMemo.tags.push(tagObj);
      }
      this.tagInput = null;
    },
    removeTag(tagId) {
      this.localMemo.tags = this.localMemo.tags.filter(t => t.id !== tagId);
    },

    addUrl() {
      const url = this.urlInput.trim();
      if (url && !this.localMemo.urls.includes(url)) {
        this.localMemo.urls.push(url);
      }
      this.urlInput = "";
    },
    removeUrl(index) {
      this.localMemo.urls.splice(index, 1);
    },

    addFile() {
      const file = this.fileInput.trim();
      if (file && !this.localMemo.file_paths.includes(file)) {
        this.localMemo.file_paths.push(file);
      }
      this.fileInput = "";
    },
    removeFile(index) {
      this.localMemo.file_paths.splice(index, 1);
    },

save() {
  if (!this.localMemo.title) {
    alert("タイトルは必須です");
    return;
  }

  // tags 配列 → tag_ids 配列に変換
  const payload = {
    title: this.localMemo.title,
    content: this.localMemo.content,
    category_id: this.localMemo.category_id || null,
    important: this.localMemo.important,
    file_paths: this.localMemo.file_paths,
    urls: this.localMemo.urls,
    tag_ids: this.localMemo.tags.map(t => t.id)   // ← ここ重要
  };

  this.$emit("update", this.localMemo.id, payload);
}
,

    deleteMemo() {
      if (!confirm("本当にこのメモを削除しますか？")) return;
      this.$emit("delete", this.localMemo.id);
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



</style>
