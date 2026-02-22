// src/api/api.js
export const API_URL = "http://localhost:8000";

/* =========================
   共通：認証ヘッダ
========================= */
function authHeaders() {
  const token = localStorage.getItem("access_token");
  if (!token) throw new Error("Not logged in");
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
}

/* =========================
   AUTH
========================= */
export async function login(username, password) {
  const res = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
  localStorage.setItem("access_token", data.access_token);
  return data;
}

export function logout() {
  localStorage.removeItem("access_token");
}

/* =========================
   MEMO
========================= */
export async function fetchMemos() {
  const res = await fetch(`${API_URL}/memos`, { headers: authHeaders() });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function fetchMemo(id) {
  const res = await fetch(`${API_URL}/memos/${id}`, { headers: authHeaders() });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function addMemo(payload) {
  const res = await fetch(`${API_URL}/memos`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function updateMemo(id, payload) {
  const res = await fetch(`${API_URL}/memos/${id}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function deleteMemo(id) {
  const res = await fetch(`${API_URL}/memos/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return true;
}

/* =========================
   CATEGORY
========================= */
export async function fetchCategories() {
  const res = await fetch(`${API_URL}/categories`, { headers: authHeaders() });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function addCategory(payload) {
  const res = await fetch(`${API_URL}/categories`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function updateCategory(id, payload) {
  const res = await fetch(`${API_URL}/categories/${id}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function deleteCategory(id) {
  const res = await fetch(`${API_URL}/categories/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return true;
}

/* =========================
   TAG
========================= */
export async function fetchTags() {
  const res = await fetch(`${API_URL}/tags`, { headers: authHeaders() });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function addTag(payload) {
  const res = await fetch(`${API_URL}/tags`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function updateTag(id, payload) {
  const res = await fetch(`${API_URL}/tags/${id}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function deleteTag(id) {
  const res = await fetch(`${API_URL}/tags/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return true;
}

/* =========================
   USERS（admin only）
========================= */
export async function fetchUsers() {
  const res = await fetch(`${API_URL}/admin/users`, { headers: authHeaders() });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function fetchUser(id) {
  const res = await fetch(`${API_URL}/admin/users/${id}`, { headers: authHeaders() });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function createUser(payload) {
  const res = await fetch(`${API_URL}/admin/users`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function updateUser(id, payload) {
  const res = await fetch(`${API_URL}/admin/users/${id}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function deleteUser(id) {
  const res = await fetch(`${API_URL}/admin/users/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return true;
}
