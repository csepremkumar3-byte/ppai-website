import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the search container styles to center the form and make it ~55% wide
# to span roughly from the center of col 2 to the center of col 3.
old_container = '<div class="portal-search-container" style="grid-column: 2 / -1; display: flex; align-items: flex-start; justify-content: flex-start;">'
new_container = '<div class="portal-search-container" style="grid-column: 2 / -1; display: flex; align-items: flex-start; justify-content: center;">'

old_form = 'style="width: 100%; height: 56px; display: flex; align-items: center; background: #FFFFFF; border: 1px solid var(--border-color); border-radius: 100px; padding: 0 8px 0 24px; box-shadow: var(--shadow-soft); transition: var(--transition);"'
new_form = 'style="width: 55%; min-width: 320px; height: 56px; display: flex; align-items: center; background: #FFFFFF; border: 1px solid var(--border-color); border-radius: 100px; padding: 0 8px 0 24px; box-shadow: var(--shadow-soft); transition: var(--transition);"'

content = content.replace(old_container, new_container)
content = content.replace(old_form, new_form)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
