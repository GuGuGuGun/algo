<template>
  <section class="algo-demo">
    <template v-if="demo && currentFrame">
      <div class="demo-header">
        <div>
          <h4>{{ demo.name }} · 动画演示</h4>
          <p>{{ demo.description }}</p>
        </div>
        <div class="demo-controls">
          <button class="demo-btn" @click="prevFrame" :disabled="frameIndex === 0">上一步</button>
          <button class="demo-btn primary" @click="togglePlay" :disabled="totalFrames < 2">
            {{ isPlaying ? "暂停" : "自动播放" }}
          </button>
          <button class="demo-btn" @click="nextFrame" :disabled="frameIndex >= totalFrames - 1">下一步</button>
        </div>
      </div>

      <div class="demo-progress">
        <input type="range" min="0" :max="Math.max(totalFrames - 1, 0)" v-model.number="frameIndex" />
        <span>步骤 {{ frameIndex + 1 }} / {{ totalFrames }}</span>
      </div>

      <div v-if="currentFrame.kind === 'reverse'" class="demo-stage reverse-stage">
        <div class="reverse-lane">
          <span class="lane-title">已反转</span>
          <div class="node-line">
            <span v-for="(node, idx) in currentFrame.reversed" :key="`done-${idx}-${node}`" class="node done">{{ node }}</span>
            <span v-if="!currentFrame.reversed.length" class="node ghost">空</span>
          </div>
        </div>
        <div class="reverse-lane">
          <span class="lane-title">当前节点</span>
          <div class="node-line">
            <span v-if="currentFrame.current" class="node current">{{ currentFrame.current }}</span>
            <span v-else class="node ghost">无</span>
          </div>
        </div>
        <div class="reverse-lane">
          <span class="lane-title">待处理</span>
          <div class="node-line">
            <span v-for="(node, idx) in currentFrame.remaining" :key="`todo-${idx}-${node}`" class="node">{{ node }}</span>
            <span v-if="!currentFrame.remaining.length" class="node ghost">空</span>
          </div>
        </div>
      </div>

      <div v-else-if="currentFrame.kind === 'cycle'" class="demo-stage cycle-stage">
        <div class="node-line">
          <span
            v-for="(node, idx) in currentFrame.nodes"
            :key="`cycle-${idx}-${node}`"
            class="node"
            :class="{
              cycle: idx >= currentFrame.entry,
              slow: idx === currentFrame.slow,
              fast: idx === currentFrame.fast,
            }"
          >
            {{ node }}
            <em v-if="idx === currentFrame.slow">S</em>
            <em v-if="idx === currentFrame.fast">F</em>
          </span>
        </div>
        <p class="cycle-entry">环入口：{{ currentFrame.nodes[currentFrame.entry] }}</p>
      </div>

      <div v-else-if="currentFrame.kind === 'tree'" class="demo-stage tree-stage">
        <div v-for="(level, levelIdx) in currentFrame.levels" :key="`level-${levelIdx}`" class="tree-level">
          <span
            v-for="(node, idx) in level"
            :key="`tree-${levelIdx}-${idx}-${node}`"
            class="tree-node"
            :class="{
              active: (currentFrame.active || []).includes(node),
              target: node === currentFrame.target,
            }"
          >
            {{ node }}
          </span>
        </div>
      </div>

      <div v-else class="demo-stage array-stage">
        <div class="array-track">
          <div
            v-for="(value, idx) in currentFrame.values"
            :key="`arr-${idx}-${value}`"
            class="array-cell"
            :class="{
              left: idx === currentFrame.left,
              right: idx === currentFrame.right,
              mid: idx === currentFrame.mid,
              inside: currentFrame.kind === 'window' && idx >= currentFrame.left && idx <= currentFrame.right,
            }"
          >
            <span class="value">{{ value }}</span>
            <span class="index">{{ idx }}</span>
            <span v-if="idx === currentFrame.left" class="ptr ptr-left">L</span>
            <span v-if="idx === currentFrame.right" class="ptr ptr-right">R</span>
            <span v-if="idx === currentFrame.mid" class="ptr ptr-mid">M</span>
          </div>
        </div>
        <div class="metric-line" v-if="currentFrame.metric">
          <span v-for="(metric, idx) in currentFrame.metric" :key="`metric-${idx}`">{{ metric }}</span>
        </div>
      </div>

      <p class="demo-note">{{ currentFrame.note }}</p>
    </template>
    <template v-else>
      <div class="demo-header">
        <div>
          <h4>动画演示（筹备中）</h4>
          <p>当前知识点暂未配置动画，建议先按模板代码实操。</p>
        </div>
      </div>
      <p class="demo-note">已支持：{{ supportedTitles.join("、") }}</p>
    </template>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, ref, watch } from "vue";

const props = defineProps({
  topicTitle: {
    type: String,
    default: "",
  },
});

const DEMOS = {
  "双指针模板（有序数组）": {
    name: "双指针收缩",
    description: "有序数组中左右夹逼，目标和 target = 15。",
    frames: [
      { kind: "two-pointer", values: [1, 2, 4, 7, 11, 15], left: 0, right: 5, note: "初始：L=0，R=5，和为 16，大于 15，右移 R。", metric: ["sum=16"] },
      { kind: "two-pointer", values: [1, 2, 4, 7, 11, 15], left: 0, right: 4, note: "和为 12，小于 15，左移 L。", metric: ["sum=12"] },
      { kind: "two-pointer", values: [1, 2, 4, 7, 11, 15], left: 1, right: 4, note: "和为 13，继续左移 L。", metric: ["sum=13"] },
      { kind: "two-pointer", values: [1, 2, 4, 7, 11, 15], left: 2, right: 4, note: "和为 15，命中目标。", metric: ["sum=15", "answer=(2,4)"] },
    ],
  },
  "滑动窗口（变长）": {
    name: "滑动窗口扩缩",
    description: "最短子数组和 ≥ 7，数组 [2,3,1,2,4,3]。",
    frames: [
      { kind: "window", values: [2, 3, 1, 2, 4, 3], left: 0, right: 0, note: "先扩右端，窗口和 2。", metric: ["sum=2", "best=∞"] },
      { kind: "window", values: [2, 3, 1, 2, 4, 3], left: 0, right: 3, note: "扩到 right=3，窗口和达到 8。", metric: ["sum=8", "best=4"] },
      { kind: "window", values: [2, 3, 1, 2, 4, 3], left: 1, right: 3, note: "左端收缩，窗口和 6，不再满足。", metric: ["sum=6", "best=3"] },
      { kind: "window", values: [2, 3, 1, 2, 4, 3], left: 4, right: 5, note: "继续扩缩后得到最优窗口 [4,5]。", metric: ["sum=7", "best=2"] },
    ],
  },
  "反转链表（迭代）": {
    name: "链表指针反转",
    description: "迭代中维护 prev / cur / next。",
    frames: [
      { kind: "reverse", reversed: [], current: "1", remaining: ["2", "3", "4"], note: "初始：prev=None，cur=1。" },
      { kind: "reverse", reversed: ["1"], current: "2", remaining: ["3", "4"], note: "1 指向 prev，prev 前进到 1。" },
      { kind: "reverse", reversed: ["2", "1"], current: "3", remaining: ["4"], note: "2 也完成反转，继续推进。" },
      { kind: "reverse", reversed: ["3", "2", "1"], current: "4", remaining: [], note: "3 完成后，cur 到 4。" },
      { kind: "reverse", reversed: ["4", "3", "2", "1"], current: "", remaining: [], note: "cur 为空结束，返回 prev。" },
    ],
  },
  "二分查找边界模板": {
    name: "左闭右开二分",
    description: "在 [1,3,5,7,9,11,13] 中查找 target = 9。",
    frames: [
      { kind: "binary", values: [1, 3, 5, 7, 9, 11, 13], left: 0, right: 6, mid: 3, note: "mid=3，值 7 < 9，收缩到右半。", metric: ["l=0", "r=6", "m=3"] },
      { kind: "binary", values: [1, 3, 5, 7, 9, 11, 13], left: 4, right: 6, mid: 5, note: "mid=5，值 11 > 9，收缩到左半。", metric: ["l=4", "r=6", "m=5"] },
      { kind: "binary", values: [1, 3, 5, 7, 9, 11, 13], left: 4, right: 4, mid: 4, note: "mid=4，命中 target。", metric: ["l=4", "r=4", "m=4"] },
    ],
  },
  "快慢指针找环入口": {
    name: "Floyd 判环与找入口",
    description: "链表 A→B→C→D→E→C，入口为 C。",
    frames: [
      { kind: "cycle", nodes: ["A", "B", "C", "D", "E"], entry: 2, slow: 1, fast: 2, note: "阶段一：slow 每次 1 步，fast 每次 2 步。" },
      { kind: "cycle", nodes: ["A", "B", "C", "D", "E"], entry: 2, slow: 2, fast: 4, note: "继续前进，二者进入环内。" },
      { kind: "cycle", nodes: ["A", "B", "C", "D", "E"], entry: 2, slow: 3, fast: 3, note: "相遇后开始阶段二：一指针回头。" },
      { kind: "cycle", nodes: ["A", "B", "C", "D", "E"], entry: 2, slow: 2, fast: 2, note: "两者同速再次相遇于 C，即环入口。" },
    ],
  },
  "前缀和与子数组统计": {
    name: "前缀和 + 哈希计数",
    description: "目标 k=3，统计和为 k 的连续子数组个数。",
    frames: [
      { kind: "prefix", values: [1, 2, 1, 2, 1], mid: 0, note: "pre=1，查 pre-k=-2，不存在。", metric: ["pre=1", "ans=0", "cnt={0:1,1:1}"] },
      { kind: "prefix", values: [1, 2, 1, 2, 1], mid: 1, note: "pre=3，查 0 命中 1 次。", metric: ["pre=3", "ans=1", "cnt新增3"] },
      { kind: "prefix", values: [1, 2, 1, 2, 1], mid: 2, note: "pre=4，查 1 命中 1 次。", metric: ["pre=4", "ans=2", "cnt新增4"] },
      { kind: "prefix", values: [1, 2, 1, 2, 1], mid: 3, note: "pre=6，查 3 命中 1 次。", metric: ["pre=6", "ans=3", "cnt新增6"] },
    ],
  },
  "单调栈（下一个更大元素）": {
    name: "单调栈出栈回填",
    description: "数组 [2,1,2,4,3]，维护递减栈（存下标）。",
    frames: [
      { kind: "mono-stack", values: [2, 1, 2, 4, 3], mid: 0, note: "i=0 入栈。", metric: ["stack=[0]", "ans=[-,-,-,-,-]"] },
      { kind: "mono-stack", values: [2, 1, 2, 4, 3], mid: 1, note: "1 小于栈顶值 2，继续入栈。", metric: ["stack=[0,1]"] },
      { kind: "mono-stack", values: [2, 1, 2, 4, 3], mid: 2, note: "当前 2 > nums[1]，弹出 1 并回填答案。", metric: ["stack=[0,2]", "ans=[-,2,-,-,-]"] },
      { kind: "mono-stack", values: [2, 1, 2, 4, 3], mid: 3, note: "当前 4 触发连续弹栈，回填 0 与 2。", metric: ["stack=[3]", "ans=[4,2,4,-,-]"] },
      { kind: "mono-stack", values: [2, 1, 2, 4, 3], mid: 4, note: "3 入栈，遍历结束，栈中位置答案保持 -1。", metric: ["stack=[3,4]", "ans=[4,2,4,-1,-1]"] },
    ],
  },
  "单调队列（滑窗最大值）": {
    name: "单调队列维护窗口最大值",
    description: "k=3，数组 [1,3,-1,-3,5,3,6,7]。",
    frames: [
      { kind: "window", values: [1, 3, -1, -3, 5, 3, 6, 7], left: 0, right: 2, note: "初始化首窗 [0,2]，队列下标 [1,2]，最大值 3。", metric: ["q=[1,2]", "max=3"] },
      { kind: "window", values: [1, 3, -1, -3, 5, 3, 6, 7], left: 1, right: 3, note: "右移一格，弹出过期元素，最大值仍为 3。", metric: ["q=[1,2,3]", "max=3"] },
      { kind: "window", values: [1, 3, -1, -3, 5, 3, 6, 7], left: 2, right: 4, note: "新元素 5 入队前清空队尾较小值。", metric: ["q=[4]", "max=5"] },
      { kind: "window", values: [1, 3, -1, -3, 5, 3, 6, 7], left: 4, right: 6, note: "6 进入后成为队首最大值。", metric: ["q=[6]", "max=6"] },
      { kind: "window", values: [1, 3, -1, -3, 5, 3, 6, 7], left: 5, right: 7, note: "最后窗口最大值更新为 7。", metric: ["q=[7]", "max=7"] },
    ],
  },
  "KMP 模式匹配": {
    name: "KMP 失配回退",
    description: "主串 ababac，模式串 abac。",
    frames: [
      { kind: "kmp", values: ["a", "b", "a", "b", "a", "c"], left: 0, right: 0, note: "i=0, j=0，字符相同，双指针右移。", metric: ["j=1"] },
      { kind: "kmp", values: ["a", "b", "a", "b", "a", "c"], left: 1, right: 1, note: "i=1, j=1，继续匹配。", metric: ["j=2"] },
      { kind: "kmp", values: ["a", "b", "a", "b", "a", "c"], left: 2, right: 2, note: "i=2, j=2，再次匹配成功。", metric: ["j=3"] },
      { kind: "kmp", values: ["a", "b", "a", "b", "a", "c"], left: 1, right: 3, note: "失配：j 从 3 回退到 next[2]=1。", metric: ["回退 j=1"] },
      { kind: "kmp", values: ["a", "b", "a", "b", "a", "c"], left: 3, right: 5, note: "最终匹配完成，起点为 2。", metric: ["match_index=2"] },
    ],
  },
  "并查集模板": {
    name: "并查集合并与路径压缩",
    description: "节点 0~4，依次执行 union(1,2)、union(3,4)、union(2,4)。",
    frames: [
      { kind: "dsu", values: [0, 1, 2, 3, 4], note: "初始化 parent[i]=i。", metric: ["parent=[0,1,2,3,4]"] },
      { kind: "dsu", values: [0, 1, 2, 3, 4], mid: 2, note: "union(1,2)：让 2 的根指向 1。", metric: ["parent=[0,1,1,3,4]"] },
      { kind: "dsu", values: [0, 1, 2, 3, 4], mid: 4, note: "union(3,4)：让 4 的根指向 3。", metric: ["parent=[0,1,1,3,3]"] },
      { kind: "dsu", values: [0, 1, 2, 3, 4], mid: 3, note: "union(2,4)：根 1 与根 3 合并。", metric: ["parent=[0,1,1,1,3]"] },
      { kind: "dsu", values: [0, 1, 2, 3, 4], mid: 4, note: "find(4) 路径压缩后直接挂到根 1。", metric: ["parent=[0,1,1,1,1]"] },
    ],
  },
  "Dijkstra 最短路": {
    name: "Dijkstra 松弛流程",
    description: "从源点 0 出发，按最短距离出堆松弛。",
    frames: [
      { kind: "graph", values: [0, 1, 2, 3, 4], mid: 0, note: "初始化 dist[0]=0，其他为∞。", metric: ["dist=[0,∞,∞,∞,∞]", "pq=(0,0)"] },
      { kind: "graph", values: [0, 1, 2, 3, 4], mid: 1, note: "弹出 0，松弛到 1、2。", metric: ["dist=[0,2,5,∞,∞]", "pq=(2,1),(5,2)"] },
      { kind: "graph", values: [0, 1, 2, 3, 4], mid: 2, note: "弹出 1，更新 2、3。", metric: ["dist=[0,2,3,4,∞]", "pq=(3,2),(4,3)"] },
      { kind: "graph", values: [0, 1, 2, 3, 4], mid: 4, note: "继续松弛得到 4 的候选距离。", metric: ["dist=[0,2,3,4,6]"] },
      { kind: "graph", values: [0, 1, 2, 3, 4], mid: 4, note: "通过节点 3 再优化，最终 dist[4]=5。", metric: ["dist=[0,2,3,4,5]"] },
    ],
  },
  "线性 DP（打家劫舍）": {
    name: "线性 DP 滚动更新",
    description: "nums=[2,7,9,3,1]，状态 (prev2, prev1)。",
    frames: [
      { kind: "dp", values: [2, 7, 9, 3, 1], mid: 0, note: "处理 2：cur=max(0,0+2)=2。", metric: ["prev2=0", "prev1=2"] },
      { kind: "dp", values: [2, 7, 9, 3, 1], mid: 1, note: "处理 7：cur=max(2,0+7)=7。", metric: ["prev2=2", "prev1=7"] },
      { kind: "dp", values: [2, 7, 9, 3, 1], mid: 2, note: "处理 9：cur=max(7,2+9)=11。", metric: ["prev2=7", "prev1=11"] },
      { kind: "dp", values: [2, 7, 9, 3, 1], mid: 3, note: "处理 3：cur=max(11,7+3)=11。", metric: ["prev2=11", "prev1=11"] },
      { kind: "dp", values: [2, 7, 9, 3, 1], mid: 4, note: "处理 1：cur=max(11,11+1)=12。", metric: ["answer=12"] },
    ],
  },
  "0-1 背包模板": {
    name: "0-1 背包容量倒序",
    description: "物品 (w,v)=(2,3),(3,4),(4,5)，容量 cap=5。",
    frames: [
      { kind: "knapsack", values: [0, 1, 2, 3, 4, 5], note: "初始化：dp 全 0。", metric: ["dp=[0,0,0,0,0,0]"] },
      { kind: "knapsack", values: [0, 1, 2, 3, 4, 5], right: 5, note: "处理物品 (2,3)，容量从 5 到 2 倒序更新。", metric: ["dp=[0,0,3,3,3,3]"] },
      { kind: "knapsack", values: [0, 1, 2, 3, 4, 5], right: 5, note: "处理物品 (3,4)。", metric: ["dp=[0,0,3,4,4,7]"] },
      { kind: "knapsack", values: [0, 1, 2, 3, 4, 5], right: 5, note: "处理物品 (4,5)，最终最优值保持 7。", metric: ["dp=[0,0,3,4,5,7]", "answer=7"] },
    ],
  },
  "最长递增子序列 LIS": {
    name: "LIS 的 tails 演化",
    description: "数组 [10,9,2,5,3,7,101,18]，用 tails 维护最小结尾。",
    frames: [
      { kind: "lis", values: [10, 9, 2, 5, 3, 7, 101, 18], mid: 0, note: "读到 10：tails=[10]。", metric: ["tails=[10]"] },
      { kind: "lis", values: [10, 9, 2, 5, 3, 7, 101, 18], mid: 2, note: "9、2 依次替换 tails[0]。", metric: ["tails=[2]"] },
      { kind: "lis", values: [10, 9, 2, 5, 3, 7, 101, 18], mid: 5, note: "5、3、7 形成增长链。", metric: ["tails=[2,3,7]"] },
      { kind: "lis", values: [10, 9, 2, 5, 3, 7, 101, 18], mid: 6, note: "101 追加到末尾。", metric: ["tails=[2,3,7,101]"] },
      { kind: "lis", values: [10, 9, 2, 5, 3, 7, 101, 18], mid: 7, note: "18 替换 101，不改变长度。", metric: ["tails=[2,3,7,18]", "LIS=4"] },
    ],
  },
  "拓扑排序（Kahn）": {
    name: "拓扑排序（入度 + 队列）",
    description: "有向图边：0→1，0→2，1→3，2→3，3→4。",
    frames: [
      { kind: "topo", values: [0, 1, 2, 3, 4], mid: 0, note: "初始化入度，0 入度为 0，先入队。", metric: ["indeg=[0,1,1,2,1]", "queue=[0]", "ans=[]"] },
      { kind: "topo", values: [0, 1, 2, 3, 4], mid: 0, note: "弹出 0，更新 1 和 2 入度，二者入队。", metric: ["indeg=[0,0,0,2,1]", "queue=[1,2]", "ans=[0]"] },
      { kind: "topo", values: [0, 1, 2, 3, 4], mid: 1, note: "弹出 1，3 入度减为 1，暂不入队。", metric: ["indeg=[0,0,0,1,1]", "queue=[2]", "ans=[0,1]"] },
      { kind: "topo", values: [0, 1, 2, 3, 4], mid: 2, note: "弹出 2，3 入度减为 0，入队。", metric: ["indeg=[0,0,0,0,1]", "queue=[3]", "ans=[0,1,2]"] },
      { kind: "topo", values: [0, 1, 2, 3, 4], mid: 3, note: "弹出 3 后 4 入队，最终拓扑序完成。", metric: ["queue=[4]", "ans=[0,1,2,3,4]"] },
    ],
  },
  "回溯模板（子集/组合）": {
    name: "回溯决策树（子集）",
    description: "数组 [1,2,3]，执行“做选择 → 递归 → 撤销选择”。",
    frames: [
      { kind: "backtrack", values: [1, 2, 3], mid: 0, note: "起点 i=0，路径 path=[]，先记录空集。", metric: ["path=[]", "ans=[[]]"] },
      { kind: "backtrack", values: [1, 2, 3], mid: 0, note: "选择 1，递归到下一层。", metric: ["path=[1]", "ans增量=[1]"] },
      { kind: "backtrack", values: [1, 2, 3], mid: 1, note: "在 path=[1] 上选择 2，继续递归。", metric: ["path=[1,2]", "ans增量=[1,2]"] },
      { kind: "backtrack", values: [1, 2, 3], mid: 2, note: "选择 3 到叶子后回溯，撤销最后选择。", metric: ["path=[1,2,3] -> [1,2]"] },
      { kind: "backtrack", values: [1, 2, 3], mid: 1, note: "回到上一层后尝试新分支，最终枚举全部子集。", metric: ["最终ans共8个子集"] },
    ],
  },
  "最近公共祖先 LCA": {
    name: "LCA 后序返回",
    description: "示例二叉树中查询 p=5, q=1。",
    frames: [
      { kind: "tree", levels: [["3"], ["5", "1"], ["6", "2", "0", "8"], ["7", "4"]], active: ["5"], target: "5", note: "后序遍历先进入左子树，命中节点 5。", metric: ["left=5", "right=null"] },
      { kind: "tree", levels: [["3"], ["5", "1"], ["6", "2", "0", "8"], ["7", "4"]], active: ["1"], target: "1", note: "再进入右子树，命中节点 1。", metric: ["left=5", "right=1"] },
      { kind: "tree", levels: [["3"], ["5", "1"], ["6", "2", "0", "8"], ["7", "4"]], active: ["3"], target: "3", note: "当前节点左右子树都命中，当前节点 3 就是 LCA。", metric: ["LCA=3"] },
      { kind: "tree", levels: [["3"], ["5", "1"], ["6", "2", "0", "8"], ["7", "4"]], active: ["3", "5", "1"], target: "3", note: "返回阶段将 LCA 向上层返回，答案稳定。", metric: ["answer=3"] },
    ],
  },
};

const demo = computed(() => DEMOS[props.topicTitle] || null);
const supportedTitles = Object.keys(DEMOS);
const frameIndex = ref(0);
const isPlaying = ref(false);
let timerId = null;

const totalFrames = computed(() => (demo.value ? demo.value.frames.length : 0));
const currentFrame = computed(() => {
  if (!demo.value || !demo.value.frames.length) {
    return null;
  }
  const safeIndex = Math.min(frameIndex.value, demo.value.frames.length - 1);
  return demo.value.frames[safeIndex];
});

const stopPlay = () => {
  if (timerId) {
    clearInterval(timerId);
    timerId = null;
  }
  isPlaying.value = false;
};

const nextFrame = () => {
  if (!demo.value) {
    return;
  }
  if (frameIndex.value >= totalFrames.value - 1) {
    stopPlay();
    return;
  }
  frameIndex.value += 1;
};

const prevFrame = () => {
  if (frameIndex.value <= 0) {
    return;
  }
  frameIndex.value -= 1;
};

const togglePlay = () => {
  if (!demo.value || totalFrames.value < 2) {
    return;
  }
  if (isPlaying.value) {
    stopPlay();
    return;
  }
  isPlaying.value = true;
  timerId = setInterval(() => {
    if (frameIndex.value >= totalFrames.value - 1) {
      stopPlay();
      return;
    }
    frameIndex.value += 1;
  }, 900);
};

watch(
  () => props.topicTitle,
  () => {
    stopPlay();
    frameIndex.value = 0;
  },
);

watch(demo, () => {
  stopPlay();
  frameIndex.value = 0;
});

onBeforeUnmount(() => {
  stopPlay();
});
</script>

<style scoped>
.algo-demo {
  margin-top: 10px;
  border: 1px dashed rgba(37, 99, 235, 0.35);
  border-radius: 12px;
  background: var(--card);
  padding: 12px;
}

.demo-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 10px;
}

.demo-header h4 {
  margin: 0;
  font-size: 15px;
}

.demo-header p {
  margin: 4px 0 0;
  color: var(--muted);
  font-size: 13px;
}

.demo-controls {
  display: flex;
  gap: 6px;
}

.demo-btn {
  padding: 6px 10px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--card-strong);
  color: var(--text);
  font-size: 12px;
  cursor: pointer;
}

.demo-btn.primary {
  background: var(--primary);
  color: #fff;
  border: none;
}

.demo-btn:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.demo-progress {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.demo-progress input[type="range"] {
  flex: 1;
}

.demo-progress span {
  font-size: 12px;
  color: var(--muted);
  white-space: nowrap;
}

.demo-stage {
  margin-top: 10px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: var(--card-strong);
  padding: 10px;
}

.array-track,
.node-line {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.array-cell {
  position: relative;
  width: 52px;
  padding: 12px 6px 8px;
  text-align: center;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--card);
}

.array-cell.inside {
  background: rgba(14, 165, 233, 0.14);
}

.array-cell.left {
  border-color: #2563eb;
}

.array-cell.right {
  border-color: #db2777;
}

.array-cell.mid {
  border-color: #0f766e;
}

.array-cell .value {
  font-weight: 600;
}

.array-cell .index {
  display: block;
  margin-top: 4px;
  font-size: 11px;
  color: var(--muted);
}

.ptr {
  position: absolute;
  top: -10px;
  border-radius: 999px;
  padding: 1px 6px;
  font-size: 10px;
  color: #fff;
}

.ptr-left {
  left: 4px;
  background: #2563eb;
}

.ptr-right {
  right: 4px;
  background: #db2777;
}

.ptr-mid {
  left: 50%;
  transform: translateX(-50%);
  background: #0f766e;
}

.metric-line {
  margin-top: 8px;
  display: flex;
  gap: 10px;
  color: var(--muted);
  font-size: 12px;
}

.reverse-lane {
  display: grid;
  grid-template-columns: 64px 1fr;
  gap: 8px;
  align-items: center;
  margin-bottom: 8px;
}

.reverse-lane:last-child {
  margin-bottom: 0;
}

.lane-title {
  color: var(--muted);
  font-size: 12px;
}

.node {
  position: relative;
  min-width: 38px;
  text-align: center;
  border-radius: 8px;
  padding: 6px 8px;
  border: 1px solid var(--border);
  background: var(--card);
  font-size: 12px;
}

.node.done {
  background: rgba(16, 185, 129, 0.15);
  border-color: rgba(16, 185, 129, 0.45);
}

.node.current {
  background: rgba(37, 99, 235, 0.16);
  border-color: rgba(37, 99, 235, 0.45);
}

.node.ghost {
  opacity: 0.6;
}

.node.cycle {
  background: rgba(99, 102, 241, 0.1);
}

.node.slow {
  border-color: #2563eb;
}

.node.fast {
  border-color: #db2777;
}

.node em {
  position: absolute;
  top: -8px;
  right: -6px;
  min-width: 16px;
  height: 16px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-style: normal;
  font-size: 10px;
  color: #fff;
  background: #111827;
}

.cycle-entry {
  margin: 8px 0 0;
  color: var(--muted);
  font-size: 12px;
}

.tree-stage {
  display: grid;
  gap: 8px;
}

.tree-level {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.tree-node {
  min-width: 34px;
  text-align: center;
  border-radius: 8px;
  padding: 6px 8px;
  border: 1px solid var(--border);
  background: var(--card);
  font-size: 12px;
}

.tree-node.active {
  border-color: rgba(37, 99, 235, 0.55);
  background: rgba(37, 99, 235, 0.14);
}

.tree-node.target {
  border-color: rgba(15, 118, 110, 0.6);
  background: rgba(16, 185, 129, 0.2);
  font-weight: 600;
}

.demo-note {
  margin: 8px 0 0;
  color: var(--text);
  font-size: 13px;
  line-height: 1.6;
}

@media (max-width: 980px) {
  .demo-header {
    flex-direction: column;
  }
}
</style>
