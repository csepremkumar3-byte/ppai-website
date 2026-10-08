import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the emblem height
old_emblem = r'\.hero-jubilee-emblem \{[\s\S]*?filter: drop-shadow\(0 8px 20px rgba\(217, 119, 6, 0\.35\)\);\s*\}'
new_emblem = """.hero-jubilee-emblem {
      height: clamp(76px, 9vh, 96px);
      width: auto;
      object-fit: contain;
      display: block;
      image-rendering: -webkit-optimize-contrast;
      filter: drop-shadow(0 8px 20px rgba(217, 119, 6, 0.4));
    }"""
content = re.sub(old_emblem, new_emblem, content)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
