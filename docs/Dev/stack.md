---
title: 栈与单调栈
tags: [learning, leetcode, hot100, stack, monotonic-stack]
updated: 2026-05-27
---

# 栈与单调栈标准答案

记忆核心：普通栈处理“最近的未匹配”；单调栈处理“某个元素第一次被右边元素结算”。

## 20 有效的括号

- 题目：判断括号字符串是否合法。每个右括号必须匹配最近的左括号。
- 思路：左括号入栈；右括号来时，栈顶必须是对应左括号。
- 标准答案：

```python
class Solution:
    def isValid(self, s):
        mp = {')': '(', ']': '[', '}': '{'}
        stack = []

        for ch in s:
            if ch in mp:
                if not stack or stack[-1] != mp[ch]:
                    return False
                stack.pop()
            else:
                stack.append(ch)

        return not stack
```

- 小坑：这里 `mp` 用右括号映射左括号；遇到右括号才检查栈顶。

## 84 柱状图中最大的矩形

- 题目：给一排柱子高度，找能组成的最大矩形面积。
- 思路：单调递增栈。当前柱子更矮时，说明被弹出的柱子找到了右边界；左边界是弹出后新的栈顶。
- 标准答案：

```python
class Solution:
    def largestRectangleArea(self, heights):
        heights.append(0)
        stack = [-1]
        ans = 0

        for i, h in enumerate(heights):
            while stack[-1] != -1 and heights[stack[-1]] > h:
                height = heights[stack.pop()]
                width = i - stack[-1] - 1
                ans = max(ans, height * width)
            stack.append(i)

        heights.pop()
        return ans
```

- 小坑：`width = i - stack[-1] - 1`；末尾加 0 是为了把栈里剩余柱子全部结算。

## 155 最小栈

- 题目：设计一个栈，支持 push、pop、top，并能 O(1) 返回当前最小值。
- 思路：一个普通栈存所有数，一个辅助栈同步存“到当前位置为止的最小值”。
- 标准答案：

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        if self.min_stack:
            self.min_stack.append(min(val, self.min_stack[-1]))
        else:
            self.min_stack.append(val)

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]
```

- 小坑：两个栈要同步 push/pop，否则最小值会错位。

## 394 字符串解码

- 题目：把形如 `3[a2[c]]` 的编码字符串还原成 `accaccacc`。
- 思路：遇到 `[` 时，把当前字符串和重复次数压栈；遇到 `]` 时弹出上一层并拼接。
- 标准答案：

```python
class Solution:
    def decodeString(self, s):
        stack = []
        cur = ''
        num = 0

        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch == '[':
                stack.append((cur, num))
                cur = ''
                num = 0
            elif ch == ']':
                prev, k = stack.pop()
                cur = prev + cur * k
            else:
                cur += ch

        return cur
```

- 小坑：数字可能是多位数，所以 `num = num * 10 + int(ch)`。

## 739 每日温度

- 题目：给每天温度，返回每一天还要等几天才会遇到更高温度；没有就填 0。
- 思路：单调递减栈存下标。当前温度更高时，弹出之前更低的天数并结算等待天数。
- 标准答案：

```python
class Solution:
    def dailyTemperatures(self, temperatures):
        ans = [0] * len(temperatures)
        stack = []

        for i, t in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < t:
                j = stack.pop()
                ans[j] = i - j
            stack.append(i)

        return ans
```

- 小坑：栈里放下标，答案是下标差 `i - j`。