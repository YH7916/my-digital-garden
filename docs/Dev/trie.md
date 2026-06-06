---
title: Trie 
tags: [learning, leetcode, hot100, trie]
updated: 2026-05-27
---

# Trie 标准答案

记忆核心：Trie 是一棵字符树。每个节点有 `children` 字典和 `is_end` 标记。

## 208 实现 Trie

- 题目：实现前缀树，支持插入单词、查找完整单词、查找前缀。
- 思路：从根节点开始，一个字符走一层；没有节点就创建。
- 标准答案：

```python
class Node:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = Node()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def startsWith(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
```

- 小坑：`search` 要检查 `is_end`；`startsWith` 不需要。