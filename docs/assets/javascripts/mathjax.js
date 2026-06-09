window.MathJax = {
  loader: {
    load: ["[tex]/boldsymbol", "[tex]/physics", "[tex]/unicode"]
  },
  tex: {
    packages: { "[+]": ["boldsymbol", "physics", "unicode"] },
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
    macros: {
      bm: ["\\boldsymbol{#1}", 1],
      oiint: "\\mathop{\\unicode{x222F}}\\nolimits",
      oiiint: "\\mathop{\\unicode{x2230}}\\nolimits"
    }
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  },
  startup: {
    typeset: false,
    ready: () => {
      MathJax.startup.defaultReady();
      document$.subscribe(() => {
        const nodes = [...document.querySelectorAll(".arithmatex")]
          .filter(node => !node.querySelector("mjx-container"));
        MathJax.typesetPromise(nodes);
      });
    }
  }
};
