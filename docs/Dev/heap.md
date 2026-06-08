---
title: 堆
description: 堆题型模板与 Hot100 题解，覆盖第 K 大元素、数据流中位数和前 K 高频元素。
tags:
  - learning
  - leetcode
  - hot100
  - heap
updated: 2026-05-27
---

# 堆标准答案

记忆核心：TopK 用小根堆保留 k 个候选；动态中位数用两个堆平衡左右两半。

## 215 数组中的第 K 个最大元素

- 题目：找数组中第 `k` 大的元素，不是第 `k` 个不同元素。
- 思路：维护大小为 `k` 的小根堆，堆顶就是当前第 `k` 大。
- 标准答案：

```python
import heapq

class Solution:
    def findKthLargest(self, nums, k):
        heap = []
        for x in nums:
            heapq.heappush(heap, x)
            if len(heap) > k:
                heapq.heappop(heap)
        return heap[0]
```

- 小坑：堆大小超过 `k` 才弹；最后堆顶是第 `k` 大。

## 295 数据流的中位数

- 题目：数字不断加入，随时返回当前所有数字的中位数。
- 思路：小的一半放最大堆 `small`，大的一半放最小堆 `large`，保持 `small` 数量不少于 `large`。
- 标准答案：

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []
        self.large = []

    def addNum(self, num):
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))

        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
```

- 小坑：Python 没有最大堆，用负数模拟。

## 347 前 K 个高频元素

- 题目：返回数组中出现频率最高的 `k` 个元素。
- 思路：先计数，再用堆按频率取最大的 k 个 key。
- 标准答案：

```python
from collections import Counter
import heapq

class Solution:
    def topKFrequent(self, nums, k):
        cnt = Counter(nums)
        return heapq.nlargest(k, cnt.keys(), key=cnt.get)
```

- 小坑：按频率排序，所以 key 函数是 `cnt.get`。
