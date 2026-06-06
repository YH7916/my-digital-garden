---
title: 图与 BFS/DFS
tags: [learning, leetcode, hot100, graph, bfs, dfs]
updated: 2026-05-27
---

# 图与 BFS/DFS 标准答案

记忆核心：网格题四方向扩散；课程表是拓扑排序；多源扩散先把所有起点一起入队。

## 200 岛屿数量

- 题目：二维网格里 `1` 是陆地、`0` 是水，统计有多少块岛屿。上下左右相连算同一块。
- 思路：遇到一块没访问过的陆地，答案加一，然后 DFS 把整座岛沉掉。
- 标准答案：

```python
class Solution:
    def numIslands(self, grid):
        m, n = len(grid), len(grid[0])

        def dfs(i, j):
            if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != '1':
                return
            grid[i][j] = '0'
            dfs(i + 1, j)
            dfs(i - 1, j)
            dfs(i, j + 1)
            dfs(i, j - 1)

        ans = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1':
                    ans += 1
                    dfs(i, j)

        return ans
```

- 小坑：题目里陆地是字符串 `'1'`，不是数字 `1`。

## 207 课程表

- 题目：有课程依赖关系，判断能不能学完所有课程。
- 思路：拓扑排序。入度为 0 的课可以先学，学完后减少后续课程入度。
- 标准答案：

```python
from collections import deque

class Solution:
    def canFinish(self, numCourses, prerequisites):
        graph = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses

        for a, b in prerequisites:
            graph[b].append(a)
            indeg[a] += 1

        q = deque(i for i in range(numCourses) if indeg[i] == 0)
        count = 0

        while q:
            x = q.popleft()
            count += 1
            for y in graph[x]:
                indeg[y] -= 1
                if indeg[y] == 0:
                    q.append(y)

        return count == numCourses
```

- 小坑：`[a, b]` 表示学 `a` 前要先学 `b`，边是 `b -> a`。

## 994 腐烂的橘子

- 题目：网格里 2 是烂橘子、1 是新鲜橘子、0 是空格；每分钟烂橘子让相邻新鲜橘子腐烂，问几分钟全烂，不能全烂返回 -1。
- 思路：多源 BFS。所有初始烂橘子同时入队，按层扩散。
- 标准答案：

```python
from collections import deque

class Solution:
    def orangesRotting(self, grid):
        m, n = len(grid), len(grid[0])
        q = deque()
        fresh = 0

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    q.append((i, j))
                elif grid[i][j] == 1:
                    fresh += 1

        minutes = 0
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while q and fresh > 0:
            for _ in range(len(q)):
                i, j = q.popleft()
                for di, dj in dirs:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                        grid[ni][nj] = 2
                        fresh -= 1
                        q.append((ni, nj))
            minutes += 1

        return minutes if fresh == 0 else -1
```

- 小坑：只有发生一层扩散后才加一分钟；`fresh == 0` 时直接返回 0。