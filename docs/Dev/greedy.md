---
title: 贪心
tags: [learning, leetcode, hot100, greedy]
updated: 2026-05-27
---

# 贪心标准答案

记忆核心：贪心题通常只维护当前能达到的最远位置、当前最低价格、当前片段边界。

## 45 跳跃游戏 II

- 题目：数组每个位置表示最多能跳多远，求从起点到终点的最少跳数。
- 思路：把每一跳看成一层 BFS。扫描当前层时维护下一层最远边界 `farthest`。
- 标准答案：

```python
class Solution:
    def jump(self, nums):
        steps = 0
        end = 0
        farthest = 0

        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            if i == end:
                steps += 1
                end = farthest

        return steps
```

- 小坑：循环到 `len(nums)-2` 即可，最后一格不用再起跳。

## 55 跳跃游戏

- 题目：判断能否从数组起点跳到最后一个位置。
- 思路：维护当前能到的最远位置 `farthest`；如果当前位置都到不了，就失败。
- 标准答案：

```python
class Solution:
    def canJump(self, nums):
        farthest = 0

        for i, x in enumerate(nums):
            if i > farthest:
                return False
            farthest = max(farthest, i + x)

        return True
```

- 小坑：先判断 `i > farthest`，再更新最远位置。

## 121 买卖股票的最佳时机

- 题目：只允许买一次卖一次，求最大利润。
- 思路：遍历价格时，维护历史最低买入价，用当前价格卖出更新利润。
- 标准答案：

```python
class Solution:
    def maxProfit(self, prices):
        min_price = float('inf')
        ans = 0

        for p in prices:
            min_price = min(min_price, p)
            ans = max(ans, p - min_price)

        return ans
```

- 小坑：必须先买后卖；所以最低价只来自当前及之前。

## 763 划分字母区间

- 题目：把字符串切成尽量多的片段，使每个字母最多只出现在一个片段中。
- 思路：先记录每个字母最后出现位置；扫描时维护当前片段必须覆盖到的最远位置 `end`。
- 标准答案：

```python
class Solution:
    def partitionLabels(self, s):
        last = {ch: i for i, ch in enumerate(s)}
        ans = []
        start = 0
        end = 0

        for i, ch in enumerate(s):
            end = max(end, last[ch])
            if i == end:
                ans.append(end - start + 1)
                start = i + 1

        return ans
```

- 小坑：先记录长度，再移动 `start`。