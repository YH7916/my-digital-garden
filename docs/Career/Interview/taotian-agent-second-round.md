---
title: 淘天 Agent 二面面经信号拆解
description: 淘天 Agent 二面准备稿，整理业务表达、向量检索、Spring、网络与 Agent 执行循环。
tags:
  - learning
  - llm
  - agent
  - interview
  - taotian
  - redisearch
  - spring
  - network
updated: 2026-06-04
source: 用户转述牛客淘天 Agent 二面面经
publish: true
blog_dest: Career/Interview/taotian-agent-second-round.md
---

# 淘天 Agent 二面面经信号拆解

## 一句话结论

这条 50 分钟二面说明：淘天 Agent 面试确实会考很多八股，但不是随机八股。它围绕 Agent 工程落地的 4 条链路追问：

1. 业务逻辑链：项目到底解决什么业务问题，输入、处理、输出、异常和指标是什么。
2. 检索存储链：向量索引、召回、Redis/RediSearch、MySQL 存储结构差异。
3. 框架执行链：`@Tool`、Spring IoC/AOP、function call、MCP、Skills、Agent 循环。
4. 网络协议链：TCP 握手挥手、LLM 流式输出协议。

准备重点不是把 Java 八股百科背完，而是每个点都能接回“Agent 系统怎么跑起来”。

## 使用方式校正

用户判断：这些题不一定会直接考原题，但类似的广度和深度肯定需要拓展。

因此本页不是押题册，而是知识半径校准表。每个主题只要求达到 5 层深度：

1. 是什么：一句话定义。
2. 为什么需要：它解决 Agent 工程里的什么问题。
3. 怎么大致实现：核心链路、数据结构或框架机制。
4. 项目里怎么类比：能接回 YouNavi 或 AI coding drill。
5. 常见坑：一致性、性能、边界和失败兜底。

不要追到底层源码级细节。例如 RediSearch 不需要背完整实现，但要能说清它和普通 Redis / MySQL 的定位差异、索引大概是什么、为什么适合搜索/向量召回。

## 新优先级

P0：

- 业务逻辑说清楚。
- 向量检索从写入到召回全链路。
- `@Tool` / function call / MCP / Skills 的区别。
- Agent loop 继续循环和停止条件。
- 摘要压缩如何避免上下文扭曲。

P1：

- Redis vs RediSearch vs MySQL。
- Spring IoC/AOP。
- TCP 三次握手、四次挥手。
- SSE 流式输出。

P2：

- RediSearch 底层数据结构细节、向量索引算法细节。
- OpenClaw 是否搭建过、是否自己写过 Skills；按真实经历诚实回答。

## 1. 业务逻辑为什么说不明白

面试官问项目时，不想听“我做了 provider / benchmark / MCP”。他在听：

```text
业务问题是什么？
用户怎么触发？
系统收到什么输入？
中间查了什么数据、调用什么模型、用了什么工具？
最后输出什么？
失败时怎么兜底？
怎么证明有用？
```

YouNavi 可以改成这个讲法：

```text
业务上，YouNavi 想解决的是用户知识和工作流不能被外部 Agent 稳定调用的问题。
用户不只是想在 UI 里聊天，还希望 Claude Code、Codex、本地脚本、会议工具能调用同一批能力。
所以我做的几件事分别对应这条链路：
provider / benchmark 解决模型能力怎么选择和验证；
CLI / MCP 解决外部 Agent 怎么调用；
Skill / CLI 解决能力如何安装、复用、检测状态和排错。
```

追问时用固定骨架：

```text
入口是什么 -> 查什么数据 -> 调什么模型/工具 -> 返回什么 -> 怎么验证 -> 失败怎么处理
```

## 2. 向量模块基本索引怎么存，怎么召回

标准链路：

```text
原始文档
-> chunk 切分
-> embedding 模型转成向量
-> 向量 + 文档 id + 元数据写入向量索引
-> 用户 query 也转成 query embedding
-> 近似最近邻检索 topK
-> metadata filter / rerank
-> 取回原文片段
-> 组装进 prompt
```

可说版本：

```text
向量索引里不只是存一段文本，而是存 embedding 向量、文档 id、chunk id 和一些元数据。
召回时先把用户问题也编码成向量，再在索引里找距离最近的 topK chunk。
拿到候选后可以再按权限、时间、业务字段过滤，或者用 rerank 模型重排，最后把原文片段放回上下文。
```

## 3. 普通 Redis 和 RediSearch 有什么区别

一句话：

```text
普通 Redis 是 key-value / 数据结构存储；
RediSearch 是 Redis 上的搜索索引模块，可以给 Hash/JSON 建全文、数值、标签、地理和向量索引。
```

普通 Redis：

- 数据结构：String、Hash、List、Set、ZSet、Stream。
- 查询方式：主要按 key 直接读写，或者对集合做操作。
- `SCAN`：只是渐进式遍历 key，不等于高效搜索。

RediSearch：

- 会维护额外索引，例如倒排索引、数值索引、标签索引、向量索引。
- 支持 `FT.SEARCH` / `FT.AGGREGATE`。
- 文本可做关键词搜索和 BM25 类排序。
- 向量字段可做 KNN，相似度召回常见是 FLAT 或 HNSW 这类索引方式。

面试口径：

```text
如果只是根据用户 id 读一个 session，用普通 Redis 就够。
如果要按文本、标签、数值范围或向量相似度检索很多文档，就需要 RediSearch 维护二级索引。
```

## 4. RediSearch 和 MySQL 存储结构有什么区别

MySQL：

- 面向关系表和事务。
- InnoDB 常见主键索引是 B+Tree。
- 数据按页存储在磁盘/缓冲池里。
- 擅长精确查询、范围查询、事务一致性、关联关系。

RediSearch：

- 运行在 Redis 内存体系里，重点是搜索索引。
- 文本检索依赖倒排索引。
- 数值/标签/地理字段有对应索引结构。
- 向量检索依赖 FLAT/HNSW 等向量索引。
- 擅长低延迟搜索、全文检索、向量召回，但不是用来替代 MySQL 做完整事务系统。

口头对比：

```text
MySQL 更像事务型关系数据库，核心是表、行、B+Tree、事务和 SQL。
RediSearch 更像在 Redis 上加了一层搜索引擎索引，核心是倒排索引和向量索引。
所以优惠券订单这种强一致数据我会放 MySQL；
知识库搜索、语义召回、标签过滤这类可以用 RediSearch 或向量库。
```

## 5. `@Tool` 注解底层怎么实现

以 Spring AI / Java 框架口径回答：

```text
`@Tool` 本质是用注解标记一个可被模型调用的方法。
框架启动时通过反射扫描这些方法，读取方法名、描述、参数类型和注解信息，
生成 tool schema / function schema，注册到 tool registry。
调用 LLM 时，框架把这些 schema 发给模型；
模型返回 tool call 后，框架根据 tool name 找到对应方法，
反序列化 arguments，做类型校验，然后反射调用或通过 bean 方法调用真正执行业务逻辑。
```

关键点：

- 注解本身不会让模型自动执行工具。
- 模型只返回“我要调用哪个工具和参数”。
- 真正执行的是框架/harness 的分发逻辑。

## 6. Spring IoC 和 AOP 是什么，怎么实现

IoC：

```text
IoC 是控制反转：对象的创建、依赖注入和生命周期不由业务代码自己 new，
而是交给 Spring 容器管理。
容器启动时扫描 Bean 定义，通过构造器、字段或 setter 注入依赖，
最后业务代码从容器拿到已经组装好的对象。
```

AOP：

```text
AOP 是面向切面编程，把日志、事务、权限、监控这类横切逻辑从业务代码里抽出来。
Spring 常用代理实现：如果有接口可以用 JDK 动态代理，没有接口常用 CGLIB 生成子类代理。
调用方法时先进入代理对象，代理再执行前置/后置/环绕增强，最后调用真实业务方法。
```

Agent 关联：

```text
`@Tool` 可以理解成一种把业务方法暴露给 Agent harness 的声明；
AOP/IoC 则负责让这些业务方法作为 Spring Bean 被管理、增强和调用。
```

## 7. Agent 执行循环怎么判断是否需要下一轮

继续循环的条件：

- 模型返回了结构化 tool call。
- tool 执行结果需要再让模型解释或继续决策。
- plan 还没完成，且没有超过 max steps / timeout / token budget。
- 当前 observation 不是最终答案，只是中间状态。

停止条件：

- 模型返回 final answer，没有 tool call。
- 达到 max steps。
- 超时或 token/cost 超预算。
- 工具连续失败，进入 fallback。
- 重复调用同一工具但没有新信息，判定无进展。
- 用户任务已经满足验收条件。

口径：

```text
不是让模型无限自由循环，而是模型决定下一步，框架控制停止条件。
每轮都要记录 trace，包括输入、模型输出、工具调用、observation 和是否继续。
```

## 8. 复杂例子串一下

例子：用户问“帮我分析这场直播里某商品转化差的原因，并给主播生成一段改进话术”。

链路：

```text
1. 用户输入任务。
2. 系统判断需要业务数据和内容数据。
3. Agent 先调用商品/订单/点击数据工具，拿到转化率、曝光、点击、下单。
4. 再调用直播内容检索工具，召回相关片段、弹幕和商品讲解文本。
5. LLM 结合数据和内容判断原因：曝光不足、讲解太晚、价格解释不清、弹幕疑问未回应。
6. 如果证据不足，继续调用检索或指标工具。
7. 满足证据条件后输出分析和主播话术。
8. 记录 trace、引用证据、把 badcase 或用户确认结果写回评估/记忆。
```

这个例子能串起：

- tool calling。
- RAG/向量召回。
- Agent loop。
- 业务逻辑。
- trace/eval。
- 最终回答兜底。

## 9. 摘要错误导致上下文扭曲怎么办

风险：

- 摘要把事实写错。
- 摘要丢掉约束。
- 摘要把模型猜测当成用户真实意图。
- 后续轮次基于错误摘要越跑越偏。

控制方法：

- 摘要结构化：事实、决策、待办、偏好、未确认假设分开。
- 保留最近几轮原文，不只依赖摘要。
- 摘要里保留来源 turn id / trace id / tool result id。
- 对关键事实不要让模型自由改写，尽量从结构化状态或数据库读取。
- 重要操作前让模型显式引用依据，或者让用户确认。
- 定期做 summary verification：让模型检查摘要是否被原文支持。

可说版本：

```text
我不会让摘要直接替代全部上下文。
我的做法是：最近几轮保留原文，长历史压成结构化摘要；
摘要区分事实、决策、待办和假设；
关键业务事实从数据库或 tool result 重新读取；
如果摘要影响重要动作，就要求引用来源或让用户确认。
```

## 10. function call、MCP、Skills 有什么区别

function call：

```text
模型 API 层的工具调用机制。
开发者把函数 schema 发给模型，模型返回 function name 和 arguments，
应用程序再执行对应函数。
```

MCP：

```text
一种把工具、资源和上下文暴露给 Agent 的协议。
它解决的是不同 Agent host 和外部工具/server 之间如何标准化连接。
function call 更像一次模型调用里的工具格式；
MCP 更像跨应用、跨工具系统的连接协议。
```

Skills：

```text
一种可复用能力包，通常包含说明文档、脚本、模板、示例和约束。
它不只是一个函数，而是把某类任务的经验和执行资产封装起来，
让 Agent 遇到对应任务时能加载这套能力。
```

对比句：

```text
function call 是单次调用工具的格式；
MCP 是工具和 Agent 之间的协议；
Skills 是更高层的可复用能力资产。
```

## 11. 为什么 Skills 会流行

原因：

- 比纯 prompt 稳定：把流程、约束、脚本和示例固化下来。
- 比单个 function call 更有上下文：能包含任务说明、工作流和工具。
- 可复用、可安装、可版本管理。
- 适合 AI coding：把代码规范、测试命令、脚本和常见坑打包。
- 能降低长 prompt 成本：需要时加载，不必每次把所有知识塞进上下文。

可说版本：

```text
我理解 Skills 流行，是因为 Agent 需要的不只是“能调一个函数”，
还需要一整套完成任务的上下文、步骤、脚本和经验。
这些东西如果每次靠 prompt 临时写，很难复用也难验证；
打包成 Skill 后，就更像可安装、可测试、可迁移的能力资产。
```

## 12. OpenClaw 和自己写 Skills 怎么答

如果没有完整搭建过 OpenClaw：

```text
我没有完整搭建过 OpenClaw 生产环境。
我了解它这类 Agent harness 关注的是工具、技能、记忆、上下文和长任务执行。
我实际更熟的是 YouNavi 里 CLI/MCP/Skill 相关的工程链路，
包括能力如何被外部 Agent 调用、安装、检测状态和排错。
```

如果问是否自己写过 Skills：

```text
我写过/维护过类似 Skill 的能力包装：把某类任务需要的说明、命令、脚本和使用约束组织起来，
让 Agent 或 CLI 能稳定调用。
我不会夸成完整生态，但我理解 Skill 的价值是把一次性的 prompt 变成可复用能力。
```

## 13. TCP 握手与挥手

三次握手：

```text
客户端发 SYN；
服务端回 SYN + ACK；
客户端再回 ACK；
连接建立。
```

为什么三次：

```text
双方都要确认自己的发送和接收能力，以及对方的发送和接收能力是正常的。
```

四次挥手：

```text
主动关闭方发 FIN；
被动关闭方回 ACK；
被动关闭方处理完剩余数据后发 FIN；
主动关闭方回 ACK，并进入 TIME_WAIT。
```

TIME_WAIT：

```text
保证最后一个 ACK 能被对方收到，也让旧连接里的延迟报文自然过期。
```

## 14. 流式输出用什么协议

LLM API 最常见口径：

```text
一般用 HTTP 长连接上的 SSE，也就是 Server-Sent Events。
服务端不断推送 event/data chunk，客户端边接收边渲染。
```

补充：

- SSE：服务端到客户端单向推送，适合 LLM token streaming。
- WebSocket：双向通信，适合更强交互场景。
- 普通 HTTP：一次性返回完整响应，用户等待更久。

可说版本：

```text
我接触到的 LLM 流式输出通常是 SSE。
请求还是 HTTP，请求头里声明 stream，服务端以 event-stream 的方式持续返回 chunk。
客户端收到每个 chunk 后增量渲染，所以用户能看到模型边生成边输出。
```

## 二面校正版准备顺序

### 第一块：业务逻辑 30 分钟

把 YouNavi 按这个模板说 3 遍：

```text
业务问题 -> 用户入口 -> 数据/工具 -> 模型/Agent 决策 -> 输出 -> 验证 -> 失败兜底
```

验收：不再只说技术名词，能说明“为什么用户需要这个功能”。

### 第二块：向量/RediSearch 45 分钟

背：

- chunk -> embedding -> vector index -> query embedding -> ANN topK -> filter/rerank -> prompt。
- Redis 是 key-value 数据结构。
- RediSearch 是搜索索引模块。
- MySQL 是关系型事务数据库，常见索引是 B+Tree。

验收：能回答“数据怎么召回回来”和“为什么不用 MySQL 直接做语义搜索”。

### 第三块：框架/工具 45 分钟

背：

- `@Tool` = 注解扫描 + 反射/schema + tool registry + 模型返回 tool call + 框架执行。
- IoC = 容器管理对象和依赖。
- AOP = 代理增强方法调用。
- function call / MCP / Skills 三者区别。

验收：能从 `@Tool` 一直讲到模型怎么触发真实方法。

### 第四块：Agent loop 和摘要 30 分钟

背：

- 继续循环：返回 tool call、计划未完成、observation 需要继续解释。
- 停止：final answer、max steps、timeout、无进展、工具失败、预算耗尽。
- 摘要防扭曲：结构化摘要、保留最近原文、来源 id、关键事实回读、用户确认。

### 第五块：网络协议 20 分钟

背：

- TCP 三次握手。
- TCP 四次挥手。
- LLM streaming 通常用 SSE，WebSocket 是双向可选方案。

## 面试前最小背诵版

只背 5 句话：

1. 向量召回链路：chunk、embedding、vector index、query embedding、topK、rerank、prompt。
2. RediSearch 是 Redis 上的搜索索引模块，和普通 Redis 的 key-value 访问不同。
3. `@Tool` 底层是注解扫描生成 schema，模型返回 tool call，框架校验参数并调用真实方法。
4. Agent 是否继续循环，看模型是否返回 tool call、任务是否完成、是否超出 step/timeout/budget。
5. 流式输出常用 SSE；TCP 先三次握手建连，结束时四次挥手释放连接。
