---
title: 淘天 Agent 一面面经信号拆解
tags: [learning, llm, agent, interview, taotian, ai-coding, backend]
updated: 2026-06-04
source: 用户转述牛客淘天 Agent 一面面经
publish: true
blog_dest: Career/Interview/taotian-agent-first-round.md
---

# 淘天 Agent 一面面经信号拆解

## 一句话结论

这条 70 分钟一面说明：淘天 Agent 岗不是传统力扣主线，但也不是只聊 AI coding 方法论。它更像三段组合：

1. 项目和 Agent 机制深挖：项目细节、Agent loop、prompt、tool calling、memory。
2. 后端基础八股：线程池、线程数估算、MySQL 查询优化。
3. AI coding 工程题：高并发优惠券/秒杀类服务，重点看能否 review AI 代码并指出一致性、并发和容错问题。

对 Yohaku 的准备结论：音视频仍按 JD 保留最小词表，但面试前 P0 要改成 **Agent loop 全链路 + 高并发优惠券服务 + 线程池/MySQL 够用层**。

## 题型权重判断

按这条面经，准备时间建议粗分：

- Agent 项目/机制追问：45%。
- AI coding 高并发服务：35%。
- Java/后端八股：20%。
- 音视频/直播词表：只保留 10 分钟级别的 JD 匹配口径，不再扩成主线。

## P0：Agent 机制 9 问

### 1. 拷打项目，追问项目细节

准备方式：不要背大词，直接按真实贡献讲。

可防守主线：

```text
我在 YouNavi 里做的不是完整多 Agent 平台，
而是 Agent 产品的工程基础设施：
多模型 provider / benchmark、CLI/MCP 外部调用链路、Skill/CLI 工具链。
```

每条都要能补 4 个点：

- 背景：为什么要做。
- 输入输出：接收什么，产出什么。
- 你改了哪里：具体模块/流程/验证。
- 风险边界：没有做模型训练、生产级多 Agent 或完整推理优化。

### 2. Agent 项目中做了什么

不要答“我用了 Agent”。要答：

```text
我主要做的是让 Agent 能被稳定调用、验证和产品化管理。
具体包括模型 provider 的差异适配和 benchmark，
外部 Agent 通过 CLI/MCP 调用产品能力，
以及 Skill/CLI 这类工具资产的安装、状态检测和排错。
```

### 3. 怎么设计 Agent 循环执行

最小 loop：

```text
user input
-> context assembly
-> LLM decide
-> if tool_call: validate schema / permission
-> execute tool
-> append observation
-> LLM decide again
-> final answer / max_steps / timeout / fallback
```

口头解释：

```text
我会把 Agent loop 理解成 observe-decide-act-observe。
LLM 负责决定下一步，harness 负责工具注册、参数校验、执行、trace、停止条件和错误兜底。
```

### 4. 是 Spring AI 框架内的，还是 prompt 控制输出

标准口径：

```text
两者分工不同。框架负责模型客户端、tool schema 注册、结构化解析、执行链路和状态管理；
prompt 负责告诉模型任务边界、工具使用规则、输出格式和失败时怎么处理。
真正执行工具的一定是代码里的 harness，不应该让 prompt 自己“执行”。
```

如果自己项目没用 Spring AI：

```text
我项目里不是基于 Spring AI，而是更偏自己控制调用链路/CLI/MCP。
但机制上类似：工具 schema 和执行逻辑在代码侧，prompt 只影响模型如何选择和填写参数。
```

### 5. system prompt 怎么设计

结构：

```text
角色定位
任务边界
可用工具和使用条件
输出格式 / JSON schema
不能做什么
错误处理和澄清策略
记忆使用规则
安全和权限约束
```

可说版本：

```text
我不会把 system prompt 写成一大段口号，而会把它写成工程约束：
先定义角色和边界，再定义什么时候调用工具、参数格式、失败时是否重试或澄清，
最后要求输出可解析格式，并提醒模型不要编造工具结果。
```

### 6. 调用 LLM 的全过程

链路：

```text
业务请求
-> 鉴权/参数校验
-> 取会话历史/摘要记忆/检索内容
-> 组装 system + user + history + tools
-> 调用 LLM API
-> 接收 streaming 或完整响应
-> 判断 final answer 还是 tool_call
-> 执行工具并写 observation
-> 循环直到结束
-> 记录 trace / token / latency / error
-> 必要时写回记忆或 badcase
```

### 7. tool 什么时候发给 LLM，什么时候执行

关键区分：

```text
工具 schema 在模型决策前作为可用能力发给 LLM；
工具只有在 LLM 返回结构化 tool_call 后，才由程序校验并执行。
```

工程补充：

- 不是每轮都必须发全部工具；可以按任务路由裁剪工具集合，降低 token 和误调用。
- 执行前要做 schema 校验、权限检查、参数边界检查。
- 工具结果要作为 observation 回填给模型，不能让模型假装已经执行。

### 8. 返回结果怎么知道需要调用哪个 tool

标准答案：

```text
不是靠人去猜自然语言，而是靠模型返回的结构化 tool_call。
里面通常有 tool name / function name 和 arguments。
程序按 name 找到注册表里的工具，再校验 arguments 后执行。
```

如果模型只返回自然语言：

```text
那是工程上不稳定的做法。更好的方式是 function calling / tool calling / JSON schema，
失败时要求模型重试结构化输出，或直接走 fallback。
```

### 9. 记忆压缩方式，怎么生成摘要

触发条件：

- history 超过上下文预算。
- 长工具结果太占 token。
- 一个任务阶段结束。
- 会话要长期保存。

摘要结构：

```text
用户目标
已确认事实
关键决策
已完成动作
未完成 todo
偏好/约束
重要证据引用
```

口头解释：

```text
我不会简单把历史压成一段散文，而会用结构化摘要。
摘要要区分事实、决策、待办和用户偏好，并尽量保留来源或 trace id。
生成后可以用新摘要替换旧长历史，但最近几轮原文要保留，避免丢失上下文细节。
```

## P0：AI coding 高并发优惠券服务

题目形态：实现高并发场景下发放优惠券模板、购买优惠券、下单优惠券、容错处理的服务，类似秒杀。

### 业务对象

最小表/对象：

- `coupon_template`：模板 id、库存、开始/结束时间、状态、每人限领数量。
- `user_coupon`：用户 id、模板 id、状态、领取时间、使用时间。
- `coupon_order`：订单 id、用户 id、模板 id、状态、金额、创建时间。
- `coupon_stock_log` 或消息表：库存扣减/回滚/补偿记录。

### 正确性约束

必须防：

- 超卖：库存不能被并发扣成负数。
- 重复领取：同一用户不能超过限领数量。
- 重复下单：同一个业务请求重试不能创建多张券/多条订单。
- 库存和订单不一致：扣了库存但订单失败，要有回滚或补偿。
- 本地锁失效：多实例部署时 `synchronized` / 本地锁不够。
- 缓存和 DB 不一致：Redis 预扣成功后 DB 失败要处理。

### 推荐设计口径

```text
入口先做参数校验和活动状态校验；
用 Redis/Lua 或数据库原子 update 防止库存超卖；
用唯一索引或幂等 key 防止用户重复领取/重复下单；
订单状态用状态机管理；
异步消息或 outbox 做扣库存、创建订单、补偿的可靠衔接；
失败时要有重试、回滚、超时关闭和人工/定时补偿。
```

数据库原子扣库存示例口径：

```sql
UPDATE coupon_template
SET stock = stock - 1
WHERE id = ? AND stock > 0 AND status = 'ACTIVE';
```

判断影响行数为 1 才算扣减成功。

Redis/Lua 口径：

```text
高并发入口可以先用 Redis Lua 把“判断库存、判断用户是否领取、扣库存、写领取标记”做成原子操作，
再异步落库。落库失败时要有消息重试和补偿，不能只相信缓存成功。
```

### 面试官看 AI 代码时常追的问题

如果 AI 写出代码，要主动 review：

- 有没有幂等 key。
- 有没有唯一索引兜底。
- 库存扣减是不是原子操作。
- 多实例下锁是否有效。
- 事务边界是否过大。
- Redis 成功但 DB 失败怎么补偿。
- MQ 发送成功但本地事务失败怎么办。
- 重试会不会重复扣库存/重复发券。
- 异常吞掉后调用方是否误以为成功。
- 是否有超时、限流、降级。

### 你可以直接说的 review 句

```text
这段 AI 代码的主流程能跑，但高并发下不够安全。
我首先会看库存扣减是否原子，其次看用户领取是否有唯一索引或幂等 key，
再看扣库存、创建订单、发券之间是否存在部分成功。
如果 Redis 和 DB 混用，还要补消息重试或 outbox，避免缓存成功但落库失败。
```

## P1：线程池八股够用层

### 线程池参数

Java `ThreadPoolExecutor` 七个核心参数：

```text
corePoolSize
maximumPoolSize
keepAliveTime
TimeUnit
workQueue
threadFactory
RejectedExecutionHandler
```

解释顺序：

```text
先创建核心线程；
核心线程满了任务进队列；
队列满了才扩到最大线程数；
最大线程也满了就触发拒绝策略。
```

注意：

- 如果是无界队列，`maximumPoolSize` 基本不会生效。
- IO 密集型可以比 CPU 核数大很多，但最终要压测，不是只套公式。

### 正在运行线程数怎么算

答题模板：

```text
先看当前线程数是否小于 core。
如果小于 core，新任务直接建线程。
达到 core 后，任务先进入队列。
只有队列满了，才继续扩线程到 max。
所以要同时看 core、max、queue 容量和当前任务数。
```

### IO 密集型 90%，四核机器核心线程数

公式：

```text
线程数 ≈ CPU 核数 * (1 + 等待时间 / 计算时间)
```

IO 占 90%，计算占 10%，等待/计算约为 9：

```text
4 * (1 + 9) = 40
```

口径：

```text
理论值可以从 40 附近起步，但实际要结合下游连接数、数据库 QPS、内存和压测结果调整。
不能只为了提高线程数把数据库打爆。
```

## P1：MySQL 查询优化够用层

结合优惠券项目举例：

常见查询：

```sql
SELECT *
FROM user_coupon
WHERE user_id = ?
  AND status = ?
  AND expire_time > ?
ORDER BY expire_time ASC
LIMIT 20;
```

优化口径：

- 建联合索引，例如 `(user_id, status, expire_time)`。
- 等值条件放前面，范围/排序字段放后面。
- 避免 `SELECT *`，只查必要字段，必要时做覆盖索引。
- 避免在索引列上套函数。
- 用 `EXPLAIN` 看是否走索引、扫描行数、是否 filesort。
- 深分页用游标/上次最大 id 或时间条件，不要无限 `OFFSET`。

唯一约束：

```sql
UNIQUE KEY uk_user_template (user_id, template_id)
```

用途：

```text
即使应用层并发判断漏了，数据库唯一索引也能兜住重复领取。
```

## 面试前修正版计划

### 2026-06-04 周四晚上

- 背本页 P0 Agent 机制 9 问。
- 把 Agent loop 画成一条链：context -> LLM -> tool_call -> validate -> execute -> observation -> final。
- 只保留音视频最小词表，不扩学习。

验收：能连续回答 tool 什么时候发、什么时候执行、怎么知道调哪个 tool、memory 怎么压缩。

### 2026-06-05 周五晚上

- 过 YouNavi 项目 2 分钟稿。
- 准备“agent项目中做了什么”的 3 条真实贡献。
- 读线程池参数和 IO 90% 算法。

验收：不用看稿回答项目细节，不把自己包装成完整 Agent 平台作者。

### 2026-06-06 周六

- 做一次高并发优惠券 AI coding drill。
- 先让 AI 给设计，再让 AI 写代码，最后自己 review 10 个问题。
- 重点不是写完，而是能指出 AI 代码哪里不可靠。

验收：能讲清超卖、幂等、唯一索引、事务/消息补偿、Redis/DB 一致性。

### 2026-06-07 周日

- 补 MySQL 查询优化。
- 用优惠券表字段讲联合索引。
- 做一次 45 分钟模拟：项目 20 分钟、Agent 20 分钟、八股 5 分钟。

验收：能结合 `user_coupon` / `coupon_template` 字段讲怎么查更优。

### 2026-06-08 周一晚上

- 整理 AI coding 复盘稿。
- 准备一句话指出 AI 生成代码的问题。
- 复述 system prompt、LLM 调用全过程、tool 执行链路。

验收：能边看代码边说 review 顺序。

### 2026-06-09 周二晚上

- 70 分钟模拟一面：
  - 25 分钟项目拷打。
  - 25 分钟 Agent 机制。
  - 15 分钟优惠券服务设计。
  - 5 分钟线程池/MySQL。
- 不再新增知识。

验收：只修最卡的 3 个回答。

### 2026-06-10 周三面试前

- 背项目三条线。
- 背 Agent loop 9 问。
- 背优惠券服务 10 个 review 点。
- 背线程池 7 参数和 IO 90% = 40 附近这个估算。

禁止：刷新题、开新技术栈、补完整音视频课程。
