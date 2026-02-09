from django.core.management.base import BaseCommand

from algonotes.models import Chapter, ProblemTag, StudyPlan, Topic


CHAPTERS = [
    {"key": "intro", "title": "算法基础与机试技巧", "summary": "复杂度评估 + 机试输入输出模板。", "order": 1, "difficulty": "easy", "estimated_hours": 6},
    {"key": "array", "title": "数组、前缀和与双指针", "summary": "双指针、滑动窗口、前缀和是线性结构拿分核心。", "order": 2, "difficulty": "easy", "estimated_hours": 14},
    {"key": "linked", "title": "链表专题", "summary": "链表操作与快慢指针是复试高频。", "order": 3, "difficulty": "medium", "estimated_hours": 12},
    {"key": "stack", "title": "栈、队列与单调结构", "summary": "单调栈/队列模板必须熟练。", "order": 4, "difficulty": "medium", "estimated_hours": 12},
    {"key": "string", "title": "哈希、字符串与 KMP", "summary": "字符串匹配与哈希统计常在机试出现。", "order": 5, "difficulty": "medium", "estimated_hours": 14},
    {"key": "binary", "title": "二分查找与分治", "summary": "边界二分和答案二分是稳定得分点。", "order": 6, "difficulty": "medium", "estimated_hours": 10},
    {"key": "tree", "title": "二叉树与二叉搜索树", "summary": "树遍历与 LCA 是复试常问。", "order": 7, "difficulty": "medium", "estimated_hours": 18},
    {"key": "graph", "title": "图论基础与并查集", "summary": "拓扑、并查集、最短路覆盖图论主干。", "order": 8, "difficulty": "hard", "estimated_hours": 20},
    {"key": "search", "title": "回溯与搜索剪枝", "summary": "回溯题关键在剪枝与状态恢复。", "order": 9, "difficulty": "hard", "estimated_hours": 14},
    {"key": "greedy", "title": "贪心算法", "summary": "局部最优策略与正确性证明。", "order": 10, "difficulty": "medium", "estimated_hours": 10},
    {"key": "dp1", "title": "动态规划基础", "summary": "状态定义、转移方程和滚动优化。", "order": 11, "difficulty": "hard", "estimated_hours": 22},
    {"key": "dp2", "title": "背包与进阶动态规划", "summary": "背包、区间 DP、状态压缩。", "order": 12, "difficulty": "hard", "estimated_hours": 22},
    {"key": "math", "title": "数学、位运算与数论", "summary": "快速幂、gcd 与位运算技巧。", "order": 13, "difficulty": "medium", "estimated_hours": 10},
    {"key": "sprint", "title": "真题复盘与冲刺策略", "summary": "真题复盘、错题归类、机试冲刺。", "order": 14, "difficulty": "easy", "estimated_hours": 8},
]


TOPICS = [
    {
        "chapter": "intro",
        "title": "时间复杂度与空间复杂度评估",
        "knowledge_point": "大 O、最坏复杂度、规模估算",
        "note": "先根据数据规模估算可接受复杂度，再选算法。\n机试中 n=1e5 一般要求 O(nlogn) 或更优。",
        "template_code": "def complexity_hint(n):\n    return 'O(nlogn)可行' if n <= 10**5 else '优先O(n)'",
        "exam_tip": "做题第一步先估复杂度，避免写完才发现超时。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "intro",
        "title": "Python 机试输入输出模板",
        "knowledge_point": "sys.stdin、快速读取、多组输入",
        "note": "统一写 read_ints 模板可以显著减少读题失误。\n注意处理空行与多组样例。",
        "template_code": "import sys\n\ndef read_ints():\n    return list(map(int, sys.stdin.readline().split()))",
        "exam_tip": "先写输入框架再写算法，提交更稳。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "array",
        "title": "双指针模板（有序数组）",
        "knowledge_point": "左右指针、收缩策略、去重",
        "note": "双指针适合单调推进问题，常用于两数和、三数和、去重场景。",
        "template_code": "def two_sum_sorted(nums, target):\n    l, r = 0, len(nums) - 1\n    while l < r:\n        s = nums[l] + nums[r]\n        if s == target: return [l, r]\n        l, r = (l + 1, r) if s < target else (l, r - 1)\n    return []",
        "exam_tip": "指针移动必须有单调依据。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "array",
        "title": "滑动窗口（变长）",
        "knowledge_point": "窗口扩张、收缩时机、答案更新",
        "note": "窗口题核心是何时收缩。\n常见于最短子数组、最小覆盖子串。",
        "template_code": "def min_sub_len(nums, k):\n    left = s = 0\n    ans = float('inf')\n    for right, x in enumerate(nums):\n        s += x\n        while s >= k:\n            ans = min(ans, right - left + 1)\n            s -= nums[left]; left += 1\n    return 0 if ans == float('inf') else ans",
        "exam_tip": "窗口题易错点是更新答案时机。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "array",
        "title": "前缀和与子数组统计",
        "knowledge_point": "prefix、哈希计数、子数组和为 k",
        "note": "子数组和问题常可转为前缀和差值问题。",
        "template_code": "from collections import defaultdict\n\ndef subarray_sum(nums, k):\n    pre = ans = 0\n    cnt = defaultdict(int); cnt[0] = 1\n    for x in nums:\n        pre += x\n        ans += cnt[pre - k]\n        cnt[pre] += 1\n    return ans",
        "exam_tip": "初始化 cnt[0]=1 是高频细节。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "linked",
        "title": "反转链表（迭代）",
        "knowledge_point": "prev-cur-next 三指针",
        "note": "反转链表是链表题母题，指针重连必须一步不丢链。",
        "template_code": "def reverse_list(head):\n    prev, cur = None, head\n    while cur:\n        nxt = cur.next\n        cur.next = prev\n        prev, cur = cur, nxt\n    return prev",
        "exam_tip": "复试面试常要求口述每一步指针变化。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "linked",
        "title": "快慢指针找环入口",
        "knowledge_point": "Floyd 判圈、相遇点性质",
        "note": "相遇后一个指针回头，二者等速再次相遇点即环入口。",
        "template_code": "def detect_cycle(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow, fast = slow.next, fast.next.next\n        if slow == fast:\n            p1, p2 = head, slow\n            while p1 != p2:\n                p1, p2 = p1.next, p2.next\n            return p1\n    return None",
        "exam_tip": "先判空再访问 fast.next。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "stack",
        "title": "单调栈（下一个更大元素）",
        "knowledge_point": "单调性维护、下标入栈",
        "note": "出现“下一个更大/更小”时优先考虑单调栈。",
        "template_code": "def next_greater(nums):\n    ans = [-1] * len(nums)\n    st = []\n    for i, x in enumerate(nums):\n        while st and nums[st[-1]] < x:\n            ans[st.pop()] = x\n        st.append(i)\n    return ans",
        "exam_tip": "栈里放下标而不是值，便于回填答案。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "stack",
        "title": "单调队列（滑窗最大值）",
        "knowledge_point": "队首合法性、队尾弹出",
        "note": "单调队列可将滑窗最值降到 O(n)。",
        "template_code": "from collections import deque\n\ndef max_window(nums, k):\n    q, ans = deque(), []\n    for i, x in enumerate(nums):\n        while q and nums[q[-1]] <= x: q.pop()\n        q.append(i)\n        if q[0] <= i - k: q.popleft()\n        if i >= k - 1: ans.append(nums[q[0]])\n    return ans",
        "exam_tip": "按固定顺序写：入队 -> 去过期 -> 记录答案。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "string",
        "title": "哈希计数与异位词判断",
        "knowledge_point": "Counter、频次比较、set 去重",
        "note": "字符统计题首选哈希计数。",
        "template_code": "from collections import Counter\n\ndef is_anagram(s, t):\n    return Counter(s) == Counter(t)",
        "exam_tip": "固定字符集可用长度 26 数组优化常数。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "string",
        "title": "KMP 模式匹配",
        "knowledge_point": "next 数组、失配回退",
        "note": "KMP 本质是利用前后缀信息避免主串回退。",
        "template_code": "def build_next(p):\n    nxt, j = [0] * len(p), 0\n    for i in range(1, len(p)):\n        while j > 0 and p[i] != p[j]: j = nxt[j - 1]\n        if p[i] == p[j]: j += 1\n        nxt[i] = j\n    return nxt",
        "exam_tip": "先背 next 构造，再写匹配流程。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "binary",
        "title": "二分查找边界模板",
        "knowledge_point": "左闭右开、lower_bound、循环不变量",
        "note": "建议固定左闭右开模板，降低边界错误。",
        "template_code": "def lower_bound(nums, target):\n    l, r = 0, len(nums)\n    while l < r:\n        m = (l + r) // 2\n        if nums[m] < target: l = m + 1\n        else: r = m\n    return l",
        "exam_tip": "统一模板比“临场写新”更可靠。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "binary",
        "title": "答案二分（最小可行值）",
        "knowledge_point": "可行性函数、单调性",
        "note": "当答案具备单调性时，用 check(mid) + 二分。",
        "template_code": "def binary_answer(l, r, check):\n    while l < r:\n        m = (l + r) // 2\n        if check(m): r = m\n        else: l = m + 1\n    return l",
        "exam_tip": "先写 check，再写二分壳子。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "tree",
        "title": "二叉树 DFS 递归模板",
        "knowledge_point": "前中后序、递归定义、子树思维",
        "note": "树题先明确递归函数返回值，再写递归逻辑。",
        "template_code": "def preorder(root, ans):\n    if not root: return\n    ans.append(root.val)\n    preorder(root.left, ans)\n    preorder(root.right, ans)",
        "exam_tip": "先把前中后序默写熟练再刷综合题。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "tree",
        "title": "最近公共祖先 LCA",
        "knowledge_point": "后序返回、左右子树命中",
        "note": "若左右子树分别命中目标节点，当前节点即 LCA。",
        "template_code": "def lca(root, p, q):\n    if not root or root == p or root == q: return root\n    left, right = lca(root.left, p, q), lca(root.right, p, q)\n    if left and right: return root\n    return left or right",
        "exam_tip": "复试常问“为什么这样返回就是祖先”。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "graph",
        "title": "拓扑排序（Kahn）",
        "knowledge_point": "入度数组、队列、DAG",
        "note": "依赖关系题优先想到拓扑排序。",
        "template_code": "from collections import deque\n\ndef topo(n, edges):\n    g = [[] for _ in range(n)]\n    indeg = [0] * n\n    for u, v in edges:\n        g[u].append(v); indeg[v] += 1\n    q = deque([i for i in range(n) if indeg[i] == 0])\n    ans = []\n    while q:\n        u = q.popleft(); ans.append(u)\n        for v in g[u]:\n            indeg[v] -= 1\n            if indeg[v] == 0: q.append(v)\n    return ans if len(ans) == n else []",
        "exam_tip": "输出数量小于 n 说明图有环。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "graph",
        "title": "并查集模板",
        "knowledge_point": "路径压缩、连通性判定",
        "note": "并查集适用于动态连通块问题。",
        "template_code": "class DSU:\n    def __init__(self, n):\n        self.p = list(range(n))\n    def find(self, x):\n        if self.p[x] != x: self.p[x] = self.find(self.p[x])\n        return self.p[x]\n    def union(self, a, b):\n        pa, pb = self.find(a), self.find(b)\n        if pa == pb: return False\n        self.p[pb] = pa\n        return True",
        "exam_tip": "并查集是图题降维工具。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "graph",
        "title": "Dijkstra 最短路",
        "knowledge_point": "堆优化、松弛、非负权",
        "note": "单源最短路常用 Dijkstra（边权非负）。",
        "template_code": "import heapq\n\ndef dijkstra(n, g, s):\n    dist = [float('inf')] * n\n    dist[s] = 0\n    h = [(0, s)]\n    while h:\n        d, u = heapq.heappop(h)\n        if d > dist[u]: continue\n        for v, w in g[u]:\n            nd = d + w\n            if nd < dist[v]:\n                dist[v] = nd\n                heapq.heappush(h, (nd, v))\n    return dist",
        "exam_tip": "有负权边时不能用 Dijkstra。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "search",
        "title": "回溯模板（子集/组合）",
        "knowledge_point": "路径、选择、撤销选择",
        "note": "回溯是深度优先 + 状态恢复。",
        "template_code": "def subsets(nums):\n    ans, path = [], []\n    def dfs(i):\n        ans.append(path[:])\n        for j in range(i, len(nums)):\n            path.append(nums[j])\n            dfs(j + 1)\n            path.pop()\n    dfs(0)\n    return ans",
        "exam_tip": "画决策树后再写代码，正确率更高。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "greedy",
        "title": "区间调度贪心",
        "knowledge_point": "按右端点排序、最优选择",
        "note": "区间不重叠最大数量：优先选择右端点最小区间。",
        "template_code": "def interval_select(intervals):\n    intervals.sort(key=lambda x: x[1])\n    end, count = float('-inf'), 0\n    for s, e in intervals:\n        if s >= end:\n            end, count = e, count + 1\n    return count",
        "exam_tip": "贪心题要能解释为什么排序策略正确。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "greedy",
        "title": "跳跃游戏",
        "knowledge_point": "最远可达边界、线性扫描",
        "note": "维护 far 表示当前最远可达位置。",
        "template_code": "def can_jump(nums):\n    far = 0\n    for i, x in enumerate(nums):\n        if i > far: return False\n        far = max(far, i + x)\n    return True",
        "exam_tip": "覆盖类题常可转成边界更新问题。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "dp1",
        "title": "线性 DP（打家劫舍）",
        "knowledge_point": "状态定义、滚动数组",
        "note": "dp[i]=max(dp[i-1],dp[i-2]+nums[i])。",
        "template_code": "def rob(nums):\n    a = b = 0\n    for x in nums:\n        a, b = b, max(b, a + x)\n    return b",
        "exam_tip": "先讲状态含义，再讲转移。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "dp1",
        "title": "最长递增子序列 LIS",
        "knowledge_point": "贪心 + 二分、tails 数组",
        "note": "LIS 可由 O(n^2) 优化到 O(nlogn)。",
        "template_code": "import bisect\n\ndef lis(nums):\n    tails = []\n    for x in nums:\n        i = bisect.bisect_left(tails, x)\n        if i == len(tails): tails.append(x)\n        else: tails[i] = x\n    return len(tails)",
        "exam_tip": "tails 不是实际序列，只是最优末尾集合。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "dp1",
        "title": "最长公共子序列 LCS",
        "knowledge_point": "二维 DP、字符匹配转移",
        "note": "经典二维 DP，常作为状态定义考点。",
        "template_code": "def lcs(a, b):\n    m, n = len(a), len(b)\n    dp = [[0]*(n+1) for _ in range(m+1)]\n    for i in range(1, m+1):\n        for j in range(1, n+1):\n            dp[i][j] = dp[i-1][j-1] + 1 if a[i-1]==b[j-1] else max(dp[i-1][j], dp[i][j-1])\n    return dp[m][n]",
        "exam_tip": "注意下标偏移：字符 i-1 对应 dp 第 i 行。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "dp2",
        "title": "0-1 背包模板",
        "knowledge_point": "容量倒序、选与不选",
        "note": "一维优化时容量必须倒序遍历。",
        "template_code": "def knapsack_01(w, v, cap):\n    dp = [0] * (cap + 1)\n    for i in range(len(w)):\n        for c in range(cap, w[i] - 1, -1):\n            dp[c] = max(dp[c], dp[c - w[i]] + v[i])\n    return dp[cap]",
        "exam_tip": "0-1 背包倒序，完全背包正序。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "dp2",
        "title": "完全背包（方案计数）",
        "knowledge_point": "容量正序、组合计数",
        "note": "硬币兑换类常用完全背包。",
        "template_code": "def coin_change_count(coins, amount):\n    dp = [0] * (amount + 1)\n    dp[0] = 1\n    for coin in coins:\n        for s in range(coin, amount + 1):\n            dp[s] += dp[s - coin]\n    return dp[amount]",
        "exam_tip": "问组合数时先物品后容量。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "dp2",
        "title": "区间 DP（回文子序列）",
        "knowledge_point": "区间长度枚举、左右转移",
        "note": "区间 DP 关键是遍历顺序：短区间到长区间。",
        "template_code": "def lps(s):\n    n = len(s)\n    dp = [[0]*n for _ in range(n)]\n    for i in range(n - 1, -1, -1):\n        dp[i][i] = 1\n        for j in range(i + 1, n):\n            dp[i][j] = dp[i + 1][j - 1] + 2 if s[i] == s[j] else max(dp[i + 1][j], dp[i][j - 1])\n    return dp[0][n - 1]",
        "exam_tip": "区间 DP 常卡在循环顺序，必须先画依赖关系。",
        "is_key_for_exam": False,
    },
    {
        "chapter": "math",
        "title": "快速幂（取模）",
        "knowledge_point": "二进制拆幂、快速乘法",
        "note": "大指数取模几乎都要用快速幂。",
        "template_code": "def qpow(a, b, mod):\n    ans = 1\n    a %= mod\n    while b:\n        if b & 1: ans = ans * a % mod\n        a = a * a % mod\n        b >>= 1\n    return ans",
        "exam_tip": "中间过程也要取模。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "math",
        "title": "gcd 与位运算 lowbit",
        "knowledge_point": "欧几里得算法、x&-x",
        "note": "gcd 处理整除关系，lowbit 处理二进制最低位 1。",
        "template_code": "def gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a\n\ndef lowbit(x):\n    return x & -x",
        "exam_tip": "位运算题先写注释说明每一位语义。",
        "is_key_for_exam": True,
    },
    {
        "chapter": "sprint",
        "title": "真题复盘与冲刺流程",
        "knowledge_point": "错题标签、模板回写、模拟机试",
        "note": "按题型复盘比按日期复盘更有效。\n冲刺阶段每天固定“模板默写 + 限时机试”。",
        "template_code": "def review(problem, tag, reason, template):\n    return {'problem': problem, 'tag': tag, 'reason': reason, 'template': template}",
        "exam_tip": "冲刺期优先保分题，难题控制投入时长。",
        "is_key_for_exam": True,
    },
]


TOPIC_EXAM_YEARS = {
    "时间复杂度与空间复杂度评估": [2016, 2019, 2022, 2024],
    "Python 机试输入输出模板": [2017, 2020, 2023, 2025],
    "双指针模板（有序数组）": [2018, 2020, 2022, 2024],
    "滑动窗口（变长）": [2019, 2021, 2023, 2025],
    "前缀和与子数组统计": [2017, 2020, 2022, 2025],
    "反转链表（迭代）": [2016, 2018, 2021, 2024],
    "快慢指针找环入口": [2017, 2019, 2022, 2025],
    "单调栈（下一个更大元素）": [2018, 2021, 2023],
    "单调队列（滑窗最大值）": [2020, 2022, 2024],
    "哈希计数与异位词判断": [2016, 2019, 2021, 2023],
    "KMP 模式匹配": [2017, 2020, 2022, 2025],
    "二分查找边界模板": [2016, 2018, 2021, 2024],
    "答案二分（最小可行值）": [2019, 2022, 2023, 2025],
    "二叉树 DFS 递归模板": [2017, 2019, 2021, 2024],
    "最近公共祖先 LCA": [2018, 2020, 2022, 2025],
    "拓扑排序（Kahn）": [2019, 2021, 2023, 2025],
    "并查集模板": [2018, 2020, 2022, 2024],
    "Dijkstra 最短路": [2017, 2020, 2023, 2025],
    "回溯模板（子集/组合）": [2019, 2021, 2024],
    "区间调度贪心": [2016, 2018, 2022, 2024],
    "跳跃游戏": [2017, 2019, 2021, 2023],
    "线性 DP（打家劫舍）": [2018, 2020, 2022, 2025],
    "最长递增子序列 LIS": [2019, 2021, 2023, 2025],
    "最长公共子序列 LCS": [2017, 2020, 2022, 2024],
    "0-1 背包模板": [2016, 2018, 2021, 2023, 2025],
    "完全背包（方案计数）": [2017, 2019, 2022, 2024],
    "区间 DP（回文子序列）": [2020, 2023, 2025],
    "快速幂（取模）": [2016, 2019, 2022, 2025],
    "gcd 与位运算 lowbit": [2018, 2021, 2024],
    "真题复盘与冲刺流程": [2025],
}


CPP_TEMPLATE_LIBRARY = {
    "Python 机试输入输出模板": """
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; ++i) cin >> arr[i];
    long long sum = 0;
    for (int x : arr) sum += x;
    cout << sum << "\\n";
    return 0;
}
""",
    "双指针模板（有序数组）": """
vector<int> twoSumSorted(const vector<int>& nums, int target) {
    int left = 0, right = (int)nums.size() - 1;
    while (left < right) {
        int s = nums[left] + nums[right];
        if (s == target) return {left, right};
        if (s < target) ++left;
        else --right;
    }
    return {};
}
""",
    "滑动窗口（变长）": """
int minSubLen(const vector<int>& nums, int k) {
    int left = 0, sum = 0, ans = INT_MAX;
    for (int right = 0; right < (int)nums.size(); ++right) {
        sum += nums[right];
        while (sum >= k) {
            ans = min(ans, right - left + 1);
            sum -= nums[left++];
        }
    }
    return ans == INT_MAX ? 0 : ans;
}
""",
    "前缀和与子数组统计": """
int subarraySum(vector<int>& nums, int k) {
    unordered_map<int, int> cnt;
    cnt[0] = 1;
    int pre = 0, ans = 0;
    for (int x : nums) {
        pre += x;
        if (cnt.count(pre - k)) ans += cnt[pre - k];
        ++cnt[pre];
    }
    return ans;
}
""",
    "反转链表（迭代）": """
ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* cur = head;
    while (cur) {
        ListNode* nxt = cur->next;
        cur->next = prev;
        prev = cur;
        cur = nxt;
    }
    return prev;
}
""",
    "快慢指针找环入口": """
ListNode* detectCycle(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            ListNode *p1 = head, *p2 = slow;
            while (p1 != p2) {
                p1 = p1->next;
                p2 = p2->next;
            }
            return p1;
        }
    }
    return nullptr;
}
""",
    "单调栈（下一个更大元素）": """
vector<int> nextGreater(vector<int>& nums) {
    vector<int> ans(nums.size(), -1);
    stack<int> st;
    for (int i = 0; i < (int)nums.size(); ++i) {
        while (!st.empty() && nums[st.top()] < nums[i]) {
            ans[st.top()] = nums[i];
            st.pop();
        }
        st.push(i);
    }
    return ans;
}
""",
    "二分查找边界模板": """
int lowerBound(vector<int>& nums, int target) {
    int left = 0, right = nums.size();
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] < target) left = mid + 1;
        else right = mid;
    }
    return left;
}
""",
    "最近公共祖先 LCA": """
TreeNode* lca(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root || root == p || root == q) return root;
    TreeNode* left = lca(root->left, p, q);
    TreeNode* right = lca(root->right, p, q);
    if (left && right) return root;
    return left ? left : right;
}
""",
    "拓扑排序（Kahn）": """
vector<int> topo(int n, vector<vector<int>>& edges) {
    vector<vector<int>> g(n);
    vector<int> indeg(n, 0), ans;
    for (auto& e : edges) {
        g[e[0]].push_back(e[1]);
        ++indeg[e[1]];
    }
    queue<int> q;
    for (int i = 0; i < n; ++i) if (indeg[i] == 0) q.push(i);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        ans.push_back(u);
        for (int v : g[u]) {
            if (--indeg[v] == 0) q.push(v);
        }
    }
    return ans.size() == n ? ans : vector<int>{};
}
""",
    "并查集模板": """
struct DSU {
    vector<int> parent;
    DSU(int n): parent(n) { iota(parent.begin(), parent.end(), 0); }
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }
    bool unite(int a, int b) {
        int pa = find(a), pb = find(b);
        if (pa == pb) return false;
        parent[pb] = pa;
        return true;
    }
};
""",
    "Dijkstra 最短路": """
vector<long long> dijkstra(int n, vector<vector<pair<int,int>>>& g, int s) {
    const long long INF = (1LL << 60);
    vector<long long> dist(n, INF);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    dist[s] = 0;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto [v, w] : g[u]) {
            if (dist[v] > d + w) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
""",
    "线性 DP（打家劫舍）": """
int rob(vector<int>& nums) {
    int prev2 = 0, prev1 = 0;
    for (int x : nums) {
        int cur = max(prev1, prev2 + x);
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
""",
    "0-1 背包模板": """
int knapsack01(vector<int>& w, vector<int>& v, int cap) {
    vector<int> dp(cap + 1, 0);
    for (int i = 0; i < (int)w.size(); ++i) {
        for (int c = cap; c >= w[i]; --c) {
            dp[c] = max(dp[c], dp[c - w[i]] + v[i]);
        }
    }
    return dp[cap];
}
""",
    "快速幂（取模）": """
long long qpow(long long a, long long b, long long mod) {
    long long ans = 1 % mod;
    a %= mod;
    while (b) {
        if (b & 1) ans = ans * a % mod;
        a = a * a % mod;
        b >>= 1;
    }
    return ans;
}
""",
    "gcd 与位运算 lowbit": """
long long gcdll(long long a, long long b) {
    while (b) {
        long long t = a % b;
        a = b;
        b = t;
    }
    return a;
}

int lowbit(int x) {
    return x & -x;
}
""",
}


JAVA_TEMPLATE_LIBRARY = {
    "Python 机试输入输出模板": """
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String[] parts = br.readLine().trim().split("\\\\s+");
        long sum = 0;
        for (int i = 0; i < n; i++) sum += Integer.parseInt(parts[i]);
        System.out.println(sum);
    }
}
""",
    "双指针模板（有序数组）": """
int[] twoSumSorted(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    while (left < right) {
        int s = nums[left] + nums[right];
        if (s == target) return new int[]{left, right};
        if (s < target) left++;
        else right--;
    }
    return new int[0];
}
""",
    "滑动窗口（变长）": """
int minSubLen(int[] nums, int k) {
    int left = 0, sum = 0, ans = Integer.MAX_VALUE;
    for (int right = 0; right < nums.length; right++) {
        sum += nums[right];
        while (sum >= k) {
            ans = Math.min(ans, right - left + 1);
            sum -= nums[left++];
        }
    }
    return ans == Integer.MAX_VALUE ? 0 : ans;
}
""",
    "前缀和与子数组统计": """
int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> cnt = new HashMap<>();
    cnt.put(0, 1);
    int pre = 0, ans = 0;
    for (int x : nums) {
        pre += x;
        ans += cnt.getOrDefault(pre - k, 0);
        cnt.put(pre, cnt.getOrDefault(pre, 0) + 1);
    }
    return ans;
}
""",
    "反转链表（迭代）": """
ListNode reverseList(ListNode head) {
    ListNode prev = null, cur = head;
    while (cur != null) {
        ListNode nxt = cur.next;
        cur.next = prev;
        prev = cur;
        cur = nxt;
    }
    return prev;
}
""",
    "快慢指针找环入口": """
ListNode detectCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {
            ListNode p1 = head, p2 = slow;
            while (p1 != p2) {
                p1 = p1.next;
                p2 = p2.next;
            }
            return p1;
        }
    }
    return null;
}
""",
    "单调栈（下一个更大元素）": """
int[] nextGreater(int[] nums) {
    int n = nums.length;
    int[] ans = new int[n];
    Arrays.fill(ans, -1);
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && nums[stack.peek()] < nums[i]) {
            ans[stack.pop()] = nums[i];
        }
        stack.push(i);
    }
    return ans;
}
""",
    "二分查找边界模板": """
int lowerBound(int[] nums, int target) {
    int left = 0, right = nums.length;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] < target) left = mid + 1;
        else right = mid;
    }
    return left;
}
""",
    "最近公共祖先 LCA": """
TreeNode lca(TreeNode root, TreeNode p, TreeNode q) {
    if (root == null || root == p || root == q) return root;
    TreeNode left = lca(root.left, p, q);
    TreeNode right = lca(root.right, p, q);
    if (left != null && right != null) return root;
    return left != null ? left : right;
}
""",
    "拓扑排序（Kahn）": """
List<Integer> topo(int n, int[][] edges) {
    List<List<Integer>> g = new ArrayList<>();
    for (int i = 0; i < n; i++) g.add(new ArrayList<>());
    int[] indeg = new int[n];
    for (int[] e : edges) {
        g.get(e[0]).add(e[1]);
        indeg[e[1]]++;
    }
    Deque<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q.offer(i);
    List<Integer> ans = new ArrayList<>();
    while (!q.isEmpty()) {
        int u = q.poll();
        ans.add(u);
        for (int v : g.get(u)) {
            if (--indeg[v] == 0) q.offer(v);
        }
    }
    return ans.size() == n ? ans : Collections.emptyList();
}
""",
    "并查集模板": """
class DSU {
    int[] parent;
    DSU(int n) {
        parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }
    boolean union(int a, int b) {
        int pa = find(a), pb = find(b);
        if (pa == pb) return false;
        parent[pb] = pa;
        return true;
    }
}
""",
    "Dijkstra 最短路": """
long[] dijkstra(List<int[]>[] g, int s) {
    int n = g.length;
    long INF = Long.MAX_VALUE / 4;
    long[] dist = new long[n];
    Arrays.fill(dist, INF);
    dist[s] = 0;
    PriorityQueue<long[]> pq = new PriorityQueue<>(Comparator.comparingLong(a -> a[0]));
    pq.offer(new long[]{0, s});
    while (!pq.isEmpty()) {
        long[] cur = pq.poll();
        long d = cur[0];
        int u = (int) cur[1];
        if (d > dist[u]) continue;
        for (int[] edge : g[u]) {
            int v = edge[0], w = edge[1];
            if (dist[v] > d + w) {
                dist[v] = d + w;
                pq.offer(new long[]{dist[v], v});
            }
        }
    }
    return dist;
}
""",
    "线性 DP（打家劫舍）": """
int rob(int[] nums) {
    int prev2 = 0, prev1 = 0;
    for (int x : nums) {
        int cur = Math.max(prev1, prev2 + x);
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
""",
    "0-1 背包模板": """
int knapsack01(int[] w, int[] v, int cap) {
    int[] dp = new int[cap + 1];
    for (int i = 0; i < w.length; i++) {
        for (int c = cap; c >= w[i]; c--) {
            dp[c] = Math.max(dp[c], dp[c - w[i]] + v[i]);
        }
    }
    return dp[cap];
}
""",
    "快速幂（取模）": """
long qpow(long a, long b, long mod) {
    long ans = 1 % mod;
    a %= mod;
    while (b > 0) {
        if ((b & 1) == 1) ans = ans * a % mod;
        a = a * a % mod;
        b >>= 1;
    }
    return ans;
}
""",
    "gcd 与位运算 lowbit": """
long gcd(long a, long b) {
    while (b != 0) {
        long t = a % b;
        a = b;
        b = t;
    }
    return a;
}

int lowbit(int x) {
    return x & -x;
}
""",
}


def build_template_codes(topic_title, python_code):
    template_codes = {"python": python_code}
    cpp_code = CPP_TEMPLATE_LIBRARY.get(topic_title)
    java_code = JAVA_TEMPLATE_LIBRARY.get(topic_title)
    if cpp_code:
        template_codes["cpp"] = cpp_code.strip()
    if java_code:
        template_codes["java"] = java_code.strip()
    return template_codes


def build_nowcoder_python(code):
    stripped = code.strip()
    if "if __name__ == \"__main__\"" in stripped or "if __name__ == '__main__'" in stripped:
        return stripped
    return (
        "import sys\n\n"
        f"{stripped}\n\n"
        "def solve_case(tokens, index):\n"
        "    \"\"\"按题目格式解析单组数据，返回 (new_index, output_str)。\"\"\"\n"
        "    # 示例：\n"
        "    # n = int(tokens[index]); index += 1\n"
        "    # nums = list(map(int, tokens[index:index + n])); index += n\n"
        "    # ans = your_function(nums)\n"
        "    # return index, str(ans)\n"
        "    return index, \"\"\n\n"
        "def solve():\n"
        "    tokens = sys.stdin.buffer.read().split()\n"
        "    if not tokens:\n"
        "        return\n"
        "    index = 0\n"
        "    outputs = []\n"
        "    while index < len(tokens):\n"
        "        next_index, out = solve_case(tokens, index)\n"
        "        if next_index <= index:\n"
        "            break\n"
        "        index = next_index\n"
        "        if out != \"\":\n"
        "            outputs.append(str(out))\n"
        "    if outputs:\n"
        "        sys.stdout.write(\"\\n\".join(outputs))\n\n"
        "if __name__ == \"__main__\":\n"
        "    solve()"
    )


def build_nowcoder_cpp(code):
    stripped = code.strip()
    if "int main(" in stripped:
        return stripped
    return (
        "#include <bits/stdc++.h>\n"
        "using namespace std;\n\n"
        f"{stripped}\n\n"
        "bool solveCase(istream& in, string& out) {\n"
        "    // TODO: 按题目读取一组数据；读取失败时返回 false\n"
        "    // 示例：int n; if (!(in >> n)) return false;\n"
        "    // out = to_string(answer);\n"
        "    return false;\n"
        "}\n\n"
        "int main() {\n"
        "    ios::sync_with_stdio(false);\n"
        "    cin.tie(nullptr);\n\n"
        "    string out;\n"
        "    bool firstLine = true;\n"
        "    while (solveCase(cin, out)) {\n"
        "        if (!firstLine) cout << '\\n';\n"
        "        firstLine = false;\n"
        "        cout << out;\n"
        "    }\n"
        "    return 0;\n"
        "}"
    )


def build_nowcoder_java(code):
    stripped = code.strip()
    if "public class Main" in stripped or "public static void main(String[] args)" in stripped:
        return stripped
    indented_code = "\n".join(f"    {line}" if line else "" for line in stripped.splitlines())
    return (
        "import java.io.*;\n"
        "import java.util.*;\n\n"
        "public class Main {\n"
        "    static class FastScanner {\n"
        "        private final InputStream in;\n"
        "        private final byte[] buffer = new byte[1 << 16];\n"
        "        private int ptr = 0;\n"
        "        private int len = 0;\n\n"
        "        FastScanner(InputStream is) {\n"
        "            this.in = is;\n"
        "        }\n\n"
        "        private int read() throws IOException {\n"
        "            if (ptr >= len) {\n"
        "                len = in.read(buffer);\n"
        "                ptr = 0;\n"
        "                if (len <= 0) return -1;\n"
        "            }\n"
        "            return buffer[ptr++];\n"
        "        }\n\n"
        "        String next() throws IOException {\n"
        "            int c;\n"
        "            while ((c = read()) != -1 && c <= 32) {}\n"
        "            if (c == -1) return null;\n"
        "            StringBuilder sb = new StringBuilder();\n"
        "            while (c > 32) {\n"
        "                sb.append((char) c);\n"
        "                c = read();\n"
        "            }\n"
        "            return sb.toString();\n"
        "        }\n\n"
        "        Integer nextIntOrNull() throws IOException {\n"
        "            String s = next();\n"
        "            return s == null ? null : Integer.parseInt(s);\n"
        "        }\n\n"
        "        int nextInt() throws IOException {\n"
        "            return Integer.parseInt(next());\n"
        "        }\n\n"
        "        long nextLong() throws IOException {\n"
        "            return Long.parseLong(next());\n"
        "        }\n"
        "    }\n\n"
        f"{indented_code}\n\n"
        "    static String solveCase(FastScanner fs, Main solver) throws Exception {\n"
        "        // TODO: 按题目读取一组数据；读不到数据时返回 null\n"
        "        // 示例：Integer n = fs.nextIntOrNull(); if (n == null) return null;\n"
        "        // int[] nums = new int[n]; for (int i = 0; i < n; i++) nums[i] = fs.nextInt();\n"
        "        // return String.valueOf(solver.yourMethod(nums));\n"
        "        return null;\n"
        "    }\n\n"
        "    public static void main(String[] args) throws Exception {\n"
        "        FastScanner fs = new FastScanner(System.in);\n"
        "        Main solver = new Main();\n"
        "        StringBuilder out = new StringBuilder();\n"
        "        while (true) {\n"
        "            String line = solveCase(fs, solver);\n"
        "            if (line == null) break;\n"
        "            if (out.length() > 0) out.append('\\n');\n"
        "            out.append(line);\n"
        "        }\n"
        "        System.out.print(out);\n"
        "    }\n"
        "}"
    )


def build_template_modes(template_codes):
    leetcode_codes = dict(template_codes)
    nowcoder_codes = {}
    if "python" in leetcode_codes:
        nowcoder_codes["python"] = build_nowcoder_python(leetcode_codes["python"])
    if "cpp" in leetcode_codes:
        nowcoder_codes["cpp"] = build_nowcoder_cpp(leetcode_codes["cpp"])
    if "java" in leetcode_codes:
        nowcoder_codes["java"] = build_nowcoder_java(leetcode_codes["java"])
    return {
        "leetcode": leetcode_codes,
        "nowcoder": nowcoder_codes,
    }


CHAPTER_SOLVING_STEPS = {
    "intro": "先审题并估算 n 的数量级，再确定输入输出模板与可行复杂度上界。",
    "array": "先确认是否具备单调性/区间性质，再选择双指针、滑窗或前缀和。",
    "linked": "先画指针移动轨迹，保证每一步都可解释，再落地到 prev/cur/next 或快慢指针。",
    "stack": "识别“下一个更大/更小”或“区间最值”后，再确定是单调栈还是单调队列。",
    "string": "先判断是否是匹配/统计问题，再选择哈希计数或 KMP 前后缀逻辑。",
    "binary": "先证明单调性与边界，再套统一二分模板并检验循环不变量。",
    "tree": "先定义递归函数语义，再写左右子树合并逻辑并处理空节点。",
    "graph": "先明确图模型（有向/无向、权值），再选拓扑、并查集或最短路。",
    "search": "先确定状态与剪枝条件，再写“做选择-递归-撤销选择”骨架。",
    "greedy": "先证明局部最优策略，再用排序或边界推进实现。",
    "dp1": "先定义状态，再列转移方程，最后做初始化与滚动优化。",
    "dp2": "先确认背包/区间依赖方向，再严格控制遍历顺序。",
    "math": "先写数学结论与边界，再实现并验证取模/位运算细节。",
    "sprint": "先按题型分组复盘，再围绕错因进行二刷和计时训练。",
}

TOPIC_DETAIL_SUPPLEMENTS = {
    "反转链表（迭代）": (
        "【链表技巧补充】\n"
        "1. 建议先写出 `nxt = cur.next` 再改指针，避免链断。\n"
        "2. 面试常追问递归版，需能解释递归返回后如何回接。"
    ),
    "快慢指针找环入口": (
        "【链表技巧补充】\n"
        "1. 一快一慢相遇后，让一个指针回到头部并与慢指针同速前进。\n"
        "2. 两者再次相遇节点就是环入口，面试中要能说明数学推导。"
    ),
}

LEETCODE_LINK_LIBRARY = {
    "时间复杂度与空间复杂度评估": [{"title": "两数之和", "url": "https://leetcode.cn/problems/two-sum/"}],
    "Python 机试输入输出模板": [{"title": "Fizz Buzz（热身）", "url": "https://leetcode.cn/problems/fizz-buzz/"}],
    "双指针模板（有序数组）": [{"title": "两数之和 II", "url": "https://leetcode.cn/problems/two-sum-ii-input-array-is-sorted/"}],
    "滑动窗口（变长）": [{"title": "长度最小的子数组", "url": "https://leetcode.cn/problems/minimum-size-subarray-sum/"}],
    "前缀和与子数组统计": [{"title": "和为 K 的子数组", "url": "https://leetcode.cn/problems/subarray-sum-equals-k/"}],
    "反转链表（迭代）": [{"title": "反转链表", "url": "https://leetcode.cn/problems/reverse-linked-list/"}],
    "快慢指针找环入口": [{"title": "环形链表 II", "url": "https://leetcode.cn/problems/linked-list-cycle-ii/"}],
    "单调栈（下一个更大元素）": [{"title": "下一个更大元素 I", "url": "https://leetcode.cn/problems/next-greater-element-i/"}],
    "单调队列（滑窗最大值）": [{"title": "滑动窗口最大值", "url": "https://leetcode.cn/problems/sliding-window-maximum/"}],
    "哈希计数与异位词判断": [{"title": "有效的字母异位词", "url": "https://leetcode.cn/problems/valid-anagram/"}],
    "KMP 模式匹配": [{"title": "找出字符串中第一个匹配项", "url": "https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/"}],
    "二分查找边界模板": [{"title": "二分查找", "url": "https://leetcode.cn/problems/binary-search/"}],
    "答案二分（最小可行值）": [{"title": "分割数组的最大值", "url": "https://leetcode.cn/problems/split-array-largest-sum/"}],
    "二叉树 DFS 递归模板": [{"title": "二叉树前序遍历", "url": "https://leetcode.cn/problems/binary-tree-preorder-traversal/"}],
    "最近公共祖先 LCA": [{"title": "二叉树的最近公共祖先", "url": "https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/"}],
    "拓扑排序（Kahn）": [{"title": "课程表 II", "url": "https://leetcode.cn/problems/course-schedule-ii/"}],
    "并查集模板": [{"title": "冗余连接", "url": "https://leetcode.cn/problems/redundant-connection/"}],
    "Dijkstra 最短路": [{"title": "网络延迟时间", "url": "https://leetcode.cn/problems/network-delay-time/"}],
    "回溯模板（子集/组合）": [{"title": "子集", "url": "https://leetcode.cn/problems/subsets/"}],
    "区间调度贪心": [{"title": "无重叠区间", "url": "https://leetcode.cn/problems/non-overlapping-intervals/"}],
    "跳跃游戏": [{"title": "跳跃游戏", "url": "https://leetcode.cn/problems/jump-game/"}],
    "线性 DP（打家劫舍）": [{"title": "打家劫舍", "url": "https://leetcode.cn/problems/house-robber/"}],
    "最长递增子序列 LIS": [{"title": "最长递增子序列", "url": "https://leetcode.cn/problems/longest-increasing-subsequence/"}],
    "最长公共子序列 LCS": [{"title": "最长公共子序列", "url": "https://leetcode.cn/problems/longest-common-subsequence/"}],
    "0-1 背包模板": [{"title": "分割等和子集", "url": "https://leetcode.cn/problems/partition-equal-subset-sum/"}],
    "完全背包（方案计数）": [{"title": "零钱兑换 II", "url": "https://leetcode.cn/problems/coin-change-ii/"}],
    "区间 DP（回文子序列）": [{"title": "最长回文子序列", "url": "https://leetcode.cn/problems/longest-palindromic-subsequence/"}],
    "快速幂（取模）": [{"title": "Pow(x, n)", "url": "https://leetcode.cn/problems/powx-n/"}],
    "gcd 与位运算 lowbit": [{"title": "位1的个数", "url": "https://leetcode.cn/problems/number-of-1-bits/"}],
    "真题复盘与冲刺流程": [{"title": "LRU 缓存（冲刺综合）", "url": "https://leetcode.cn/problems/lru-cache/"}],
}


NOWCODER_LINK_LIBRARY = {
    "时间复杂度与空间复杂度评估": [{"title": "A+B（复杂度热身）", "url": "https://www.nowcoder.com/questionTerminal/93bc96f6d19f4795a4b893ee16e97654"}],
    "Python 机试输入输出模板": [{"title": "A+B(7)（ACM 多组输入）", "url": "https://www.nowcoder.com/questionTerminal/0c9d6d9b54d04f928896971648cb16b6"}],
    "双指针模板（有序数组）": [{"title": "两数之和", "url": "https://www.nowcoder.com/questionTerminal/20ef0972485e41019e39543e8e895b7f"}],
    "滑动窗口（变长）": [{"title": "和大于等于 K 的最短子数组", "url": "https://www.nowcoder.com/questionTerminal/3e1fd3d19fb0479d94652d49c7e1ead1"}],
    "前缀和与子数组统计": [{"title": "和为 K 的连续子数组", "url": "https://www.nowcoder.com/questionTerminal/704c8388a82e42e58b7f5751ec943a11"}],
    "反转链表（迭代）": [{"title": "反转链表", "url": "https://www.nowcoder.com/practice/75e878df47f24fdc9dc3e400ec6058ca"}],
    "快慢指针找环入口": [{"title": "链表中环的入口结点", "url": "https://www.nowcoder.com/questionTerminal/253d2c59ec3e4bc68da16833f79a38e4"}],
    "单调栈（下一个更大元素）": [{"title": "栈和排序（单调栈）", "url": "https://ac.nowcoder.com/acm/problem/14893"}],
    "单调队列（滑窗最大值）": [{"title": "滑动窗口的最大值", "url": "https://www.nowcoder.com/questionTerminal/1624bc35a45c42c0bc17d17fa0cba788"}],
    "哈希计数与异位词判断": [{"title": "字符串计数（哈希）", "url": "https://www.nowcoder.com/questionTerminal/7615ed51b7b94b9eadf0776146b4e23c"}],
    "KMP 模式匹配": [{"title": "KMP算法", "url": "https://www.nowcoder.com/questionTerminal/bb1615c381cc4237919d1aa448083bcc"}],
    "二分查找边界模板": [{"title": "二分查找-I", "url": "https://www.nowcoder.com/questionTerminal/d3df40bd23594118b57554129cadf47b"}],
    "答案二分（最小可行值）": [{"title": "分割数组（二分答案）", "url": "https://www.nowcoder.com/questionTerminal/7a41720ebed04f37bb015febda6a75cb"}],
    "二叉树 DFS 递归模板": [{"title": "实现二叉树先中后序遍历", "url": "https://www.nowcoder.com/questionTerminal/a9fec6c46a684ad5a3abd4e365a9d362"}],
    "最近公共祖先 LCA": [{"title": "无穷大二叉树的最近公共祖先", "url": "https://www.nowcoder.com/questionTerminal/d3ab2bff09cf4e89aaeb32a4380fb2c2"}],
    "拓扑排序（Kahn）": [{"title": "拓扑排序模板（检测循环依赖）", "url": "https://www.nowcoder.com/practice/88f7e15672314fcaa08ff95cb04f70a5"}],
    "并查集模板": [{"title": "最小生成树（并查集模板）", "url": "https://www.nowcoder.com/practice/735a34ff4672498b95660f43b7fcd628"}],
    "Dijkstra 最短路": [{"title": "最短路（Dijkstra）", "url": "https://www.nowcoder.com/practice/401cdf98e8494e0f99278e0f8104464d"}],
    "回溯模板（子集/组合）": [{"title": "分割等和子集（回溯/DP）", "url": "https://www.nowcoder.com/questionTerminal/0b18d3e11c8f4c5b833d2a9a43fa7772"}],
    "区间调度贪心": [{"title": "挑选代表（区间贪心）", "url": "https://www.nowcoder.com/questionTerminal/c563cc42459d49d5923b3460ba142cf8"}],
    "跳跃游戏": [{"title": "跳跃游戏(一)", "url": "https://www.nowcoder.com/practice/07484f4377344d3590045a095910992b"}],
    "线性 DP（打家劫舍）": [{"title": "打家劫舍(一)", "url": "https://www.nowcoder.com/practice/c5fbf7325fbd4c0ea3d0c3ea6bc6cc79"}],
    "最长递增子序列 LIS": [{"title": "最长递增子序列(一)", "url": "https://www.nowcoder.com/questionTerminal/d83721575bd4418eae76c916483493de"}],
    "最长公共子序列 LCS": [{"title": "最长公共子序列(一)", "url": "https://www.nowcoder.com/practice/672ab5e541c64e4b9d11f66011059498"}],
    "0-1 背包模板": [{"title": "购物单（0-1 背包）", "url": "https://www.nowcoder.com/practice/f9c6f980eeec43ef85be20755ddbeaf4"}],
    "完全背包（方案计数）": [{"title": "找零钱（完全背包）", "url": "https://www.nowcoder.com/questionTerminal/944e5ca0513f457d9d71dee1e404a11c"}],
    "区间 DP（回文子序列）": [{"title": "最长回文子串（区间 DP）", "url": "https://www.nowcoder.com/practice/b4525d1d84934cf280439aeecc36f4af"}],
    "快速幂（取模）": [{"title": "求逆元（快速幂取模）", "url": "https://ac.nowcoder.com/acm/problem/229004"}],
    "gcd 与位运算 lowbit": [
        {"title": "Modified GCD", "url": "https://www.nowcoder.com/questionTerminal/4ea812f6f88b4d4f8c7610f33fb5d0f3"},
        {"title": "lowbit 操作", "url": "https://ac.nowcoder.com/acm/problem/16745"},
    ],
    "真题复盘与冲刺流程": [{"title": "检测循环依赖（冲刺综合）", "url": "https://www.nowcoder.com/practice/8dc02aab397f41f7adffb53aa5500b54"}],
}


def build_practice_links(topic_title):
    leetcode_links = LEETCODE_LINK_LIBRARY.get(
        topic_title,
        [{"title": "LeetCode 算法题单", "url": "https://leetcode.cn/problemset/"}],
    )
    nowcoder_links = NOWCODER_LINK_LIBRARY.get(
        topic_title,
        [{"title": "牛客 ACM 题库", "url": "https://ac.nowcoder.com/acm/problemsets"}],
    )
    return {
        "leetcode": [dict(item) for item in leetcode_links],
        "nowcoder": [dict(item) for item in nowcoder_links],
    }


def build_detailed_note(topic):
    sections = [
        topic["note"].strip(),
        f"【考点拆解】{topic['knowledge_point']}",
        f"【标准解题流程】{CHAPTER_SOLVING_STEPS.get(topic['chapter'], '先明确题型与边界，再按模板实现。')}",
        "【复杂度检查】提交前明确时间复杂度和空间复杂度，并对照数据规模判断是否会超时。",
        f"【常见失分点】{topic.get('exam_tip', '注意边界、判空和下标偏移。')}",
        "【复习行动】同类题至少刷 2 题，记录“错因 + 修正方案 + 模板复盘”。",
    ]
    supplement = TOPIC_DETAIL_SUPPLEMENTS.get(topic["title"])
    if supplement:
        sections.append(supplement.strip())
    return "\n".join(part for part in sections if part)


STUDY_PLANS = [
    (1, "算法热身", "复杂度与机试模板", 12),
    (2, "线性结构 I", "数组、双指针、滑窗、前缀和", 14),
    (3, "线性结构 II", "链表、栈队列、单调结构", 15),
    (4, "字符串专题", "哈希统计、KMP", 14),
    (5, "二分分治", "边界二分、答案二分", 14),
    (6, "树专题", "DFS/BFS、LCA、BST", 16),
    (7, "图专题", "拓扑、并查集、最短路", 18),
    (8, "搜索回溯", "组合子集、剪枝", 16),
    (9, "贪心专题", "区间调度、跳跃游戏", 14),
    (10, "DP 基础", "线性 DP、LIS、LCS", 20),
    (11, "DP 进阶", "背包、区间 DP", 20),
    (12, "冲刺复盘", "真题二刷、错题清零", 18),
]


HOT100_TITLES = {
    "双指针模板（有序数组）",
    "滑动窗口（变长）",
    "反转链表（迭代）",
    "单调栈（下一个更大元素）",
    "最近公共祖先 LCA",
    "拓扑排序（Kahn）",
    "并查集模板",
    "Dijkstra 最短路",
    "线性 DP（打家劫舍）",
    "最长递增子序列 LIS",
    "0-1 背包模板",
}

TEMPLATE_KEYWORDS = ("模板", "二分", "KMP", "背包", "LCA", "并查集", "快速幂", "单调")
PITFALL_KEYWORDS = ("滑动窗口", "边界", "二分", "区间 DP", "LCS")
INTERVIEW_TITLES = {"反转链表（迭代）", "快慢指针找环入口", "最近公共祖先 LCA", "并查集模板", "Dijkstra 最短路"}


class Command(BaseCommand):
    help = "初始化考研算法笔记完整数据（章节 + 知识点 + 标签 + 学习计划）"

    def handle(self, *args, **options):
        ProblemTag.objects.all().delete()
        Topic.objects.all().delete()
        Chapter.objects.all().delete()
        StudyPlan.objects.all().delete()

        chapter_map = {}
        for chapter in CHAPTERS:
            chapter_map[chapter["key"]] = Chapter.objects.create(
                title=chapter["title"],
                summary=chapter["summary"],
                order=chapter["order"],
                difficulty=chapter["difficulty"],
                estimated_hours=chapter["estimated_hours"],
            )

        topics = []
        for topic in TOPICS:
            template_codes = build_template_codes(topic["title"], topic["template_code"])
            detailed_note = build_detailed_note(topic)
            practice_links = build_practice_links(topic["title"])
            topics.append(
                Topic.objects.create(
                    chapter=chapter_map[topic["chapter"]],
                    title=topic["title"],
                    knowledge_point=topic["knowledge_point"],
                    note=detailed_note,
                    template_code=topic["template_code"],
                    template_codes=template_codes,
                    template_modes=build_template_modes(template_codes),
                    practice_links=practice_links,
                    exam_tip=topic["exam_tip"],
                    exam_years=TOPIC_EXAM_YEARS.get(topic["title"], []),
                    is_key_for_exam=topic["is_key_for_exam"],
                )
            )

        tags = {
            "hot100": ProblemTag.objects.create(name="LeetCode Hot100", category="hot100"),
            "exam": ProblemTag.objects.create(name="408 机试高频", category="exam"),
            "wangdao": ProblemTag.objects.create(name="王道真题对应", category="exam"),
            "template": ProblemTag.objects.create(name="模板必背", category="template"),
            "pitfall": ProblemTag.objects.create(name="容易失分", category="exam"),
            "interview": ProblemTag.objects.create(name="复试面试高频", category="exam"),
        }

        for topic in topics:
            tags["exam"].topics.add(topic)
            tags["wangdao"].topics.add(topic)
            if topic.title in HOT100_TITLES:
                tags["hot100"].topics.add(topic)
            if any(keyword in topic.title for keyword in TEMPLATE_KEYWORDS):
                tags["template"].topics.add(topic)
            if any(keyword in topic.title for keyword in PITFALL_KEYWORDS):
                tags["pitfall"].topics.add(topic)
            if topic.title in INTERVIEW_TITLES:
                tags["interview"].topics.add(topic)

        for week, target, focus, hours in STUDY_PLANS:
            StudyPlan.objects.create(week=week, target=target, focus=focus, recommended_hours=hours)

        self.stdout.write(
            self.style.SUCCESS(
                f"初始化完成：{len(CHAPTERS)} 个章节，{len(topics)} 个知识点，{len(STUDY_PLANS)} 周学习计划。"
            )
        )
