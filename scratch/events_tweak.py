import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Reduce font size of event title even more
old_event_title = r'\.event-title \{[\s\S]*?font-size: clamp\(13px, 0\.95vw, 15px\);[\s\S]*?\}'
new_event_title = """.event-title {
      font-size: clamp(12px, 0.85vw, 14px);
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
content = re.sub(old_event_title, new_event_title, content)

# Restore/increase box size of event items (padding)
old_event_item = r'\.event-item \{[\s\S]*?padding: 6px 8px;[\s\S]*?\}'
new_event_item = """.event-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 14px 12px;
      border-bottom: 1px solid #EDF1EF;
      text-decoration: none;
      transition: background 0.15s ease;
      cursor: pointer;
      background: #FFFFFF;
      width: 100%;
      box-sizing: border-box;
      border-radius: 6px;
    }"""
content = re.sub(old_event_item, new_event_item, content)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
