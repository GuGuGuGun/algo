<template>
  <main class="container admin-console">
    <section v-if="!isLoggedIn" class="card admin-auth-card">
      <h2>后台管理登录</h2>
      <p class="summary">请输入 Django 管理员账号，用于管理章节、知识点、标签和学习计划。</p>
      <form class="admin-login-form" @submit.prevent="login">
        <label for="admin-username">管理员用户名</label>
        <input id="admin-username" v-model.trim="loginForm.username" type="text" required placeholder="例如：admin" />
        <label for="admin-password">管理员密码</label>
        <input id="admin-password" v-model="loginForm.password" type="password" required placeholder="请输入密码" />
        <button type="submit" :disabled="isLoading">{{ isLoading ? "登录中..." : "登录后台" }}</button>
      </form>
      <p v-if="loginMessage" class="empty-tip">{{ loginMessage }}</p>
    </section>

    <section v-else class="card admin-shell">
      <aside class="admin-sidebar">
        <h2>内容管理后台</h2>
        <p class="summary">当前登录：{{ adminUsername }}</p>
        <div class="admin-side-actions">
          <button class="ghost-btn admin-ghost" @click="loadAllData">刷新</button>
          <button class="ghost-btn admin-ghost" @click="logout">退出</button>
        </div>

        <ul class="resource-menu">
          <li
            v-for="tab in tabOptions"
            :key="tab.key"
            class="resource-item"
            :class="{ active: adminTab === tab.key }"
            @click="switchTab(tab.key)"
          >
            <span>{{ tab.label }}</span>
            <span class="resource-count">{{ tabCountMap[tab.key] || 0 }}</span>
          </li>
        </ul>
      </aside>

      <div class="admin-main">
        <div class="admin-main-header">
          <div>
            <h3>{{ activeTabTitle }}</h3>
            <p class="summary">共 {{ activeTotal }} 条，当前第 {{ currentPage }} / {{ totalPages }} 页</p>
          </div>
          <div class="admin-toolbar">
            <input
              v-model.trim="tableKeyword"
              type="text"
              placeholder="搜索当前资源（服务端）..."
              @keydown.enter.prevent="applySearch"
            />
            <div class="admin-toolbar-actions">
              <button class="admin-small-btn" @click="applySearch">搜索</button>
              <button class="admin-small-btn secondary-btn" @click="clearSearch">清空</button>
            </div>
            <select v-model.number="pageSize">
              <option :value="5">每页 5 条</option>
              <option :value="10">每页 10 条</option>
              <option :value="20">每页 20 条</option>
            </select>
            <button @click="resetActiveForm">
              {{ activeFormId ? `取消编辑${activeTabTitle}` : `新建${activeTabTitle}` }}
            </button>
          </div>
        </div>

        <p v-if="errorMessage" class="empty-tip admin-error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="empty-tip admin-success">{{ successMessage }}</p>

        <div class="admin-table-wrap">
          <table class="admin-table">
            <thead>
              <tr>
                <th v-for="column in tableColumns" :key="column">{{ column }}</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in activeRows" :key="row.id">
                <td v-for="(cell, index) in getRowCells(row)" :key="`${row.id}-${index}`">{{ cell }}</td>
                <td class="action-cell">
                  <button class="admin-small-btn" @click="editActiveRow(row)">编辑</button>
                  <button class="admin-small-btn danger-btn" @click="deleteActiveRow(row.id)">删除</button>
                </td>
              </tr>
              <tr v-if="!activeRows.length">
                <td :colspan="tableColumns.length + 1" class="empty-row">暂无数据</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="admin-pagination">
          <button class="admin-small-btn" :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)">上一页</button>
          <span>{{ currentPage }} / {{ totalPages }}</span>
          <button class="admin-small-btn" :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)">下一页</button>
        </div>

        <form class="admin-form" @submit.prevent="saveActiveForm">
          <h4>{{ activeFormId ? `编辑${activeTabTitle}` : `新建${activeTabTitle}` }}</h4>

          <template v-if="adminTab === 'chapters'">
            <label>标题</label>
            <input v-model.trim="chapterForm.title" required />
            <label>摘要</label>
            <textarea v-model.trim="chapterForm.summary" rows="4" required />
            <label>顺序</label>
            <input v-model.number="chapterForm.order" type="number" min="1" required />
            <label>难度</label>
            <select v-model="chapterForm.difficulty">
              <option value="easy">easy</option>
              <option value="medium">medium</option>
              <option value="hard">hard</option>
            </select>
            <label>预计学时</label>
            <input v-model.number="chapterForm.estimated_hours" type="number" min="1" required />
          </template>

          <template v-if="adminTab === 'topics'">
            <label>所属章节</label>
            <select v-model.number="topicForm.chapter" required>
              <option :value="0" disabled>请选择章节</option>
              <option v-for="chapter in chapterOptions" :key="chapter.id" :value="chapter.id">
                {{ chapter.order }}. {{ chapter.title }}
              </option>
            </select>
            <label>标题</label>
            <input v-model.trim="topicForm.title" required />
            <label>核心考点</label>
            <input v-model.trim="topicForm.knowledge_point" required />
            <label>笔记内容</label>
            <textarea v-model="topicForm.note" rows="5" required />
            <label>应试提示</label>
            <textarea v-model="topicForm.exam_tip" rows="3" />
            <label>真题年份（逗号分隔）</label>
            <input v-model="topicForm.exam_years" placeholder="例如：2021,2023,2025" />
            <label class="checkbox-line">
              <input v-model="topicForm.is_key_for_exam" type="checkbox" />
              是否关键考点
            </label>
            <label>基础模板代码（字符串）</label>
            <textarea v-model="topicForm.template_code" rows="4" />
            <label>多语言模板 JSON（template_codes）</label>
            <textarea v-model="topicForm.template_codes" rows="8" />
            <label>双模式模板 JSON（template_modes）</label>
            <textarea v-model="topicForm.template_modes" rows="10" />
            <label>题目链接 JSON（practice_links）</label>
            <textarea v-model="topicForm.practice_links" rows="8" />
            <label>标签 ID（逗号分隔）</label>
            <input v-model="topicForm.tags" placeholder="例如：1,2,6" />
          </template>

          <template v-if="adminTab === 'tags'">
            <label>标签名</label>
            <input v-model.trim="tagForm.name" required />
            <label>分类</label>
            <select v-model="tagForm.category">
              <option value="hot100">hot100</option>
              <option value="exam">exam</option>
              <option value="template">template</option>
            </select>
            <label>关联知识点 ID（逗号分隔）</label>
            <input v-model="tagForm.topics" placeholder="例如：3,5,9" />
          </template>

          <template v-if="adminTab === 'plans'">
            <label>周次</label>
            <input v-model.number="planForm.week" type="number" min="1" required />
            <label>目标</label>
            <input v-model.trim="planForm.target" required />
            <label>重点</label>
            <textarea v-model.trim="planForm.focus" rows="4" required />
            <label>建议学时</label>
            <input v-model.number="planForm.recommended_hours" type="number" min="1" required />
          </template>

          <div class="admin-form-actions">
            <button type="submit">{{ activeFormId ? "保存修改" : "创建" }}</button>
            <button class="ghost-btn admin-ghost" type="button" @click="resetActiveForm">清空</button>
          </div>
        </form>
      </div>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from "vue";

const props = defineProps({
  apiBase: {
    type: String,
    required: true,
  },
});

const STORAGE_KEYS = {
  token: "labelu_admin_basic_token",
  username: "labelu_admin_username",
  activeTab: "labelu_admin_active_tab",
};

const RESOURCE_CONFIG = {
  chapters: { endpoint: "chapters", label: "章节管理" },
  topics: { endpoint: "topics", label: "知识点管理" },
  tags: { endpoint: "tags", label: "标签管理" },
  plans: { endpoint: "study-plans", label: "学习计划" },
};

const RESOURCE_KEYS = Object.keys(RESOURCE_CONFIG);

const tabOptions = [
  { key: "chapters", label: "章节管理" },
  { key: "topics", label: "知识点管理" },
  { key: "tags", label: "标签管理" },
  { key: "plans", label: "学习计划" },
];

const isLoading = ref(false);
const loginMessage = ref("");
const errorMessage = ref("");
const successMessage = ref("");
const tableKeyword = ref("");
const pageSize = ref(10);
const currentPage = ref(1);

const loginForm = reactive({
  username: "",
  password: "",
});

const adminUsername = ref("");
const adminBasicToken = ref("");
const adminTab = ref("chapters");

const resourceRows = reactive({
  chapters: [],
  topics: [],
  tags: [],
  plans: [],
});

const resourceTotals = reactive({
  chapters: 0,
  topics: 0,
  tags: 0,
  plans: 0,
});

const chapterOptions = ref([]);

const chapterForm = reactive({
  id: null,
  title: "",
  summary: "",
  order: 1,
  difficulty: "medium",
  estimated_hours: 8,
});

const topicForm = reactive({
  id: null,
  chapter: 0,
  title: "",
  knowledge_point: "",
  note: "",
  template_code: "",
  template_codes: JSON.stringify({ python: "" }, null, 2),
  template_modes: JSON.stringify({ leetcode: { python: "" }, nowcoder: { python: "" } }, null, 2),
  practice_links: JSON.stringify({ leetcode: [], nowcoder: [] }, null, 2),
  exam_tip: "",
  exam_years: "",
  is_key_for_exam: true,
  tags: "",
});

const tagForm = reactive({
  id: null,
  name: "",
  category: "exam",
  topics: "",
});

const planForm = reactive({
  id: null,
  week: 1,
  target: "",
  focus: "",
  recommended_hours: 12,
});

const isLoggedIn = computed(() => Boolean(adminBasicToken.value));

const tabCountMap = computed(() => ({
  chapters: resourceTotals.chapters,
  topics: resourceTotals.topics,
  tags: resourceTotals.tags,
  plans: resourceTotals.plans,
}));

const activeTabTitle = computed(() => RESOURCE_CONFIG[adminTab.value]?.label || "资源管理");

const activeRows = computed(() => resourceRows[adminTab.value] || []);

const activeTotal = computed(() => resourceTotals[adminTab.value] || 0);

const totalPages = computed(() => Math.max(1, Math.ceil(activeTotal.value / pageSize.value)));

const tableColumns = computed(() => {
  if (adminTab.value === "chapters") return ["ID", "顺序", "标题", "难度", "学时"];
  if (adminTab.value === "topics") return ["ID", "章节", "标题", "关键考点", "真题年份"];
  if (adminTab.value === "tags") return ["ID", "标签名", "分类", "关联数量"];
  return ["ID", "周次", "目标", "建议学时"];
});

const activeFormId = computed(() => {
  if (adminTab.value === "chapters") return chapterForm.id;
  if (adminTab.value === "topics") return topicForm.id;
  if (adminTab.value === "tags") return tagForm.id;
  return planForm.id;
});

function clearMessages() {
  errorMessage.value = "";
  successMessage.value = "";
}

function normalizeList(payload) {
  if (Array.isArray(payload)) {
    return payload;
  }
  if (payload && Array.isArray(payload.results)) {
    return payload.results;
  }
  return [];
}

function authHeader() {
  return adminBasicToken.value ? { Authorization: `Basic ${adminBasicToken.value}` } : {};
}

function buildManageListPath(tabKey, page, size, keyword) {
  const params = new URLSearchParams();
  params.set("page", String(page));
  params.set("page_size", String(size));
  if (keyword) {
    params.set("search", keyword);
  }
  const endpoint = RESOURCE_CONFIG[tabKey].endpoint;
  return `/manage/${endpoint}/?${params.toString()}`;
}

async function adminRequest(path, options = {}) {
  const headers = { ...authHeader(), ...(options.headers || {}) };
  if (options.body) {
    headers["Content-Type"] = "application/json";
  }

  const response = await fetch(`${props.apiBase}${path}`, {
    ...options,
    headers,
  });

  let payload = null;
  if (response.status !== 204) {
    const raw = await response.text();
    if (raw) {
      try {
        payload = JSON.parse(raw);
      } catch {
        payload = raw;
      }
    }
  }

  if (!response.ok) {
    const detail =
      (payload && typeof payload === "object" && (payload.detail || payload.non_field_errors?.[0])) || `HTTP ${response.status}`;
    throw new Error(String(detail));
  }
  return payload;
}

async function fetchResourcePage(tabKey, page = currentPage.value, keyword = tableKeyword.value.trim()) {
  const payload = await adminRequest(buildManageListPath(tabKey, page, pageSize.value, keyword));
  const rows = normalizeList(payload);
  resourceRows[tabKey] = rows;
  resourceTotals[tabKey] = typeof payload?.count === "number" ? payload.count : rows.length;
}

async function fetchResourceCount(tabKey) {
  const payload = await adminRequest(buildManageListPath(tabKey, 1, 1, ""));
  const rows = normalizeList(payload);
  resourceTotals[tabKey] = typeof payload?.count === "number" ? payload.count : rows.length;
}

async function loadAllCounts() {
  await Promise.all(RESOURCE_KEYS.map((key) => fetchResourceCount(key)));
}

async function loadChapterOptions() {
  const rows = [];
  let page = 1;
  while (page <= 50) {
    const payload = await adminRequest(`/manage/chapters/?page=${page}&page_size=100&ordering=order`);
    const chunk = normalizeList(payload);
    rows.push(...chunk);
    if (!payload?.next) {
      break;
    }
    page += 1;
  }
  chapterOptions.value = rows;
}

async function loadActiveResource() {
  if (!isLoggedIn.value) return;
  await fetchResourcePage(adminTab.value, currentPage.value, tableKeyword.value.trim());
  const maxPage = Math.max(1, Math.ceil(activeTotal.value / pageSize.value));
  if (currentPage.value > maxPage) {
    currentPage.value = maxPage;
    await fetchResourcePage(adminTab.value, currentPage.value, tableKeyword.value.trim());
  }
}

async function loadAllData() {
  if (!isLoggedIn.value) return;
  clearMessages();
  isLoading.value = true;
  try {
    await Promise.all([loadAllCounts(), loadChapterOptions(), loadActiveResource()]);
  } catch (error) {
    errorMessage.value = `加载后台数据失败：${error.message}`;
  } finally {
    isLoading.value = false;
  }
}

async function switchTab(tabKey) {
  if (adminTab.value === tabKey) return;
  adminTab.value = tabKey;
  tableKeyword.value = "";
  currentPage.value = 1;
  clearMessages();
  resetActiveForm();
  await loadActiveResource();
}

async function applySearch() {
  currentPage.value = 1;
  await loadActiveResource();
}

async function clearSearch() {
  if (!tableKeyword.value.trim()) return;
  tableKeyword.value = "";
  currentPage.value = 1;
  await loadActiveResource();
}

async function goToPage(page) {
  if (page < 1 || page > totalPages.value || page === currentPage.value) {
    return;
  }
  currentPage.value = page;
  await loadActiveResource();
}

async function login() {
  clearMessages();
  loginMessage.value = "";
  if (!loginForm.username || !loginForm.password) {
    loginMessage.value = "请输入管理员用户名和密码。";
    return;
  }

  isLoading.value = true;
  try {
    const token = window.btoa(`${loginForm.username}:${loginForm.password}`);
    await adminRequest("/manage/chapters/?page=1&page_size=1", {
      headers: { Authorization: `Basic ${token}` },
    });
    adminBasicToken.value = token;
    adminUsername.value = loginForm.username;
    window.localStorage.setItem(STORAGE_KEYS.token, token);
    window.localStorage.setItem(STORAGE_KEYS.username, loginForm.username);
    loginForm.password = "";
    loginMessage.value = "登录成功。";
    await loadAllData();
  } catch (error) {
    loginMessage.value = `登录失败：${error.message}`;
  } finally {
    isLoading.value = false;
  }
}

function logout() {
  adminBasicToken.value = "";
  adminUsername.value = "";
  RESOURCE_KEYS.forEach((key) => {
    resourceRows[key] = [];
    resourceTotals[key] = 0;
  });
  chapterOptions.value = [];
  window.localStorage.removeItem(STORAGE_KEYS.token);
  window.localStorage.removeItem(STORAGE_KEYS.username);
  clearMessages();
  loginMessage.value = "已退出后台。";
}

function parseNumberList(input, label) {
  const raw = String(input || "").replaceAll("，", ",").trim();
  if (!raw) return [];
  const values = raw
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean)
    .map((item) => Number(item));
  if (values.some((item) => !Number.isInteger(item) || item < 0)) {
    throw new Error(`${label} 必须是逗号分隔的整数。`);
  }
  return values;
}

function parseJsonObject(input, label) {
  const raw = String(input || "").trim();
  if (!raw) return {};
  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch {
    throw new Error(`${label} 不是合法 JSON。`);
  }
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    throw new Error(`${label} 必须是 JSON 对象。`);
  }
  return parsed;
}

function resetChapterForm() {
  chapterForm.id = null;
  chapterForm.title = "";
  chapterForm.summary = "";
  chapterForm.order = 1;
  chapterForm.difficulty = "medium";
  chapterForm.estimated_hours = 8;
}

function resetTopicForm() {
  topicForm.id = null;
  topicForm.chapter = 0;
  topicForm.title = "";
  topicForm.knowledge_point = "";
  topicForm.note = "";
  topicForm.template_code = "";
  topicForm.template_codes = JSON.stringify({ python: "" }, null, 2);
  topicForm.template_modes = JSON.stringify({ leetcode: { python: "" }, nowcoder: { python: "" } }, null, 2);
  topicForm.practice_links = JSON.stringify({ leetcode: [], nowcoder: [] }, null, 2);
  topicForm.exam_tip = "";
  topicForm.exam_years = "";
  topicForm.is_key_for_exam = true;
  topicForm.tags = "";
}

function resetTagForm() {
  tagForm.id = null;
  tagForm.name = "";
  tagForm.category = "exam";
  tagForm.topics = "";
}

function resetPlanForm() {
  planForm.id = null;
  planForm.week = 1;
  planForm.target = "";
  planForm.focus = "";
  planForm.recommended_hours = 12;
}

function resetActiveForm() {
  if (adminTab.value === "chapters") {
    resetChapterForm();
    return;
  }
  if (adminTab.value === "topics") {
    resetTopicForm();
    return;
  }
  if (adminTab.value === "tags") {
    resetTagForm();
    return;
  }
  resetPlanForm();
}

async function saveChapter() {
  const payload = {
    title: chapterForm.title,
    summary: chapterForm.summary,
    order: Number(chapterForm.order),
    difficulty: chapterForm.difficulty,
    estimated_hours: Number(chapterForm.estimated_hours),
  };
  if (!payload.title || !payload.summary) {
    throw new Error("章节标题和摘要不能为空。");
  }
  if (!Number.isInteger(payload.order) || payload.order <= 0) {
    throw new Error("章节顺序必须是正整数。");
  }
  if (!Number.isInteger(payload.estimated_hours) || payload.estimated_hours <= 0) {
    throw new Error("预计学时必须是正整数。");
  }
  if (chapterForm.id) {
    await adminRequest(`/manage/chapters/${chapterForm.id}/`, { method: "PATCH", body: JSON.stringify(payload) });
    successMessage.value = "章节修改成功。";
  } else {
    await adminRequest("/manage/chapters/", { method: "POST", body: JSON.stringify(payload) });
    successMessage.value = "章节创建成功。";
  }
}

async function saveTopic() {
  if (!Number.isInteger(Number(topicForm.chapter)) || Number(topicForm.chapter) <= 0) {
    throw new Error("请先选择知识点所属章节。");
  }
  const payload = {
    chapter: Number(topicForm.chapter),
    title: topicForm.title,
    knowledge_point: topicForm.knowledge_point,
    note: topicForm.note,
    template_code: topicForm.template_code,
    template_codes: parseJsonObject(topicForm.template_codes, "template_codes"),
    template_modes: parseJsonObject(topicForm.template_modes, "template_modes"),
    practice_links: parseJsonObject(topicForm.practice_links, "practice_links"),
    exam_tip: topicForm.exam_tip,
    exam_years: parseNumberList(topicForm.exam_years, "真题年份"),
    is_key_for_exam: Boolean(topicForm.is_key_for_exam),
    tags: parseNumberList(topicForm.tags, "标签 ID"),
  };
  if (!payload.title || !payload.knowledge_point || !payload.note) {
    throw new Error("标题、核心考点和笔记内容不能为空。");
  }
  if (topicForm.id) {
    await adminRequest(`/manage/topics/${topicForm.id}/`, { method: "PATCH", body: JSON.stringify(payload) });
    successMessage.value = "知识点修改成功。";
  } else {
    await adminRequest("/manage/topics/", { method: "POST", body: JSON.stringify(payload) });
    successMessage.value = "知识点创建成功。";
  }
}

async function saveTag() {
  const payload = {
    name: tagForm.name,
    category: tagForm.category,
    topics: parseNumberList(tagForm.topics, "关联知识点 ID"),
  };
  if (!payload.name) {
    throw new Error("标签名不能为空。");
  }
  if (tagForm.id) {
    await adminRequest(`/manage/tags/${tagForm.id}/`, { method: "PATCH", body: JSON.stringify(payload) });
    successMessage.value = "标签修改成功。";
  } else {
    await adminRequest("/manage/tags/", { method: "POST", body: JSON.stringify(payload) });
    successMessage.value = "标签创建成功。";
  }
}

async function savePlan() {
  const payload = {
    week: Number(planForm.week),
    target: planForm.target,
    focus: planForm.focus,
    recommended_hours: Number(planForm.recommended_hours),
  };
  if (!Number.isInteger(payload.week) || payload.week <= 0) {
    throw new Error("周次必须是正整数。");
  }
  if (!payload.target || !payload.focus) {
    throw new Error("目标和重点不能为空。");
  }
  if (!Number.isInteger(payload.recommended_hours) || payload.recommended_hours <= 0) {
    throw new Error("建议学时必须是正整数。");
  }
  if (planForm.id) {
    await adminRequest(`/manage/study-plans/${planForm.id}/`, { method: "PATCH", body: JSON.stringify(payload) });
    successMessage.value = "学习计划修改成功。";
  } else {
    await adminRequest("/manage/study-plans/", { method: "POST", body: JSON.stringify(payload) });
    successMessage.value = "学习计划创建成功。";
  }
}

async function saveActiveForm() {
  clearMessages();
  try {
    if (adminTab.value === "chapters") {
      await saveChapter();
    } else if (adminTab.value === "topics") {
      await saveTopic();
    } else if (adminTab.value === "tags") {
      await saveTag();
    } else {
      await savePlan();
    }
    await loadAllData();
    resetActiveForm();
  } catch (error) {
    errorMessage.value = `保存失败：${error.message}`;
  }
}

async function deleteResource(resource, id, label) {
  clearMessages();
  if (!window.confirm(`确认删除${label} #${id}？`)) {
    return;
  }
  try {
    await adminRequest(`/manage/${resource}/${id}/`, { method: "DELETE" });
    successMessage.value = `${label}已删除。`;
    await loadAllData();
  } catch (error) {
    errorMessage.value = `删除失败：${error.message}`;
  }
}

function editChapter(chapter) {
  chapterForm.id = chapter.id;
  chapterForm.title = chapter.title;
  chapterForm.summary = chapter.summary;
  chapterForm.order = chapter.order;
  chapterForm.difficulty = chapter.difficulty;
  chapterForm.estimated_hours = chapter.estimated_hours;
}

function editTopic(topic) {
  topicForm.id = topic.id;
  topicForm.chapter = Number(topic.chapter) || 0;
  topicForm.title = topic.title || "";
  topicForm.knowledge_point = topic.knowledge_point || "";
  topicForm.note = topic.note || "";
  topicForm.template_code = topic.template_code || "";
  topicForm.template_codes = JSON.stringify(topic.template_codes || { python: "" }, null, 2);
  topicForm.template_modes = JSON.stringify(topic.template_modes || { leetcode: { python: "" }, nowcoder: { python: "" } }, null, 2);
  topicForm.practice_links = JSON.stringify(topic.practice_links || { leetcode: [], nowcoder: [] }, null, 2);
  topicForm.exam_tip = topic.exam_tip || "";
  topicForm.exam_years = (topic.exam_years || []).join(",");
  topicForm.is_key_for_exam = Boolean(topic.is_key_for_exam);
  topicForm.tags = (topic.tags || []).join(",");
}

function editTag(tag) {
  tagForm.id = tag.id;
  tagForm.name = tag.name || "";
  tagForm.category = tag.category || "exam";
  tagForm.topics = (tag.topics || []).join(",");
}

function editPlan(plan) {
  planForm.id = plan.id;
  planForm.week = plan.week;
  planForm.target = plan.target || "";
  planForm.focus = plan.focus || "";
  planForm.recommended_hours = plan.recommended_hours;
}

function editActiveRow(row) {
  if (adminTab.value === "chapters") {
    editChapter(row);
    return;
  }
  if (adminTab.value === "topics") {
    editTopic(row);
    return;
  }
  if (adminTab.value === "tags") {
    editTag(row);
    return;
  }
  editPlan(row);
}

function deleteActiveRow(id) {
  if (adminTab.value === "chapters") {
    deleteResource("chapters", id, "章节");
    return;
  }
  if (adminTab.value === "topics") {
    deleteResource("topics", id, "知识点");
    return;
  }
  if (adminTab.value === "tags") {
    deleteResource("tags", id, "标签");
    return;
  }
  deleteResource("study-plans", id, "学习计划");
}

function getRowCells(row) {
  if (adminTab.value === "chapters") {
    return [row.id, row.order, row.title, row.difficulty, row.estimated_hours];
  }
  if (adminTab.value === "topics") {
    return [
      row.id,
      row.chapter_title || row.chapter,
      row.title,
      row.is_key_for_exam ? "是" : "否",
      row.exam_years?.length ? row.exam_years.join("、") : "-",
    ];
  }
  if (adminTab.value === "tags") {
    return [row.id, row.name, row.category, row.topics?.length || 0];
  }
  return [row.id, row.week, row.target, row.recommended_hours];
}

watch(adminTab, (value) => {
  window.localStorage.setItem(STORAGE_KEYS.activeTab, value);
});

watch(pageSize, async () => {
  currentPage.value = 1;
  if (!isLoggedIn.value) return;
  await loadActiveResource();
});

onMounted(async () => {
  const savedTab = window.localStorage.getItem(STORAGE_KEYS.activeTab);
  if (savedTab && tabOptions.some((item) => item.key === savedTab)) {
    adminTab.value = savedTab;
  }

  const savedToken = window.localStorage.getItem(STORAGE_KEYS.token);
  const savedUsername = window.localStorage.getItem(STORAGE_KEYS.username);
  if (savedToken && savedUsername) {
    adminBasicToken.value = savedToken;
    adminUsername.value = savedUsername;
    await loadAllData();
  }
});
</script>

<style scoped>
.admin-console {
  padding-top: 12px;
  padding-bottom: 40px;
}

.admin-auth-card {
  max-width: 520px;
  margin: 0 auto;
}

.admin-login-form {
  display: grid;
  gap: 8px;
}

.admin-shell {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 14px;
  padding: 14px;
}

.admin-sidebar {
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px;
  background: var(--card-strong);
  align-self: start;
  position: sticky;
  top: 12px;
}

.admin-sidebar h2 {
  margin: 0 0 8px;
  font-size: 18px;
}

.admin-side-actions {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.resource-menu {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 8px;
}

.resource-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 9px 10px;
  background: var(--card);
  cursor: pointer;
}

.resource-item.active {
  border-color: rgba(37, 99, 235, 0.4);
  background: var(--active-card);
}

.resource-count {
  min-width: 26px;
  padding: 2px 8px;
  border-radius: 999px;
  text-align: center;
  font-size: 12px;
  background: var(--primary-soft);
}

.admin-main {
  display: grid;
  gap: 12px;
}

.admin-main-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}

.admin-main-header h3 {
  margin: 0 0 6px;
}

.admin-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.admin-toolbar input {
  min-width: 220px;
}

.admin-toolbar-actions {
  display: inline-flex;
  gap: 6px;
}

.admin-table-wrap {
  overflow: auto;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--card-strong);
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
}

.admin-table th,
.admin-table td {
  border-bottom: 1px solid var(--border);
  padding: 10px;
  text-align: left;
  font-size: 13px;
  vertical-align: top;
}

.admin-table th {
  background: var(--primary-soft);
}

.action-cell {
  white-space: nowrap;
}

.admin-small-btn {
  padding: 6px 10px;
  font-size: 12px;
  margin-right: 6px;
}

.secondary-btn {
  background: #64748b;
}

.secondary-btn:hover {
  box-shadow: 0 8px 14px rgba(100, 116, 139, 0.26);
}

.empty-row {
  text-align: center;
  color: var(--muted);
}

.admin-pagination {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
}

.admin-form {
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--card-strong);
  padding: 12px;
  display: grid;
  gap: 8px;
}

.admin-form h4 {
  margin: 0 0 6px;
}

.admin-form textarea {
  resize: vertical;
}

.admin-form-actions {
  display: flex;
  gap: 8px;
  margin-top: 6px;
}

.checkbox-line {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.danger-btn {
  background: #dc2626;
}

.danger-btn:hover {
  box-shadow: 0 8px 14px rgba(220, 38, 38, 0.28);
}

.admin-error {
  color: #dc2626;
}

.admin-success {
  color: #059669;
}

.admin-ghost {
  background: var(--card-strong);
  color: var(--text);
  border: 1px solid var(--border);
}

.admin-ghost:hover {
  background: var(--active-card);
}

@media (max-width: 1100px) {
  .admin-shell {
    grid-template-columns: 1fr;
  }

  .admin-sidebar {
    position: static;
  }

  .admin-main-header {
    flex-direction: column;
  }

  .admin-toolbar {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
