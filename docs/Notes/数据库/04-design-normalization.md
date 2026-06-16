---
title: PPT 04 数据库设计：范式与函数依赖
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
blog_dest: Notes/数据库/04-design-normalization.md
---
## 4. PPT 04 数据库设计：坏表为什么要拆

这一章以 `第七章 关系数据库设计.docx` 为主要讲解来源。PPT 的关键词是 FD、closure、BCNF、3NF、4NF；Word 笔记真正讲清楚的是：一张坏表为什么会冗余、怎么用函数依赖证明它坏、怎么拆才不丢信息。

先记住全章主线：

```text
函数依赖告诉你“谁决定谁”。
候选键告诉你“谁能识别一整行”。
范式告诉你“非主键信息有没有偷偷决定别的信息”。
分解告诉你“把坏依赖拆出去，但别把原信息拆丢”。
```

### 4.1 坏表的三种病

看这张表：

```text
instructor(ID, name, salary, dept_name, building, budget)
```

假设有：

$$ID \to name,\ salary,\ dept\_name \qquad dept\_name \to building,\ budget$$

人话：

```text
ID 决定老师是谁、工资多少、属于哪个系。
dept_name 决定这个系在哪栋楼、预算多少。
```

问题在于：`building` 和 `budget` 是系的信息，却被塞进了老师表。

这会带来三种考试常问的异常：

```text
信息冗余：同一个系的 building/budget 在很多老师行里重复。
插入异常：新建一个没有老师的系，因为没有 ID，可能插不进去。
更新异常：系预算改了，要改很多老师行；漏改一行就不一致。
```

所以范式不是玄学，它是在避免：

```text
同一件事实被重复存很多次。
```

### 4.2 函数依赖 FD：左边相同，右边必须相同

`X -> Y` 读作 $X \to Y$，即「$X$ 函数决定 $Y$」。

更白话：

```text
只要两行的 X 相同，它们的 Y 就必须相同。
```

例子：

$$student\_id \to student\_name \qquad dept\_name \to building$$

注意一个重要细节：函数依赖是业务规则，不是只看一张当前表就能永远证明的事实。

如果当前表里出现 $A=1, B=2$ 和 $A=1, B=3$，那可以直接证伪 $A \to B$ 不成立。

但如果当前表暂时没冲突，只能说明它“可能成立”，不能说明它在业务上永远成立。

平凡函数依赖，比如 $AB \to A$，因为右边本来就是左边的一部分。BCNF/3NF 判断时，平凡依赖通常不构成问题。

### 4.3 属性闭包 X+：从手里的牌能推出哪些牌

属性闭包 $X^+$ 的意思是：

```text
已知 X，根据所有 FD，最多能推出哪些属性？
```

它是候选键、BCNF、分解题的发动机。

算法很机械：

```text
1. X+ 先等于 X。
2. 扫描所有 FD。
3. 如果某条 FD 左边已经包含在 X+ 里，就把右边加入 X+。
4. 重复扫描，直到 X+ 不再变大。
```

例子：

$$R(A,B,C,D,E,F), \quad F = \{\, A\to B,\ A\to C,\ B\to C,\ D\to E,\ D\to F,\ EF\to D \,\}$$

算 $(AD)^+$：

$$AD \xrightarrow{A\to B} ADB \xrightarrow{A\to C} ADBC \xrightarrow{D\to E} ADBCE \xrightarrow{D\to F} ABCDEF$$

最后 $(AD)^+ = ABCDEF$。

所以 $AD$ 能推出整个关系的全部属性，$AD$ 是 super key。若去掉 $A$ 或 $D$ 后不能推出全部，$AD$ 就是 candidate key。

### 4.4 候选键：先找“没人能推出它”的属性

候选键是最小的 super key。

做题第一招：

```text
从来没出现在任何 FD 右边的属性，通常必须包含在候选键里。
```

为什么？因为没人能推出它，你想拥有它，只能一开始就带上。

例子：

$$R(A,B,C,D,E,F), \quad F = \{\, A\to B,\ B\to C,\ C\to B,\ D\to E,\ D\to F \,\}$$

右边出现过：$B, C, E, F$。

没出现在右边：$A, D$。

所以候选键至少包含 $AD$。

算闭包：$(AD)^+ = ABCDEF$。

$AD$ 能推出全部。再检查：

$$A^+ = ABC \ (\text{不能推出 } D/E/F), \qquad D^+ = DEF \ (\text{不能推出 } A/B/C)$$

所以 $AD$ 是候选键。

考场写法：

```text
Because A and D never appear on RHS, every key must contain AD.
(AD)+ = ABCDEF, so AD is a superkey.
A+ != R and D+ != R, so AD is a candidate key.
```

### 4.5 无损连接分解：拆完还能拼回原表

把关系 `R` 拆成 `R1` 和 `R2` 后，如果 $R_1 \bowtie R_2 = R$（自然连接拼回原表），就是无损连接分解。

如果 join 后多出一些原来没有的行，就是有损。这个“多出来的行”会制造假信息，所以很危险。

二表无损快速判断：公共属性 $R_1 \cap R_2$ 如果能决定 $R_1$，或能决定 $R_2$，则分解无损。

更像做题语言：

$$R \to R_1, R_2 \ \text{无损} \iff (R_1 \cap R_2) \to R_1 \ \text{或}\ (R_1 \cap R_2) \to R_2$$

例子：

$$R(ID, dept\_name, salary), \quad F = \{\, ID \to dept\_name,\ dept\_name \to salary \,\}$$

如果拆成 $R_1(ID, dept\_name)$ 和 $R_2(dept\_name, salary)$，公共属性是 $dept\_name$。因为 $dept\_name \to salary$，所以 $dept\_name$ 能决定 $R_2$，分解无损。

如果分解成多个关系，Word 笔记里说“只要找出一条路径就可以了”：意思是你要能说明每一步二表分解都是无损，最后整体也无损。

### 4.6 正则覆盖 canonical cover：把 FD 集合瘦身

正则覆盖 `Fc` 是和原 FD 集合等价、但更干净的一组依赖。

它满足：

```text
F 能推出 Fc。
Fc 也能推出 F。
Fc 中没有多余 FD。
Fc 中没有多余左属性或右属性。
左边相同的 FD 合并。
```

常见操作：把 $A \to C$ 和 $A \to D$ 合并成 $A \to CD$。

判断某个属性是否多余，用闭包。

左边多余例子 $AB \to C$：想判断 $B$ 是否多余，就看在用 $A \to C$ 替代后，是否仍能推出原来的依赖。做题时通常写：算修改后 $F$ 下的 $A^+$，若 $C \in A^+$，则 $B$ 在 $AB \to C$ 里多余。

右边多余例子 $A \to BC$：想判断 $C$ 是否多余，就临时把它从右边删掉，看 $A^+$ 是否仍能推出 $C$。

正则覆盖题的策略：

```text
先拆右边，再删多余属性，再删多余依赖，最后合并相同左边。
```

### 4.7 BCNF：每个非平凡决定者都必须像主键一样强

BCNF 的人话定义：对每条非平凡 FD $X \to Y$，$X$ 必须是 super key。

也就是：如果 $X$ 不能决定整张表，却能决定某些非自己属性，就说明这张表混进了不该混的信息。

判断模板：

```text
For FD X->Y:
Y is not subset of X, so it is non-trivial.
Compute X+.
If X+ does not contain all attributes of R, X is not a superkey.
Therefore R violates BCNF.
```

例子：

$$R(ID, name, salary, dept\_name, building, budget)$$
$$ID \to name, salary, dept\_name \qquad dept\_name \to building, budget$$

看 $dept\_name \to building, budget$：

$$dept\_name^+ = \{dept\_name, building, budget\}$$

它不能推出 $ID/name/salary$，所以 $dept\_name$ 不是 super key。

因此这张表不满足 BCNF。

### 4.8 BCNF 分解：把坏依赖单独拎出去

如果 $X \to Y$ 违反 BCNF，就按这个公式拆：

$$R_1 = X \cup Y, \qquad R_2 = R - (Y - X)$$

记忆句：坏依赖自己成表；原表删掉被决定的右边，但保留决定者左边。

例子：

$$R(ID, name, salary, dept\_name, building, budget), \quad \text{违反}\ dept\_name \to building, budget$$

拆成：

$$R_1(dept\_name, building, budget), \qquad R_2(ID, name, salary, dept\_name)$$

这样 $building/budget$ 不再重复出现在每个老师行里。

BCNF 分解保证无损，但不保证依赖保持。

### 4.9 依赖保持：不 join 回去也能检查原 FD

依赖保持的意思是：

```text
分解后，只检查单个小表里的约束，就能保证原来的所有 FD。
```

反例来自 Word 笔记：

$$R(ID, dept\_name, salary), \quad F = \{\, ID \to dept\_name,\ dept\_name \to salary \,\}$$

如果拆成 $R_1(ID, dept\_name)$ 和 $R_2(ID, salary)$，那 $dept\_name \to salary$ 没有落在任何单张表里。你必须把 $R_1$ 和 $R_2$ join 起来，才能检查一个系是否对应唯一 salary。

所以这个分解不依赖保持。

考试中遇到：

```text
BCNF 无损但不依赖保持。
```

不要惊慌。这正是 3NF 要出场的原因。

### 4.10 3NF：为了依赖保持，稍微放宽 BCNF

3NF 判断一条非平凡 FD $X \to A$ 是否可以接受：

1. $X$ 是 super key；或
2. $A$ 是某个候选键的一部分，也叫 prime attribute。

人话：

```text
BCNF 要求每个决定者都必须像主键一样强。
3NF 允许右边是关键属性时放宽一点，从而换来依赖保持。
```

3NF 分解算法：

```text
1. 先求正则覆盖 Fc。
2. 对 Fc 中每条 FD X->Y，建立关系 XY。
3. 如果所有关系里没有任何一个包含原关系的候选键，就额外加入一个候选键关系。
4. 删除被其他关系包含的冗余小关系。
```

例子 $F_c = \{\, A \to BC,\ D \to E \,\}$。

先建 $R_1(A, B, C)$ 和 $R_2(D, E)$。

如果候选键是 $AD$，但没有任何一个关系包含 $AD$，就补 $R_3(A, D)$。

这样能保证无损并依赖保持。

### 4.11 4NF：多值依赖不要混在一张表里

Word 笔记最后讲 4NF。它处理的是多值依赖。

直觉例子：

```text
person(ID, phone_number, child_name)
```

一个人可以有多个电话，也可以有多个孩子。电话和孩子彼此无关，但放在同一张表里会形成组合爆炸：

```text
ID=1 有 2 个 phone，3 个 child
表里可能要出现 2*3 = 6 行
```

这就是信息冗余。

多值依赖写作 $ID \twoheadrightarrow phone\_number$ 和 $ID \twoheadrightarrow child\_name$。

4NF 的核心：非平凡多值依赖 $X \twoheadrightarrow Y$ 中，$X$ 必须是 super key。

否则就拆成 $person\_phone(ID, phone\_number)$ 和 $person\_child(ID, child\_name)$。

考试要会说问题：

```text
信息冗余、插入异常、更新困难。
```

### 4.12 范式题 A4 规则

```text
FD：X->Y 表示 X 相同则 Y 必须相同。
闭包：X+ 从 X 开始，能推就加，直到不变。
候选键：先找没出现在 RHS 的属性，再算闭包验证最小性。
无损二表分解：公共属性能决定其中一边。
BCNF：每条非平凡 FD 的左边必须是 super key。
BCNF 分解：X->Y 违规，拆 X∪Y 和 R-(Y-X)。
依赖保持：不用 join 分解后的表，也能检查原 FD。
3NF：左边是 super key，或右边是 prime attribute。
3NF 分解：canonical cover 每条依赖建表，必要时补候选键。
4NF：非平凡多值依赖左边必须是 super key。
```
