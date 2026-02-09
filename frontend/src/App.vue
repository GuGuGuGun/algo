<template>
  <div>
    <header class="site-header">
      <div class="container header-row">
        <div>
          <h1>考研算法笔记</h1>
          <p>面向考研 408 与复试机试，按章节沉淀模板、考点和易错点。</p>
        </div>
        <div class="header-actions">
          <span class="badge">Django API + Vue 3</span>
          <button class="ghost-btn mode-btn" :class="{ 'mode-active': appMode === 'study' }" @click="appMode = 'study'">
            学习模式
          </button>
          <button class="ghost-btn mode-btn" :class="{ 'mode-active': appMode === 'admin' }" @click="appMode = 'admin'">
            后台管理
          </button>
          <button class="ghost-btn theme-btn" @click="toggleTheme">
            {{ selectedTheme === "dark" ? "切换浅色" : "切换深色" }}
          </button>
          <button class="ghost-btn" @click="resetPreferences">重置偏好</button>
        </div>
      </div>
    </header>

    <main v-if="appMode === 'study'" class="container main-layout">
      <section class="sidebar card">
        <h2>章节目录</h2>
        <div class="filters">
          <label for="difficulty">难度筛选</label>
          <select id="difficulty" v-model="difficulty" @change="loadChapters">
            <option value="">全部</option>
            <option value="easy">简单</option>
            <option value="medium">中等</option>
            <option value="hard">困难</option>
          </select>
        </div>
        <div class="filters">
          <label for="exam-year">408 真题年份</label>
          <select id="exam-year" v-model="selectedYear">
            <option value="">全部年份</option>
            <option v-for="item in examYears" :key="item.year" :value="String(item.year)">
              {{ item.year }}（{{ item.topic_count }}）
            </option>
          </select>
        </div>
        <div class="filters">
          <label for="language">代码语言</label>
          <select id="language" v-model="selectedLanguage">
            <option v-for="item in languageOptions" :key="item.value" :value="item.value">
              {{ item.label }}
            </option>
          </select>
        </div>
        <div class="filters">
          <label for="template-mode">模板模式</label>
          <select id="template-mode" v-model="selectedTemplateMode">
            <option v-for="item in templateModeOptions" :key="item.value" :value="item.value">
              {{ item.label }}
            </option>
          </select>
        </div>
        <div class="active-state">
          <span class="chip">模式：{{ templateModeLabelMap[selectedTemplateMode] }}</span>
          <span class="chip">语言：{{ languageLabelMap[selectedLanguage] }}</span>
          <span class="chip">{{ difficulty ? `难度：${difficultyToZh(difficulty)}` : "难度：全部" }}</span>
          <span class="chip">{{ selectedYear ? `年份：${selectedYear}` : "年份：全部" }}</span>
          <span class="chip">主题：{{ themeLabelMap[selectedTheme] }}</span>
        </div>
        <button class="reset-btn" @click="resetPreferences">清空本地偏好</button>

        <ul class="chapter-list">
          <li
            v-for="chapter in chapters"
            :key="chapter.id"
            class="chapter-item"
            :class="{ active: activeChapterId === chapter.id }"
            @click="loadChapterDetail(chapter.id)"
          >
            <strong>{{ chapter.order }}. {{ chapter.title }}</strong>
            <br />
            <small>
              难度：{{ difficultyToZh(chapter.difficulty) }} · 知识点：{{ chapter.topic_count }} · 预计 {{ chapter.estimated_hours
              }}h
            </small>
          </li>
        </ul>
        <p v-if="!chapters.length" class="empty-tip">暂无匹配章节</p>
      </section>

      <section class="content">
        <article class="card">
          <h2>{{ activeChapterTitle }}</h2>
          <p class="summary">{{ activeChapterSummary }}</p>
          <div class="section-toolbar">
            <span class="chip chip-soft">模板模式：{{ templateModeLabelMap[selectedTemplateMode] }}</span>
            <span class="chip chip-soft">代码语言：{{ languageLabelMap[selectedLanguage] }}</span>
            <span class="chip chip-soft">{{ selectedYear ? `年份筛选：${selectedYear}` : "年份筛选：全部" }}</span>
          </div>
          <p class="summary" v-if="filteredActiveTopics.length">
            本章共 {{ filteredActiveTopics.length }} 个知识点
            <span v-if="selectedYear">（已按 {{ selectedYear }} 年筛选）</span>
          </p>

          <p v-if="isLoadingDetail" class="empty-tip">正在加载章节详情...</p>
          <div v-else-if="filteredActiveTopics.length" class="topics">
            <div v-for="topic in filteredActiveTopics" :key="topic.id" class="topic-card">
              <h3>{{ topic.title }}</h3>
              <div class="topic-meta">
                考点：{{ topic.knowledge_point }} ｜ 标签：{{ topic.tags.length ? topic.tags.join("、") : "无" }}
              </div>
              <div class="topic-lang">
                当前显示：{{ templateModeLabelMap[selectedTemplateMode] }} · {{ languageLabelMap[selectedLanguage] }} ｜ 已提供：{{ getAvailableLanguages(topic) }}
              </div>
              <div class="topic-year">408 真题年份：{{ topic.exam_years.length ? topic.exam_years.join("、") : "暂未标注" }}</div>
              <div class="topic-links">
                <div class="topic-link-group">
                  <strong>LeetCode：</strong>
                  <template v-if="getPracticeLinks(topic, 'leetcode').length">
                    <a
                      v-for="item in getPracticeLinks(topic, 'leetcode')"
                      :key="`lc-${topic.id}-${item.url}`"
                      :href="item.url"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {{ item.title }}
                    </a>
                  </template>
                  <span v-else>暂无</span>
                </div>
                <div class="topic-link-group">
                  <strong>牛客网（ACM）：</strong>
                  <template v-if="getPracticeLinks(topic, 'nowcoder').length">
                    <a
                      v-for="item in getPracticeLinks(topic, 'nowcoder')"
                      :key="`nc-${topic.id}-${item.url}`"
                      :href="item.url"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {{ item.title }}
                    </a>
                  </template>
                  <span v-else>暂无</span>
                </div>
              </div>
              <p class="topic-note">{{ topic.note }}</p>
              <p class="topic-tip"><strong>应试提示：</strong>{{ topic.exam_tip || "暂无" }}</p>
              <pre class="topic-code"><code>{{ getTemplateCode(topic) }}</code></pre>
            </div>
          </div>
          <p v-else class="empty-tip">{{ selectedYear ? "该章节在所选年份暂无收录。" : "该章节暂无知识点。" }}</p>
        </article>

        <article class="card">
          <h2>12 周考研算法计划</h2>
          <ul class="study-plan">
            <li v-for="plan in studyPlans" :key="plan.id">
              第 {{ plan.week }} 周：<strong>{{ plan.target }}</strong>（{{ plan.focus }}，建议 {{ plan.recommended_hours }} 小时）
            </li>
          </ul>
        </article>

        <article class="card">
          <h2>知识点搜索（仅关键考点）</h2>
          <p class="summary" v-if="selectedYear">当前搜索年份：{{ selectedYear }}（可切换为全部年份）</p>
          <div class="search-bar">
            <input
              type="text"
              v-model.trim="searchKeyword"
              placeholder="输入关键词，如：背包、并查集、LCS"
              @keydown.enter="searchTopics"
            />
            <button @click="searchTopics">搜索</button>
          </div>

          <ul class="search-result">
            <li v-for="topic in searchResults" :key="topic.id">
              <strong>{{ topic.title }}</strong>（{{ topic.chapter_title }}）- {{ topic.knowledge_point }}
              <span class="year-inline" v-if="topic.exam_years.length"> [{{ topic.exam_years.join("、") }}]</span>
            </li>
          </ul>
          <p v-if="searchMessage" class="empty-tip">{{ searchMessage }}</p>
        </article>

        <article v-if="errorMessage" class="card error-card">
          <h2>连接提示</h2>
          <p>{{ errorMessage }}</p>
        </article>
      </section>
    </main>
    <AdminPanel v-else :api-base="API_BASE" />

    <footer class="site-footer">
      <div class="container">
        <p>Labelu · 前后端分离（Django API + Vue 3）</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import AdminPanel from "./components/AdminPanel.vue";

const API_BASE = "http://127.0.0.1:8000/api";

const appMode = ref("study");
const chapters = ref([]);
const difficulty = ref("");
const examYears = ref([]);
const selectedYear = ref("");
const selectedLanguage = ref("python");
const selectedTemplateMode = ref("leetcode");
const selectedTheme = ref("light");
const activeChapterId = ref(null);
const activeChapterTitle = ref("请选择左侧章节");
const activeChapterSummary = ref("章节摘要会显示在这里。");
const activeTopics = ref([]);
const studyPlans = ref([]);
const searchKeyword = ref("");
const searchResults = ref([]);
const searchMessage = ref("");
const errorMessage = ref("");
const isLoadingDetail = ref(false);
const languageOptions = [
  { value: "python", label: "Python" },
  { value: "cpp", label: "C/C++" },
  { value: "java", label: "Java" },
];
const templateModeOptions = [
  { value: "leetcode", label: "LeetCode 模式" },
  { value: "nowcoder", label: "牛客网 ACM 模式" },
];
const languageLabelMap = {
  python: "Python",
  cpp: "C/C++",
  java: "Java",
};
const templateModeLabelMap = {
  leetcode: "LeetCode",
  nowcoder: "牛客 ACM",
};
const themeLabelMap = {
  light: "浅色",
  dark: "深色",
};
const STORAGE_KEYS = {
  appMode: "labelu_app_mode",
  language: "labelu_preferred_language",
  templateMode: "labelu_preferred_template_mode",
  difficulty: "labelu_preferred_difficulty",
  year: "labelu_preferred_exam_year",
  theme: "labelu_preferred_theme",
};

const filteredActiveTopics = computed(() => {
  if (!selectedYear.value) {
    return activeTopics.value;
  }
  const year = Number(selectedYear.value);
  return activeTopics.value.filter((topic) => (topic.exam_years || []).includes(year));
});

const difficultyToZh = (level) => {
  if (level === "easy") return "简单";
  if (level === "medium") return "中等";
  if (level === "hard") return "困难";
  return "未知";
};

const apiGet = async (path) => {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`请求失败：${response.status}`);
  }
  return response.json();
};

const applyTheme = (theme) => {
  if (typeof window === "undefined") {
    return;
  }
  document.documentElement.setAttribute("data-theme", theme);
};

const restorePreferences = () => {
  if (typeof window === "undefined") {
    return;
  }

  const savedLanguage = window.localStorage.getItem(STORAGE_KEYS.language);
  if (savedLanguage && languageOptions.some((item) => item.value === savedLanguage)) {
    selectedLanguage.value = savedLanguage;
  }

  const savedAppMode = window.localStorage.getItem(STORAGE_KEYS.appMode);
  if (savedAppMode && ["study", "admin"].includes(savedAppMode)) {
    appMode.value = savedAppMode;
  }

  const savedTemplateMode = window.localStorage.getItem(STORAGE_KEYS.templateMode);
  if (savedTemplateMode && templateModeOptions.some((item) => item.value === savedTemplateMode)) {
    selectedTemplateMode.value = savedTemplateMode;
  }

  const savedDifficulty = window.localStorage.getItem(STORAGE_KEYS.difficulty);
  if (savedDifficulty && ["easy", "medium", "hard"].includes(savedDifficulty)) {
    difficulty.value = savedDifficulty;
  }

  const savedYear = window.localStorage.getItem(STORAGE_KEYS.year);
  if (savedYear) {
    selectedYear.value = savedYear;
  }

  const savedTheme = window.localStorage.getItem(STORAGE_KEYS.theme);
  if (savedTheme && ["light", "dark"].includes(savedTheme)) {
    selectedTheme.value = savedTheme;
  }
  applyTheme(selectedTheme.value);
};

const getTemplateCodesByMode = (topic) => {
  const modes = topic.template_modes || {};
  const modeCodes = modes[selectedTemplateMode.value];
  if (modeCodes && Object.keys(modeCodes).length) {
    return modeCodes;
  }
  const fallbackCodes = topic.template_codes || {};
  if (Object.keys(fallbackCodes).length) {
    return fallbackCodes;
  }
  if (topic.template_code) {
    return { python: topic.template_code };
  }
  return {};
};

const getAvailableLanguages = (topic) => {
  const codes = getTemplateCodesByMode(topic);
  const keys = Object.keys(codes);
  if (!keys.length) {
    return "Python";
  }
  return keys.map((key) => languageLabelMap[key] || key).join("、");
};

const getTemplateCode = (topic) => {
  const codes = getTemplateCodesByMode(topic);
  const lang = selectedLanguage.value;
  const selectedCode = codes[lang];
  if (selectedCode) {
    return selectedCode;
  }
  const pythonCode = codes.python || topic.template_code || "";
  if (!pythonCode) {
    return "# 暂无模板代码";
  }
  if (lang === "python") {
    return pythonCode;
  }
  const modeLabel = templateModeLabelMap[selectedTemplateMode.value] || "当前模式";
  const fallbackPrefix =
    lang === "cpp"
      ? `// ${modeLabel}暂无 C/C++ 模板，以下展示 Python 版本`
      : `// ${modeLabel}暂无 Java 模板，以下展示 Python 版本`;
  return `${fallbackPrefix}\n${pythonCode}`;
};

const getPracticeLinks = (topic, platform) => {
  const links = topic.practice_links || {};
  const items = links[platform];
  if (!Array.isArray(items)) {
    return [];
  }
  return items.filter((item) => item && typeof item.title === "string" && typeof item.url === "string");
};

const loadChapterDetail = async (chapterId) => {
  isLoadingDetail.value = true;
  try {
    const chapter = await apiGet(`/chapters/${chapterId}/`);
    activeChapterId.value = chapter.id;
    activeChapterTitle.value = `${chapter.order}. ${chapter.title}`;
    activeChapterSummary.value = `${chapter.summary}（预计 ${chapter.estimated_hours} 小时）`;
    activeTopics.value = chapter.topics || [];
    errorMessage.value = "";
  } catch (error) {
    errorMessage.value = "章节详情加载失败，请检查后端接口。";
    console.error(error);
  } finally {
    isLoadingDetail.value = false;
  }
};

const loadChapters = async () => {
  try {
    const query = difficulty.value ? `?difficulty=${difficulty.value}` : "";
    const data = await apiGet(`/chapters/${query}`);
    chapters.value = data;

    if (!data.length) {
      activeChapterId.value = null;
      activeChapterTitle.value = "暂无章节";
      activeChapterSummary.value = "当前筛选条件下没有可展示内容。";
      activeTopics.value = [];
      return;
    }

    const stillExists = data.some((chapter) => chapter.id === activeChapterId.value);
    const targetId = stillExists && activeChapterId.value ? activeChapterId.value : data[0].id;
    await loadChapterDetail(targetId);
  } catch (error) {
    errorMessage.value = "后端连接失败，请先启动 Django 服务（http://127.0.0.1:8000）。";
    console.error(error);
  }
};

const loadStudyPlans = async () => {
  try {
    studyPlans.value = await apiGet("/study-plans/");
  } catch (error) {
    errorMessage.value = "学习计划加载失败，请检查后端接口。";
    console.error(error);
  }
};

const loadExamYears = async () => {
  try {
    examYears.value = await apiGet("/exam-years/");
  } catch (error) {
    errorMessage.value = "年份索引加载失败，请检查后端接口。";
    console.error(error);
  }
};

const searchTopics = async () => {
  const keyword = searchKeyword.value.trim();
  searchResults.value = [];
  searchMessage.value = "";
  if (!keyword && !selectedYear.value) {
    searchMessage.value = "请输入关键词或选择真题年份后再搜索。";
    return;
  }

  try {
    const params = new URLSearchParams({ key_exam_only: "true" });
    if (keyword) {
      params.set("keyword", keyword);
    }
    if (selectedYear.value) {
      params.set("year", selectedYear.value);
    }
    const result = await apiGet(`/topics/?${params.toString()}`);
    searchResults.value = result;
    if (!result.length) {
      searchMessage.value = selectedYear.value
        ? `没有找到 ${selectedYear.value} 年的匹配知识点。`
        : "没有找到匹配知识点。";
    }
  } catch (error) {
    searchMessage.value = "搜索失败，请稍后重试。";
    console.error(error);
  }
};

const resetPreferences = async () => {
  if (typeof window !== "undefined") {
    window.localStorage.removeItem(STORAGE_KEYS.language);
    window.localStorage.removeItem(STORAGE_KEYS.templateMode);
    window.localStorage.removeItem(STORAGE_KEYS.difficulty);
    window.localStorage.removeItem(STORAGE_KEYS.year);
    window.localStorage.removeItem(STORAGE_KEYS.theme);
  }
  selectedLanguage.value = "python";
  selectedTemplateMode.value = "leetcode";
  difficulty.value = "";
  selectedYear.value = "";
  selectedTheme.value = "light";
  applyTheme("light");
  searchKeyword.value = "";
  searchResults.value = [];
  searchMessage.value = "已清空本地偏好与筛选条件。";
  await loadChapters();
};

const toggleTheme = () => {
  selectedTheme.value = selectedTheme.value === "dark" ? "light" : "dark";
};

watch(selectedLanguage, (value) => {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(STORAGE_KEYS.language, value);
});

watch(appMode, (value) => {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(STORAGE_KEYS.appMode, value);
});

watch(selectedTemplateMode, (value) => {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(STORAGE_KEYS.templateMode, value);
});

watch(difficulty, (value) => {
  if (typeof window === "undefined") return;
  if (!value) {
    window.localStorage.removeItem(STORAGE_KEYS.difficulty);
    return;
  }
  window.localStorage.setItem(STORAGE_KEYS.difficulty, value);
});

watch(selectedYear, (value) => {
  if (typeof window === "undefined") return;
  if (!value) {
    window.localStorage.removeItem(STORAGE_KEYS.year);
    return;
  }
  window.localStorage.setItem(STORAGE_KEYS.year, value);
});

watch(selectedTheme, (value) => {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(STORAGE_KEYS.theme, value);
  applyTheme(value);
});

onMounted(async () => {
  restorePreferences();
  await Promise.all([loadChapters(), loadStudyPlans(), loadExamYears()]);
});
</script>
