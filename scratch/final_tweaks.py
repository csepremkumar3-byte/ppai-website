import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Very High Visibility Logo
old_emblem = r'\.hero-jubilee-emblem \{[\s\S]*?filter: drop-shadow\(0 8px 20px rgba\(217, 119, 6, 0\.4\)\);\s*\}'
new_emblem = """.hero-jubilee-emblem {
      height: clamp(110px, 12vh, 150px);
      width: auto;
      object-fit: contain;
      display: block;
      image-rendering: -webkit-optimize-contrast;
      filter: drop-shadow(0 12px 28px rgba(217, 119, 6, 0.65)) drop-shadow(0 4px 8px rgba(0,0,0,0.2));
      transform: scale(1.05);
    }"""
content = re.sub(old_emblem, new_emblem, content)

# 2. Move Search Element to starting of Conferences & Seminars (column 3)
old_search_container = '<div class="portal-search-container" style="grid-column: 2 / -1; display: flex; align-items: flex-start; justify-content: center;">'
new_search_container = '<div class="portal-search-container" style="grid-column: 3 / 4; display: flex; align-items: flex-start; justify-content: flex-start;">'

old_form = 'style="width: 55%; min-width: 320px; height: 56px; display: flex; align-items: center; background: #FFFFFF; border: 1px solid var(--border-color); border-radius: 100px; padding: 0 8px 0 24px; box-shadow: var(--shadow-soft); transition: var(--transition);"'
new_form = 'style="width: 100%; height: 56px; display: flex; align-items: center; background: #FFFFFF; border: 1px solid var(--border-color); border-radius: 100px; padding: 0 8px 0 24px; box-shadow: var(--shadow-soft); transition: var(--transition);"'

content = content.replace(old_search_container, new_search_container)
content = content.replace(old_form, new_form)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
