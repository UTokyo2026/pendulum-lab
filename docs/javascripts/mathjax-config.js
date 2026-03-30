// Must be loaded before MathJax script.
window.MathJax = {
  tex: {
    // Ensure AMS features like \eqref are available.
    packages: { "[+]": ["ams"] },
    // Number all display math, including $$...$$ blocks.
    tags: "all",
    tagSide: "right",
    tagIndent: "0.8em",
  },
};

