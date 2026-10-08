import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix the typo: Fifty decades -> Five Decades, plant -> Plant
content = content.replace(
    '<h1 class="hero-main-title">Fifty decades of Excellence in plant<br>Protection.</h1>',
    '<h1 class="hero-main-title">Five Decades of Excellence in Plant<br>Protection.</h1>'
)

# 2. Move Search Bar inside the f-pattern-grid
# Currently the search bar is at the bottom, just before </section> of portal-section.
search_html = """
        <!-- Search Bar at the bottom right -->
        <div class="portal-search-container">
          <form class="hero-search" action="{% url 'search' %}" method="get">
            <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input type="text" name="q" placeholder="Search journals, members, awards..." required>
            <button type="submit" class="btn-search">Search</button>
          </form>
        </div>"""
content = content.replace(search_html, "")

# The new search bar inside the grid should span the remaining 2 columns on the second row
awards_card_end = content.find('</a>', content.find('Awards &amp; Honors')) + len('</a>')

new_search_html = """
          <!-- Search Bar Spanning the rest of row 2 -->
          <div class="portal-search-container" style="grid-column: 2 / -1; display: flex; align-items: stretch; justify-content: flex-start; height: 100%;">
            <form class="hero-search" action="{% url 'search' %}" method="get" style="width: 100%; display: flex; align-items: center; background: #FFFFFF; border: 1px solid var(--border-color); border-radius: 18px; padding: 10px 16px 10px 30px; box-shadow: var(--shadow-soft); transition: var(--transition); margin-top: 0;">
              <svg class="search-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color: var(--text-muted); margin-right: 18px;"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              <input type="text" name="q" placeholder="Search journals, members, awards..." required style="flex: 1; border: none; background: none; outline: none; font-size: 16px; color: var(--deep-forest); font-family: inherit;">
              <button type="submit" class="btn-search" style="padding: 12px 32px; border-radius: 12px; border: none; background: var(--vibrant-green); color: #FFF; font-weight: 700; font-size: 15px; cursor: pointer; transition: background 0.2s ease;">Search</button>
            </form>
          </div>
"""
content = content[:awards_card_end] + "\n" + new_search_html + content[awards_card_end:]

# Update CSS for search container margin
content = content.replace("margin-top: 24px;", "margin-top: 0;")

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
