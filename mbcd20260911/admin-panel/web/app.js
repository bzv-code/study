/* Фронт админ-панели «Дом цветов»: вход по логину/паролю + управление товарами. */
"use strict";

const $ = (id) => document.getElementById(id);

const loginScreen = $("login-screen");
const appScreen = $("app-screen");
const modalBackdrop = $("modal-backdrop");

let token = localStorage.getItem("admin_token") || "";

/* ---------------- API-хелперы ---------------- */
async function api(path, options = {}) {
  const headers = options.headers || {};
  if (token) headers["Authorization"] = "Bearer " + token;
  if (options.json !== undefined) {
    headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(options.json);
    delete options.json;
  }
  const res = await fetch(path, { ...options, headers });
  if (res.status === 401 && !path.endsWith("/api/login")) {
    logout();
    throw new Error("Сессия истекла, войдите заново");
  }
  if (!res.ok) {
    let detail = "Ошибка запроса";
    try { detail = (await res.json()).detail || detail; } catch (_) {}
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return res.status === 204 ? null : res.json();
}

function toast(text) {
  const el = $("toast");
  el.textContent = text;
  el.classList.remove("hidden");
  clearTimeout(toast._t);
  toast._t = setTimeout(() => el.classList.add("hidden"), 2500);
}

/* ---------------- Экран входа ---------------- */
function showLogin() {
  loginScreen.classList.remove("hidden");
  appScreen.classList.add("hidden");
}

function showApp(username) {
  loginScreen.classList.add("hidden");
  appScreen.classList.remove("hidden");
  $("whoami").textContent = username ? `Вы вошли как ${username}` : "";
  loadProducts().catch((e) => toast(e.message));
}

function logout() {
  token = "";
  localStorage.removeItem("admin_token");
  showLogin();
}

$("login-form").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const errBox = $("login-error");
  errBox.classList.add("hidden");
  try {
    const data = await api("/api/login", {
      method: "POST",
      json: { username: $("login-username").value.trim(), password: $("login-password").value },
    });
    token = data.token;
    localStorage.setItem("admin_token", token);
    $("login-password").value = "";
    showApp(data.username);
  } catch (e) {
    errBox.textContent = e.message;
    errBox.classList.remove("hidden");
  }
});

$("logout-btn").addEventListener("click", logout);

/* ---------------- Список товаров ---------------- */
function fmtPrice(v) {
  return new Intl.NumberFormat("ru-RU").format(v) + " ₽";
}

async function loadProducts() {
  const products = await api("/api/products");
  const grid = $("products-grid");
  grid.innerHTML = "";
  $("empty-hint").classList.toggle("hidden", products.length > 0);

  for (const p of products) {
    const card = document.createElement("div");
    card.className = "card";

    const img = document.createElement(p.photo_url ? "img" : "div");
    img.className = "card-img" + (p.photo_url ? "" : " placeholder");
    if (p.photo_url) { img.src = p.photo_url; img.alt = p.title; }
    else img.textContent = "🌷";

    const body = document.createElement("div");
    body.className = "card-body";
    body.innerHTML = `
      <span class="badge ${p.is_active ? "" : "off"}">${p.is_active ? "В каталоге" : "Скрыт"}</span>
      ${p.category ? `<span class="card-cat"></span>` : ""}
      <span class="card-title"></span>
      <span class="card-price">${fmtPrice(p.price)}</span>
    `;
    if (p.category) body.querySelector(".card-cat").textContent = p.category;
    body.querySelector(".card-title").textContent = p.title;

    const actions = document.createElement("div");
    actions.className = "card-actions";

    const editBtn = document.createElement("button");
    editBtn.className = "btn btn-secondary";
    editBtn.textContent = "Редактировать";
    editBtn.onclick = () => openModal(p);

    const toggleBtn = document.createElement("button");
    toggleBtn.className = "btn btn-ghost";
    toggleBtn.textContent = p.is_active ? "Скрыть" : "Показать";
    toggleBtn.onclick = async () => {
      try {
        await api(`/api/products/${p.id}`, { method: "PATCH", json: { is_active: !p.is_active } });
        loadProducts();
      } catch (e) { toast(e.message); }
    };

    const delBtn = document.createElement("button");
    delBtn.className = "btn btn-danger";
    delBtn.textContent = "Удалить";
    delBtn.onclick = async () => {
      if (!confirm(`Удалить товар «${p.title}»?`)) return;
      try {
        await api(`/api/products/${p.id}`, { method: "DELETE" });
        toast("Товар удалён");
        loadProducts();
      } catch (e) { toast(e.message); }
    };

    actions.append(editBtn, toggleBtn, delBtn);
    body.append(actions);
    card.append(img, body);
    grid.append(card);
  }
}

/* ---------------- Модальное окно (добавление / редактирование) ---------------- */
function openModal(product = null) {
  $("modal-title").textContent = product ? "Редактирование товара" : "Новый товар";
  $("f-id").value = product ? product.id : "";
  $("f-title").value = product ? product.title : "";
  $("f-category").value = product ? product.category : "";
  $("f-description").value = product ? product.description : "";
  $("f-price").value = product ? product.price : "";
  $("f-active").checked = product ? product.is_active : true;
  $("f-photo-url").value = product ? product.photo_url : "";
  $("f-photo-file").value = "";
  $("upload-status").textContent = "";
  $("form-error").classList.add("hidden");
  $("delete-btn").classList.toggle("hidden", !product);
  updatePreview();
  modalBackdrop.classList.remove("hidden");
  $("f-title").focus();
}

function closeModal() {
  modalBackdrop.classList.add("hidden");
}

$("add-product-btn").addEventListener("click", () => openModal());
$("modal-close").addEventListener("click", closeModal);
modalBackdrop.addEventListener("click", (ev) => { if (ev.target === modalBackdrop) closeModal(); });
document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") closeModal(); });

function updatePreview() {
  const url = $("f-photo-url").value.trim();
  const img = $("photo-preview");
  if (url) {
    img.src = url;
    img.classList.remove("hidden");
    $("no-photo").classList.add("hidden");
  } else {
    img.classList.add("hidden");
    $("no-photo").classList.remove("hidden");
  }
}

$("f-photo-url").addEventListener("input", updatePreview);

$("f-photo-file").addEventListener("change", async () => {
  const file = $("f-photo-file").files[0];
  if (!file) return;
  const status = $("upload-status");
  status.textContent = "Загрузка…";
  try {
    const form = new FormData();
    form.append("file", file);
    const data = await api("/api/upload", { method: "POST", body: form });
    $("f-photo-url").value = data.photo_url;
    updatePreview();
    status.textContent = "Картинка загружена ✓";
  } catch (e) {
    status.textContent = "";
    $("form-error").textContent = e.message;
    $("form-error").classList.remove("hidden");
  }
});

$("product-form").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const id = $("f-id").value;
  const payload = {
    title: $("f-title").value.trim(),
    category: $("f-category").value.trim(),
    description: $("f-description").value.trim(),
    price: parseInt($("f-price").value, 10),
    photo_url: $("f-photo-url").value.trim(),
    is_active: $("f-active").checked,
  };
  try {
    if (id) {
      await api(`/api/products/${id}`, { method: "PATCH", json: payload });
      toast("Товар обновлён");
    } else {
      await api("/api/products", { method: "POST", json: payload });
      toast("Товар добавлен");
    }
    closeModal();
    loadProducts();
  } catch (e) {
    $("form-error").textContent = e.message;
    $("form-error").classList.remove("hidden");
  }
});

$("delete-btn").addEventListener("click", async () => {
  const id = $("f-id").value;
  if (!id) return;
  if (!confirm("Удалить этот товар?")) return;
  try {
    await api(`/api/products/${id}`, { method: "DELETE" });
    toast("Товар удалён");
    closeModal();
    loadProducts();
  } catch (e) { toast(e.message); }
});

/* ---------------- Старт ---------------- */
(async function init() {
  if (!token) return showLogin();
  try {
    const me = await api("/api/me");
    showApp(me.username);
  } catch (_) {
    showLogin();
  }
})();
