---
title: 动态规划
description: 动态规划题型模板与 Hot100 题解，覆盖路径、背包、序列、字符串与区间问题。
tags:
  - learning
  - leetcode
  - hot100
  - dp
updated: 2026-05-27
---

# 动态规划标准答案

记忆核心：先说 `dp[i]` 表示什么，再写从更小状态怎么转移过来。背包题先问“每个物品能不能重复用”。

## 5 最长回文子串

- 题目：找字符串中最长的连续回文子串。
- 思路：中心扩展。每个位置都试奇数中心和偶数中心。
- 标准答案：

```python
class Solution:
    def longestPalindrome(self, s):
        ans = ''

        def expand(l, r):
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            return s[l + 1:r]

        for i in range(len(s)):
            a = expand(i, i)
            b = expand(i, i + 1)
            if len(a) > len(ans):
                ans = a
            if len(b) > len(ans):
                ans = b

        return ans
```

- 小坑：扩展停止后左右各多走了一步，所以返回 `s[l + 1:r]`。

## 32 最长有效括号

- 题目：给一串括号，找最长的合法连续括号子串长度。
- 思路：栈存未匹配位置。栈底放 `-1` 当哨兵，方便计算长度。
- 标准答案：

```python
class Solution:
    def longestValidParentheses(self, s):
        stack = [-1]
        ans = 0

        for i, ch in enumerate(s):
            if ch == '(':
                stack.append(i)
            else:
                stack.pop()
                if not stack:
                    stack.append(i)
                else:
                    ans = max(ans, i - stack[-1])

        return ans
```

- 小坑：栈空时把当前右括号下标放进去，作为新的断点。

## 62 不同路径

- 题目：机器人从左上角走到右下角，只能向右或向下，问有多少条路径。
- 思路：`dp[j]` 表示当前行第 `j` 列的路径数，来自上方和左方。
- 标准答案：

```python
class Solution:
    def uniquePaths(self, m, n):
        dp = [1] * n

        for _ in range(1, m):
            for j in range(1, n):
                dp[j] += dp[j - 1]

        return dp[-1]
```

- 小坑：第一行和第一列都只有一种走法。

## 64 最小路径和

- 题目：从左上到右下，只能向右或向下，路径经过数字之和最小是多少。
- 思路：`dp[j]` 表示到当前行第 `j` 列的最小路径和。
- 标准答案：

```python
class Solution:
    def minPathSum(self, grid):
        m, n = len(grid), len(grid[0])
        dp = [float('inf')] * n
        dp[0] = 0

        for i in range(m):
            for j in range(n):
                if j == 0:
                    dp[j] = dp[j] + grid[i][j]
                else:
                    dp[j] = min(dp[j], dp[j - 1]) + grid[i][j]

        return dp[-1]
```

- 小坑：`dp[j]` 是从上面来，`dp[j-1]` 是从左边来。

## 70 爬楼梯

- 题目：每次爬 1 或 2 阶，爬到第 `n` 阶有多少种方法。
- 思路：到第 `i` 阶，可以从 `i-1` 或 `i-2` 来。
- 标准答案：

```python
class Solution:
    def climbStairs(self, n):
        a, b = 1, 1
        for _ in range(n):
            a, b = b, a + b
        return a
```

- 小坑：这是斐波那契；`n=1` 返回 1，`n=2` 返回 2。

## 72 编辑距离

- 题目：把 `word1` 变成 `word2`，每次可以插入、删除、替换一个字符，求最少操作数。
- 思路：`dp[i][j]` 表示 `word1[:i]` 变成 `word2[:j]` 的最少操作。
- 标准答案：

```python
class Solution:
    def minDistance(self, word1, word2):
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(
                        dp[i - 1][j],
                        dp[i][j - 1],
                        dp[i - 1][j - 1]
                    ) + 1

        return dp[m][n]
```

- 小坑：空串变长度为 `i` 的串，需要 `i` 次操作；下标字符是 `word1[i-1]`。

## 118 杨辉三角

- 题目：生成前 `numRows` 行杨辉三角。
- 思路：每行两边是 1，中间位置等于上一行相邻两个数之和。
- 标准答案：

```python
class Solution:
    def generate(self, numRows):
        ans = []

        for i in range(numRows):
            row = [1] * (i + 1)
            for j in range(1, i):
                row[j] = ans[i - 1][j - 1] + ans[i - 1][j]
            ans.append(row)

        return ans
```

- 小坑：中间循环是 `range(1, i)`，两端不用改。

## 139 单词拆分

- 题目：判断字符串能否被字典里的单词拼出来。
- 思路：`dp[i]` 表示 `s[:i]` 能否拼出；枚举最后一刀 `j`。
- 标准答案：

```python
class Solution:
    def wordBreak(self, s, wordDict):
        words = set(wordDict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True

        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break

        return dp[n]
```

- 小坑：`s[j:i]` 是切片，不是 `s[j, i]`。

## 152 乘积最大子数组

- 题目：找连续子数组，使乘积最大。
- 思路：负数会让最大变最小、最小变最大，所以同时维护当前位置结尾的最大/最小乘积。
- 标准答案：

```python
class Solution:
    def maxProduct(self, nums):
        max_prod = min_prod = ans = nums[0]

        for x in nums[1:]:
            a = max_prod * x
            b = min_prod * x
            max_prod = max(x, a, b)
            min_prod = min(x, a, b)
            ans = max(ans, max_prod)

        return ans
```

- 小坑：候选必须包含 `x` 自己，表示从当前位置重新开始。

## 198 打家劫舍

- 题目：一排房子不能偷相邻两家，求最多能偷多少钱。
- 思路：每家只有偷或不偷。滚动维护前两个状态。
- 标准答案：

```python
class Solution:
    def rob(self, nums):
        prev2 = 0
        prev1 = 0

        for x in nums:
            cur = max(prev1, prev2 + x)
            prev2 = prev1
            prev1 = cur

        return prev1
```

- 小坑：`prev2 + x` 是偷当前家，`prev1` 是不偷当前家。

## 279 完全平方数

- 题目：把 `n` 拆成若干完全平方数之和，求最少需要几个。
- 思路：`dp[i]` 表示凑出 `i` 的最少数量；枚举最后一个平方数 `j*j`。
- 标准答案：

```python
class Solution:
    def numSquares(self, n):
        dp = [float('inf')] * (n + 1)
        dp[0] = 0

        for i in range(1, n + 1):
            j = 1
            while j * j <= i:
                dp[i] = min(dp[i], dp[i - j * j] + 1)
                j += 1

        return dp[n]
```

- 小坑：`dp[0] = 0` 是所有转移的起点。

## 300 最长递增子序列

- 题目：找数组中最长严格递增子序列的长度，不要求连续。
- 思路：`tails[i]` 表示长度为 `i+1` 的递增子序列的最小尾巴，用二分维护。
- 标准答案：

```python
import bisect

class Solution:
    def lengthOfLIS(self, nums):
        tails = []

        for x in nums:
            i = bisect.bisect_left(tails, x)
            if i == len(tails):
                tails.append(x)
            else:
                tails[i] = x

        return len(tails)
```

- 小坑：严格递增用 `bisect_left`，相等时替换原位置。

## 322 零钱兑换

- 题目：给硬币面额和总金额，求凑出金额的最少硬币数；凑不出返回 -1。
- 思路：完全背包。每种硬币可以无限用，所以金额正序更新。
- 标准答案：

```python
class Solution:
    def coinChange(self, coins, amount):
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0

        for coin in coins:
            for j in range(coin, amount + 1):
                dp[j] = min(dp[j], dp[j - coin] + 1)

        return -1 if dp[amount] == float('inf') else dp[amount]
```

- 小坑：硬币可重复使用，所以内层金额正序。

## 416 分割等和子集

- 题目：判断数组能不能分成两个子集，使两个子集和相等。
- 思路：总和必须是偶数；问题变成能否用每个数最多一次凑出一半。
- 标准答案：

```python
class Solution:
    def canPartition(self, nums):
        total = sum(nums)
        if total % 2 == 1:
            return False

        target = total // 2
        dp = [False] * (target + 1)
        dp[0] = True

        for x in nums:
            for j in range(target, x - 1, -1):
                dp[j] = dp[j] or dp[j - x]

        return dp[target]
```

- 小坑：每个数只能用一次，所以 `j` 必须倒序。

## 1143 最长公共子序列

- 题目：给两个字符串，找最长公共子序列长度；子序列可以不连续，但相对顺序不能变。
- 思路：`dp[i][j]` 表示 `text1[:i]` 和 `text2[:j]` 的最长公共子序列长度。
- 标准答案：

```python
class Solution:
    def longestCommonSubsequence(self, text1, text2):
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]
```

- 小坑：`dp` 下标是长度，字符下标要减一。
