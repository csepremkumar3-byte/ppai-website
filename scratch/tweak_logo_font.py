import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Increase Title Font Size slightly
old_title = r'\.hero-main-title \{[\s\S]*?font-size: clamp\(18px, 1\.7vw, 26px\);[\s\S]*?\}'
new_title = """.hero-main-title {
      font-size: clamp(20px, 1.9vw, 29px);
      font-weight: 800;
      color: var(--deep-forest);
      line-height: 1.15;
      letter-spacing: -0.03em;
      margin-bottom: 12px;
      text-align: left;
    }"""
content = re.sub(old_title, new_title, content)

# 2. Center Logo and Enhance Visibility
old_wrapper = r'\.hero-jubilee-wrapper \{[\s\S]*?margin-bottom: 16px;\s*\}'
new_wrapper = """.hero-jubilee-wrapper {
      display: inline-flex;
      align-self: center;
      margin-bottom: 24px;
    }"""
content = re.sub(old_wrapper, new_wrapper, content)

old_emblem = r'\.hero-jubilee-emblem \{[\s\S]*?filter: drop-shadow\(0 4px 10px rgba\(0, 0, 0, 0\.12\)\);\s*\}'
new_emblem = """.hero-jubilee-emblem {
      height: 64px;
      width: auto;
      display: block;
      image-rendering: -webkit-optimize-contrast;
      filter: drop-shadow(0 8px 20px rgba(217, 119, 6, 0.35));
    }"""
content = re.sub(old_emblem, new_emblem, content)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
