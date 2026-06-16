---
title: CA 刷题实战 — 历年卷精解
tags:
  - course
  - ca
  - exams
  - finals
  - review
updated: 2026-06-16
publish: true
blog_dest: Notes/体系结构/exam-drills.md
---
# CA 刷题实战：历年卷精解

→ 课程索引：[CA 首页](index.md)
→ 章节复习：[Chap 1](chap1.md) · [Chap 2](chap2.md) · [Chap 3](chap3.md) · [Chap 4](chap4.md) · [Chap 5](chap5.md)

这页把历年卷的**题型和答题模板**集中起来。考试结构稳定：**约 35 道选择题（每题 2 分，共 70）+ 3 道大题（每题 10 分）**。大题方向高度固定：

1. **Cache / 循环访存**（→ Chap 2）
2. **Scoreboard / Tomasulo / 推测时序表**（→ Chap 3）
3. **MESI / 目录协议状态题**（→ Chap 5）

偶尔混入向量化改写（→ Chap 4）。先把这三类大题练熟，再扫选择题。

---

## 一、三大题答题模板速记

### 模板 A：Cache 循环访存（Chap 2）

1. 一个 cache line 放几个元素 = line size / element size。
2. 连续访问每隔"块内元素数"次迭代发生一次 compulsory miss。
3. 分别数 a/b/c 各自的 miss。
4. write-back + write-allocate：写 c 也先 write miss 调块；替换 dirty 块再 write back（多付一次代价）。
5. 直接映射且地址冲突：逐次判断是否互相替换（conflict miss 爆炸）。
6. 平均周期 = `(Σ各迭代代价) / 迭代数`，代价 = `L + 各 miss × penalty`。

### 模板 B：Scoreboard / Tomasulo / 推测 时序表（Chap 3）

**Scoreboard 四列**：issue / read operand / execution / write result
- issue：功能单元空闲 + 无 WAW（目标寄存器无活跃写）
- read：所有源的 RAW 解除
- exec：占 latency 拍
- write：无 WAR（更早指令已读走我要覆盖的源）

**Tomasulo / 推测 四列**：issue / execution / write result / commit
- issue：需保留站（+ROB）有空
- exec：操作数齐（RAW 靠等）
- write：上 CDB 广播
- commit：按 ROB 顺序，前面慢指令没 commit，后面快指令只能等

### 模板 C：一致性状态题（Chap 5）

**MESI 状态跟踪**：
- read miss：无人有→E；有共享→S；有 M→对方写回，双方 S
- write hit：在 E→静默 M；在 S→发 invalidate，别人 I，自己 M
- write miss：发 BusRdX/invalidate，别人 I；别人 M 则先供数据

**目录协议消息流程**：找 home → 发 ReadMiss/WriteMiss → home 看目录 → 向 owner 发 Fetch / 向 sharers 发 invalidate → 更新目录 sharer/owner → 更新请求方 cache。

---

## 二、22-23 完整卷答案（自测对照）

### 选择题答案

```
 1.B  2.C  3.B  4.B  5.D
 6.C  7.A  8.C  9.C 10.A
11.B 12.A 13.D 14.A 15.C
16.C 17.C 18.A 19.A 20.A
21.C 22.A 23.C 24.A 25.C
26.C 27.C 28.B 29.B 30.D
31.C 32.D 33.C 34.C 35.D
```

??? note "若与课程标准答案有出入，以题目规则推导为准"
    historical 答案中个别题（如 scoreboard 时序）社区有争议，做题时按"功能单元/保留站规则 + latency"自己推一遍最稳。

### 高频选择题考点回顾（对应章节）

| 题号 | 考点 | 章节 |
|---|---|---|
| 1 | pipeline 不引入 exception hazard | Chap 3 |
| 2 | 精确异常，地址进 mepc 非 mtvec | Chap 3 |
| 3 | 循环展开受益条件（迭代独立） | Chap 3 |
| 4 | 执行顺序违反依赖 | Chap 3 |
| 5 | 动态调度辨析（Scoreboard 不消 WAR/WAW） | Chap 3 |
| 6 | 单核失效不含 coherency miss | Chap 2 |
| 7,8,19,23,28 | Cache 优化辨析、写策略 | Chap 2 |
| 9 | SMP/NUMA + coherence/consistency 定义 | Chap 5 |
| 10,15 | forwarding 解决不了 load-use | Chap 3 |
| 12,21 | AMAT / stall / 真实 CPI 计算 | Chap 2 |
| 14,16 | RAR 非冒险、Tomasulo 消 WAR/WAW | Chap 3 |
| 17,32 | 多发射 CPI<1、superscalar vs VLIW | Chap 3 |
| 18 | 顺序一致性保证 if 不同真 | Chap 5 |
| 20 | blocking 减少 miss | Chap 2 |
| 22 | 宽向量加法周期数 264 | Chap 4 |
| 24 | 分支损失 (2,0) | Chap 3 |
| 25,34,35 | MESI 状态、自旋锁、写无效 vs 广播 | Chap 5 |
| 29,30,31,33 | TLB Tag=VPN、地址位、VIPT | Chap 2 |

### 大题二（Cache）三档答案

| 配置 | 结论 |
|---|---|
| line=16B（4 int/块） | L + 75 |
| line=64B（16 int/块） | L + 18.75 |
| 直接映射 2KB + 64B 块 | 约 L + 400（a/b/c 冲突 + write back） |

### 大题三（Scoreboard vs 推测）核心差异

同段指令、单保留站、latency add=1/mul=10/div=40：
- Scoreboard 版无 commit 列，read/write 不重叠。
- 推测版有 commit 列，**commit 严格按程序顺序**——所以最后那条快指令的 commit 周期被前面 div(40 拍) 拖到很后。

### 大题四（目录协议）

见 [Chap 5](chap5.md) §7 的三个事件消息流程（P0 read 300 / P2 read 218 / P0 write 210）。

---

## 三、24-25 秋冬回忆卷题型

- 选择：归一化几何平均、带投机 Tomasulo issue 条件、(2,2) predictor bits、2-bit 预测循环 miss rate、提频+CPI 性能比、**向量三连**（无链/有链时间 + convoy 数）。
- 大题1：Cache（块大小、locality 判断）+ AMAT（5.4/6.6）。
- 大题2：循环依赖判断 + 重命名消依赖 + 向量化改写。
- 大题3：MESI 四状态全名 + 五步状态跟踪。
- 大题4：Scoreboard 时序表（两个时间点快照）。

---

## 四、考前 48 小时冲刺顺序

1. **三大题模板**（A/B/C）各手推一遍完整例子——这是 30 分的命脉。
2. **Chap 2 选择题**：AMAT、地址位、3C、写策略、优化辨析。
3. **Chap 3 选择题**：依赖/冒险、精确异常、predictor 位数、分支损失。
4. **Chap 5 选择题**：coherence/consistency、MESI 状态、SC、写无效。
5. **Chap 1 小计算**：CPU time/CPI/Amdahl/几何平均。
6. **Chap 4**：向量 convoy/chime、GCD、向量化改写。

记住：**大题占 30 分且模板化，选择题占 70 分但很碎**。先保大题模板不丢分，再用章节考点清单扫选择。

→ 回到 [CA 首页](index.md)
