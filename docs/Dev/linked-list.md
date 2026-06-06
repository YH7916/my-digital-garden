---
title: 链表
tags: [learning, leetcode, hot100, linked-list]
updated: 2026-05-27
---

# 链表标准答案

记忆核心：链表先上 `dummy`。改指针前先保存 `next`，删除/拼接都让指针停在“前一个节点”。

## 2 两数相加

- 题目：两个链表倒序表示两个非负整数，返回它们相加后的倒序链表。
- 思路：像竖式加法一样，一位一位加，维护进位 `carry`。
- 标准答案：

```python
class Solution:
    def addTwoNumbers(self, l1, l2):
        dummy = ListNode(0)
        cur = dummy
        carry = 0

        while l1 or l2 or carry:
            x = l1.val if l1 else 0
            y = l2.val if l2 else 0
            s = x + y + carry
            carry = s // 10
            cur.next = ListNode(s % 10)
            cur = cur.next

            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next

        return dummy.next
```

- 小坑：循环条件要包含 `carry`，最后可能多出一位。

## 19 删除链表的倒数第 N 个结点

- 题目：删除链表倒数第 `n` 个节点，返回头节点。
- 思路：`fast` 先走 `n + 1` 步，让 `slow` 停在待删节点前一个位置。
- 标准答案：

```python
class Solution:
    def removeNthFromEnd(self, head, n):
        dummy = ListNode(0, head)
        fast = slow = dummy

        for _ in range(n + 1):
            fast = fast.next

        while fast:
            fast = fast.next
            slow = slow.next

        slow.next = slow.next.next
        return dummy.next
```

- 小坑：用 `dummy` 才能处理删除头节点的情况。

## 21 合并两个有序链表

- 题目：合并两个升序链表，返回新的升序链表头。
- 思路：谁小就接谁，最后把剩余链表接上。
- 标准答案：

```python
class Solution:
    def mergeTwoLists(self, list1, list2):
        dummy = ListNode(0)
        cur = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                cur.next = list1
                list1 = list1.next
            else:
                cur.next = list2
                list2 = list2.next
            cur = cur.next

        cur.next = list1 if list1 else list2
        return dummy.next
```

- 小坑：循环结束后别忘了接剩余部分。

## 23 合并 K 个升序链表

- 题目：合并 `k` 个升序链表，返回一个升序链表。
- 思路：每条链表只派当前头节点进“小根堆候选池”；每次弹出全局最小节点接到答案，再让它的下一个节点补位。
- 记忆画面：`k` 条队伍都已经从小到大排好，每条队伍最前面的人代表这条队伍参赛；谁最小谁先出列，出列后同队下一个人再来参赛。
- 标准答案：

```python
from heapq import heappush, heappop

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        heap = []
        for i, node in enumerate(lists):
            if node:
                heappush(heap, (node.val, i, node))

        dummy = ListNode(0)
        cur = dummy

        while heap:
            _, i, node = heappop(heap)
            cur.next = node      # 把当前最小节点接到答案后面
            cur = cur.next
            if node.next:
                heappush(heap, (node.next.val, i, node.next))

        return dummy.next
```

- 小坑：堆里只放“当前头节点”，不是一次性放所有节点；弹出谁，就把谁的 `next` 放回堆；元组里的 `i` 是原链表编号，节点值相同时避免 Python 直接比较 `ListNode`，弹出后给 `node.next` 继续沿用同一个 `i`。

## 24 两两交换链表中的节点

- 题目：每两个相邻节点交换一次，不能只交换值。
- 思路：`pre` 永远指向当前一对节点的前一个节点，重接 `a,b`。
- 标准答案：

```python
class Solution:
    def swapPairs(self, head):
        dummy = ListNode(0, head)
        pre = dummy

        while pre.next and pre.next.next:
            a = pre.next
            b = a.next

            pre.next = b
            a.next = b.next
            b.next = a

            pre = a

        return dummy.next
```

- 小坑：交换后 `pre` 要移动到这一对的尾巴，也就是 `a`。

## 25 K 个一组翻转链表

- 题目：每 `k` 个节点一组翻转链表，不足 `k` 个的尾巴保持原样。
- 思路：先找这一组的第 `k` 个节点；数够了才翻转这一段，然后接回前后链表。
- 标准答案：

```python
class Solution:
    def reverseKGroup(self, head, k):
        dummy = ListNode(0, head)
        group_prev = dummy

        while True:
            kth = group_prev
            for _ in range(k):
                kth = kth.next
                if not kth:
                    return dummy.next

            group_next = kth.next
            prev = group_next
            cur = group_prev.next

            while cur != group_next:
                nxt = cur.next
                cur.next = prev
                prev = cur
                cur = nxt

            old_head = group_prev.next
            group_prev.next = kth
            group_prev = old_head
```

- 小坑：不足 `k` 个直接返回；翻转区间是 `[group_prev.next, group_next)`。

## 138 随机链表的复制

- 题目：链表每个节点除了 `next` 还有 `random` 指针，要求深拷贝整条链表。
- 思路：哈希表建立旧节点到新节点的映射，再补 `next/random`。
- 标准答案：

```python
class Solution:
    def copyRandomList(self, head):
        if not head:
            return None

        mp = {}
        cur = head
        while cur:
            mp[cur] = Node(cur.val)
            cur = cur.next

        cur = head
        while cur:
            mp[cur].next = mp.get(cur.next)
            mp[cur].random = mp.get(cur.random)
            cur = cur.next

        return mp[head]
```

- 小坑：`mp.get(None)` 会返回 `None`，正好处理空指针。

## 141 环形链表

- 题目：判断链表是否有环。
- 思路：快慢指针。如果有环，快指针最终会追上慢指针。
- 标准答案：

```python
class Solution:
    def hasCycle(self, head):
        slow = fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True

        return False
```

- 小坑：循环条件必须检查 `fast` 和 `fast.next`。

## 142 环形链表 II

- 题目：如果链表有环，返回入环的第一个节点；没有环返回 `None`。
- 思路：快慢指针相遇后，一个指针回头节点，两个指针同步走，相遇处就是入口。
- 标准答案：

```python
class Solution:
    def detectCycle(self, head):
        slow = fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                p = head
                while p != slow:
                    p = p.next
                    slow = slow.next
                return p

        return None
```

- 小坑：第二阶段两个指针每次都只走一步。

## 146 LRU 缓存

- 题目：设计一个固定容量缓存，`get/put` 都要 O(1)，最近最少使用的 key 要最先淘汰。
- 思路：面试急救用 `OrderedDict`。访问或插入后把 key 移到末尾；超容量时弹出最前面的旧 key。
- 标准答案：

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

- 小坑：`popitem(last=False)` 弹出最久没用的头部元素。

## 148 排序链表

- 题目：对链表排序，要求尽量做到 O(n log n)。
- 思路：归并排序。快慢指针切成两半，分别排序，再合并两个有序链表。
- 标准答案：

```python
class Solution:
    def sortList(self, head):
        if not head or not head.next:
            return head

        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        mid = slow.next
        slow.next = None

        left = self.sortList(head)
        right = self.sortList(mid)
        return self.merge(left, right)

    def merge(self, a, b):
        dummy = ListNode(0)
        cur = dummy

        while a and b:
            if a.val <= b.val:
                cur.next = a
                a = a.next
            else:
                cur.next = b
                b = b.next
            cur = cur.next

        cur.next = a if a else b
        return dummy.next
```

- 小坑：切链必须写 `slow.next = None`，否则递归不会变短。

## 160 相交链表

- 题目：给两条链表，返回它们开始相交的节点；不相交返回 `None`。
- 思路：两个指针分别走 A+B 和 B+A，路程一样；若有交点会同时到达交点。
- 标准答案：

```python
class Solution:
    def getIntersectionNode(self, headA, headB):
        a, b = headA, headB

        while a != b:
            a = a.next if a else headB
            b = b.next if b else headA

        return a
```

- 小坑：比较的是节点对象，不是节点值。

## 206 反转链表

- 题目：反转单链表，返回新头节点。
- 思路：`pre` 是已经反转好的前半段，`cur` 是当前要处理的节点。
- 标准答案：

```python
class Solution:
    def reverseList(self, head):
        pre = None
        cur = head

        while cur:
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt

        return pre
```

- 小坑：改 `cur.next` 前要先保存 `nxt`。

## 234 回文链表

- 题目：判断链表节点值从前往后和从后往前是否一样。
- 思路：快慢指针找中点，反转后半段，再从两头比较。
- 标准答案：

```python
class Solution:
    def isPalindrome(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        pre = None
        cur = slow
        while cur:
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt

        p1, p2 = head, pre
        while p2:
            if p1.val != p2.val:
                return False
            p1 = p1.next
            p2 = p2.next

        return True
```

- 小坑：比较时只需要遍历后半段 `p2`。
