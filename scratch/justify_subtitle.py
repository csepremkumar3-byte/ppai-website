import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Change subtitle alignment
old_subtitle_css = r'\.hero-main-subtitle \{[\s\S]*?text-align: left;\s*\}'
new_subtitle_css = """.hero-main-subtitle {
      font-size: clamp(13px, 0.9vw, 15px);
      color: var(--text-muted);
      line-height: 1.6;
      max-width: 100%;
      text-align: justify;
      text-justify: inter-word;
    }"""
content = re.sub(old_subtitle_css, new_subtitle_css, content)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
