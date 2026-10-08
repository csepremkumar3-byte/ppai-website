import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_title_css = r'\.hero-main-title \{[\s\S]*?font-size: clamp\(20px, 1\.9vw, 29px\);[\s\S]*?\}'
new_title_css = """.hero-main-title {
      font-size: clamp(16px, 1.4vw, 22px);
      font-weight: 800;
      color: var(--deep-forest);
      line-height: 1.15;
      letter-spacing: -0.03em;
      margin-bottom: 6px;
      text-align: left;
    }"""
content = re.sub(old_title_css, new_title_css, content)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
