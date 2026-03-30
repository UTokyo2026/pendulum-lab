#!/usr/bin/env python
"""
Post-processing script: pandoc LaTeX→Markdown cleanup for MkDocs Material.
Fixes:
  1. :::divname blocks → MkDocs admonitions (cautionbox/tcolorbox → warning,
     submissionbox → note "Submission", minipage/tabular/others → strip wrapper)
  2. [text]{style="color: X"} spans → strip brackets+style, keep inner text
  3. <img src="..."> → ![](../figs/...) markdown
  4. {reference-type="ref" reference="..."} → remove
  5. <!-- -->{=html} and `xxx`{=html} → remove
  6. Content inside admonitions indented 4 spaces
"""

import re
import os
import sys


# ---------------------------------------------------------------------------
# Step 1: Remove <!-- -->{=html} and `xxx`{=html}
# ---------------------------------------------------------------------------
def remove_html_junk(text):
    # Remove `xxx`{=html} (backtick spans with {=html})
    text = re.sub(r'`[^`]*`\{=html\}', '', text)
    # Remove <!-- -->{=html}
    text = re.sub(r'<!--\s*-->\{=html\}', '', text)
    return text


# ---------------------------------------------------------------------------
# Step 2: Remove {reference-type="ref" reference="..."} junk
# ---------------------------------------------------------------------------
def remove_reference_junk(text):
    text = re.sub(r'\{reference-type="[^"]*"\s+reference="[^"]*"\}', '', text)
    return text


# ---------------------------------------------------------------------------
# Step 3: Fix <img src="filename" style="..."> → ![](../figs/filename)
# ---------------------------------------------------------------------------
def fix_images(text):
    def replace_img(m):
        src = m.group(1)
        # Strip any leading path separators and add ../figs/ prefix
        # If src is already ../figs/... leave it alone
        if src.startswith('../figs/'):
            return '![](' + src + ')'
        # Strip leading directory parts that are just the filename or subdir
        # e.g. "fig2026/foo.png" → "../figs/fig2026/foo.png"
        # e.g. "foo.png" → "../figs/foo.png"
        return '![](' + '../figs/' + src + ')'
    # Match <img src="..." .../>  or <img src="..." ...> (self-closing or not)
    text = re.sub(r'<img\s+src="([^"]+)"[^>]*/>', replace_img, text)
    text = re.sub(r'<img\s+src="([^"]+)"[^>]*>', replace_img, text)
    return text


# ---------------------------------------------------------------------------
# Step 4: Remove {style="color: ..."} spans — [text]{style="color: X"}
# Keep only the inner text. Handle nesting carefully using a loop.
# ---------------------------------------------------------------------------
def remove_style_spans(text):
    # We need to match [<inner>]{style="..."} where <inner> can contain
    # nested [...] content. We use a greedy-resistant approach by scanning
    # for the pattern and using bracket matching.
    changed = True
    max_passes = 20
    passes = 0
    while changed and passes < max_passes:
        changed = False
        passes += 1
        # Find the first occurrence of ]{style=
        idx = text.find(']{style=')
        if idx == -1:
            break
        # Find the matching opening bracket by scanning backwards
        # We need to find the '[' that pairs with the ']' at idx
        depth = 0
        open_pos = -1
        for i in range(idx - 1, -1, -1):
            if text[i] == ']':
                depth += 1
            elif text[i] == '[':
                if depth == 0:
                    open_pos = i
                    break
                else:
                    depth -= 1
        if open_pos == -1:
            break
        # Now find the end of {style="..."} after idx+1
        # The ] is at idx, the { starts at idx+1
        rest = text[idx + 1:]  # starts with ]{style=... wait no
        # Actually idx points to ], and rest of span starts at idx+1 → {style=...}
        style_match = re.match(r'\]\{style="[^"]*"\}', text[idx:])
        if not style_match:
            break
        end_pos = idx + len(style_match.group(0))
        inner = text[open_pos + 1:idx]
        text = text[:open_pos] + inner + text[end_pos:]
        changed = True
    return text


# ---------------------------------------------------------------------------
# Step 5: Process ::: div blocks and build admonition-indented output
# ---------------------------------------------------------------------------

ADMONITION_TYPES = {
    'cautionbox': '!!! warning',
    'tcolorbox': '!!! warning',
    'submissionbox': '!!! note "Submission"',
}

# Wrappers to strip (just remove open/close lines, keep content)
STRIP_TYPES = {'minipage', 'tabular', 'center', 'wrapfigure'}

def classify_div(name):
    """Return ('admonition', header) or ('strip', None) or ('strip', None) for others."""
    name = name.strip().lower()
    if name in ADMONITION_TYPES:
        return ('admonition', ADMONITION_TYPES[name])
    # All others: strip the wrapper
    return ('strip', None)


def process_div_blocks(text):
    """
    State-machine approach:
    - Track a stack of open ::: blocks
    - For admonition blocks: emit the !!! header, then indent all content 4 spaces
    - For strip blocks: just skip the open/close lines, emit content as-is
    - Closing ::: pops the stack
    """
    lines = text.split('\n')
    out_lines = []
    # Stack entries: ('admonition', header) or ('strip', None)
    stack = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect opening ::: (one or more colons followed by a name)
        open_match = re.match(r'^(:{3,})\s+(\S+)', line)
        # Detect closing ::: (just colons, no name, on its own line)
        close_match = re.match(r'^:{3,}\s*$', line)

        if open_match:
            colons = open_match.group(1)
            div_name = open_match.group(2)
            kind, header = classify_div(div_name)
            stack.append((kind, header, colons))
            if kind == 'admonition':
                # Emit the admonition header (indented by enclosing admonitions)
                indent = '    ' * sum(1 for s in stack[:-1] if s[0] == 'admonition')
                out_lines.append(indent + header)
                out_lines.append(indent)  # blank line after header (will be stripped later)
            # For strip: emit nothing for the opening line
            i += 1
            continue

        if close_match and stack:
            stack.pop()
            # For closing: just skip the line
            i += 1
            continue

        # Regular content line
        if stack:
            # Count how many enclosing admonition levels
            admon_depth = sum(1 for s in stack if s[0] == 'admonition')
            if admon_depth > 0:
                indent = '    ' * admon_depth
                out_lines.append(indent + line)
            else:
                out_lines.append(line)
        else:
            out_lines.append(line)

        i += 1

    return '\n'.join(out_lines)


# ---------------------------------------------------------------------------
# Admonition blank-line cleanup:
# MkDocs admonitions end when content returns to non-indented lines.
# We need to ensure there's no trailing blank line inside admonitions that
# would confuse MkDocs. Actually MkDocs Material handles this fine.
# But we should clean up the extra blank line we emit after the header.
# ---------------------------------------------------------------------------
def cleanup_admonition_blanks(text):
    """
    After '!!! warning' or '!!! note "..."' line, remove immediately following
    blank lines that we inserted as spacers (MkDocs doesn't need them).
    But a blank line that is INDENTED (part of admonition content) is fine.
    Actually: remove blank lines immediately after the !!! header line.
    """
    lines = text.split('\n')
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r'^    *!!! ', line) or re.match(r'^!!! ', line):
            out.append(line)
            i += 1
            # Skip blank lines immediately after admonition header
            while i < len(lines) and lines[i].strip() == '':
                i += 1
            continue
        out.append(line)
        i += 1
    return '\n'.join(out)


# ---------------------------------------------------------------------------
# Main processing pipeline
# ---------------------------------------------------------------------------
def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    original = text

    # Step 1: Remove HTML junk
    text = remove_html_junk(text)

    # Step 2: Remove reference junk
    text = remove_reference_junk(text)

    # Step 3: Fix images
    text = fix_images(text)

    # Step 4: Remove style spans
    text = remove_style_spans(text)

    # Step 5: Process div blocks (admonitions + strip wrappers)
    text = process_div_blocks(text)

    # Step 6: Cleanup blank lines after admonition headers
    text = cleanup_admonition_blanks(text)

    if text != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'  [MODIFIED] {filepath}')
    else:
        print(f'  [unchanged] {filepath}')


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    base = 'd:/Local/20251230_Inverted_Pendulum/text2026/pendulum-lab/docs'
    files = []
    for lang in ('en', 'jp'):
        for name in ('intro.md', 'overview.md', 'week1.md', 'week2.md', 'week3.md', 'week4.md'):
            p = os.path.join(base, lang, name)
            if os.path.exists(p):
                files.append(p)
            else:
                print(f'  [MISSING] {p}')

    if '--file' in sys.argv:
        idx = sys.argv.index('--file')
        files = [sys.argv[idx + 1]]

    print(f'Processing {len(files)} files...')
    for fp in files:
        process_file(fp)
    print('Done.')
