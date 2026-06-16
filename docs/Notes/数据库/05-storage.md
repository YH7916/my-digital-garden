---
title: PPT 05 数据库存储
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
blog_dest: Notes/数据库/05-storage.md
---
## 5. PPT 05 数据库存储：数据库为什么总在数 block

这一章以 `第九章 数据存储.docx` 为主要讲解来源。PPT 给了存储层级和 buffer 的骨架；Word 笔记补足了磁盘访问、记录组织、分槽页、文件组织、buffer manager、LRU/MRU 等细节。

先抓住一句话：

```text
数据库不是一条 tuple 一条 tuple 地从磁盘读，而是一块 block/page 一块 block/page 地读。
```

所以后面查询处理、索引、join cost 全都建立在这里：

```text
到底读了多少块？
到底随机定位了多少次？
```

### 5.1 易失和非易失：内存快，但断电会忘；磁盘慢，但能留下

Word 笔记把物理存储分成两类：

```text
易失存储：CPU cache、内存。快，贵，断电丢。
非易失存储：磁盘、SSD、闪存、光盘。慢一些，但断电不丢。
```

数据库最关心三个指标：

```text
速度：访问数据有多快。
价格：每 GB 成本多高。
可靠性：多久可能坏一次。
```

层级越靠近 CPU：

```text
越快，越贵，容量越小。
```

层级越靠近磁盘/备份：

```text
越慢，越便宜，容量越大。
```

DBMS 的基本动作就是：

```text
把磁盘上的 page 搬到内存 buffer；
在内存里处理；
必要时再把脏页写回磁盘。
```

### 5.2 磁盘为什么怕随机访问

传统磁盘不是“直接拿到数据”，而像唱片机。

一次读盘大致包含：

```text
seek time：磁头移动到正确磁道。
rotational latency：等待目标扇区转到磁头下面。
transfer time：真正把 block 传出来。
```

前两步是机械等待，常常比真正传输还贵。

所以：

```text
随机访问：每次都要重新找位置，贵。
顺序访问：定位一次后连续读很多块，便宜。
```

这解释了后面很多反直觉结论：

```text
全表扫描虽然读很多块，但如果是顺序读，可能还可以。
二级索引如果导致大量随机 I/O，可能比全表扫描更慢。
```

### 5.3 block/page：做题时先把 tuple 数换成 block 数

内外存传输以 block 为单位。

哪怕你只要读一个整数：

```text
磁盘也会把包含这个整数的整个 block 读到内存。
```

所以题目给：

```text
nr：tuple 数
lr：每条 tuple 大小
block_size：块大小
```

你先算：

$$f_r = \left\lfloor \frac{block\_size}{l_r} \right\rfloor, \qquad b_r = \left\lceil \frac{n_r}{f_r} \right\rceil$$

其中 $f_r$ 是 blocking factor（一个 block 能放多少条记录），$b_r$ 是关系 $r$ 总共占多少 block。

例子：

```text
block_size = 4096 bytes
record_size = 68 bytes
nr = 1,000,000
```

先算：

$$f_r = \lfloor 4096 / 68 \rfloor = 60, \qquad b_r = \lceil 1000000 / 60 \rceil = 16667$$

后面无论是全表扫描、B+ 树、join，第一步都别忘了把 tuple 数转成 block 数。

### 5.4 定长记录：位置可以直接算

定长记录的好处是简单。

如果每条记录长度是 $n$ bytes，那么第 $i$ 条记录从偏移 $n \times (i - 1)$ 开始。

例子：

```text
block = 4096 bytes
record = 100 bytes
```

一个 block 最多放 $\lfloor 4096 / 100 \rfloor = 40$ 条。

剩下 96 bytes 宁可浪费，也常常不让一条记录跨两个 block，因为跨块会让一次读取变成两次读取。

删除定长记录有三种做法：

```text
1. 后面的记录整体前移：保持紧凑，但移动成本高。
2. 最后一条记录搬到空位：快，但打乱顺序。
3. 空位链表 free list：不移动记录，用指针把空洞串起来。
```

做题看到 “free list”，就想到第三种。

### 5.5 不定长记录：前面放目录，后面放真实内容

`varchar` 这种字段长度不固定。如果全部按最大长度存，会浪费空间。

所以不定长记录常用这种结构：

```text
固定部分：字段偏移、长度、null bitmap
变长部分：真正的字符串内容
```

null bitmap 是一串 bit：

```text
0 表示该属性不是 NULL
1 表示该属性是 NULL
```

这样数据库不用给 NULL 字段浪费完整空间。

### 5.6 分槽页 slotted page：页头管目录，页尾放记录

不定长记录放进一个 block/page 时，常用分槽页结构。

画面是：

```text
page 头部：slot directory，记录每条 tuple 的位置和长度。
page 尾部：真正的不定长 tuple，从后往前放。
中间：free space。
```

为什么要这样？

```text
tuple 变长，位置会动。
但外部可以只记 slot number。
slot 里更新偏移即可，不必让所有指针失效。
```

这就是“页内小目录”的思想。

### 5.7 文件组织：新记录到底插到哪一页

一个表通常由很多 page 组成。插入一条记录时，DBMS 要决定：

```text
放到哪个 page？
放到 page 的哪个空位？
```

常见组织方式：

```text
heap file：哪里有空放哪里。
sequential file：按某个 key 保持顺序。
B+ tree file organization：叶子节点直接存记录本身。
hash organization：按 hash 值分桶。
clustering / multi-table organization：相关表的数据靠近放。
```

heap file 的关键问题是找空位。Word 笔记提到可以在第一页维护每个 page 的空闲程度，例如用几个 bit 表示：

```text
4 表示大约 4/8 空闲
2 表示大约 2/8 空闲
```

如果页很多，还可以做第二层目录：

```text
第二层的一个条目概括第一层一组 page 中最大的空闲程度。
```

这和多级索引的思想类似：先粗略定位，再精确找页。

### 5.8 Buffer manager：内存里的临时书桌

上层查询想访问某个 block 时，会先问 buffer manager：

```text
这个 block 在不在内存？
```

如果在：

```text
直接返回内存地址。
```

如果不在：

```text
从磁盘读入 buffer。
如果 buffer 满了，先挑一个 page 替换出去。
```

被修改过但还没写回磁盘的页叫 dirty page。

替换 dirty page 时，不能直接丢：

```text
必须先写回磁盘。
```

没有修改过的 clean page 可以直接丢。

### 5.9 Pin count：正在被用的页不能踢走

如果上层操作正在读某个 page，buffer manager 不能把它替换出去。

所以有 pin：

```text
pin：钉住这个页，表示有人正在用。
unpin：用完了，解除钉住。
pin count：当前有多少使用者钉住它。
```

替换页时，只能考虑：

```text
pin count = 0
```

的页。

如果多个程序同时读写同一个 buffer page，还要考虑并发冲突：

```text
读读不冲突。
读写冲突。
写写冲突。
```

这就和后面的锁机制连起来了。

### 5.10 LRU、MRU、Clock：替换谁不是永远固定

LRU：

```text
Least Recently Used，替换最近最少使用的页。
```

直觉：

```text
很久没碰的书，可能暂时用不到，先拿走。
```

MRU：

```text
Most Recently Used，替换最近刚使用的页。
```

MRU 什么时候有用？Word 笔记提到嵌套循环场景：内循环刚扫过的最后一页，下一轮可能最后才会再用；而内循环最早扫过的页，下一轮马上又会用。此时简单 LRU 可能不理想。

Clock 是 LRU 的简化实现：

```text
每页一个 reference bit。
被访问过就置 1。
指针转圈扫描：
如果 bit=1，改成 0，给第二次机会；
如果 bit=0 且 pin count=0，就替换它。
```

### 5.11 SSD/闪存：读按页，写前常要擦

Word 笔记对闪存强调两点：

```text
读通常按页进行。
重新写入前需要先擦除。
```

热数据如果老写在同一物理位置，会把那块磨损得很快。

所以 SSD 会做磨损均衡：

```text
逻辑页号不变，但映射到不同物理页，避免某些物理页被反复写坏。
```

### 5.12 存储题 A4 规则

```text
DB 读写以 block/page 为单位，不以 tuple 为单位。
随机 I/O 贵，顺序 I/O 便宜。
fr = floor(block_size / record_size)，br = ceil(nr / fr)。
定长记录可直接算偏移；删除可移动、尾记录填洞、free list。
不定长记录用 offset/length/null bitmap 管理。
slotted page：页头 slot directory，页尾放真实记录。
dirty page 被替换前必须写回；clean page 可直接丢。
pin count > 0 的页不能替换。
LRU 不是永远最好；某些循环扫描中 MRU 可能更合适。
Clock 用 reference bit 近似 LRU。
```
