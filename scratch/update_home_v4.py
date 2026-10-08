import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Reduce Event Title Font Size
css_event_title = r'\.event-title \{[\s\S]*?font-size: clamp\(16\.5px, 1\.15vw, 19px\);[\s\S]*?\}'
replacement_event_title = """.event-title {
      font-size: clamp(12.5px, 0.85vw, 14.5px);
      font-weight: 700;
      color: var(--deep-forest);
      line-height: 1.35;
      margin-top: 2px;
      transition: color 0.2s ease;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }"""
content = re.sub(css_event_title, replacement_event_title, content)

# Reduce Event Item padding
css_event_item = r'\.event-item \{[\s\S]*?padding: 6px 6px;[\s\S]*?\}'
replacement_event_item = """.event-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 4px 6px;
      border-bottom: 1px solid #EDF1EF;
      text-decoration: none;
      transition: background 0.15s ease;
      cursor: pointer;
      background: #FFFFFF;
      width: 100%;
      box-sizing: border-box;
      border-radius: 6px;
    }"""
content = re.sub(css_event_item, replacement_event_item, content)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
