(() => {
  function buildFigNoById(container) {
    const figures = Array.from(container.querySelectorAll('figure[id^="fig:"]'));
    const figNoById = new Map();

    let n = 0;
    for (const fig of figures) {
      n += 1;
      figNoById.set(fig.id, n);

      // Also map any nested fig:* anchors (e.g. sub-images) to the same figure number.
      const nested = Array.from(fig.querySelectorAll('[id^="fig:"]'));
      for (const el of nested) {
        if (!el.id) continue;
        if (!figNoById.has(el.id)) figNoById.set(el.id, n);
      }
    }

    return figNoById;
  }

  function updateFigureRefsIn(container, figNoById) {
    const links = Array.from(container.querySelectorAll('a[href^="#fig:"]'));
    for (const a of links) {
      const href = a.getAttribute("href");
      if (!href) continue;
      const id = href.slice(1); // strip leading '#'
      const n = figNoById.get(id);
      if (!n) continue;
      a.textContent = `Fig. ${n}`;
    }
  }

  function run() {
    const root = document.querySelector(".md-content");
    if (!root) return;
    const figNoById = buildFigNoById(root);
    updateFigureRefsIn(root, figNoById);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();

