---
title: 滑动窗口
tags: [learning, leetcode, hot100, sliding-window]
updated: 2026-05-27
---

# 滑动窗口标准答案

记忆核心：右指针负责扩张，左指针负责把窗口修回合法状态。窗口题一定要先说清楚“合法条件”。

## 3 无重复字符的最长子串

- 题目：找字符串中不含重复字符的最长连续子串长度。
- 思路：窗口 `[l, r]` 保持不重复；遇到重复字符，就把左边界跳到上次出现位置之后。
- 标准答案：

```python
class Solution:
    def lengthOfLongestSubstring(self, s):
        last = {}
        l = 0
        ans = 0

        for r, ch in enumerate(s):
            if ch in last and last[ch] >= l:
                l = last[ch] + 1
            last[ch] = r
            ans = max(ans, r - l + 1)

        return ans
```

- 小坑：只有重复字符位置在当前窗口内，才更新 `l`。

## 76 最小覆盖子串

- 题目：在 `s` 中找最短子串，要求包含 `t` 的所有字符和次数。
- 思路：右指针扩张直到覆盖，覆盖后左指针尽量收缩，同时记录最短答案。
- 标准答案：

```python
from collections import Counter, defaultdict

class Solution:
    def minWindow(self, s, t):
        need = Counter(t)
        window = defaultdict(int)
        valid = 0
        l = 0
        best_len = float('inf')
        best_l = 0

        for r, ch in enumerate(s):
            window[ch] += 1
            if ch in need and window[ch] == need[ch]:
                valid += 1

            while valid == len(need):
                if r - l + 1 < best_len:
                    best_len = r - l + 1
                    best_l = l

                left = s[l]
                if left in need and window[left] == need[left]:
                    valid -= 1
                window[left] -= 1
                l += 1

        if best_len == float('inf'):
            return ''
        return s[best_l:best_l + best_len]
```

- 小坑：`valid` 统计的是满足次数要求的字符种类数，不是字符总数。

## 239 滑动窗口最大值

- 题目：给数组和窗口大小 `k`，返回每个长度为 `k` 的窗口中的最大值。
- 思路：单调队列保存下标，队头永远是当前窗口最大值下标。
- 标准答案：

```python
from collections import deque

class Solution:
    def maxSlidingWindow(self, nums, k):
        q = deque()
        ans = []

        for i, x in enumerate(nums):
            while q and nums[q[-1]] <= x:
                q.pop()
            q.append(i)

            if q[0] <= i - k:
                q.popleft()

            if i >= k - 1:
                ans.append(nums[q[0]])

        return ans
```

- 小坑：队列里放下标，不放值；这样才能判断是否滑出窗口。

## 438 找到字符串中所有字母异位词

- 题目：在 `s` 中找所有长度等于 `p`、字符组成和 `p` 一样的子串起点。
- 思路：固定长度窗口。窗口长度超过 `len(p)` 时移出最左字符；窗口计数等于 `p` 的计数时记录起点。
- 标准答案：

```python
from collections import Counter

class Solution:
    def findAnagrams(self, s, p):
        need = Counter(p)
        window = Counter()
        ans = []
        m = len(p)

        for r, ch in enumerate(s):
            window[ch] += 1

            if r >= m:
                left = s[r - m]
                window[left] -= 1
                if window[left] == 0:
                    del window[left]

            if window == need:
                ans.append(r - m + 1)

        return ans
```

- 小坑：固定窗口长度是 `len(p)`；删除计数为 0 的字符，方便比较两个 Counter。