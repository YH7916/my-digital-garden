---
title: PPT 07 查询处理
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
blog_dest: Notes/数据库/07-query-processing.md
---
## 7. PPT 07 查询处理：同一句 SQL，数据库到底怎么跑

这一章以 `第十一章 查询处理.docx` 为主要讲解来源。PPT 给了算法名，Word 笔记真正讲清楚了 cost 为什么这么算，尤其是 selection、external sort、block nested-loop join、hash join。

全章主线：

```text
逻辑优化：关系代数表达式怎么变形，比如选择下推。
物理优化：同一个算子具体用什么算法，比如全表扫、B+ 树、hash join。
代价估计：主要数 block transfer 和 seek。
```

### 7.1 代价符号：先把每个字母翻译成人话

| 符号 | 含义 |
|---|---|
| $n_r$ | 关系 $r$ 的 tuple 数 |
| $b_r$ | 关系 $r$ 占用的 block 数 |
| $l_r$ | 关系 $r$ 的一条 tuple 大小 |
| $f_r$ | blocking factor，一个 block 能放多少 tuple |
| $M$ | 内存 buffer 一共有多少个 block |
| $t_T$ | 传输一个 block 的时间 |
| $t_S$ | 一次 seek / 随机定位的时间 |
| $V(A,r)$ | $r$ 中属性 $A$ 有多少个不同值 |

考试默认：

```text
只估算磁盘 I/O。
忽略 CPU 成本。
通常忽略最终输出写回磁盘的成本，除非题目特别说要算。
假设需要的数据不在 buffer 里，按最坏情况估。
```

第一步永远是：

$$f_r = \left\lfloor \frac{block\_size}{tuple\_size} \right\rfloor, \qquad b_r = \left\lceil \frac{n_r}{f_r} \right\rceil$$

不要拿 tuple 数直接套 join 公式。

### 7.2 Selection：先判断全表扫还是用索引

Selection 就是 $\sigma_{condition}(r)$。

人话：

```text
从表 r 里筛出满足条件的行。
```

#### A1 线性扫描

如果没有可用索引，就扫整个文件。

如果文件连续存放：

$$\text{cost} = b_r \ \text{transfers} + 1 \ \text{seek}$$

如果条件是 key 等值查询，比如：

```text
ID = '123'
```

平均找到一半就能停：

$$\text{cost} \approx \frac{b_r}{2} \ \text{transfers} + 1 \ \text{seek}$$

但最坏情况还是可能扫完整表。

#### A2/A3 主索引或聚集索引

如果数据文件按属性 A 排序，并且 A 上有 B+ 树索引：

```text
先走 B+ 树找到第一个匹配位置；
再顺序读匹配的数据块。
```

如果 A 是 key：

```text
只会有一条记录。
```

如果 A 不是 key：

```text
可能有多条，但因为文件按 A 排，它们通常连续存放。
```

所以聚集索引对范围查询很舒服。

#### A4/A4' 辅助索引

辅助索引的关键问题：

```text
索引顺序和数据文件顺序不同。
```

如果辅助索引查的是 key：

```text
只返回一条记录，通常没问题。
```

如果辅助索引查的是 non-key：

```text
可能返回很多记录；
这些记录可能散落在很多数据块中；
每个数据块都可能要一次随机 I/O。
```

所以客观题常见结论：

```text
二级索引不是永远比全表扫描快。
当返回结果很多时，二级索引可能很慢。
```

### 7.3 多条件 selection：先用最能过滤的条件

如果条件是：

```text
dept_name = 'CS' AND salary > 100000
```

Word 笔记里的策略：

```text
先选择过滤最狠的条件。
```

比如：

```text
dept_name='CS' 剩 30%
salary>100000 剩 5%
```

就先用 `salary>100000`。

常见算法：

```text
A7：用一个索引先筛，再在内存里检查其他条件。
A8：如果有复合索引，优先用复合索引。
A9：每个条件分别用索引找 record id，再取交集。
A10：OR 条件可分别找 record id，再取并集；但最好每个条件都有索引。
```

### 7.4 External sort：内存放不下，就先分 run 再归并

如果关系 `r` 有 `br` 个 block，内存有 `M` 个 block。

第一阶段 run generation：

```text
每次读 M 个 block 到内存；
在内存里排序；
写回磁盘，形成一个 sorted run。
```

初始 run 个数：

$$N = \lceil b_r / M \rceil$$

这个阶段：

$$\text{读 } b_r \text{ 个 block，写 } b_r \text{ 个 block} \implies \text{transfers} = 2 b_r$$

第二阶段 merge：

```text
每轮最多归并 M-1 个 run。
```

为什么是 `M-1`？

```text
每个输入 run 需要 1 个 input buffer；
还要留 1 个 output buffer。
```

需要的归并轮数：

$$\left\lceil \log_{M-1}(N) \right\rceil$$

代价要看题目是否把最终结果写回磁盘。

常用记忆：

```text
每完整一轮：读一遍 + 写一遍 = 2br transfers。
如果最后结果直接送给下一个算子，最后一轮可以少写一次。
```

考试如果只问算法流程，就写：

```text
先生成 sorted runs，再多路归并。
```

### 7.5 Nested-loop join：最朴素，但通常最慢

Join 是 $r \bowtie s$。

人话：

```text
把 r 和 s 中满足连接条件的 tuple 拼起来。
```

Tuple nested-loop join：

```text
外表每一条 tuple，都去扫一遍内表。
```

如果外关系是 `r`，内关系是 `s`：

$$\text{transfers} \approx b_r + n_r \times b_s$$

因为：

```text
r 的每个 block 至少读一次；
r 的每条 tuple 都要让 s 全表进来一次。
```

这个算法一般只是理解基线，真正考试更常算 block nested-loop join。

### 7.6 Block nested-loop join：外表一次装 M-2 个 block

Block nested-loop join 的画面：

```text
把 outer 的一批 block 放进内存；
再顺序扫描 inner 的所有 block；
在内存里做匹配。
```

为什么是 `M-2`？

```text
1 个 buffer 留给 inner 输入。
1 个 buffer 留给 output。
剩下 M-2 个 buffer 装 outer。
```

公式：

$$\text{transfers} = B(outer) + \left\lceil \frac{B(outer)}{M-2} \right\rceil \times B(inner)$$

seek 粗略理解：

```text
outer 每批一次 seek；
inner 每轮扫描一次 seek。
```

做题模板：

```text
1. 让 R 做 outer 算一次。
2. 让 S 做 outer 算一次。
3. 选代价小的。
```

例子：

```text
B(R)=100, B(S)=500, M=12
```

R 做 outer：

$$100 + \lceil 100/10 \rceil \times 500 = 5100$$

S 做 outer：

$$500 + \lceil 500/10 \rceil \times 100 = 5500$$

选 R 做 outer。

### 7.7 Index nested-loop join：内表连接属性有索引时很香

Index nested-loop join 的条件：

```text
inner relation 在 join attribute 上有索引。
```

画面：

```text
outer 每来一条 tuple；
拿 join key 去 inner 的索引里查匹配 tuple。
```

如果 outer 是 `r`：

```text
读 outer 的成本 + nr 次索引查找成本
```

它适合：

```text
outer 较小；
inner join key 上有好索引；
每次索引查找返回不多。
```

如果每次查索引都返回很多分散记录，它也会变差。

### 7.8 Sort-merge join：两边有序时，像拉拉链

Sort-merge join 适用于等值连接，尤其是两边已经按 join key 排好序时。

流程：

```text
1. r 和 s 都按 join attribute 排序。
2. 两个指针分别指向 r 和 s 当前最小 key。
3. key 小的一边往前走。
4. key 相等时，输出所有匹配组合。
```

如果两边已经排好序：

$$\text{transfers} \approx b_r + b_s$$

如果没排序，要先加外部排序成本。

它的直觉就是归并排序最后一步：

```text
两个有序列表，从左到右同步推进。
```

### 7.9 Hash join：先分桶，再桶内匹配

Hash join 是你当前最需要补画面的部分。

它只适合：

```text
等值连接。
```

例如 $r.A = s.A$。

#### 第一步：partition，按连接属性分桶

用同一个 hash 函数 `h`：

```text
r 的每条 tuple 按 h(A) 放进 r0, r1, r2...
s 的每条 tuple 按 h(A) 放进 s0, s1, s2...
```

关键性质：

```text
能连接上的 tuple，join key 相等；
join key 相等，hash 值相同；
所以它们一定被分到同编号桶里。
```

因此：

```text
r0 只需要和 s0 join；
r1 只需要和 s1 join；
r0 不需要和 s1 join。
```

这一步就是把大问题切成很多小问题。

#### 第二步：build/probe，桶内连接

对每个桶 `i`：

```text
把较小的 si 放进内存，建立内存 hash table。
再读 ri 的每条 tuple，去这个 hash table 里探测匹配项。
```

术语：

```text
build input：能放进内存的小桶，用它建立 hash table。
probe input：另一边的桶，逐条拿来查 hash table。
```

一般选小关系做 build input，因为它的每个 partition 更容易放进内存。

#### buffer 为什么限制 partition 数

如果要一次分成 `N` 个 partition：

```text
每个 partition 至少需要一个 output buffer。
```

内存一共 `M` 个 block，通常最多分 $M-1$ 个 partition，还要留一个 input buffer。

#### 什么时候不用 recursive partition

Hash join 希望 build input 的每个 partition 能放进内存。

如果 build relation 有 `b_build` 个 block，分成 `N` 个桶，平均每桶 $b_{build} / N$。

希望：

$$\frac{b_{build}}{N} \leq M - 2$$

也就是每个 build partition 能放进内存，还留出输入/输出空间。

如果做不到：

```text
某些桶还是太大，需要 recursive partition，再分一次桶。
```

#### 2021 样卷画面

题目类似：

```text
r = 100 blocks
s = 20 blocks
M = 6
```

选 build：

```text
s 小，所以 s 是 build input。
```

最多 partition：$M - 1 = 5$。

s 平均每桶：$20 / 5 = 4$ blocks。

内存可容纳 build partition：$M - 2 = 4$ blocks。

刚好放下，所以不需要 recursive partition。

如果不递归，block transfer 近似：

$$\text{partition 阶段：读 } r{+}s\text{，写 } r{+}s \to 2(b_r + b_s)$$
$$\text{join 阶段：再读 } r{+}s \to b_r + b_s$$
$$\text{总计：} 3(b_r + b_s)$$

对于上例：

$$3 \times (100 + 20) = 360 \ \text{transfers}$$

题目如果要求算 seek，按它给的 `bb`、连续存放假设再补。

### 7.10 查询处理 A4 规则

```text
先算 br，别直接用 nr。
全表扫：br transfers + 1 seek；key 平均 br/2。
secondary index 返回很多记录时可能很慢。
BNLJ：B(outer)+ceil(B(outer)/(M-2))*B(inner)，两边都试。
External sort：初始 runs = ceil(br/M)，每轮最多 merge M-1 个 runs。
Sort-merge join：两边已有序时约 br+bs；没序先加排序成本。
Hash join：等值连接；partition 后同编号桶 join。
Hash join build 选小表；最多 M-1 个 partition。
不递归 hash join transfers 约 3(br+bs)。
build partition 必须能放进内存，否则 recursive partition。
```
