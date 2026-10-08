import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('padding: 12px 32px; border-radius: 12px; border: none;', 'padding: 10px 32px; border-radius: 100px; border: none;')

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
