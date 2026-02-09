# 考研算法笔记网站（Labelu）

前后端分离项目，面向考研 408 与复试机试：

- 后端：Django + DRF + MySQL
- 前端：Vue 3 + Vite
- 环境：`conda` 环境名 `labelu`

## 目录结构

```text
t10/
├─ backend/
│  ├─ manage.py
│  ├─ requirements.txt
│  ├─ labelu_backend/
│  └─ algonotes/
│     ├─ models.py
│     ├─ views.py
│     ├─ serializers.py
│     ├─ urls.py
│     └─ management/commands/seed_initial_data.py
	└─ frontend/
	   ├─ package.json
	   ├─ vite.config.js
	   └─ src/
	      ├─ main.js
	      ├─ App.vue
	      ├─ components/AdminPanel.vue
	      └─ style.css
```

## 后端启动（labelu 环境）

1. 激活环境并安装依赖

```powershell
conda activate labelu
cd backend
pip install -r requirements.txt
```

2. 创建数据库（你提供的 MySQL 账号）

- 用户：`root`
- 密码：`1314520Luo`

```sql
CREATE DATABASE IF NOT EXISTS labelu_algo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. 迁移并导入完整考研笔记数据

```powershell
python manage.py migrate
python manage.py seed_initial_data
```

4. 运行后端

```powershell
python manage.py runserver 127.0.0.1:8000
```

## 前端启动（Vue）

```powershell
cd frontend
npm install
npm run dev
```

访问：`http://127.0.0.1:5173`

## 主要接口

- `GET /api/chapters/`：章节列表
- `GET /api/chapters/<id>/`：章节详情（含知识点）
- `GET /api/topics/?keyword=背包&key_exam_only=true`：关键词搜索
- `GET /api/topics/?year=2023&key_exam_only=true`：按真题年份筛选
- `GET /api/exam-years/`：真题年份索引（年份 + 知识点数量）
- `GET /api/chapters/<id>/` 返回中包含 `template_modes`（LeetCode/牛客 ACM 双模式模板）
- `GET /api/chapters/<id>/` 返回中包含 `practice_links`（LeetCode/牛客逐题直链）

## 后台管理（内容增删改查）

### 1) Django Admin 后台

```powershell
cd backend
python manage.py runserver 127.0.0.1:8000
```

访问：`http://127.0.0.1:8000/admin/`

默认开发账号（本地）：

- 用户名：`admin`
- 密码：`admin123456`

如需重置为该默认账号，可执行：

```powershell
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','labelu_backend.settings'); import django; django.setup(); from django.contrib.auth import get_user_model; User=get_user_model(); u,_=User.objects.get_or_create(username='admin', defaults={'email':'admin@example.com','is_staff':True,'is_superuser':True,'is_active':True}); u.is_staff=True; u.is_superuser=True; u.is_active=True; u.set_password('admin123456'); u.save(); print('ok')"
```

可在后台直接管理：章节、知识点、标签、学习计划。

### 2) 管理 API（仅管理员可用）

新增管理接口（需要 `is_staff=True` 用户）：

- `GET/POST /api/manage/chapters/`
- `GET/PATCH/DELETE /api/manage/chapters/<id>/`
- `GET/POST /api/manage/topics/`
- `GET/PATCH/DELETE /api/manage/topics/<id>/`
- `GET/POST /api/manage/tags/`
- `GET/PATCH/DELETE /api/manage/tags/<id>/`
- `GET/POST /api/manage/study-plans/`
- `GET/PATCH/DELETE /api/manage/study-plans/<id>/`

列表接口支持后端分页与搜索（DRF）：

- 分页参数：`page`、`page_size`
- 搜索参数：`search`
- 示例：`GET /api/manage/topics/?page=2&page_size=10&search=并查集`

管理端 `Topic` 支持直接维护：

- `template_codes`（多语言模板）
- `template_modes`（LeetCode/牛客 ACM 双模式）
- `practice_links`（LeetCode/牛客逐题直链）
- `tags`（标签 ID 列表）

### 3) Vue 后台管理页面

- 前端右上角新增「学习模式 / 后台管理」切换按钮
- 进入「后台管理」后使用 Django 管理员账号登录
- 后台页面结构升级为「左侧资源菜单 + 右侧管理区」
- 右侧采用表格展示，并对接后端真分页（5/10/20 每页）与服务端关键字搜索
- 登录后可在页面内直接管理：
  - 章节（Chapter）
  - 知识点（Topic，含 `template_codes/template_modes` JSON）
  - 标签（ProblemTag）
  - 学习计划（StudyPlan）
- 登录状态与当前后台页签会保存在 `localStorage`

## 已覆盖的算法笔记模块

- 算法基础与机试技巧
- 数组、前缀和与双指针
- 链表专题
- 栈、队列与单调结构
- 哈希、字符串与 KMP
- 二分查找与分治
- 二叉树与二叉搜索树
- 图论基础与并查集
- 回溯与搜索剪枝
- 贪心算法
- 动态规划基础
- 背包与进阶动态规划
- 数学、位运算与数论
- 真题复盘与冲刺策略

## 408 真题年份索引

- 每个知识点都包含 `exam_years` 字段（对应 408 相关年份）
- 前端支持全局年份筛选（章节详情与搜索结果联动）
- 可用年份索引快速定位某一年的高频考点

## 代码模板切换（语言 + 模式）

- 前端支持按语言查看模板代码：`Python`、`C/C++`、`Java`
- 前端支持按模式切换：`LeetCode 模式`、`牛客网 ACM 模式`
- 牛客 ACM 模式模板已统一为机试骨架：多组输入循环、快速读入、按行输出
- 后端知识点包含 `template_modes` 字段，结构示例：

```json
{
  "leetcode": {
    "python": "...",
    "cpp": "...",
    "java": "..."
  },
  "nowcoder": {
    "python": "...",
    "cpp": "...",
    "java": "..."
  }
}
```

- 若当前模式下暂未提供所选语言模板，页面会自动回退显示 Python 版本并给出提示

## 知识点细化与题链

- 每个知识点会自动生成更细化的学习结构：
  - `【考点拆解】`
  - `【标准解题流程】`
  - `【复杂度检查】`
  - `【常见失分点】`
  - `【复习行动】`
- 链表相关知识点额外补充了“链表技巧补充”（参考 labuladong 链表技巧总结的思路）
- 每个知识点都包含 `practice_links` 字段，按平台分组（逐题精准直链）：

```json
{
  "leetcode": [
    { "title": "反转链表", "url": "https://leetcode.cn/problems/reverse-linked-list/" }
  ],
  "nowcoder": [
    { "title": "反转链表", "url": "https://www.nowcoder.com/practice/75e878df47f24fdc9dc3e400ec6058ca" }
  ]
}
```

## 本地偏好记忆（localStorage）

- 自动记忆并恢复：模板模式、代码语言、难度筛选、真题年份、主题模式
- 提供“重置偏好 / 清空本地偏好”按钮，一键恢复默认设置
- 重置后会同时清空当前筛选与搜索条件

## 深色模式

- 支持浅色/深色一键切换
- 主题选择会持久化到 `localStorage`
- 刷新页面后自动恢复上次主题

## UI 现代化优化

- 全局渐变背景与玻璃卡片风格（glassmorphism）
- 顶部操作区新增状态徽标与快捷重置按钮
- 章节页增加筛选状态胶囊标签与更清晰的信息层级
- 代码区视觉升级，提升跨语言阅读体验
