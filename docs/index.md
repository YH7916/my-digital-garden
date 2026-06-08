---
title: 🏠 首页
description: Yohaku 的个人数字花园，整理科研、实习、算法、课程笔记与随笔。
hide:
  - navigation
  - toc
---

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Caveat:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.5.2/css/all.min.css">

<div class="yohaku-header-row">
  <div class="yohaku-header-text">
    <h1 class="yohaku-header-title">Hi, I'm <span class="yohaku-name-box"><span class="name-text">Yohaku</span></span></h1>
    <div class="yohaku-header-subtitle">
      <span class="yohaku-header-subtitle-inner">
        <span id="typewriter-text"></span><span class="typewriter-cursor">|</span>
      </span>
    </div>
    <div class="yohaku-header-btns">
      <a href="https://github.com/YH7916" target="_blank" rel="noopener noreferrer" class="md-button md-button--primary">
        <span class="yohaku-button-icon yohaku-button-icon--github" aria-hidden="true">
          <i class="fa-brands fa-github"></i>
        </span>
        GitHub
      </a>
      <a href="mailto:3188127343@qq.com" class="md-button">
        <span class="yohaku-button-icon yohaku-button-icon--mail" aria-hidden="true">
          <i class="fa-solid fa-paper-plane"></i>
        </span>
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

(function () {
  const hero = document.querySelector(".yohaku-header-row");
  const avatar = document.querySelector(".yohaku-header-avatar");
  const canTrackPointer = window.matchMedia("(pointer: fine)").matches;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!hero || !avatar || !canTrackPointer || reduceMotion) return;

  let frame = 0;

  function setGlowFromPointer(event) {
    if (frame) cancelAnimationFrame(frame);
    frame = requestAnimationFrame(function () {
      const rect = avatar.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      const deltaX = event.clientX - centerX;
      const deltaY = event.clientY - centerY;
      const distance = Math.hypot(deltaX, deltaY);
      const maxDistance = Math.hypot(rect.width / 2, rect.height / 2);
      const proximity = Math.max(0, 1 - Math.min(distance / maxDistance, 1));
      const angle = Math.atan2(deltaY, deltaX) * 180 / Math.PI + 90;

      avatar.style.setProperty("--glow-angle", angle.toFixed(1) + "deg");
      avatar.style.setProperty("--glow-opacity", (0.54 + proximity * 0.16).toFixed(2));
      avatar.style.setProperty("--glow-ring-opacity", (0.34 + proximity * 0.26).toFixed(2));
      avatar.style.setProperty("--glow-core-opacity", (0.58 + proximity * 0.22).toFixed(2));
      avatar.style.setProperty("--glow-scale", (1.01 + proximity * 0.055).toFixed(3));
      avatar.style.setProperty("--glow-saturation", (0.88 + proximity * 0.16).toFixed(2));
    });
  }

  function resetGlow() {
    if (frame) cancelAnimationFrame(frame);
    avatar.style.setProperty("--glow-angle", "135deg");
    avatar.style.setProperty("--glow-opacity", "0.54");
    avatar.style.setProperty("--glow-ring-opacity", "0.34");
    avatar.style.setProperty("--glow-core-opacity", "0.58");
    avatar.style.setProperty("--glow-scale", "1.01");
    avatar.style.setProperty("--glow-saturation", "0.88");
  }

  hero.addEventListener("pointermove", setGlowFromPointer);
  hero.addEventListener("pointerleave", resetGlow);
})();
</script>

<style>
.md-typeset > h1:first-of-type {
  display: none;
}

.yohaku-header-row {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(220px, 0.82fr);
  align-items: center;
  justify-content: space-between;
  gap: clamp(40px, 7vw, 88px);
  max-width: 1120px;
  min-height: 390px;
  margin: clamp(8px, 4vw, 44px) auto clamp(28px, 6vw, 64px);
  padding: clamp(14px, 3vw, 32px) 0;
}

.yohaku-header-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  max-width: 680px;
  min-width: 0;
  padding: 0;
}

.md-typeset .yohaku-header-title {
  font-size: clamp(2.6rem, 6vw, 4.9rem);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-weight: 900;
  letter-spacing: 0;
  line-height: 0.98;
  margin: 0 0 24px;
  color: var(--md-default-fg-color);
  white-space: normal;
}

.yohaku-name-box {
  --yohaku-name-accent: var(--md-accent-fg-color);
  display: inline-flex;
  align-items: center;
  position: relative;
  width: auto;
  max-width: 100%;
  padding: 4px 14px;
  margin-left: 12px;
  background:
    linear-gradient(
      135deg,
      color-mix(in srgb, var(--yohaku-name-accent) 10%, var(--md-default-bg-color)) 0%,
      color-mix(in srgb, var(--yohaku-name-accent) 4%, var(--md-default-bg-color)) 100%
    );
  border: 4px dashed var(--yohaku-name-accent);
  border-radius: 10px;
  box-shadow: 0 2px 10px color-mix(in srgb, var(--yohaku-name-accent) 22%, transparent);
  overflow: hidden;
  vertical-align: 0.04em;
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
  background:
    linear-gradient(
      90deg,
      transparent,
      color-mix(in srgb, var(--yohaku-name-accent) 18%, rgba(255,255,255,0.88)),
      transparent
    );
  transition: left 0.6s ease;
  z-index: 1;
}

.yohaku-name-box:hover::before { left: 100%; }

[data-md-color-scheme="slate"] .yohaku-name-box {
  background:
    linear-gradient(
      135deg,
      color-mix(in srgb, var(--yohaku-name-accent) 18%, #1a202c) 0%,
      color-mix(in srgb, var(--yohaku-name-accent) 8%, #0f172a) 100%
    );
  box-shadow: 0 2px 12px color-mix(in srgb, var(--yohaku-name-accent) 34%, transparent);
}

[data-md-color-scheme="slate"] .yohaku-name-box .name-text { color: #f7fafc; }

.yohaku-header-subtitle {
  min-height: 2.1em;
  font-size: clamp(1.25rem, 2.3vw, 1.75rem);
  font-weight: 700;
  color: var(--md-default-fg-color--light);
  margin-bottom: 30px;
  line-height: 1.35;
  overflow: visible;
}

.yohaku-header-subtitle-inner {
  display: inline-block;
  min-width: min(320px, 100%);
  padding-bottom: 0;
}

.typewriter-cursor {
  display: inline-block;
  color: #41a6ff;
  font-weight: 300;
  animation: blink 1s steps(1, end) infinite;
  margin-left: 2px;
}

@keyframes blink {
  0%, 49% { opacity: 1; }
  50%, 100% { opacity: 0; }
}

.yohaku-header-btns {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 0;
}

.yohaku-header-btns .md-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5em;
  border-radius: 999px;
  padding: 0.72em 1.25em;
  font-size: 0.82rem;
  font-weight: 700;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.yohaku-button-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.12em;
  height: 1.12em;
  flex: 0 0 auto;
  transform-origin: center;
  transition: transform 0.18s ease;
}

.yohaku-button-icon i {
  font-size: 1.12em;
  line-height: 1;
}

.yohaku-header-btns .md-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(65, 166, 255, 0.16);
}

.yohaku-header-btns .md-button:hover .yohaku-button-icon {
  transform: translateY(-1px) rotate(-4deg) scale(1.06);
}

/* 头像区 */
.yohaku-header-avatar {
  --glow-angle: 135deg;
  --glow-opacity: 0.54;
  --glow-ring-opacity: 0.34;
  --glow-core-opacity: 0.58;
  --glow-scale: 1.01;
  --glow-saturation: 0.88;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 370px;
}

.yohaku-avatar-glow {
  position: relative;
  width: clamp(260px, 32vw, 370px);
  height: clamp(260px, 32vw, 370px);
  border-radius: 50%;
  overflow: hidden;
  border: 1px solid rgba(65, 166, 255, 0.26);
  box-shadow:
    0 30px 76px rgba(92, 118, 154, 0.22),
    0 0 46px rgba(255, 255, 255, 0.34),
    0 0 34px rgba(154, 190, 220, 0.18),
    inset 0 1px 0 rgba(255, 255, 255, 0.52);
  z-index: 1;
}

.yohaku-header-avatar::before {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: clamp(320px, 40vw, 470px);
  height: clamp(320px, 40vw, 470px);
  border-radius: 50%;
  background:
    radial-gradient(circle at 42% 36%, rgba(255, 255, 255, var(--glow-core-opacity)), transparent 22%),
    radial-gradient(circle at 50% 52%, rgba(210, 226, 245, 0.48), transparent 58%),
    radial-gradient(circle at 68% 42%, rgba(172, 190, 218, 0.26), transparent 50%),
    linear-gradient(var(--glow-angle), rgba(235, 241, 255, 0.46), rgba(155, 188, 218, 0.32), rgba(230, 236, 248, 0.28));
  filter: blur(60px) saturate(var(--glow-saturation));
  opacity: var(--glow-opacity);
  transform: translate(-50%, -50%) translate3d(8px, 0, 0) scale(var(--glow-scale));
  transform-origin: center;
  transition: opacity 0.22s ease, transform 0.22s ease, filter 0.22s ease, background 0.22s ease;
  will-change: opacity, transform, filter;
  pointer-events: none;
}

.yohaku-header-avatar::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: clamp(274px, 33.5vw, 388px);
  height: clamp(274px, 33.5vw, 388px);
  border-radius: 50%;
  background:
    radial-gradient(circle, transparent 59%, rgba(255, 255, 255, 0.58) 63%, rgba(184, 207, 232, 0.34) 68%, transparent 73%),
    conic-gradient(from var(--glow-angle), rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.92), rgba(176, 202, 230, 0.52), rgba(255, 255, 255, 0));
  opacity: var(--glow-ring-opacity);
  transform: translate(-50%, -50%) translate3d(8px, 0, 0) scale(var(--glow-scale));
  filter: blur(9px) saturate(var(--glow-saturation));
  transition: opacity 0.22s ease, transform 0.22s ease, filter 0.22s ease, background 0.22s ease;
  will-change: opacity, transform, filter;
  pointer-events: none;
}

@media (prefers-reduced-motion: reduce) {
  .yohaku-header-avatar::before,
  .yohaku-header-avatar::after {
    transition: none;
  }
}

.yohaku-avatar-glow img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}


/* 移动端 */
@media (max-width: 960px) {
  .yohaku-header-row {
    grid-template-columns: 1fr;
    gap: 26px;
    min-height: unset;
    margin: 0 auto 30px;
    padding: 10px 0 12px;
    text-align: center;
  }
  .yohaku-header-text {
    align-items: center;
    max-width: 680px;
    margin: 0 auto;
    order: 2;
  }
  .md-typeset .yohaku-header-title {
    font-size: clamp(2.5rem, 13vw, 4rem);
    margin-bottom: 18px;
  }
  .yohaku-name-box {
    margin-left: 8px;
    padding: 3px 12px;
    border-width: 3px;
  }
  .yohaku-header-subtitle {
    min-height: 1.8em;
    font-size: clamp(1.15rem, 5vw, 1.45rem);
    margin-bottom: 24px;
  }
  .yohaku-header-subtitle-inner {
    min-width: 0;
  }
  .yohaku-header-btns {
    justify-content: center;
  }
  .yohaku-header-avatar {
    order: 1;
    min-height: 230px;
  }
  .yohaku-avatar-glow {
    width: clamp(180px, 52vw, 230px);
    height: clamp(180px, 52vw, 230px);
  }
  .yohaku-header-avatar::after {
    width: clamp(194px, 56vw, 246px);
    height: clamp(194px, 56vw, 246px);
  }
}

@media (max-width: 480px) {
  .yohaku-header-row {
    margin-top: 0;
  }
  .md-typeset .yohaku-header-title {
    font-size: clamp(2.25rem, 12vw, 3.25rem);
  }
  .yohaku-header-btns {
    width: 100%;
  }
  .yohaku-header-btns .md-button {
    flex: 1 1 136px;
    text-align: center;
  }
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

* **2026-06** 进入期末周，ZipLab 科研暂停，整理量化方向笔记
* **2026-04** 加入 ZJU ZipLab，方向：Efficient LLM Training/Inference
* **2026-02** 基于 Zensical 的个人博客重新上线
* **2026-01** 成功实现 KataGo 在 AutoDL 服务器上的云端部署
