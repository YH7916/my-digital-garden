---
title: 数据库系统期末终极复习讲义
tags:
  - learning
  - courses
  - database
  - finals
  - exam
  - ultimate-review
updated: 2026-06-16
publish: true
blog_dest: Notes/数据库/index.md
---
# 数据库系统期末终极复习讲义

这套 DB wiki 现在以 `D:\Plan\.raw\期末复习\CA\数据库系统期末梳理.pdf` 为纲，但讲解主体来自同目录下的逐章 `.docx` 口语笔记。原始 PPT / PDF 负责定顺序、定考试重点；Word 笔记负责把每个概念说完整；wiki 负责把这些内容重写成从零基础也能跟着做题的复习资料。

旧的 DB 分散页面已删除。后续所有 DB 复习、补洞、做题、A4 纸整理，都以本目录下这些章节文件为准。

## 使用方式

```text
1. 先看下面同名 wiki 章节，建立人话画面和做题动作。
2. 再回原始 PPT/PDF 对照页码，确认考试骨架。
3. 如果 PPT 某页看不懂，优先回到 wiki 对应小节看 Word 笔记扩写版。
4. 做题卡住时，回到对应章节的模板 / A4 规则。
```

## 章节目录

| PPT 章节 | 页码 | Wiki 讲义 | 目标 |
|---|---:|---|---|
| 01 备考建议 | 2-4 | [考试地图](00-exam-map.md) | 知道 DB 考什么、怎么安排复习 |
| 02 关系代数 | 5-28 | [关系代数](01-relational-algebra.md) | 表、键、筛行、挑列、拼表 |
| 03 SQL 语句 | 29-80 | [SQL](02-sql.md) | 会写查询、聚合、嵌套查询 |
| 03 E-R 模型 | 81-100 | [E-R 模型](03-er-model.md) | 会画 E-R 和转 schema |
| 04 数据库设计 | 101-128 | [数据库设计与范式](04-design-normalization.md) | 会算闭包、候选键、BCNF/3NF |
| 05 数据库存储 | 129-143 | [数据库存储](05-storage.md) | 理解 block、buffer、I/O |
| 06 数据库索引 | 144-172 | [索引与 B+ Tree](06-index-btree.md) | 会 B+ Tree 插入删除和索引判断 |
| 07 查询处理 | 173-185 | [查询处理](07-query-processing.md) | 会 scan / join / hash join 代价 |
| 08 查询优化 | 186-196 | [查询优化](08-query-optimization.md) | 会选择下推、投影下推、估计结果 |
| 事务夹层 + 09 并发控制 | 197-210 | [事务与并发控制](09-transactions-concurrency.md) | 会前驱图、2PL、死锁、recoverable |
| 10 错误恢复 | 211-225 | [错误恢复](10-recovery.md) | 会 WAL、Undo/Redo、ARIES 三遍 |
| 补充 XML | 样卷补充 | [XML 补充](11-xml.md) | 拿 XML / DTD / XPath 保底分 |
| A4 与路线 | 总复习 | [A4 与路线](12-objective-a4-roadmap.md) | 客观题坑、A4 纸、最后复习路线 |

## 当前原则

```text
PPT 是纲，决定章节顺序和考试骨架。
Word 笔记是主要讲解来源，负责把 PPT 没讲透的地方讲完整。
能转成文字讲清楚的，不用截图糊弄。
只有 ER 图、B+ Tree、并发等待图、日志/ARIES 表这类结构图，才保留图片。
每章都要落到“这类题第一笔写什么”和“A4 纸怎么记”。
```
