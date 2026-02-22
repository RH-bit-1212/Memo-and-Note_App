<template>
  <div class="category-manager-container">
    <h2>カテゴリ管理</h2>

    <!-- 新規追加フォーム -->
    <div class="form">
      <input v-model="newName" placeholder="カテゴリ名" />
      <input v-model="newDescription" placeholder="説明（任意）" />
      <button @click="createCategory">追加</button>
    </div>

    <!-- 一覧テーブル -->
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>名前</th>
            <th>説明</th>
            <th>作成日</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cat in localCategories" :key="cat.id">
            <td><input v-model="cat.name" /></td>
            <td><input v-model="cat.description" /></td>
            <td>{{ cat.created_at?.substring(0, 10) }}</td>
            <td>
              <button @click="updateCategory(cat)" class="update">更新</button>
              <button @click="deleteCategory(cat.id)" class="delete">削除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import {
  addCategory,
  updateCategory as apiUpdateCategory,
  deleteCategory as apiDeleteCategory,
} from "@/api/api";

export default {
  name: "CategoryManager",

  props: {
    modelValue: { type: Array, required: true },
  },

  emits: ["reload"],

  data() {
    return {
      newName: "",
      newDescription: "",
      localCategories: [], // ← props のコピー
    };
  },

  watch: {
    modelValue: {
      immediate: true,
      handler(newVal) {
        // ローカル編集用のコピーを作成
        this.localCategories = JSON.parse(JSON.stringify(newVal));
      },
    },
  },

  methods: {
    async createCategory() {
      const name = this.newName.trim();
      if (!name) return alert("名前は必須です");

      if (this.localCategories.some((c) => c.name === name)) {
        return alert("同じカテゴリ名が既に存在します");
      }

      if (name.length > 50) {
        return alert("カテゴリ名は50文字以内にしてください");
      }

      const now = new Date().toISOString();

      const payload = {
        name,
        description: this.newDescription.trim(),
        created_at: now,
        updated_at: now,
      };

      await addCategory(payload);

      this.$emit("reload");

      this.newName = "";
      this.newDescription = "";
    },

    async updateCategory(cat) {
      const payload = {
        ...cat,
        updated_at: new Date().toISOString(),
      };

      await apiUpdateCategory(cat.id, payload);
      this.$emit("reload");
    },

    async deleteCategory(id) {
      if (!confirm("削除しますか？")) return;

      await apiDeleteCategory(id);

      this.$emit("reload");
    },
  },
};
</script>

<style scoped>
.category-manager-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  overflow: hidden; /* 画面全体の縦スクロール禁止 */
}

/* タイトル */
h2 {
  margin-bottom: 1rem;
  color: #3b82f6;
}

/* ヘッダーを中央揃え */
table thead th {
  text-align: center;
}

/* データセルは左揃え（既存の設定） */
table tbody td {
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 新規追加フォーム：1行3列 */
.form {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr; /* カテゴリ名:説明:追加ボタン */
  gap: 0.5rem;
  margin-bottom: 1rem;
  width: 80%;
  max-width: 100%;
  box-sizing: border-box;
}

.form input,
.form button {
  padding: 0.4rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

/* テーブルラッパー */
.table-wrapper {
  width: 80%;
  max-height: 550px; /* 縦スクロール高さ */
  overflow-y: auto;
  border: 1px solid #ccc;
}

table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed; /* 列幅固定 */
}

th,
td {
  padding: 0.5rem;
  border: 1px solid #ccc;
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap; /* 1行に固定 */
}

/* 列幅調整（PC画面用） */
th:nth-child(1), td:nth-child(1) { width: 20%; } /* カテゴリ名 */
th:nth-child(2), td:nth-child(2) { width: 50%; } /* 説明 */
th:nth-child(3), td:nth-child(3) { width: 90px; } /*作成日 */
th:nth-child(4), td:nth-child(4) { width: 150px; } /* 操作列 */

/* ボタンは横に並べる */
td button.update,
td button.delete {
  width: 48%;
  box-sizing: border-box;
}


input {
  width: 100%;
  box-sizing: border-box;
}

button.update {
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.3rem 0.6rem;
  cursor: pointer;
  margin-right: 0.2rem;
}

button.delete {
  background-color: #f87171;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.3rem 0.6rem;
  cursor: pointer;
}

/* スマホ対応 */
@media (max-width: 600px) {
  .form {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr; /* カテゴリ名:説明:追加 */
    gap: 0.5rem;
    width: 100%;
  }
  .table-wrapper {
    width: 100%;
  }
}

/* 小さい画面で調整 */
@media (max-width: 600px) {
  th:nth-child(2),
  td:nth-child(2) {
    width: 100px;
  }

  th:nth-child(3),
  td:nth-child(3) {
    width: 85px;
  }

  th:nth-child(4),
  td:nth-child(4) {
    width: 120px;
  }

  td button.update,
  td button.delete {
    width: 48%;
  }
}

</style>