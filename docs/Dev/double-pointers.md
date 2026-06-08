---
title: 双指针
description: 双指针题型模板与 Hot100 题解，覆盖三数之和、接雨水、盛水容器和移动零。
tags:
  - learning
  - leetcode
  - hot100
  - two-pointers
updated: 2026-05-27
---

# 双指针标准答案

记忆核心：两个指针代表一个可收缩范围。每一步都移动“不可能让答案更好”的那一边。

## 11 盛最多水的容器

- 题目：给一排柱子高度，找两根柱子和 x 轴围成的最大水量。
- 思路：左右指针夹逼。面积由短板决定，所以每次移动较矮的一边。
- 标准答案：

```python
class Solution:
    def maxArea(self, height):
        l, r = 0, len(height) - 1
        ans = 0

        while l < r:
            ans = max(ans, min(height[l], height[r]) * (r - l))
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1

        return ans
```

- 小坑：移动高的一边没有意义，因为短板没变、宽度还变小。

## 15 三数之和

- 题目：找所有不重复三元组，使三个数之和等于 0。
- 思路：排序后固定第一个数，剩下两个数用左右指针找 `-nums[i]`。
- 标准答案：

```python
class Solution:
    def threeSum(self, nums):
        nums.sort()
        ans = []
        n = len(nums)

        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            if nums[i] > 0:
                break

            l, r = i + 1, n - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s == 0:
                    ans.append([nums[i], nums[l], nums[r]])
                    l += 1
                    r -= 1
                    while l < r and nums[l] == nums[l - 1]:
                        l += 1
                    while l < r and nums[r] == nums[r + 1]:
                        r -= 1
                elif s < 0:
                    l += 1
                else:
                    r -= 1

        return ans
```

- 小坑：固定层、左指针、右指针都要去重；去重发生在加入答案后。

## 42 接雨水

- 题目：给柱子高度，问下雨后最多能接多少水。
- 思路：左右指针维护左边最高 `lmax` 和右边最高 `rmax`；短板那侧可以确定水量。
- 标准答案：

```python
class Solution:
    def trap(self, height):
        l, r = 0, len(height) - 1
        lmax = rmax = 0
        ans = 0

        while l < r:
            lmax = max(lmax, height[l])
            rmax = max(rmax, height[r])

            if lmax < rmax:
                ans += lmax - height[l]
                l += 1
            else:
                ans += rmax - height[r]
                r -= 1

        return ans
```

- 小坑：先更新 `lmax/rmax`，再算水量；水量不会是负数。

## 283 移动零

- 题目：把数组里的 0 移到末尾，同时保持非零元素相对顺序，要求原地修改。
- 思路：`slow` 指向下一个非零数该放的位置；遇到非零就交换到前面。
- 标准答案：

```python
class Solution:
    def moveZeroes(self, nums):
        slow = 0
        for i in range(len(nums)):
            if nums[i] != 0:
                nums[slow], nums[i] = nums[i], nums[slow]
                slow += 1
```

- 小坑：这题没有返回值；直接改 `nums`。
