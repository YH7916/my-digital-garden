---
title: 数组综合
description: 数组综合题型模板与 Hot100 题解，覆盖下一个排列、最大子数组、合并区间和原地操作。
tags:
  - learning
  - leetcode
  - hot100
  - array
updated: 2026-05-27
---

# 数组综合标准答案

记忆核心：数组题先判断是哪类动作：排序合并、原地交换、前后缀、投票、异或、快慢指针。

## 31 下一个排列

- 题目：把数组改成字典序中的下一个更大排列；如果已经最大，就变成最小排列。
- 思路：从右找第一个下降点，再找右侧刚好比它大的数交换，最后反转后缀。
- 标准答案：

```python
class Solution:
    def nextPermutation(self, nums):
        n = len(nums)
        i = n - 2

        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1

        if i >= 0:
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]

        l, r = i + 1, n - 1
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1
```

- 小坑：完全降序时 `i` 会变成 -1，然后反转整个数组。

## 41 缺失的第一个正数

- 题目：在无序数组中找没有出现的最小正整数，要求 O(n) 时间、O(1) 额外空间。
- 思路：把数字 `x` 尽量放到下标 `x-1` 的位置；最后第一个不对位的位置就是答案。
- 标准答案：

```python
class Solution:
    def firstMissingPositive(self, nums):
        n = len(nums)

        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                j = nums[i] - 1
                nums[i], nums[j] = nums[j], nums[i]

        for i in range(n):
            if nums[i] != i + 1:
                return i + 1

        return n + 1
```

- 小坑：while 条件里要防止重复数字导致死循环。

## 53 最大子数组和

- 题目：找连续子数组，使元素和最大。
- 思路：如果前面的和是负数，不如从当前数重新开始。
- 标准答案：

```python
class Solution:
    def maxSubArray(self, nums):
        cur = ans = nums[0]

        for x in nums[1:]:
            cur = max(x, cur + x)
            ans = max(ans, cur)

        return ans
```

- 小坑：答案初始化为 `nums[0]`，才能处理全负数。

## 56 合并区间

- 题目：给若干区间，合并所有重叠区间。
- 思路：按左端点排序；当前区间和答案最后一个区间重叠就扩右端点，否则新开一段。
- 标准答案：

```python
class Solution:
    def merge(self, intervals):
        intervals.sort(key=lambda x: x[0])
        ans = []

        for l, r in intervals:
            if not ans or ans[-1][1] < l:
                ans.append([l, r])
            else:
                ans[-1][1] = max(ans[-1][1], r)

        return ans
```

- 小坑：判断不重叠是 `ans[-1][1] < l`，等于时也要合并。

## 75 颜色分类

- 题目：数组只包含 0、1、2，原地排序成 0 在前、1 中间、2 在后。
- 思路：三指针。`p0` 放下一个 0，`p2` 放下一个 2，`i` 扫描当前元素。
- 标准答案：

```python
class Solution:
    def sortColors(self, nums):
        p0, i, p2 = 0, 0, len(nums) - 1

        while i <= p2:
            if nums[i] == 0:
                nums[p0], nums[i] = nums[i], nums[p0]
                p0 += 1
                i += 1
            elif nums[i] == 2:
                nums[p2], nums[i] = nums[i], nums[p2]
                p2 -= 1
            else:
                i += 1
```

- 小坑：换来右边的数还没检查，所以遇到 2 时 `i` 不动。

## 136 只出现一次的数字

- 题目：数组里除了一个数只出现一次，其余都出现两次，找这个数。
- 思路：异或。相同数字异或为 0，0 异或任何数还是它自己。
- 标准答案：

```python
class Solution:
    def singleNumber(self, nums):
        ans = 0
        for x in nums:
            ans ^= x
        return ans
```

- 小坑：异或符号是 `^`。

## 169 多数元素

- 题目：找数组中出现次数超过一半的元素。
- 思路：摩尔投票。不同元素互相抵消，最后剩下的一定是多数元素。
- 标准答案：

```python
class Solution:
    def majorityElement(self, nums):
        cand = None
        count = 0

        for x in nums:
            if count == 0:
                cand = x
            count += 1 if x == cand else -1

        return cand
```

- 小坑：题目保证多数元素存在，所以最后不用再验证。

## 189 轮转数组

- 题目：把数组向右轮转 `k` 步，要求原地修改。
- 思路：三次反转：整体反转，前 `k` 个反转，后面反转。
- 标准答案：

```python
class Solution:
    def rotate(self, nums, k):
        n = len(nums)
        k %= n

        def rev(l, r):
            while l < r:
                nums[l], nums[r] = nums[r], nums[l]
                l += 1
                r -= 1

        rev(0, n - 1)
        rev(0, k - 1)
        rev(k, n - 1)
```

- 小坑：先 `k %= n`，否则 k 可能大于数组长度。

## 238 除自身以外数组的乘积

- 题目：返回数组 `answer`，其中 `answer[i]` 等于除了 `nums[i]` 以外所有数的乘积，不能用除法。
- 思路：先把左侧乘积写进答案，再从右往左乘上右侧乘积。
- 标准答案：

```python
class Solution:
    def productExceptSelf(self, nums):
        n = len(nums)
        ans = [1] * n

        left = 1
        for i in range(n):
            ans[i] = left
            left *= nums[i]

        right = 1
        for i in range(n - 1, -1, -1):
            ans[i] *= right
            right *= nums[i]

        return ans
```

- 小坑：`ans[i]` 先存左边乘积，再乘右边乘积。

## 287 寻找重复数

- 题目：数组长度为 `n+1`，数字范围是 `1..n`，只有一个重复数，找出来。
- 思路：把数组看成链表，`i -> nums[i]`。重复数就是环入口，用快慢指针找。
- 标准答案：

```python
class Solution:
    def findDuplicate(self, nums):
        slow = nums[0]
        fast = nums[0]

        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break

        p = nums[0]
        while p != slow:
            p = nums[p]
            slow = nums[slow]

        return p
```

- 小坑：这里的“next 指针”是 `nums[i]`，不是 `i + 1`。
