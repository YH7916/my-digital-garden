---
title: YouNavi AI Agent 项目深挖稿
description: YouNavi AI Agent 实习项目复盘，整理模型接入、CLI/MCP、Skills 与稳定性经验。
tags:
  - project
  - internship
  - agent
  - interview
  - younavi
updated: 2026-05-10
source: D:/Desktop/younavi-pr-summary-ai-agent-internship-2026-02-09-to-2026-05-09.md
publish: true
blog_dest: Career/Internship/younavi-agent-deep-dive.md
---

# YouNavi AI Agent 项目深挖稿

定位：这不是“我做了一个 Agent 应用”，而是“我参与了 YouNavi 的模型接入与评测、外部 Agent 调用链路、CLI/MCP 服务封装，以及 Skill/CLI 工具链工程化”。

核心边界：我可以讲清楚模型 provider 接入、benchmark 测试、CLI/MCP 两条外部调用链路、Skill 工具链和飞书 CLI 集成；不要把自己包装成做完整多 Agent 编排、RAG 平台或模型训练的人。MCP 和 CLI 是并行的两种封装方案，其中 MCP 方案后续没有作为主方案继续使用，面试时要主动讲清楚。Windows/WSL/PyInstaller 适配只是稳定性补充点，不作为主线。

面试现实：面试官只能看到简历，看不到我的实际 PR。准备重点不是逐个 PR 背诵，而是让简历上的每个关键词都能自圆其说：背景是什么、我负责哪一段、难点是什么、怎么验证、哪里用了 AI 工具、我如何 review 和兜底。

## 30 秒开场

我在 YouNavi 的实习主要做三块：第一是模型接入和 benchmark，扩展 OpenRouter、网宿、直连等多种模型通路，重构测试工具并做延迟和效果评测；第二是把 YouNavi 的核心能力通过 CLI 和 MCP 两条链路封装成外部 Agent 可以调用的接口，其中 MCP 面向 Claude Code、Codex、OpenClaw 等外部 Agent，但后续没有作为主方案继续使用；第三是 Skill 和 CLI 工具链，包括飞书 CLI 的安装/调用 skill、YouNavi CLI 前端重构、YouNavi CLI 可用性 bugfix、skill 删除边界修复。Windows/WSL/打包问题只作为这些链路里的工程稳定性补充。

## 2 分钟项目介绍

YouNavi 是一个桌面端 AI Agent 产品，本地客户端里有后端服务、CLI、技能系统、模型 provider 和一些外部渠道能力。我的工作不是训练模型，也不是做完整 Agent planning，而是围绕“模型怎么接入和评测”“核心能力怎么被外部 Agent 调用”“CLI/Skill 怎么产品化”做工程落地。

第一条主线是模型集成与 benchmark。我做过 OpenRouter 大量模型支持，比如智谱 GLM、Kimi 等模型的路由和模型目录支持，也接过网宿 API，并对 OpenRouter、网宿、直连等不同通路做过较大规模 benchmark。这里的重点不是“接一个 API key”，而是把 provider 路由、模型目录、测试脚本、延迟/效果评测和结果展示串起来，用测试结论辅助模型选择。

第二条主线是 CLI/MCP 服务封装。目标是把 YouNavi 的核心能力，比如会议采集、内容分析等，通过标准接口暴露给其他 Agent 或自动化流程。这里有两条并行链路：CLI 更偏稳定、可脚本化、适合本地工具调用；MCP 更偏外部 Agent 协议接入，面向 Claude Code、Codex、OpenClaw。MCP 方案后续没有作为主链路继续使用，但这段工作让我理解了外部 Agent 工具封装的接口、状态、安装和环境适配问题。

第三条主线是 Skill 与 CLI 工具链重构。我重构过飞书 CLI 的两个核心 skill：`lark-cli-setup` 负责安装、配置和授权引导，`lark-context` 负责通过 CLI 调用飞书上下文能力，目标是减少用户手动配置成本。后面也参与 YouNavi CLI 前端重构，把原来偏 A2A 的入口改成面向 Claude Code、Codex、OpenClaw 等 Agent 的 YouNavi CLI 管理页。同时，我也修过 YouNavi CLI 链路里的可用性 bug，比如 `navi-transcribe` 重构和 CLI 复用客户端登录态；这些属于 CLI 工具链修补，不单独包装成一条主项目。另一个重要边界是 skill 删除：修复 skill 重名、目录名和 skill 名不匹配导致无法删除的问题。

补充点是工程稳定性。除了 OpenRouter 和网宿，我也做过新模型接入，比如 Opus 4.7，为后续多模型切换和调度做模型目录层面的准备。MCP/CLI/Skill 链路里也修过状态显示、WSL 适配、打包依赖和路径相关问题，但这些是主线背后的稳定性工作，不单独包装成一条主项目。

整体上，我的价值主要在 AI Agent 产品的工程基础设施：模型接入要能被测试，工具链要能被外部 Agent 调用，CLI/Skill 要能被用户安装、管理和排错。

## 贡献地图

| 主线 | 可以讲的内容 | 代表 PR |
|---|---|---|
| 模型集成与 benchmark | OpenRouter 大量模型、网宿 API、直连通路、延迟/效果评测、benchmark 工具重构 | #562, #565, #568, #585, #605, #616 |
| CLI/MCP 服务封装 | 将 YouNavi 核心能力封装给外部 Agent/自动化流程调用；CLI 和 MCP 是并行链路 | #675, #674, #692, #691, #776, #786, #789, #793, #965 |
| 多模型接入 | 新模型接入、模型目录、provider 路由，为后续多模型切换和调度做准备 | #562, #568, #585, #798 |
| Skill 与 CLI 工具链 | 飞书 CLI 安装/调用 skill、YouNavi CLI 前端、YouNavi CLI 可用性 bugfix、skill 删除边界 | #933, #965, #985, #990, #954, #955 |

稳定性补充点：Windows/WSL/PyInstaller 相关问题只在被追问工程落地、环境兼容、工具链稳定性时讲，不作为简历主线或项目主故事。

## 故事 1：模型集成与 benchmark

### 面试官问：你做过哪些模型相关工作？

短答：我没有做模型训练，但做过模型 provider 接入和 benchmark。主要是 OpenRouter、网宿和直连等通路，新增过大量 OpenRouter 模型支持，比如 GLM、Kimi 等，接入过网宿 API，也重构过 benchmark 测试工具，对不同通路的模型延迟和效果做过大规模测试并输出结论。

更完整回答：这块工作不是调一个模型 API 就结束。要让产品支持多模型，至少要处理 provider 路由、模型目录、API 参数差异、是否走代理、可用性测试、延迟测试、效果评测和结果展示。比如 OpenRouter 和 Kimi/Google 等模型的网络通路不一样，有些要走代理，有些可以直连；benchmark 工具也要支持文本、视觉、工具调用等不同测试维度。我的贡献主要在工程接入、测试工具重构和 benchmark 结论输出。

### 面试官追问：benchmark 你具体测什么？

可以分三类讲：

1. 延迟：TTFT、流式耗时、非流式耗时，不同 provider 通路对比。
2. 效果：用预设任务或 judge 评估回答质量，记录评分方法和理由。
3. 能力：工具调用、视觉输入、模型可用性、API 参数兼容性。

边界：如果没有可引用的具体数字，现场不要编“提升了多少”。可以说我输出过测试结论，但具体数字以当时 benchmark 报告为准。

### 面试官追问：如果模型效果和延迟冲突，你怎么选？

回答：看场景。交互式 Agent 更关注 TTFT 和稳定性，长文分析可以接受更高延迟换更好效果；工具调用场景更关注结构化输出稳定性；成本敏感场景还要看单次调用价格。benchmark 的价值是把这些维度显性化，而不是直接给一个“最强模型”。

## 故事 2：CLI/MCP 服务封装

### 面试官问：为什么要做 CLI/MCP 服务封装？

短答：因为 YouNavi 的能力不应该只能在自己的客户端 UI 里点按钮调用，还应该能被外部 Agent 或脚本化 workflow 调用。CLI 和 MCP 是两种并行封装方式：CLI 更直接稳定，适合本地命令和自动化；MCP 更面向 Claude Code、Codex、OpenClaw 这类外部 Agent 的工具协议接入。

更完整回答：YouNavi 有会议采集、内容分析等核心能力，如果这些能力只能通过 UI 使用，就很难接入外部 Agent。CLI 的好处是明确、可测试、容易被本地 agent 调用；MCP 的好处是更贴近外部 Agent 的工具发现和调用协议。后续项目没有继续把 MCP 作为主方案，但这段工作暴露了真实问题：工具如何注册、参数如何传递、状态如何检测，以及不同运行环境下怎么安装和启动。

### 面试官追问：MCP 和普通 HTTP API 有什么区别？

守住边界：底层调用仍然可能是 HTTP，但 MCP 的抽象重点是“给 Agent 用的工具协议”，包括工具发现、参数 schema、调用语义、客户端配置和生命周期管理。普通 HTTP API 更像给业务系统或前端调用，MCP 更强调模型/Agent 如何知道有哪些工具、每个工具能做什么、如何以结构化参数调用。

可以补一句：在 YouNavi 里我做的是 MCP 接入和工程落地，不是发明协议本身。

### 面试官追问：你具体解决了什么难点？

可以讲三类：

1. Windows/WSL 网络差异：WSL 有 NAT 和 mirrored 模式，外部 Agent 和本地后端之间的地址、端口、portproxy 处理不一样。
2. 打包环境路径差异：开发环境能跑的 Python 模块路径，在 PyInstaller packaged executable 里不一定存在，所以需要处理 launcher、CLI executable path、依赖元数据。
3. 可用性闭环：不仅服务能启动，还要有安装、卸载、状态检测、前端 UI 反馈，否则用户不知道外部调用链路到底是否可用。

### 面试官追问：既然后续没用 MCP，这段经历还怎么讲？

回答：可以讲，但不能夸大成最终主方案。我会说 MCP 是当时探索外部 Agent 接入的一条链路，验证了工具封装、安装、状态检测和 WSL/打包适配中的问题；后续主线更偏 CLI/Skill，但 MCP 经历仍然帮助我理解外部 Agent 工具协议和产品化边界。这比硬说“MCP 是最终核心能力”更稳。

## 故事 3：Skill 与 CLI 工具链重构

### 面试官问：你怎么理解 Skill？它和 MCP 有什么区别？

短答：Skill 更像可复用能力资产，CLI/MCP 是能力调用链路。Skill 里可以包含说明、prompt、脚本、工具调用方式和使用边界；CLI 让这个能力能稳定执行，MCP 让能力能被外部 Agent 以工具协议发现和调用。

结合项目：我这块最能讲的是飞书 CLI 和 YouNavi CLI。PR #933 里我把飞书 CLI 拆成 `lark-cli-setup` 和 `lark-context` 两个 skill：前者负责安装、环境检查、配置和授权引导，后者负责真正调用飞书上下文能力。PR #965 里我参与把原 A2A 管理入口重构成 YouNavi CLI 前端，支持按 Claude Code、Codex、OpenClaw 等 Agent 独立安装、卸载和查看 YouNavi Skill。

### 面试官追问：Skill 触发不稳定怎么办？

回答方向：不能只依赖模型自由判断。工程上可以做三层：

1. description 写清楚：让模型能知道什么时候用。
2. CLI 或显式命令强触发：比如用户明确调用某个 `navi-*` skill 时，不靠模糊识别。
3. 管理层可观测：前端显示、CLI 列表、安装状态、错误信息都要能看见。

我在项目里更偏第二和第三层，也就是让 skill 能被安装、管理、调用和排错。飞书 CLI 的两个 skill 也是这个思路：setup 负责降低配置门槛，context 负责稳定调用。

### 面试官追问：你修过哪些真实边界？

可以讲这些：

- 安装 skill 不应该污染用户 PATH，否则会造成环境副作用。
- WSL 下 OpenClaw skill 安装路径和 Windows 路径不同。
- 用户 skill 和内置 skill 重名时，删除必须以真实用户目录为准，不能误删内置 skill。
- 目录名和 `SKILL.md` 里的 name 不一致时，删除逻辑不能只按显示名猜路径。
- 前端 skill hover 展示完整描述，是为了让用户能理解 skill 能力，但不额外打乱主 UI。

### 面试官追问：YouNavi CLI 前端重构到底做了什么？

回答：原来入口偏 A2A 展示，后来重构成 YouNavi CLI 管理页。后端接口支持按 Agent 维度传入安装/卸载范围，避免未选中的项被误卸载；前端展示 Claude Code、Codex、OpenClaw 等目标 Agent 的安装状态和操作入口。这个改动的重点是把 CLI/Skill 从内部能力变成用户可以理解和管理的产品入口。

### 面试官追问：`navi-transcribe` 和登录态复用算什么贡献？

回答：它们属于 YouNavi CLI 工具链里的可用性 bugfix，不是我单独拿来包装的大项目。`navi-transcribe` 是让音频转写这个 skill/CLI 链路更稳定，登录态复用是解决用户已经在桌面端登录后，CLI 仍然重复要求登录的问题。它们能体现我对 CLI 调用链路、状态文件和外部 Agent 调用体验的理解，但面试中我会把它们放在 YouNavi CLI 修补这一层讲。

## 故事 4：多模型接入和 provider 边界

### 面试官问：你做过模型相关的东西吗？

短答：我没有做模型训练，但做过 provider 路由、模型目录和新模型接入。比如 OpenRouter 大量模型、网宿 API、Claude/Opus 4.7 这类新模型接入，以及对应 benchmark 工具和测试流程。

边界：不要说自己做了推理引擎优化，也不要说做了模型微调。可以说这部分帮助我理解 Agent 系统里模型 provider 的工程选择：不同模型有不同能力、成本、延迟和稳定性，需要通过 model catalog 和 benchmark 做选择依据。

### 面试官追问：benchmark 具体评什么？

可以答：

- 模型是否可用，API 参数和 provider 路由是否正确。
- 工具调用能力是否能按预期输出结构。
- 多模态或视觉输入是否能走通。
- 会议类场景是否能完成摘要、抽取等任务。
- 脚本本身也要通过 lint/type check，避免 benchmark 工具快速腐化。

如果被追问具体指标，没有证据就不要编数字。

## 稳定性补充点：Windows/WSL/PyInstaller

### 面试官问：这些稳定性修复和 Agent 有什么关系？

短答：这不是我的主线，只是工程落地补充。Agent 工具链不是只在开发机上跑通就行。YouNavi 是桌面端产品，用户在 Windows、WSL、打包后的环境里使用。外部 Agent 调工具时，如果路径、依赖、网络、子进程 pipe 出问题，workflow 就会断掉。所以它可以证明我处理过产品化边界，但不把它包装成独立主项目。

可以讲的真实问题：

- PyInstaller 打包后缺少 fastmcp 元数据、pywintypes、win32 动态库。
- 打包环境下不能按源码路径找 CLI，需要使用 packaged executable path。
- WSL OpenClaw 安装可能因为环境探测返回值或提前 return 被跳过。
- Windows 子进程 pipe 读取可能出现 WinError 10038。
- PowerShell worktree 脚本支持并行开发和环境配置复制。

### 面试官追问：你怎么定位这些问题？

回答模板：

1. 先复现具体环境：开发环境、打包环境、Windows、WSL 要分开看。
2. 看错误发生层级：路径、依赖、网络、权限、子进程、协议调用。
3. 收敛最小修复：比如只补 PyInstaller hidden import 或 metadata，不顺手重构无关模块。
4. 加验证：CLI 命令、前端状态、打包运行、单测或类型检查。

这点可以顺便体现你不是只会写功能，也能处理产品化落地问题。

## AI 工具使用口径

### 面试官问：你开发过程中是不是大量用 AI？

短答：是，我重度使用 AI 工具，尤其是 Claude Code/Codex 这类 coding agent。但我的角色不是直接接受 AI 输出，而是负责把需求拆成可执行任务、提供项目上下文和边界、review 代码 diff、跑测试和验证，并决定哪些改动可以合入。

更完整回答：在这种 AI Agent 产品开发里，用 AI 工具本身不是问题，关键是怎么控制它。我通常会先明确目标和范围，比如只修 CLI 登录态、只改 skill 删除逻辑、只处理 benchmark 脚本；然后给 AI 相关代码路径、现有模式和失败现象。生成后我重点检查三类东西：有没有越界改无关代码、有没有破坏已有接口契约、有没有缺少验证。最后用单测、typecheck、CLI 命令、benchmark 或打包环境复现来确认，而不是只看它“写完了”。

### 面试官追问：那这些代码到底算不算你写的？

回答：我会区分“代码由谁生成”和“工程结果由谁负责”。AI 可以生成部分实现，但需求拆解、方案取舍、上下文选择、diff review、测试验证和最终合入责任在我。尤其像 provider 路由、benchmark 口径、WSL/打包路径、skill 删除边界这类问题，AI 不知道项目真实约束，必须由我判断它的输出是否符合系统。

### 面试官追问：AI 生成错了怎么办？

回答：我不会让 AI 一次性改大块。一般会缩小任务、要求它解释改动点，然后我用真实失败用例或测试去约束它。如果发现它跑偏，比如改了无关模块、绕过了现有接口、或者只是表面修复，我会回到最小复现和源码路径重新限定范围。我的经验是 AI 适合加速定位和生成样板，但复杂边界必须靠人来验证。

## 面试官拷打清单

### P0：一定会问

1. OpenRouter 你具体新增了哪些模型？只是改配置还是改了 provider 路由？
2. 网宿 API 接入和 OpenRouter 接入有什么差异？
3. benchmark 具体测了哪些指标？延迟和效果怎么评？
4. 你怎么从 benchmark 结论反推模型选择？
5. CLI 和 MCP 为什么是两条并行链路？各自适合什么场景？
6. 既然后续没继续用 MCP，为什么这段经历还值得讲？
7. 飞书 CLI 的 `lark-cli-setup` 和 `lark-context` 为什么要拆成两个 skill？
8. YouNavi CLI 前端重构具体改了什么？为什么从 A2A 改成 CLI 管理页？
9. `navi-transcribe` 和登录态复用在 YouNavi CLI 里分别解决了什么问题？
10. Skill 删除为什么会出 bug？你怎么保证不误删？
11. 你怎么验证这些 PR 真的可用？

### P1：容易暴露浅答

1. 你们的 Agent 有没有 planning？如果没有，为什么你还说这是 Agent 相关工作？
2. 你有没有做过 RAG？如果没有，怎么回答 RAG 高频问题？
3. 你有没有做多 Agent？A2A 页面是不是你做的核心能力？
4. 你有没有做模型训练、LoRA、DPO？
5. 你怎么评价 Claude Code/Codex/OpenClaw 的差异？
6. 如果 CLI/MCP 工具调用失败，Agent 应该 retry 还是停止？
7. 如果工具 description 写得不好，会发生什么？
8. 你怎么防止外部 Agent 调危险工具？
9. 你们有没有 trace 和监控？没有的话你会怎么补？
10. 你这些 PR 里哪些是最有技术含量的？为什么？
11. 你开发过程中大量用 AI，那么你的不可替代贡献是什么？

### P2：高级追问

1. 如果 MCP 工具很多，怎么做工具发现和按需注入？
2. 如果 Skill 数量很多，怎么避免 prompt 变长？
3. 如果用户同时安装内置 skill 和同名用户 skill，优先级怎么设计？
4. 如果 WSL NAT 和 mirrored 都要支持，地址探测怎么做？
5. 如果打包后二进制路径变了，如何设计路径解析更稳定？
6. 如果 CLI JSON 模式被外部 Agent 调用，错误码和 stderr/stdout 怎么设计？
7. 如果 provider 很多，model catalog 怎么避免散落在各处？
8. benchmark 如何区分模型能力问题、provider 参数问题和业务 prompt 问题？
9. 如果让你重新设计 Skill 系统，你会先补哪三个能力？
10. 如果线上用户反馈 Agent 工具不可用，你的排查路径是什么？

## 高频问题回答草稿

### Q1：你在 YouNavi 里最核心的贡献是什么？

我认为最核心的是两件事。第一是模型接入和评测，把 OpenRouter、网宿、直连等不同模型通路接进系统，并用 benchmark 测延迟、效果和能力边界。第二是工具链工程化，把 YouNavi 的能力通过 CLI/MCP/Skill 暴露给外部 Agent 和用户 workflow，包括飞书 CLI、YouNavi CLI 前端、skill 删除边界这些真实产品化问题。WSL/打包适配只能作为补充例子。

### Q2：为什么这不是普通 CRUD？

普通 CRUD 更多是数据增删改查。这里的复杂点在于通路和环境都不稳定：模型通路有 OpenRouter、网宿、直连、代理差异；调用方可能是 Claude Code、Codex、OpenClaw 或 CLI；运行环境可能是源码、打包后的 Windows executable 或 WSL；能力本身还要被包装成 Agent 能理解的 tool/skill。很多 bug 发生在 provider 参数、路径、依赖、网络、状态检测、用户环境副作用这些边界上。

### Q3：你怎么证明自己不是只用 AI 写代码？

我会从三个方面讲。第一，PR 里有大量真实边界修复，比如 provider 路由、benchmark 工具、skill 删除路径、CLI 可用性问题，这些需要理解系统状态和运行环境，不是单纯生成代码。第二，我会控制 AI 的作用范围，先给它明确上下文和目标，再 review diff 是否越界。第三，验证上我会跑 benchmark、CLI 命令、单测、打包环境或前端状态，而不是只看代码能生成。

补充一句：我不回避 AI 参与开发，但我会强调自己负责的是工程判断和交付闭环。面试官问得越细，我越要回到具体例子：benchmark 怎么测、CLI 为什么重复登录、skill 删除为什么不能按显示名删。WSL/打包问题只在被追问环境兼容时补充。

### Q4：如果面试官问 RAG，但你项目里不是 RAG 怎么办？

可以直接说：我这个实习项目主线不是 RAG，而是 Agent 工具生态和本地运行时。不过我理解 RAG 在 Agent 应用里常作为知识工具存在，关键链路是切分、索引、检索、rerank、context 构造和忠实度评估。如果结合 YouNavi，我更可能把 RAG 作为一个可被 Skill 或 MCP 暴露的工具，而不是把它说成我已经上线过的主模块。

### Q5：你最大的技术成长是什么？

以前我容易把 Agent 理解成模型规划和多轮推理，但这段实习让我意识到 Agent 应用落地很大一部分是模型通路、评测体系、工具生态和运行时工程。模型能不能稳定接入、效果和延迟有没有评测、CLI/Skill 能不能被用户正确安装和调用、跨平台路径和打包是否稳定，这些东西如果不稳，模型再强也无法完成真实任务。

## 不能乱说的边界

- 不要说“我主导了整个 YouNavi Agent 平台”。
- 不要说“我实现了完整多 Agent 编排系统”。
- 不要说“我做了 RAG 系统上线”。
- 不要说“我做了模型训练、LoRA、DPO、RLHF”。
- 不要编性能提升数字。
- 不要把 closed PR 当作已上线成果；#562 可以作为实际做过的大型模型/benchmark 工作讲，但如果被问 PR 状态，要说清它不是最终 merged 成果，后续有拆分/替代路径。
- 不要把 AI 生成的代码说成完全手写，也不要装作没有用 AI；要强调你负责需求拆解、约束、review、验证和最终交付责任。

## 最适合放进简历的三条

1. 参与 YouNavi 多模型接入与评测体系建设，扩展 OpenRouter、网宿、直连等模型通路，重构 benchmark 工具，覆盖延迟、效果、工具调用和视觉等测试维度，为模型选择提供工程化评测依据。

2. 参与 YouNavi 外部调用链路建设，将会议采集、内容分析等核心能力通过 CLI/MCP 两类接口封装给 Claude Code、Codex、OpenClaw 等外部 Agent 或本地 workflow 调用，并补齐安装、调用和状态检测链路。

3. 重构 Skill 与 CLI 工具链，落地飞书 CLI 安装/调用 skill、YouNavi CLI 管理页，并修复 skill 重名、目录名与 skill 名不一致导致的删除失败等边界问题。

## 模拟面试打法

第一轮模拟只练 4 个问题：

1. 2 分钟讲项目。
2. 模型接入和 benchmark 怎么做。
3. CLI 和 MCP 为什么并行，后续不用 MCP 怎么解释。
4. 飞书 CLI skill 和 YouNavi CLI 前端怎么讲。

第二轮模拟加压：

1. 你做的东西和真正 Agent planning 有什么关系？
2. 如果工具调用失败，系统怎么处理？
3. benchmark 如何区分 provider 问题、模型能力问题和 prompt 问题？
4. 如果让你补 trace 和安全，你怎么设计？

第三轮模拟冲刺：

1. 随机抽一个 PR，让你说背景、改动、风险、验证。
2. 随机抽一个面经高频题，让你绑定到 YouNavi 回答。
3. 手撕一道 Python Easy/Medium。
