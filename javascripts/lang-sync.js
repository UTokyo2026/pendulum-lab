(() => {
  const STORAGE_KEY = "langSync:pending";
  const LANGS = new Set(["en", "jp"]);

  function getPathParts(pathname) {
    const hasTrailingSlash = pathname.endsWith("/");
    const parts = pathname.split("/").filter(Boolean);
    return { parts, hasTrailingSlash };
  }

  function detectLang(pathname) {
    const { parts, hasTrailingSlash } = getPathParts(pathname);
    const idx = parts.findIndex((p) => LANGS.has(p));
    if (idx < 0) return null;
    return { lang: parts[idx], idx, parts, hasTrailingSlash };
  }

  function swapLangInPath(pathname, toLang) {
    const info = detectLang(pathname);
    if (!info) return null;
    const next = [...info.parts];
    next[info.idx] = toLang;
    return "/" + next.join("/") + (info.hasTrailingSlash ? "/" : "");
  }

  function closestHeadingId() {
    const candidates = Array.from(
      document.querySelectorAll(
        ".md-content h1[id], .md-content h2[id], .md-content h3[id], .md-content h4[id], .md-content h5[id], .md-content h6[id]"
      )
    );
    if (candidates.length === 0) return null;

    const y = window.scrollY;
    let best = candidates[0];
    for (const h of candidates) {
      const top = h.getBoundingClientRect().top + window.scrollY;
      if (top <= y + 8) best = h;
      else break;
    }
    return best.id || null;
  }

  function computeOffsetFromAnchorId(id) {
    const el = document.getElementById(id);
    if (!el) return 0;
    const top = el.getBoundingClientRect().top + window.scrollY;
    return window.scrollY - top;
  }

  function getTargetLangFromHref(href) {
    try {
      const u = new URL(href, window.location.href);
      const info = detectLang(u.pathname);
      return info?.lang ?? null;
    } catch {
      return null;
    }
  }

  function storePending(targetPath, anchorId, offset) {
    const payload = {
      targetPath,
      anchorId,
      offset,
      ts: Date.now(),
    };
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
    } catch {
      // ignore
    }
  }

  function readPending() {
    try {
      const raw = sessionStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch {
      return null;
    }
  }

  function clearPending() {
    try {
      sessionStorage.removeItem(STORAGE_KEY);
    } catch {
      // ignore
    }
  }

  function applyPendingIfAny() {
    const pending = readPending();
    if (!pending) return;

    if (pending.targetPath !== window.location.pathname) return;
    if (!pending.anchorId) {
      clearPending();
      return;
    }

    const startedAt = Date.now();
    const maxWaitMs = 1500;

    const tryApply = () => {
      const el = document.getElementById(pending.anchorId);
      if (!el) {
        clearPending();
        return;
      }

      const top = el.getBoundingClientRect().top + window.scrollY;
      window.scrollTo({ top: top + (pending.offset || 0) });
      clearPending();
    };

    const loop = () => {
      if (Date.now() - startedAt > maxWaitMs) {
        tryApply();
        return;
      }
      // Wait until layout stabilizes a bit (images/fonts)
      requestAnimationFrame(() => requestAnimationFrame(loop));
    };

    window.addEventListener(
      "load",
      () => {
        loop();
      },
      { once: true }
    );
  }

  function onTabClick(e) {
    const a = e.target instanceof Element ? e.target.closest("a") : null;
    if (!a) return;

    // Only intercept top navigation tabs (Material theme).
    if (!a.closest(".md-tabs")) return;

    const toLang = getTargetLangFromHref(a.getAttribute("href") || "");
    if (!toLang) return;

    const cur = detectLang(window.location.pathname);
    if (!cur || cur.lang === toLang) return;

    const targetPath = swapLangInPath(window.location.pathname, toLang);
    if (!targetPath) return;

    // Prefer existing hash if it points to a real element; otherwise use closest heading.
    let anchorId = null;
    if (window.location.hash && window.location.hash.length > 1) {
      const id = decodeURIComponent(window.location.hash.slice(1));
      if (document.getElementById(id)) anchorId = id;
    }
    if (!anchorId) anchorId = closestHeadingId();

    const offset = anchorId ? computeOffsetFromAnchorId(anchorId) : 0;

    e.preventDefault();
    e.stopPropagation();

    const hash = anchorId ? `#${encodeURIComponent(anchorId)}` : "";
    storePending(targetPath, anchorId, offset);
    window.location.assign(targetPath + window.location.search + hash);
  }

  document.addEventListener("click", onTabClick, true);
  applyPendingIfAny();
})();

