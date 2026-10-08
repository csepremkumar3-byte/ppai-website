import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Change "Five Decades" back to "Fifty decades", and "Plant" to "plant"
content = content.replace(
    '<h1 class="hero-main-title">Five Decades of Excellence in Plant<br>Protection.</h1>',
    '<h1 class="hero-main-title">Fifty decades of Excellence in plant<br>Protection.</h1>'
)

# 2. Fix the Search Bar size
# We want it to be a thin pill, vertically centered or top-aligned next to Card 4, NOT stretching to card height.
old_search_container = '<div class="portal-search-container" style="grid-column: 2 / -1; display: flex; align-items: stretch; justify-content: flex-start; height: 100%;">'
new_search_container = '<div class="portal-search-container" style="grid-column: 2 / -1; display: flex; align-items: flex-start; justify-content: flex-start;">'

old_form = 'style="width: 100%; display: flex; align-items: center; background: #FFFFFF; border: 1px solid var(--border-color); border-radius: 18px; padding: 10px 16px 10px 30px; box-shadow: var(--shadow-soft); transition: var(--transition); margin-top: 0;"'
new_form = 'style="width: 100%; height: 56px; display: flex; align-items: center; background: #FFFFFF; border: 1px solid var(--border-color); border-radius: 100px; padding: 0 8px 0 24px; box-shadow: var(--shadow-soft); transition: var(--transition);"'

content = content.replace(old_search_container, new_search_container)
content = content.replace(old_form, new_form)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
