---
title: 🏠 首页
hide:
  - navigation
  - toc
---

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Caveat:wght@700&display=swap" rel="stylesheet">

<div class="yohaku-header-row">
  <div class="yohaku-header-text">
    <div class="yohaku-header-title">Hi, I'm <span class="yohaku-name-box"><span class="name-text">Yohaku</span></span></div>
    <div class="yohaku-header-subtitle">
      <span class="yohaku-header-subtitle-inner">
        <span id="typewriter-text"></span><span class="typewriter-cursor">|</span>
      </span>
    </div>
    <div class="yohaku-header-btns">
      <a href="https://github.com/YH7916" target="_blank" rel="noopener noreferrer" class="md-button md-button--primary">
        GitHub
      </a>
      <a href="mailto:3188127343@qq.com" class="md-button">
        联系我
      </a>
    </div>
  </div>
  <div class="yohaku-header-avatar">
    <div class="yohaku-avatar-glow">
      <img src="assets/images/avatar.jpg" alt="Yohaku" width="200" height="200" loading="eager">
    </div>
  </div>
</div>

<script>
(function () {
  const lines = [
    "浙大 CS 大二在读",
    "ZipLab 科研实习",
    "AI Agent 开发实习",
    "期末补天ing",
  ];
  let lineIdx = 0, charIdx = 0, deleting = false;
  const el = document.getElementById("typewriter-text");
  if (!el) return;
  function tick() {
    const line = lines[lineIdx];
    if (!deleting) {
      el.textContent = line.slice(0, ++charIdx);
      if (charIdx === line.length) {
        deleting = true;
        setTimeout(tick, 1800);
        return;
      }
    } else {
      el.textContent = line.slice(0, --charIdx);
      if (charIdx === 0) {
        deleting = false;
        lineIdx = (lineIdx + 1) % lines.length;
      }
    }
    setTimeout(tick, deleting ? 40 : 80);
  }
  tick();
})();
</script>

<style>
.yohaku-header-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 64px;
  margin: -30px 0 32px 0;
  flex-wrap: wrap;
  min-height: 280px;
}

.yohaku-header-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-width: 240px;
  max-width: 420px;
  flex: 1 1 300px;
  padding: 0 8px;
}

.yohaku-header-title {
  font-size: 2.1rem;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-weight: 700;
  letter-spacing: 1px;
  margin-bottom: 16px;
  color: var(--md-default-fg-color);
  white-space: nowrap;
}

.yohaku-name-box {
  display: inline-flex;
  align-items: center;
  position: relative;
  padding: 4px 14px;
  margin-left: 8px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 4px dashed #518FC1;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(81, 143, 193, 0.15);
  overflow: hidden;
}

.yohaku-name-box .name-text {
  font-family: 'Caveat', cursive;
  font-weight: 700;
  font-size: 1.15em;
  color: #2d3436;
  position: relative;
  z-index: 2;
}

.yohaku-name-box::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.8), transparent);
  transition: left 0.6s ease;
  z-index: 1;
}

.yohaku-name-box:hover::before { left: 100%; }

[data-md-color-scheme="slate"] .yohaku-name-box {
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
  border-color: #518FC1;
  box-shadow: 0 2px 8px rgba(81, 143, 193, 0.3);
}

[data-md-color-scheme="slate"] .yohaku-name-box .name-text { color: #f7fafc; }

.yohaku-header-subtitle {
  font-size: 1.4rem;
  font-weight: bold;
  color: #6D6D6D;
  margin-bottom: 22px;
  line-height: 1.3;
  overflow: visible;
}

.yohaku-header-subtitle-inner {
  display: inline-block;
  min-width: 260px;
  padding-bottom: 10px;
}

.typewriter-cursor {
  display: inline-block;
  color: #518FC1;
  font-weight: 300;
  animation: blink 1s steps(1, end) infinite;
  margin-left: 2px;
}

@keyframes blink {
  0%, 49% { opacity: 1; }
  50%, 100% { opacity: 0; }
}

[data-md-color-scheme="slate"] .yohaku-header-subtitle { color: #b0b0b0; }

.yohaku-header-btns {
  display: flex;
  gap: 16px;
  margin-top: 8px;
}

/* 头像区 */
.yohaku-header-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 200px;
}

.yohaku-avatar-glow {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid rgba(81, 143, 193, 0.35);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.10);
}

.yohaku-avatar-glow img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}


/* 移动端 */
@media (max-width: 768px) {
  .yohaku-header-row {
    gap: 28px;
    margin-bottom: 24px;
    min-height: unset;
  }
  .yohaku-header-title { font-size: 1.6rem; }
  .yohaku-header-subtitle { font-size: 1.1rem; }
  .yohaku-header-avatar { flex: 0 0 140px; }
  .yohaku-avatar-glow { width: 140px; height: 140px; }
  .yohaku-header-subtitle-inner { min-width: 180px; }
}

</style>

---

## 核心板块

<div class="grid cards home-cards" markdown>

-   :microscope: **科研**

    ---
    TinyML · Efficient LLM · ZipLab 方向笔记

    [:octicons-arrow-right-24: 浏览笔记](Research/index.md)

-   :briefcase: **Career**

    ---
    AI Agent 实习经历 · 面经整理 · 技术复盘

    [:octicons-arrow-right-24: 查看经历](Career/index.md)

-   :jigsaw: **算法**

    ---
    力扣 Hot100 · 手撕代码 · ACM 模式

    [:octicons-arrow-right-24: 题解整理](Dev/index.md)

-   :pencil: **随笔**

    ---
    生活碎片 · 深夜思考 · 文字记录

    [:octicons-arrow-right-24: 浏览文章](Diary/index.md)

</div>

---

## 🕰️ 近期动态

* [2026-06] 进入期末周，ZipLab 科研暂停，整理量化方向笔记
* [2026-04] 加入 ZJU ZipLab，方向：Efficient LLM Training/Inference
* [2026-02] 基于 Zensical 的个人博客重新上线
* [2026-01] 成功实现 KataGo 在 AutoDL 服务器上的云端部署
