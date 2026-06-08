---
title: 二叉树
description: 二叉树题型模板与 Hot100 题解，覆盖遍历、BST、路径、构造和最近公共祖先。
tags:
  - learning
  - leetcode
  - hot100
  - binary-tree
updated: 2026-05-27
---

# 二叉树标准答案

记忆核心：树题先问“递归函数返回什么”。需要全局答案时，在 DFS 过程中更新外层变量。

## 94 二叉树的中序遍历

- 题目：返回二叉树的中序遍历结果，顺序是左子树、根、右子树。
- 思路：递归先走左边，再记录当前节点，再走右边。
- 标准答案：

```python
class Solution:
    def inorderTraversal(self, root):
        ans = []

        def dfs(node):
            if not node:
                return
            dfs(node.left)
            ans.append(node.val)
            dfs(node.right)

        dfs(root)
        return ans
```

- 小坑：中序不是层序；顺序固定是左、根、右。

## 98 验证二叉搜索树

- 题目：判断一棵树是否是二叉搜索树，要求每个节点都满足左边所有值更小，右边所有值更大。
- 思路：递归传上下界。左子树上界变成当前值，右子树下界变成当前值。
- 标准答案：

```python
class Solution:
    def isValidBST(self, root):
        def dfs(node, low, high):
            if not node:
                return True
            if not (low < node.val < high):
                return False
            return dfs(node.left, low, node.val) and dfs(node.right, node.val, high)

        return dfs(root, float('-inf'), float('inf'))
```

- 小坑：不能只比较父子节点；要比较整棵子树的上下界。

## 101 对称二叉树

- 题目：判断一棵树是否关于中心镜像对称。
- 思路：比较两棵子树是否镜像：外侧对外侧，内侧对内侧。
- 标准答案：

```python
class Solution:
    def isSymmetric(self, root):
        def check(a, b):
            if not a and not b:
                return True
            if not a or not b:
                return False
            return a.val == b.val and check(a.left, b.right) and check(a.right, b.left)

        return check(root.left, root.right)
```

- 小坑：镜像比较是 `a.left` 对 `b.right`，`a.right` 对 `b.left`。

## 102 二叉树的层序遍历

- 题目：按层返回二叉树节点值，每一层一个列表。
- 思路：队列 BFS；每层开始先固定当前队列长度。
- 标准答案：

```python
from collections import deque

class Solution:
    def levelOrder(self, root):
        if not root:
            return []

        q = deque([root])
        ans = []

        while q:
            level = []
            for _ in range(len(q)):
                node = q.popleft()
                level.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            ans.append(level)

        return ans
```

- 小坑：`len(q)` 要在每层开始时固定。

## 104 二叉树的最大深度

- 题目：返回二叉树从根到最远叶子的节点数。
- 思路：空树深度 0；非空树深度是左右最大深度加 1。
- 标准答案：

```python
class Solution:
    def maxDepth(self, root):
        if not root:
            return 0
        return max(self.maxDepth(root.left), self.maxDepth(root.right)) + 1
```

- 小坑：深度按节点数算，空节点返回 0。

## 105 从前序与中序遍历序列构造二叉树

- 题目：给前序和中序遍历，还原原来的二叉树。
- 思路：前序第一个是根；中序里根左边是左子树，右边是右子树。
- 标准答案：

```python
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if len(inorder) == 0:
            return None

        root = TreeNode(preorder[0])
        mid = inorder.index(preorder[0])
        root.left = self.buildTree(preorder[1 : mid + 1], inorder[:mid])
        root.right = self.buildTree(preorder[mid + 1:], inorder[mid + 1:])

        return root
```

- 小坑：前序第一个就是根；`mid` 左边的中序是左子树，右边是右子树；前序也要按左子树长度切开。

## 108 将有序数组转换为二叉搜索树

- 题目：把升序数组转换成高度平衡的二叉搜索树。
- 思路：每次取中点当根，左半边建左子树，右半边建右子树。
- 标准答案：

```python
class Solution:
    def sortedArrayToBST(self, nums):
        def build(l, r):
            if l > r:
                return None
            mid = (l + r) // 2
            root = TreeNode(nums[mid])
            root.left = build(l, mid - 1)
            root.right = build(mid + 1, r)
            return root

        return build(0, len(nums) - 1)
```

- 小坑：右子树从 `mid + 1` 开始，不要再包含中点。

## 114 二叉树展开为链表

- 题目：把二叉树原地展开成前序遍历顺序的单链表，全部用右指针连接。
- 思路：递归拉平左右子树，再把左链插到根和原右链中间。
- 标准答案：

```python
class Solution:
    def flatten(self, root):
        def dfs(node):
            if not node:
                return None

            left_tail = dfs(node.left)
            right_tail = dfs(node.right)

            if left_tail:
                left_tail.right = node.right
                node.right = node.left
                node.left = None

            return right_tail or left_tail or node

        dfs(root)
```

- 小坑：先让 `left_tail.right` 接原右链，再把左链挪到右边。

## 124 二叉树中的最大路径和

- 题目：找树中任意一条路径的最大节点值之和，路径不一定经过根。
- 思路：DFS 返回“从当前节点往父节点能贡献的最大单边收益”；全局答案可以用左右两边加当前节点更新。
- 标准答案：

```python
class Solution:
    def maxPathSum(self, root):
        ans = float('-inf')

        def dfs(node):
            nonlocal ans
            if not node:
                return 0

            left = max(dfs(node.left), 0)
            right = max(dfs(node.right), 0)
            ans = max(ans, node.val + left + right)

            return node.val + max(left, right)

        dfs(root)
        return ans
```

- 小坑：更新答案可以左右都要；返回给父节点只能选一边。

### 124 和 543 的区别

- `543 二叉树的直径`：每条边/节点长度都默认是正贡献，所以左右高度都可以拿来更新答案；返回给父节点的是“继续往下走的最长高度”。
- `124 二叉树中的最大路径和`：节点值可能是负数，负贡献要主动丢掉，所以左右收益先写 `max(dfs(child), 0)`；返回给父节点时也只能返回单边，因为路径不能在父节点那里分叉两次。
- 记忆句：`543` 数边数，左右高度天然能加；`124` 算价值，负数要砍掉，返回只能单边。

## 199 二叉树的右视图

- 题目：从右侧看二叉树，返回每一层最右边的节点值。
- 思路：层序遍历，每层最后弹出的节点就是右视图。
- 标准答案：

```python
from collections import deque

class Solution:
    def rightSideView(self, root):
        if not root:
            return []

        q = deque([root])
        ans = []

        while q:
            size = len(q)
            for i in range(size):
                node = q.popleft()
                if i == size - 1:
                    ans.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)

        return ans
```

- 小坑：右视图不是只沿右边走；缺右节点时可能看到左节点。

## 226 翻转二叉树

- 题目：把二叉树每个节点的左右子树交换。
- 思路：当前节点交换左右，然后递归处理左右子树。
- 标准答案：

```python
class Solution:
    def invertTree(self, root):
        if not root:
            return None
        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root
```

- 小坑：要返回 `root`，不是返回左右子树。

## 230 二叉搜索树中第 K 小的元素

- 题目：在 BST 中找第 `k` 小的节点值。
- 思路：BST 中序遍历是升序，第 `k` 个就是答案。
- 标准答案：

```python
class Solution:
    def kthSmallest(self, root, k):
        arr = []

        def dfs(node):
            if not node:
                return
            dfs(node.left)
            arr.append(node.val)
            dfs(node.right)

        dfs(root)
        return arr[k - 1]
```

- 小坑：第 `k` 小对应下标 `k - 1`。

## 236 二叉树的最近公共祖先

- 题目：给普通二叉树中的两个节点 `p/q`，找它们最近的公共祖先。
- 思路：左右子树分别找 `p/q`；两边都找到，当前节点就是答案。
- 标准答案：

```python
class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if not root or root == p or root == q:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        if left and right:
            return root
        return left if left else right
```

- 小坑：普通二叉树不能用大小比较；递归方法前要写 `self.`。

## 437 路径总和 III

- 题目：统计树中有多少条向下路径的节点和等于目标值，路径不要求从根开始。
- 思路：树上前缀和。当前前缀和为 `cur`，之前出现过 `cur - target` 几次，就新增几条路径。
- 标准答案：

```python
from collections import defaultdict

class Solution:
    def pathSum(self, root, targetSum):
        cnt = defaultdict(int)
        cnt[0] = 1

        def dfs(node, cur):
            if not node:
                return 0

            cur += node.val
            ans = cnt[cur - targetSum]

            cnt[cur] += 1
            ans += dfs(node.left, cur)
            ans += dfs(node.right, cur)
            cnt[cur] -= 1

            return ans

        return dfs(root, 0)
```

- 小坑：离开节点时要 `cnt[cur] -= 1`，防止左右分支互相污染。

## 543 二叉树的直径

- 题目：返回二叉树中任意两个节点之间最长路径的边数。
- 思路：DFS 返回当前节点向下的最长链长；全局答案用左右链相加更新。
- 标准答案：

```python
class Solution:
    def diameterOfBinaryTree(self, root):
        ans = 0

        def dfs(node):
            nonlocal ans
            if not node:
                return 0

            left = dfs(node.left)
            right = dfs(node.right)
            ans = max(ans, left + right)
            return max(left, right) + 1

        dfs(root)
        return ans
```

- 小坑：返回的是节点高度，但答案是边数；`left + right` 正好是经过当前节点的边数。
