---
title: 二分查找
tags: [learning, leetcode, hot100, binary-search]
updated: 2026-05-27
---

# 二分查找标准答案

记忆核心：找具体值常用 `while l <= r`；找边界常写一个 `lower_bound`。

## 4 寻找两个正序数组的中位数

- 题目：给两个已经升序的数组 `nums1`、`nums2`，要求在 O(log(m+n)) 时间内找到合并后数组的中位数。
- 思路：在较短数组上二分切一刀，让左右两边数量相等或左边多一个；只要左半边最大值不大于右半边最小值，就切对了。
- 标准答案：

```python
class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1

        m, n = len(nums1), len(nums2)
        total_left = (m + n + 1) // 2
        l, r = 0, m

        while l <= r:
            i = (l + r) // 2
            j = total_left - i

            a_left = nums1[i - 1] if i > 0 else float('-inf')
            a_right = nums1[i] if i < m else float('inf')
            b_left = nums2[j - 1] if j > 0 else float('-inf')
            b_right = nums2[j] if j < n else float('inf')

            if a_left <= b_right and b_left <= a_right:
                if (m + n) % 2 == 1:
                    return max(a_left, b_left)
                return (max(a_left, b_left) + min(a_right, b_right)) / 2

            if a_left > b_right:
                r = i - 1
            else:
                l = i + 1
```

- 小坑：一定在短数组上二分；空边界用 `-inf/inf`，避免单独讨论切在最左/最右。

## 33 搜索旋转排序数组

- 题目：升序数组被旋转后，找目标值下标，不存在返回 -1。
- 思路：每次二分，必有一半是有序的；判断目标是否落在有序半边。
- 标准答案：

```python
class Solution:
    def search(self, nums, target):
        l, r = 0, len(nums) - 1

        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target:
                return mid

            if nums[l] <= nums[mid]:
                if nums[l] <= target < nums[mid]:
                    r = mid - 1
                else:
                    l = mid + 1
            else:
                if nums[mid] < target <= nums[r]:
                    l = mid + 1
                else:
                    r = mid - 1

        return -1
```

- 小坑：先判断哪半边有序，再判断目标是否在这一半。

## 34 在排序数组中查找元素的第一个和最后一个位置

- 题目：在升序数组中找 `target` 第一次和最后一次出现的位置，不存在返回 `[-1, -1]`。
- 思路：用两次 lower_bound：第一次找 `target` 左边界，第二次找 `target + 1` 左边界再减一。
- 标准答案：

```python
class Solution:
    def searchRange(self, nums, target):
        def lower_bound(x):
            l, r = 0, len(nums)
            while l < r:
                mid = (l + r) // 2
                if nums[mid] < x:
                    l = mid + 1
                else:
                    r = mid
            return l

        left = lower_bound(target)
        right = lower_bound(target + 1) - 1

        if left <= right and right < len(nums) and nums[left] == target:
            return [left, right]
        return [-1, -1]
```

- 小坑：`lower_bound` 的右边界是 `len(nums)`，不是 `len(nums)-1`。

## 35 搜索插入位置

- 题目：在升序数组中找目标值；如果不存在，返回它应该插入的位置。
- 思路：找第一个大于等于 `target` 的位置。
- 标准答案：

```python
class Solution:
    def searchInsert(self, nums, target):
        l, r = 0, len(nums)

        while l < r:
            mid = (l + r) // 2
            if nums[mid] < target:
                l = mid + 1
            else:
                r = mid

        return l
```

- 小坑：答案可以是 `len(nums)`，所以右边界用开区间。

## 74 搜索二维矩阵

- 题目：矩阵每行升序，下一行第一个数大于上一行最后一个数；判断 target 是否存在。
- 思路：把矩阵当成一维升序数组，用下标换算到 `(row, col)`。
- 标准答案：

```python
class Solution:
    def searchMatrix(self, matrix, target):
        m, n = len(matrix), len(matrix[0])
        l, r = 0, m * n - 1

        while l <= r:
            mid = (l + r) // 2
            x = matrix[mid // n][mid % n]
            if x == target:
                return True
            if x < target:
                l = mid + 1
            else:
                r = mid - 1

        return False
```

- 小坑：一维下标转二维：行是 `mid // n`，列是 `mid % n`。

## 153 寻找旋转排序数组中的最小值

- 题目：升序数组被旋转，找最小值。
- 思路：和右端点比较。`nums[mid] > nums[r]` 说明最小值在右边，否则在左边含 mid。
- 标准答案：

```python
class Solution:
    def findMin(self, nums):
        l, r = 0, len(nums) - 1

        while l < r:
            mid = (l + r) // 2
            if nums[mid] > nums[r]:
                l = mid + 1
            else:
                r = mid

        return nums[l]
```

- 小坑：这里比较 `nums[mid]` 和 `nums[r]`，不是和 `nums[l]`。

## 704 二分查找（额外模板题，非官方 Hot100）

- 题目：在升序数组中找目标值下标，不存在返回 -1。这题是二分基础模板保险题，不属于官方 Hot100。
- 思路：标准闭区间二分。
- 标准答案：

```python
class Solution:
    def search(self, nums, target):
        l, r = 0, len(nums) - 1

        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1

        return -1
```

- 小坑：`while l <= r` 对应闭区间 `[l, r]`。
