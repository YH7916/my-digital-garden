你浙大多数人都是用的mkdocs，似乎并不在维护了。
原团队全新推出了Zensical，我来品尝一下。

安装方式和mkdocs没什么大区别。

## 🛠️ 第一阶段：纯净的本地环境配置

为了避免包管理混乱，我们采用 Miniconda 来管理虚拟环境，做到用完即焚、互不干扰。

**1. 创建并激活专属虚拟环境** 打开终端（PowerShell），创建一个名为 `mygarden` 的环境：

PowerShell

```
conda create -n mygarden python=3.13
conda activate mygarden
```

**2. 安装 Zensical 与核心主题** 在激活的环境中，直接通过 pip 安装Zensical和 Material 主题：

PowerShell

```
pip install zensical mkdocs-material
```

_(注：如果需要完美兼容 Obsidian 的 `[[双向链接]]` 且 Zensical 版本支持，可额外安装 `mkdocs-roamlinks-plugin`。)_

---

## 📂 第二阶段：初始化项目与 Obsidian 整合

**1. 初始化项目骨架** 在你的笔记根目录（例如 `D:\Vault\Notes`）下运行：

PowerShell

```
zensical new .
```

这会生成一个 `mkdocs.yml` 配置文件和一个 `docs` 文件夹。

**2. 将 docs 设为 Obsidian 仓库 (极度重要)** **不要**把外层目录作为 Obsidian 仓库，请直接在 Obsidian 中打开 `docs` 文件夹作为你的 Vault。

---

## ⚙️ 第三阶段：YAML 配置

这里给出我使用的`mkdocs.yml`。这套配置原生支持算法公式、代码块一键复制、Mermaid 架构图以及极其平滑的明暗模式切换。

YAML

```
site_name: Yohaku 的数字花园
site_description: 记录代码、算法与灵感
site_author: Yohaku

# ----------------- 界面与视觉配置 -----------------
theme:
  name: material
  language: zh
  font:
    text: Noto Sans
    code: Fira Code
  features:
    - navigation.tabs # 顶部分类标签
    - navigation.tabs.sticky # 标签页吸顶
    - navigation.top # 返回顶部按钮
    - navigation.tracking # 侧边栏自动高亮当前章节
    - search.highlight # 搜索结果高亮
    - search.suggest # 搜索词输入建议
    - content.code.copy # 代码块添加“一键复制”
    - content.code.annotate # 代码悬浮注释

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

# ----------------- 插件与渲染引擎 -----------------
plugins:
  - search

markdown_extensions:
  - abbr
  - admonition # 提示框 (!!! note)
  - attr_list # 图片缩放支持
  - def_list
  - footnotes # 脚注
  - toc:
      permalink: true # 段落锚点链接
  
  # 数学公式与算法支持
  - pymdownx.arithmatex: 
      generic: true
  
  # 高级排版控件
  - pymdownx.details # 折叠详情 (??? info)
  
  # 代码块扩展
  - pymdownx.highlight:
      anchor_linenums: true # 代码行号
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.superfences: # 支持 Mermaid 流程图
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  
  # 任务列表
  - pymdownx.tasklist: 
      custom_checkbox: true

# ----------------- 自定义数学公式脚本 -----------------
# 需在 docs/javascripts 下新建 mathjax.js
extra_javascript:
  - javascripts/mathjax.js
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js
```

在本地终端输入 `zensical serve` 即可预览网页。

---

## ☁️ 第四阶段：Cloudflare Pages 自动化部署

告别繁琐的服务器配置，我们直接将代码托管至 GitHub，并利用 Cloudflare 的全球边缘网络进行加速与部署。

**1. 准备云端依赖清单** 在项目根目录（`mkdocs.yml` 同级）新建 `requirements.txt`：

Plaintext

```
zensical
mkdocs-material
```

**2. 推送至 GitHub (SSH 方式)** 在本地初始化并推送到你的 GitHub 仓库：

PowerShell

```
git init
git add .
git commit -m "feat: init Zensical garden"
git branch -M main
git remote add origin git@github.com:你的用户名/你的仓库名.git
git push -u origin main
```

**3. 配置 Cloudflare Pages**

1. 登录 Cloudflare 控制面板，进入 **Workers & Pages** -> **Connect to Git**。
    
2. 选中刚才的仓库，关键构建配置如下：
    
    - **框架预设 (Framework preset)**：`None`
        
    - **构建命令 (Build command)**：`pip install -r requirements.txt && zensical build`
        
    - **构建输出目录 (Build output directory)**：`site`
        
3. 绑定你自己的自定义域名，并在域名服务商处将 DNS 服务器修改为 Cloudflare 接管。
    

---

## ⚡ 终极形态：Obsidian 一键同步闭环

为了实现“敲完笔记即刻上线”，无需再打开终端敲命令，我们在 Obsidian 中安装Git插件，即可实现自动同步

