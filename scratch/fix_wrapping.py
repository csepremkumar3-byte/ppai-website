import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adjust the grid to give the middle column more width
old_grid = r'\.hero-main-grid \{[\s\S]*?grid-template-columns: 1fr 1\.3fr 1\.1fr;[\s\S]*?\}'
new_grid = """.hero-main-grid {
      --hero-panel-h: clamp(320px, calc(100vh - 450px), 540px);
      display: grid;
      grid-template-columns: 0.9fr 1.6fr 1fr;
      gap: clamp(24px, 3vw, 48px);
      width: 100%;
      min-height: 0;
      flex: 1 1 auto;
      align-items: center;
    }"""
content = re.sub(old_grid, new_grid, content)

# 2. Reduce the font size of the title so it fits on one line
old_title = r'\.hero-main-title \{[\s\S]*?font-size: clamp\(24px, 2\.2vw, 34px\);[\s\S]*?\}'
new_title = """.hero-main-title {
      font-size: clamp(18px, 1.7vw, 26px);
      font-weight: 800;
      color: var(--deep-forest);
      line-height: 1.15;
      letter-spacing: -0.03em;
      margin-bottom: 12px;
      text-align: left;
    }"""
content = re.sub(old_title, new_title, content)

# Also wrap the first line in a span with white-space: nowrap just to FORCE it to stay on one line,
# while allowing the flex container to handle the width.
old_html = '<h1 class="hero-main-title">Fifty decades of Excellence in plant<br>Protection.</h1>'
new_html = '<h1 class="hero-main-title"><span style="white-space: nowrap;">Fifty decades of Excellence in plant</span><br>Protection.</h1>'
content = content.replace(old_html, new_html)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
