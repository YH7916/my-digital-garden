---
title: 回溯
description: 回溯题型模板与 Hot100 题解，覆盖组合、排列、子集、N 皇后和搜索。
tags:
  - learning
  - leetcode
  - hot100
  - backtracking
updated: 2026-05-27
---

# 回溯标准答案

记忆核心：回溯就是“选 -> 递归 -> 撤销”。`path` 存当前答案，`start/idx` 控制下一步位置。

## 17 电话号码的字母组合

- 题目：数字 2-9 各自对应几个字母，返回输入数字串能组成的所有字母组合。
- 思路：每层处理一位数字，从对应字母里选一个放入 `path`。
- 标准答案：

```python
class Solution:
    def letterCombinations(self, digits):
        if not digits:
            return []

        mp = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
        }
        ans = []
        path = []

        def dfs(idx):
            if idx == len(digits):
                ans.append(''.join(path))
                return
            for ch in mp[digits[idx]]:
                path.append(ch)
                dfs(idx + 1)
                path.pop()

        dfs(0)
        return ans
```

- 小坑：空输入返回 `[]`；保存时用 `''.join(path)`。

## 22 括号生成

- 题目：给 `n` 对括号，生成所有合法括号字符串。
- 思路：左括号没用完就能放；右括号必须少于左括号才可以放。
- 标准答案：

```python
class Solution:
    def generateParenthesis(self, n):
        ans = []
        path = []

        def dfs(left, right):
            if len(path) == 2 * n:
                ans.append(''.join(path))
                return

            if left < n:
                path.append('(')
                dfs(left + 1, right)
                path.pop()

            if right < left:
                path.append(')')
                dfs(left, right + 1)
                path.pop()

        dfs(0, 0)
        return ans
```

- 小坑：右括号条件是 `right < left`，不是 `left < right`。

## 39 组合总和

- 题目：从候选数字中选数凑 `target`，每个数字可以重复用，返回所有不重复组合。
- 思路：`start` 防止排列重复；因为能重复用当前数，递归仍传 `i`。
- 标准答案：

```python
class Solution:
    def combinationSum(self, candidates, target):
        ans = []
        path = []

        def dfs(start, remain):
            if remain == 0:
                ans.append(path.copy())
                return
            if remain < 0:
                return

            for i in range(start, len(candidates)):
                x = candidates[i]
                path.append(x)
                dfs(i, remain - x)
                path.pop()

        dfs(0, target)
        return ans
```

- 小坑：可重复选，所以是 `dfs(i, remain - x)`；保存用 `path.copy()`。

## 46 全排列

- 题目：给不重复数组，返回所有可能排列。
- 思路：每个位置从未使用过的数字里选一个。
- 标准答案：

```python
class Solution:
    def permute(self, nums):
        ans = []
        path = []
        used = [False] * len(nums)

        def dfs():
            if len(path) == len(nums):
                ans.append(path.copy())
                return

            for i, x in enumerate(nums):
                if used[i]:
                    continue
                used[i] = True
                path.append(x)
                dfs()
                path.pop()
                used[i] = False

        dfs()
        return ans
```

- 小坑：排列题没有 `start`；每层都能从头选未用数字。

## 51 N 皇后

- 题目：在 `n*n` 棋盘放 `n` 个皇后，任意两个不能同列、同行、同斜线。
- 思路：一行一行放；用三个集合记录列、主斜线 `row-col`、副斜线 `row+col`。
- 标准答案：

```python
class Solution:
    def solveNQueens(self, n):
        ans = []
        board = [['.'] * n for _ in range(n)]
        cols = set()
        diag1 = set()
        diag2 = set()

        def dfs(row):
            if row == n:
                ans.append([''.join(r) for r in board])
                return

            for col in range(n):
                if col in cols or row - col in diag1 or row + col in diag2:
                    continue

                board[row][col] = 'Q'
                cols.add(col)
                diag1.add(row - col)
                diag2.add(row + col)

                dfs(row + 1)

                board[row][col] = '.'
                cols.remove(col)
                diag1.remove(row - col)
                diag2.remove(row + col)

        dfs(0)
        return ans
```

- 小坑：两条斜线分别用 `row-col` 和 `row+col` 标识。

## 78 子集

- 题目：给一组不重复数字，返回所有子集。
- 思路：每个位置可以选或不选；用 `start` 枚举后续可选数字。
- 标准答案：

```python
class Solution:
    def subsets(self, nums):
        ans = []
        path = []

        def dfs(start):
            ans.append(path.copy())
            for i in range(start, len(nums)):
                path.append(nums[i])
                dfs(i + 1)
                path.pop()

        dfs(0)
        return ans
```

- 小坑：每个节点都是一个子集，所以进入 `dfs` 先保存答案。

## 79 单词搜索

- 题目：在字符网格中，从任意格子开始上下左右移动，判断能否拼出单词；格子不能重复用。
- 思路：DFS 匹配 `word[k]`，进入格子临时标记，用完恢复。
- 标准答案：

```python
class Solution:
    def exist(self, board, word):
        m, n = len(board), len(board[0])

        def dfs(i, j, k):
            if i < 0 or i >= m or j < 0 or j >= n:
                return False
            if board[i][j] != word[k]:
                return False
            if k == len(word) - 1:
                return True

            ch = board[i][j]
            board[i][j] = '#'
            found = (
                dfs(i + 1, j, k + 1) or
                dfs(i - 1, j, k + 1) or
                dfs(i, j + 1, k + 1) or
                dfs(i, j - 1, k + 1)
            )
            board[i][j] = ch
            return found

        for i in range(m):
            for j in range(n):
                if dfs(i, j, 0):
                    return True
        return False
```

- 小坑：成功条件是 `k == len(word) - 1`，因为当前字符已经匹配。

## 131 分割回文串

- 题目：把字符串切成若干段，要求每段都是回文，返回所有切法。
- 思路：枚举当前段右端点 `end`，如果 `s[start:end+1]` 是回文，就递归切后面。
- 标准答案：

```python
class Solution:
    def partition(self, s):
        ans = []
        path = []

        def is_pal(l, r):
            while l < r:
                if s[l] != s[r]:
                    return False
                l += 1
                r -= 1
            return True

        def dfs(start):
            if start == len(s):
                ans.append(path.copy())
                return

            for end in range(start, len(s)):
                if is_pal(start, end):
                    path.append(s[start:end + 1])
                    dfs(end + 1)
                    path.pop()

        dfs(0)
        return ans
```

- 小坑：切片右端不包含，所以当前段是 `s[start:end + 1]`。
