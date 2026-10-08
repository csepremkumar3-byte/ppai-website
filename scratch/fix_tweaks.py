import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Aspect Ratios to 3 / 4
content = content.replace('aspect-ratio: 4 / 3;', 'aspect-ratio: 3 / 4;')

# 2. Reduce Logo Visibility
old_emblem = r'\.hero-jubilee-emblem \{[\s\S]*?filter: drop-shadow\(0 12px 28px rgba\(217, 119, 6, 0\.65\)\) drop-shadow\(0 4px 8px rgba\(0,0,0,0\.2\)\);\s*transform: scale\(1\.05\);\s*\}'
new_emblem = """.hero-jubilee-emblem {
      height: clamp(70px, 8vh, 100px);
      width: auto;
      object-fit: contain;
      display: block;
      image-rendering: -webkit-optimize-contrast;
      filter: drop-shadow(0 6px 16px rgba(217, 119, 6, 0.3));
    }"""
content = re.sub(old_emblem, new_emblem, content)

# 3. Reduce Tagline Font
old_tagline = r'\.hero-tagline \{[\s\S]*?font-size: clamp\(14px, 1\.1vw, 16px\);[\s\S]*?\}'
new_tagline = """.hero-tagline {
      font-size: clamp(12px, 0.95vw, 14px);
      font-weight: 700;
      color: var(--deep-forest);
      margin-bottom: 16px;
      line-height: 1.4;
      text-align: left;
    }"""
content = re.sub(old_tagline, new_tagline, content)

# 4. Reduce Search Element font/size
old_search_input = 'style="flex: 1; border: none; background: none; outline: none; font-size: 16px; color: var(--deep-forest); font-family: inherit;"'
new_search_input = 'style="flex: 1; border: none; background: none; outline: none; font-size: 13px; color: var(--deep-forest); font-family: inherit;"'
content = content.replace(old_search_input, new_search_input)

# Also let's ensure padding of the search bar is slightly smaller to give more space
old_search_form = 'style="width: 100%; height: 56px; display: flex; align-items: center; background: #FFFFFF; border: 1px solid var(--border-color); border-radius: 100px; padding: 0 8px 0 24px; box-shadow: var(--shadow-soft); transition: var(--transition);"'
new_search_form = 'style="width: 100%; height: 50px; display: flex; align-items: center; background: #FFFFFF; border: 1px solid var(--border-color); border-radius: 100px; padding: 0 6px 0 16px; box-shadow: var(--shadow-soft); transition: var(--transition);"'
content = content.replace(old_search_form, new_search_form)

# And reduce button size slightly
old_search_btn = 'style="padding: 10px 32px; border-radius: 100px; border: none; background: var(--vibrant-green); color: #FFF; font-weight: 700; font-size: 15px; cursor: pointer; transition: background 0.2s ease;"'
new_search_btn = 'style="padding: 8px 24px; border-radius: 100px; border: none; background: var(--vibrant-green); color: #FFF; font-weight: 700; font-size: 13px; cursor: pointer; transition: background 0.2s ease;"'
content = content.replace(old_search_btn, new_search_btn)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
