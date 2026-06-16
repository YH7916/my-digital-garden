---
title: 客观题、A4 纸与复习路线
tags:
  - learning
  - courses
  - database
  - finals
  - exam
  - ppt-expanded
  - docx-first
updated: 2026-06-16
publish: true
blog_dest: Notes/数据库/12-objective-a4-roadmap.md
---
## 12. 客观题常见坑

这页不是新知识，而是最后压缩。前面章节读完后，用它检查自己有没有抓住题眼。

```text
1. 3NF 可以做到无损且依赖保持；BCNF 可以无损，但不一定依赖保持。
2. BCNF 要求每条非平凡 FD 的左边都是 super key。
3. 4NF 处理不相关的多值依赖，避免组合爆炸。
4. secondary index 通常是 dense；sparse index 通常要求文件按 search key 有序。
5. index scan 不一定总比 full table scan 快，二级索引返回大量行时可能很慢。
6. B+ tree order n：内部最多 n 个孩子，叶子最多 n-1 个 key。
7. selection / projection 下推减少中间结果，不改变最终答案。
8. Hash join 只适合等值连接；build input 选小表。
9. conflict serializable 一定 view serializable，反过来不一定。
10. 2PL 保证 conflict serializable，但不是必要条件。
11. tree protocol 不是 2PL，但能保证 conflict serializable 且无死锁。
12. wait-for graph 有环是死锁；precedence graph 有环是不可冲突串行化。
13. strict 2PL 比 basic 2PL 更能防 dirty read / 级联回滚。
14. ARIES redo history，不是只 redo committed transactions。
15. CLR 不再被 undo，Undo 时沿 UndoNextLSN 继续。
```

## 13. 最后一张 A4 纸应该写什么

如果只能带一张 A4，优先写公式、判断模板、做题顺序，不写大段定义。

### SQL

```text
SQL 四问：输出什么 SELECT；来自哪些表 FROM；表怎么接 JOIN/WHERE；怎么筛/分组/排序。
WHERE 筛原始行，HAVING 筛分组。
GROUP BY 后 SELECT 普通列必须在 GROUP BY 里。
并列最大/平均以上：先造统计表 T，再和 MAX/AVG 比较。
EXISTS 问有没有；NOT EXISTS 常表达“所有/不存在没满足的”。
```

### E-R

```text
名词找实体，动词找联系。
1:N：把 1 端主键放进 N 端。
M:N：单独建联系表，主键通常是两端主键组合。
弱实体主键 = 强实体主键 + 自己部分键。
多值属性单独建表。
双线全参与，常对应 NOT NULL / 必须存在关系。
```

### 范式

```text
闭包：X+ 从 X 开始，能推就加，直到不变。
候选键：先找没出现在 RHS 的属性，再算闭包。
```

- 无损二表分解：$(R_1 \cap R_2) \to R_1$ 或 $(R_1 \cap R_2) \to R_2$。
- BCNF：$X \to Y$ 非平凡，则 $X$ 必须是 super key。
- BCNF 拆：$R_1 = X \cup Y$，$R_2 = R - (Y - X)$。
- 3NF：$X$ super key，或右边是 prime attribute。
- 4NF：非平凡多值依赖 $X \twoheadrightarrow Y$ 中，$X$ 必须是 super key。

### Storage / Index

$$f_r = \lfloor block\_size / record\_size \rfloor, \qquad b_r = \lceil n_r / f_r \rceil$$

```text
dirty page 被替换前必须写回；pin count > 0 不能替换。
B+ tree: internal max n children / n-1 keys; leaf max n-1 keys。
leaf split：右 leaf 第一个 key 复制到父节点。
internal split：中间 key 上移，不留在原 internal。
delete：underflow -> borrow else merge -> update separator。
Buffer Tree：insert 先进 buffer，满了批量下推；查询要看 buffer。
```

B+ 树容量：$n \cdot p + (n-1) \cdot k \leq block\_size$。

### Query Cost

$$\text{Full scan: } b_r \ \text{transfers} + 1 \ \text{seek}$$
$$\text{BNLJ: } B(o) + \lceil B(o)/(M-2) \rceil \times B(i) \quad (\text{两边都试})$$
$$\text{External sort: runs} = \lceil b_r / M \rceil, \quad \text{每轮最多 merge } M-1 \ \text{个 runs}$$
$$\text{Hash join: partitions} \leq M-1, \quad \text{build} = \text{small relation}$$
$$\text{One-pass hash join transfers} \approx 3(b_r + b_s)$$
$$\text{Selection estimate: } n_r / V(A,r) \qquad \text{Join estimate: } \frac{n_r n_s}{\max(V(A,r), V(A,s))}$$

### Concurrency

```text
Conflict = different transactions + same item + at least one write。
Precedence graph: earlier conflicting op's transaction -> later transaction。
cycle => not conflict serializable；no cycle => topological order。
View serializable: same initial reads, reads-from, final writes。
Recoverable: writer commits before reader commits。
Cascadeless: only read committed data。
S/S compatible；S/X, X/S, X/X conflict。
2PL: growing then shrinking；Strict 2PL holds X locks until commit/abort。
Wait-for graph cycle => deadlock。
IS/IX/SIX 是多粒度父节点上的意向锁。
```

### ARIES

```text
WAL: log before data。
ARIES: Analysis -> Redo -> Undo。
ATT: transaction, status, LastLSN。
DPT: page, RecLSN。
Redo starts from min RecLSN in DPT。
Redo skip: page not in DPT; LSN < RecLSN; PageLSN >= LSN。
Undo losers from LastLSN backward, write CLR。
CLR has UndoNextLSN and is not undone again。
Logical undo: undo operation, not simply restore old value。
```

## 14. 复习路线

不要从头精读三遍。按题型推进：

```text
第一轮：读本讲义，每章只抓画面、模板、A4 规则。
第二轮：做 2025 final review -2，遇到卡点回对应章节。
第三轮：做 2021 样卷，重点 B+ Tree / Hash Join / Concurrency / Recovery。
第四轮：把错题压成 A4 规则。
第五轮：考前只翻 A4 和错题，不再重学整章。
```

如果状态很差，只做一件事：

```text
随机拿一道题，先判断题型，再写第一笔。
```

DB 期末的目标不是像研究者一样讲完所有系统细节，而是：

```text
看到 SQL 知道怎么拼表。
看到 ER 知道怎么圈实体和联系。
看到 FD 知道算闭包。
看到 B+ Tree 知道容量和 split/merge。
看到 cost 知道先算 block。
看到 hash join 知道 partition/build/probe。
看到 schedule 知道画前驱图或等待图。
看到 log 知道 ARIES 三遍。
```

## 15. 本讲义参考的本地资料

- `D:\Plan\.raw\期末复习\CA\数据库系统期末梳理.pdf`
- `D:\Plan\.raw\期末复习\CA\第三章 introduction to SQL.docx`
- `D:\Plan\.raw\期末复习\CA\第六章 ER模型.docx`
- `D:\Plan\.raw\期末复习\CA\第七章 关系数据库设计.docx`
- `D:\Plan\.raw\期末复习\CA\第九章 数据存储.docx`
- `D:\Plan\.raw\期末复习\CA\第十章 索引.docx`
- `D:\Plan\.raw\期末复习\CA\第十一章 查询处理.docx`
- `D:\Plan\.raw\期末复习\CA\第十二章 查询优化.docx`
- `D:\Plan\.raw\期末复习\CA\第十三章 事务管理.docx`
- `D:\Plan\.raw\期末复习\CA\第十四章 并发控制.docx`
- `D:\Plan\.raw\期末复习\CA\第十四章 数据恢复.docx`
- `D:\Plan\.raw\期末复习\DB\样卷\2025 final review -1/-2`
- `D:\Plan\.raw\期末复习\DB\样卷\cs 18/19/21 DB final`
- `D:\Plan\.raw\期末复习\DB\NoughtQ_DB_Notes\`
