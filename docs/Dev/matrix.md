---
title: 矩阵
description: 矩阵题型模板与 Hot100 题解，覆盖旋转图像、螺旋矩阵、矩阵置零和二维搜索。
tags:
  - learning
  - leetcode
  - hot100
  - matrix
updated: 2026-05-27
---

# 矩阵标准答案

记忆核心：矩阵先分清行列。访问永远是 `matrix[行][列]`。

## 48 旋转图像

- 题目：把 `n*n` 矩阵原地顺时针旋转 90 度。
- 思路：先沿主对角线转置，再反转每一行。
- 标准答案：

```python
class Solution:
    def rotate(self, matrix):
        n = len(matrix)

        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        for row in matrix:
            row.reverse()
```

- 小坑：原地修改，不需要返回矩阵。

## 54 螺旋矩阵

- 题目：按顺时针螺旋顺序返回矩阵所有元素。
- 思路：维护上下左右四条边界，每走完一圈就收缩边界。
- 标准答案：

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        l, r, t, b = 0, len(matrix[0]) - 1, 0, len(matrix) - 1
        res = []

        while True:
            for i in range(l, r + 1):
                res.append(matrix[t][i])
            t += 1
            if t > b:
                break

            for i in range(t, b + 1):
                res.append(matrix[i][r])
            r -= 1
            if l > r:
                break

            for i in range(r, l - 1, -1):
                res.append(matrix[b][i])
            b -= 1
            if t > b:
                break

            for i in range(b, t - 1, -1):
                res.append(matrix[i][l])
            l += 1
            if l > r:
                break

        return res
```

- 小坑：每走完一条边就立刻检查边界；`l/r` 是列边界，`t/b` 是行边界。

## 73 矩阵置零

- 题目：如果某个元素是 0，就把它所在行和列全部置为 0，要求原地修改。
- 思路：用第一行和第一列做标记，额外记录第一行是否本来有 0。
- 标准答案：

```python
class Solution:
    def setZeroes(self, matrix):
        m, n = len(matrix), len(matrix[0])
        first_row_zero = any(matrix[0][j] == 0 for j in range(n))

        for i in range(1, m):
            for j in range(n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        for i in range(1, m):
            for j in range(n - 1, -1, -1):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        if first_row_zero:
            for j in range(n):
                matrix[0][j] = 0
```

- 小坑：从第二行开始处理，第一行单独记录。

## 240 搜索二维矩阵 II

- 题目：矩阵每行升序、每列升序，判断 target 是否存在。
- 思路：从右上角出发。当前值太大就左移，太小就下移。
- 标准答案：

```python
class Solution:
    def searchMatrix(self, matrix, target):
        m, n = len(matrix), len(matrix[0])
        i, j = 0, n - 1

        while i < m and j >= 0:
            if matrix[i][j] == target:
                return True
            if matrix[i][j] > target:
                j -= 1
            else:
                i += 1

        return False
```

- 小坑：240 不是 74；这里不能把矩阵整体当一维有序数组。
