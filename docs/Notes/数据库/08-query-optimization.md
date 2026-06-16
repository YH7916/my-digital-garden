---
title: PPT 08 查询优化
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
blog_dest: Notes/数据库/08-query-optimization.md
---
## 8. PPT 08 查询优化：先让中间结果变小

这一章以 `第十二章 查询优化.docx` 为主要讲解来源。PPT 列出等价规则和统计量；Word 笔记把每个统计量、选择率、join size、嵌套查询优化、物化视图维护讲得更具体。

先记住一句：

```text
查询优化不改变结果，只改变执行路线。
```

优化器在做的事是：

```text
同样的 SQL，哪种关系代数表达式更便宜？
同样的关系代数算子，用哪种物理算法更便宜？
join 顺序怎么排，中间结果最小？
```

### 8.1 等价表达式：形式不同，输出相同

两个关系代数表达式等价，意思是：

```text
写法不同，但对任何合法数据库实例，输出结果都一样。
```

最重要的不是把 15 条规则全背下来，而是抓住三种动作。

第一，选择下推：

```text
能早筛行，就早筛行。
```

例子：

$$\sigma_{student.major='CS'}(student \bowtie takes)$$

可以变成：

$$\big(\sigma_{student.major='CS'}(student)\big) \bowtie takes$$

先把非 CS 学生扔掉，join 时中间结果更小。

第二，投影下推：

```text
能早丢列，就早丢列。
```

如果后面只要：

```text
student.ID, student.name
```

就没必要一直带着 `address/phone/birth_date` 这些列跑完整个计划。

第三，把笛卡尔积加选择改成 join：

$$\sigma_{r.A=s.A}(r \times s) \quad\equiv\quad r \bowtie_{r.A=s.A} s$$

这不是只换符号，而是在提醒优化器：

```text
可以用 hash join / merge join / index nested-loop join。
```

### 8.2 一个 SQL 怎么被改好

SQL：

```sql
SELECT s.name
FROM student s, takes t, course c
WHERE s.ID = t.ID
  AND t.course_id = c.course_id
  AND s.dept_name = 'CS'
  AND c.title = 'Database';
```

差的路线：

```text
student ⋈ takes ⋈ course
最后再筛 CS 和 Database
最后再投影 name
```

好的路线：

```text
先筛 student：dept_name='CS'
先筛 course：title='Database'
再和 takes join
最后只保留 name
```

人话：

```text
先让参赛选手变少，再让他们配对。
```

这就是查询优化的核心直觉。

### 8.3 统计量：优化器靠这些粗略估算成本

Word 笔记列了这些符号：

| 符号 | 含义 |
|---|---|
| $n_r$ | 关系 $r$ 中 tuple 个数 |
| $b_r$ | 关系 $r$ 占多少 block |
| $l_r$ | $r$ 中一条 tuple 的大小 |
| $f_r$ | 一个 block 能放多少条 $r$ 的 tuple |
| $V(A,r)$ | $r$ 中属性 $A$ 有多少个不同值 |

如果关系 r 连续存放：

$$b_r = \lceil n_r / f_r \rceil$$

`V(A,r)` 很重要。它的直觉是：

```text
A 这个属性能把 r 分成多少种值。
```

如果：

```text
nr = 10000
V(dept_name, instructor) = 20
```

在没有直方图的情况下，优化器会粗略假设均匀分布：

$$\text{每个 dept\_name 大约有 } 10000 / 20 = 500 \text{ 个老师}$$

现实不一定均匀，但考试一般按均匀估。

### 8.4 等值选择估计：A=value 大概剩多少行

条件 $A = v$。

如果 A 是 key：结果最多 $1$ 行。

如果 A 不是 key，且均匀分布：

$$\text{估计结果大小} = \frac{n_r}{V(A,r)}$$

例子：

```text
instructor 有 10000 行。
dept_name 有 20 个不同值。
```

估计：

$$\sigma_{dept\_name='CS'}(instructor) \approx \frac{10000}{20} = 500 \ \text{行}$$

### 8.5 范围选择估计：没有 min/max 时常按一半

条件 $A \leq v$。

如果数据库有 min/max，可以按线性比例估：

$$n_r \times \frac{v - \min(A)}{\max(A) - \min(A)}$$

如果没有维护 min/max，常粗略估成 $n_r / 2$。

考试如果题目直接给选择率，比如 $\text{selectivity} = 0.1$，那就直接：

$$\text{结果大小} = 0.1 \times n_r$$

### 8.6 多条件选择：AND 乘起来，OR 用容斥

中选率 selectivity：

```text
一个 tuple 满足条件的概率。
```

如果两个条件独立：

$$P(A \wedge B) = P(A) \times P(B)$$

所以：

$$\text{结果大小} = n_r \times s_1 \times s_2$$

OR 条件用容斥：

$$P(A \vee B) = P(A) + P(B) - P(A) \times P(B)$$

前提是条件独立。

Word 笔记强调这些公式都有独立性假设。现实中 `major='CS'` 和 `takes Database` 可能相关，但考试通常按独立算。

### 8.7 Join size：先看有没有 key / foreign key

估计 join 大小时，先问：

```text
连接属性是不是某边的 key？
有没有 foreign key 约束？
```

情况 1：没有公共属性。

$$|r \times s| = n_r \times n_s$$

情况 2：连接属性是 R 的 key。

$$\text{S 中每条 tuple 最多匹配 R 中一条} \implies |r \bowtie s| \leq n_s$$

情况 3：连接属性是 R 的 key，而且 S 的该属性是指向 R 的 foreign key。

$$\text{S 中每条 tuple 都一定能匹配 R 中一条} \implies |r \bowtie s| = n_s$$

情况 4：连接属性不是 key。

常用估计：

$$|r \bowtie s| \approx \frac{n_r \times n_s}{\max(V(A,r),\ V(A,s))}$$

Word 笔记里的直觉：

```text
站在 r 的一条 tuple 看，s 里大约有 ns / V(A,s) 条能和它同值。
反过来站在 s 看也可以。
取更保守的估计。
```

考试常写：

$$|r \bowtie s| \approx \min\!\left(\frac{n_r n_s}{V(A,r)},\ \frac{n_r n_s}{V(A,s)}\right)$$

这等价于除以较大的 $V$。

### 8.8 中间结果的 V(A, result) 怎么估

这类题容易显得抽象。记住两个直觉。

选择之后：

$$V(A,\ \sigma_{condition}(r)) \leq V(A,r), \qquad V(A,\ \sigma_{condition}(r)) \leq \text{选择结果大小}$$

所以常估：

$$\min\big(V(A,r),\ \text{result tuple count}\big)$$

连接之后，如果 A 只来自 r：

$$V(A,\ r \bowtie s) \leq V(A,r)$$

如果 A 是连接属性，结果里的不同值不会超过两边较小的那个：

$$\min\big(V(A,r),\ V(A,s)\big)$$

这类估算不是为了绝对准确，而是为了比较计划大小。

### 8.9 Join 顺序：最关心中间结果

如果要 join 五张表，理论上计划非常多，不可能全靠人枚举。

优化器会用动态规划：

```text
先求每个小集合的最优计划；
再把小集合组合成更大集合；
最后得到整体最优或近似最优。
```

两类树：

```text
非左深树：左右两边都可以是中间结果。
左深树：右边总是一张基础表，左边可以是中间结果。
```

左深树更常用，因为：

```text
搜索空间小；
适合流水线执行；
实现更简单。
```

启发式规则：

```text
1. 尽早选择，减少行数。
2. 尽早投影，减少列数。
3. 先做限制最强的选择和 join。
4. 倾向使用左深 join tree。
```

### 8.10 嵌套查询优化：能改成半连接就别一行行查

Word 笔记里提到嵌套查询可能很慢。

例子：

```sql
SELECT name
FROM instructor i
WHERE EXISTS (
  SELECT *
  FROM teaches t
  WHERE t.ID = i.ID
    AND t.year = 2025
);
```

如果天真执行：

```text
对每个 instructor，都扫一遍 teaches。
```

这就是两重循环。

如果内层查询依赖外层属性 `i.ID`，优化器可以把它改写成半连接：

```text
先筛 teaches：year=2025
再取其中的 ID
再用这些 ID 去筛 instructor
```

半连接 `r ⋉ s` 的意思：

```text
只保留 r 中能和 s 匹配的 tuple；
不把 s 的属性拼到结果里。
```

这很适合 `EXISTS` / `IN` 这类“只问有没有”的查询。

### 8.11 物化视图和增量维护

物化视图：

```text
把某个查询结果真的存下来。
```

好处：

```text
下次查询快。
```

坏处：

```text
底层表变了，视图也要维护。
```

增量维护的核心：

```text
只算变化带来的差分，不重算整个视图。
```

例子 1：视图是选择：

```text
V = σ_salary>100000(instructor)
```

插入一条 instructor 时：

```text
只检查这条新 tuple 是否 salary>100000。
如果满足，就加入 V。
```

例子 2：视图是 join：

```text
V = r ⋈ s
```

如果 r 新插入一条 tuple：

```text
只拿这条新 tuple 和 s join；
把新增结果并入 V。
```

例子 3：视图是 group by count：

```text
V(A, count)
```

插入一条 tuple：

```text
如果它的 A 值已有分组，对应 count + 1。
如果是新 A 值，插入新分组，count = 1。
```

### 8.12 查询优化 A4 规则

```text
优化不改结果，只改执行路线。
选择下推：先筛行。
投影下推：先丢无用列。
笛卡尔积 + 选择条件 = join。
等值选择：非 key 估 nr / V(A,r)，key 估 1。
范围选择：无 min/max 时常估 nr/2。
AND selectivity 相乘；OR 用 s1+s2-s1*s2。
key join：若 R.A 是 key，则结果 <= ns。
foreign key join：若 S.A -> R.A，则结果 = ns。
普通等值 join：nr*ns / max(V(A,r), V(A,s))。
join 顺序优先让中间结果小。
EXISTS/IN 常可改成半连接。
物化视图维护看差分，不重算全量。
```
