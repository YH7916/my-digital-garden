你浙大多数人都是用的mkdocs，似乎并不在维护了。 原团队推出了新一代静态站点生成器 **Zensical**，底层采用 Rust 编写的 MiniJinja 引擎，我来品尝一下。

安装方式和mkdocs没什么大区别。
## 🛠️ 第一阶段：纯净的本地环境与现代依赖管理

为了避免全局包管理混乱，我们采用 Miniconda 来管理虚拟环境。同时，**彻底抛弃 `requirements.txt`**，全面拥抱当前 Python 开发的标配：`pyproject.toml`。

**1. 创建并激活专属虚拟环境** 打开终端（PowerShell），创建一个名为 `mygarden` 的环境：



```PowerShell
conda create -n mygarden python=3.13
conda activate mygarden
```

**2. 建立现代化的依赖清单** 在你的项目根目录（例如 `D:\Vault\Notes`），新建一个 `pyproject.toml` 文件。这会让你的本地环境配置和云端部署一次性打通：

```TOML
[project]
name = "yohaku-digital-garden"
version = "0.1.0"
description = "Yohaku 的数字花园"
requires-python = ">=3.9"

dependencies = [
    "zensical",
    "mkdocs-material",
    "mkdocs-roamlinks-plugin",
    "mkdocs-awesome-pages-plugin",
    "pymdown-extensions"
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
bypass-selection = true
```

**3. 一键安装全部依赖** 在包含 `pyproject.toml` 的目录下运行：



```PowerShell
pip install .
```

---

## 📂 第二阶段：初始化项目与 Obsidian 整合

**1. 生成项目骨架** 在终端运行以下命令：


```PowerShell
zensical new .
```

这会生成一个核心配置文件 `mkdocs.yml` 和一个存放笔记的 `docs` 文件夹。

**2. 将 docs 设为 Obsidian 仓库 (极度重要)** **不要**把外层目录作为 Obsidian 仓库，请直接在 Obsidian 中打开 `docs` 文件夹作为你的 Vault。这样可以保证所有的双向链接和图片路径在本地和网页端完美一致。

---

## ⚙️ 第三阶段：极简且前卫的 YAML 配置

我们要剥离旧配置中那些深度绑定 Python 底层的 `!!python/name` 语法，并开启 Zensical/Material 的 SPA（单页应用）无白屏加载和沉浸式阅读特性。

将你的 `mkdocs.yml` 替换为以下内容：



```YAML
site_name: Yohaku 的数字花园
site_description: 记录代码、算法与灵感
site_author: Yohaku

# ----------------- 界面与视觉配置 (SPA 极速体验) -----------------
theme:
  name: material
  language: zh
  font:
    text: Noto Sans
    code: Fira Code
  features:
    - navigation.instant         # 开启 SPA 级单页应用无刷新
    - navigation.instant.prefetch# 鼠标悬停链接时后台悄悄预加载
    - navigation.instant.progress# 顶部轻量加载进度条
    - navigation.tabs            # 顶部分类标签
    - navigation.tabs.sticky     # 标签页吸顶
    - navigation.path            # 面包屑导航
    - navigation.top             # 返回顶部按钮
    - navigation.footer          # 沉浸式上一篇/下一篇阅读导航
    - toc.integrate              # 将右侧大纲整合入左侧菜单，极致留白
    - search.highlight           # 搜索结果高亮
    - search.suggest             # 搜索词输入建议
    - content.code.copy          # 代码块添加“一键复制”
    - content.code.annotate      # 代码悬浮注释气泡
    - content.tooltips           # 专业名词悬浮提示气泡

  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: white
      accent: indigo
      toggle:
        icon: material/weather-sunny
        name: 切换至深色模式
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: black
      accent: blue
      toggle:
        icon: material/weather-night
        name: 切换至浅色模式

# ----------------- 插件 (自动映射 Zensical 原生模块) -----------------
plugins:
  - search
  - tags:                     # 开启全局标签引擎
      tags_file: tags.md      # 在 docs 根目录新建 tags.md 并写入 [TAGS] 即可

# ----------------- 核心 Markdown 解析 (剔除冗余 Python 绑定) -----------------
markdown_extensions:
  - abbr
  - admonition
  - attr_list
  - def_list
  - footnotes
  - toc:
      permalink: true
  - pymdownx.arithmatex: 
      generic: true
  - pymdownx.details
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.superfences # 原生支持 Mermaid，无需再写复杂的 format 映射
  - pymdownx.tasklist: 
      custom_checkbox: true

# ----------------- 现代化外部脚本 (仅保留必要的公式引擎) -----------------
extra_javascript:
  - javascripts/mathjax.js
  - https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js
```

**补充说明：公式渲染的本地配置** 摒弃带有安全隐患的 `polyfill.io`，我们在 `docs/javascripts/` 目录下新建 `mathjax.js`，写入以下标准配置：


```JavaScript
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};
```

在本地终端输入 `zensical serve`，即可本地预览。

---

## ☁️ 第四阶段：Cloudflare Pages 自动化部署

告别繁琐的服务器配置，我们直接将代码托管至 GitHub，并利用 Cloudflare 的全球边缘网络进行加速与部署。由于我们采用了现代化的 `pyproject.toml`，云端构建命令也将变得极其优雅。

**1. 推送至 GitHub (SSH 方式)** 在本地初始化并推送到你的 GitHub 仓库：

```PowerShell
git init
git add .
git commit -m "feat: init Zensical garden"
git branch -M main
git remote add origin git@github.com:你的用户名/你的仓库名.git
git push -u origin main
```

**2. 配置 Cloudflare Pages**

1. 登录 Cloudflare 控制面板，进入 **Workers & Pages** -> **Connect to Git**。
    
2. 选中刚才的仓库，关键构建配置如下：
    
    - **框架预设 (Framework preset)**：`None`
        
    - **构建命令 (Build command)**：`pip install . && zensical build`
        
    - **构建输出目录 (Build output directory)**：`site`
        
3. 保存并部署。绑定你自己的自定义域名，并在域名服务商处将 DNS 服务器修改为 Cloudflare 接管。
    

---

## ⚡ 终极形态：Obsidian 一键同步闭环

为了实现“敲完笔记即刻上线”，无需再打开终端敲命令，我们在 Obsidian 中安装 `Obsidian Git` 插件，设置好定时自动 Commit 和 Push，即可实现完美闭环。