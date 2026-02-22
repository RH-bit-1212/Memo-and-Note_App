<template>
  <div class="tag-manager-container">
    <h2>タグ管理</h2>

    <!-- 新規追加フォーム -->
    <div class="form">
      <input v-model="newName" placeholder="タグ名" />
      <input type="color" v-model="newColor" /> <!-- カラーピッカー -->
      <button @click="createTag">追加</button>
    </div>

    <!-- タグ一覧テーブル -->
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>名前</th>
            <th>色</th>
            <th>作成日</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tag in localTags" :key="tag.id">
            <td><input v-model="tag.name" /></td>
            <td>
              <input type="color" v-model="tag.color" />
            </td>
            <td>{{ tag.created_at?.substring(0, 10) }}</td>
            <td>
              <button @click="updateTag(tag)" class="update">更新</button>
              <button @click="deleteTag(tag.id)" class="delete">削除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import {
  addTag,
  updateTag as apiUpdateTag,
  deleteTag as apiDeleteTag,
} from "@/api/api";

export default {
  name: "TagManager",
  props: {
    modelValue: { type: Array, required: true },
  },
  emits: ["reload"],
  data() {
    return {
      newName: "",
      newColor: "#000000", // 初期色
      localTags: [],
    };
  },
  watch: {
    modelValue: {
      immediate: true,
      handler(newVal) {
        this.localTags = JSON.parse(JSON.stringify(newVal));
      },
    },
  },
  methods: {
    async createTag() {
      const name = this.newName.trim();
      const color = this.newColor.trim();

      if (!name) return alert("名前は必須です");
      if (name.length > 50) return alert("タグ名は50文字以内にしてください");

      if (this.localTags.some((t) => t.name === name)) {
        return alert("同じタグ名が既に存在します");
      }

      const now = new Date().toISOString();
      const payload = {
        name,
        color,
        created_at: now,
        updated_at: now,
      };

      await addTag(payload);
      this.$emit("reload");
      this.newName = "";
      this.newColor = "#000000";
    },

    async updateTag(tag) {
      const payload = {
        ...tag,
        updated_at: new Date().toISOString(),
      };
      await apiUpdateTag(tag.id, payload);
      this.$emit("reload");
    },

    async deleteTag(id) {
      if (!confirm("削除しますか？")) return;
      await apiDeleteTag(id);
      this.$emit("reload");
    },
  },
};
</script>

<style scoped>
.tag-manager-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  overflow: hidden; /* 画面全体の縦スクロールを禁止 */
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

/* 新規追加フォーム */
.form {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
  justify-content: center;
  width: 80%;
  max-width: 100%;
  box-sizing: border-box;
}

.form input,
.form button {
  padding: 0.4rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  flex: 1 1 150px;
}

/* 色選択フォームの拡大 */
.form input[type="color"] {
  width: 100%;       /* 親の幅に合わせる */
  max-width: 100px;  /* 最大幅 */
  height: 40px;      /* 高さを大きくしてクリックしやすく */
  padding: 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
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
  table-layout: fixed; /* 各列幅を固定ベースで制御 */
}

th,
td {
  padding: 0.5rem;
  border: 1px solid #ccc;
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap; /* 1行にする */
}

/* 作成日列の幅を日付に合わせる */
th:nth-child(3),
td:nth-child(3) {
  width: 100px;
}

/* 操作列の幅をボタン幅に合わせる */
th:nth-child(4),
td:nth-child(4) {
  width: 150px; /* ボタンの合計幅に調整 */
}

/* ボタンはテーブル幅に合わせる場合 */
td button.update,
td button.delete {
  width: 48%; /* 2つのボタンを並べて収める */
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

/* スマホ対応：横並び3列（タグ名・色・追加ボタン）幅比 3:1:2 */
@media (max-width: 600px) {
  .form {
    display: grid;
    grid-template-columns: 3fr 1fr 2fr; /* タグ:色:ボタン */
    gap: 0.5rem;
    width: 100%;
  }

  /* 各要素の列指定は不要（自動で並ぶ） */
  .table-wrapper {
    width: 100%;
  }
}

/* スマホ対応でさらに大きくする場合 */
@media (max-width: 600px) {
  input[type="color"] {
    width: 50px;
    height: 30px;
  }
}

/* 小さい画面で調整 */
@media (max-width: 600px) {
  th:nth-child(2),
  td:nth-child(2) {
    width: 50px;
  }

  th:nth-child(3),
  td:nth-child(3) {
    width: 90px;
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