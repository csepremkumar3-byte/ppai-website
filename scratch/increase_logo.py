import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_emblem = r'\.hero-jubilee-emblem \{[\s\S]*?filter: drop-shadow\(0 6px 16px rgba\(217, 119, 6, 0\.3\)\);\s*\}'
new_emblem = """.hero-jubilee-emblem {
      height: clamp(90px, 10vh, 130px);
      width: auto;
      object-fit: contain;
      display: block;
      image-rendering: -webkit-optimize-contrast;
      filter: drop-shadow(0 10px 24px rgba(217, 119, 6, 0.5));
    }"""
content = re.sub(old_emblem, new_emblem, content)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
