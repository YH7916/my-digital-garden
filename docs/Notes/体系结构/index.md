---
title: 计算机体系结构 (CA)
tags:
  - course
  - ca
  - architecture
  - finals
  - review
updated: 2026-06-16
publish: true
blog_dest: Notes/体系结构/index.md
---
# 计算机体系结构 (CA)

ZJU 大二课程。教材：Computer Architecture: A Quantitative Approach 6th Ed（Patterson & Hennessy）。任课教师：何水兵。

> 本套复习资料为**唯一权威复习入口**：从零基础出发、图文并茂、按章分开、面向期末做题。原始素材见 `D:\Plan\.raw\期末复习\CA\`（NoughtQ 学长完整笔记 + 历年卷 + 辅学讲义），但复习以本套为准。

## 复习章节（从这里开始）

| 章节 | 主题 | 考试地位 | 笔记 |
|------|------|------|------|
| Chap 1 | 量化设计基础、Amdahl、CPU 时间、Flynn | 选择 + 小计算 | [Chap 1](chap1.md) |
| Chap 2 | 存储器层级、Cache、AMAT、虚拟内存/TLB | ⭐ 大题主力 + 选择高频 | [Chap 2](chap2.md) |
| Chap 3 | ILP、Scoreboard、Tomasulo、ROB、分支预测 | ⭐ 大题主力 + 选择高频 | [Chap 3](chap3.md) |
| Chap 4 | DLP、向量、convoy/chime、GCD、GPU | 选择 + 向量化改写 | [Chap 4](chap4.md) |
| Chap 5 | TLP、多处理器、MESI、目录协议、同步 | ⭐ 大题主力 + 选择高频 | [Chap 5](chap5.md) |
| 刷题 | 历年卷精解 + 三大题模板 + 答案对照 | 必看 | [刷题实战](exam-drills.md) |

## 考试画像（一句话）

- **结构**：约 35 道选择（每题 2 分 = 70）+ 3 道大题（每题 10 分 = 30）。
- **三道大题方向稳定**：① Cache 循环访存（Chap 2）② Scoreboard/Tomasulo/推测时序表（Chap 3）③ MESI/目录状态题（Chap 5）。
- **策略**：先把三大题模板练到不丢分，再用各章"考点清单"扫选择题。

## 全课主线（parallelism + locality）

| 章节 | 核心问题 | 一句话答案 |
|---|---|---|
| Chap 1 | 怎么评价机器好坏？ | 用执行时间/CPI/能耗量化，不只看主频 |
| Chap 2 | 为啥 CPU 快还等内存？ | 内存层级有速度差，靠 Cache/局部性降等待 |
| Chap 3 | 单核能不能同时做很多指令？ | 能，流水线/调度/Tomasulo/ROB 挖 ILP |
| Chap 4 | 一条指令能否处理很多数据？ | 能，向量/SIMD/GPU 挖 DLP |
| Chap 5 | 多核怎么一起正确工作？ | 共享内存 + Cache 一致性 + 同步 + 一致性模型 |

## 核心概念速查（关联八股/面试）

- **三堵墙**：ILP 墙 / 内存墙 / 功耗墙 → [[concepts/ca-three-walls]]
- **Amdahl 定律**：$\text{Speedup}=1/((1-f)+f/s)$ → [[concepts/amdahls-law]]
- **CPU 时间**：`CPU time = IC × CPI × Clock cycle time`
- **AMAT**：`Hit time + Miss rate × Miss penalty`
- **Cache 四问**：块置放 / 块识别 / 块替换 / 写策略 → [[concepts/cache]]
- **ILP 技术**：Scoreboard / Tomasulo / ROB 推测 → [[concepts/ilp]]
- **DLP**：向量架构 / SIMD / GPU → [[concepts/dlp]]
- **Cache 一致性**：MSI/MESI/MOESI、监听/目录 → [[concepts/cache-coherence]]
