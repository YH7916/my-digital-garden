---
title: 哈希表
description: 哈希表题型模板与 Hot100 题解，覆盖两数之和、字母异位词、最长连续序列和前缀和。
tags:
  - learning
  - leetcode
  - hot100
  - hash-table
updated: 2026-05-27
---

# 哈希表标准答案

记忆核心：哈希表就是“我之前见过什么”。配对先查再存，计数先初始化，前缀和要记得 `cnt[0] = 1`。

## 1 两数之和

- 题目：给数组 `nums` 和目标值 `target`，找两个不同下标，使两个数相加等于 `target`，返回这两个下标。
- 思路：遍历到 `x` 时，先看 `target - x` 之前是否出现过。
- 标准答案：

```python
class Solution:
    def twoSum(self, nums, target):
        mp = {}
        for i, x in enumerate(nums):
            need = target - x
            if need in mp:
                return [mp[need], i]
            mp[x] = i
```

- 小坑：一定是先查再存，避免同一个元素被用两次。

## 49 字母异位词分组

- 题目：给一组字符串，把字母组成相同、顺序不同的字符串分到同一组。
- 思路：排序后的字符串可以当作同组 key，比如 `eat/tea/ate` 排序后都是 `aet`。
- 标准答案：

```python
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs):
        groups = defaultdict(list)
        for s in strs:
            key = ''.join(sorted(s))
            groups[key].append(s)
        return list(groups.values())
```

- 小坑：返回的是分组后的二维列表；`sorted(s)` 得到字符列表，要用 `join` 拼回字符串。

## 128 最长连续序列

- 题目：给一个无序数组，找最长的连续整数序列长度，比如 `1,2,3,4` 长度是 4。
- 思路：用集合 O(1) 查数；只从“连续段起点”开始数，也就是 `x - 1` 不存在时才往后扩。
- 标准答案：

```python
class Solution:
    def longestConsecutive(self, nums):
        s = set(nums)
        ans = 0

        for x in s:
            if x - 1 not in s:
                y = x
                while y in s:
                    y += 1
                ans = max(ans, y - x)

        return ans
```

- 小坑：遍历 `set(nums)`，不要被重复数字拖慢；只从起点开始数。

## 560 和为 K 的子数组

- 题目：给数组 `nums` 和整数 `k`，统计有多少个连续子数组的和等于 `k`。
- 思路：前缀和。当前前缀和是 `pre`，如果之前出现过 `pre - k`，中间这段和就是 `k`。
- 标准答案：

```python
from collections import defaultdict

class Solution:
    def subarraySum(self, nums, k):
        cnt = defaultdict(int)
        cnt[0] = 1
        pre = 0
        ans = 0

        for x in nums:
            pre += x
            ans += cnt[pre - k]
            cnt[pre] += 1

        return ans
```

- 小坑：`cnt[0] = 1` 表示从开头到当前位置本身就能组成答案。
