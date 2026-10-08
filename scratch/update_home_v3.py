import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Title Line Break
content = content.replace(
    '<h1 class="hero-main-title">Fifty decades of Excellence in plant Protection.</h1>',
    '<h1 class="hero-main-title">Fifty decades of Excellence in plant<br>Protection.</h1>'
)

# 2. Update Carousel Aspect Ratio
css_carousel = r'\.hero-carousel-container \{[\s\S]*?aspect-ratio: 1 / 1;[\s\S]*?\}'
replacement_carousel = """.hero-carousel-container {
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(11, 36, 23, 0.1);
      background: #0B2417;
      height: var(--hero-panel-h);
      aspect-ratio: 3 / 4;
      width: auto;
      position: relative;
      border: 1px solid rgba(11, 36, 23, 0.1);
      flex-shrink: 0;
      margin-left: auto;
    }"""
content = re.sub(css_carousel, replacement_carousel, content)

# 3. Reduce Title Font Size slightly
css_title = r'\.hero-main-title \{[\s\S]*?font-size: clamp\(28px, 2\.7vw, 40px\);[\s\S]*?\}'
replacement_title = """.hero-main-title {
      font-size: clamp(20px, 1.8vw, 28px);
      font-weight: 800;
      color: var(--deep-forest);
      line-height: 1.15;
      letter-spacing: -0.03em;
      margin-bottom: 3px;
    }"""
content = re.sub(css_title, replacement_title, content)

# Also fix the subtitle slightly so it looks neat
css_subtitle = r'\.hero-main-subtitle \{[\s\S]*?font-size: clamp\(14px, 1vw, 16\.5px\);[\s\S]*?\}'
replacement_subtitle = """.hero-main-subtitle {
      font-size: clamp(12.5px, 0.85vw, 14.5px);
      color: var(--text-muted);
      line-height: 1.6;
      max-width: 960px;
      text-align: justify;
      text-justify: inter-word;
    }"""
content = re.sub(css_subtitle, replacement_subtitle, content)

# 4. Reduce Event Title Font Size slightly (to allow 4-5 events comfortably)
css_event_title = r'\.event-title \{[\s\S]*?font-size: clamp\(14px, 1vw, 16px\);[\s\S]*?\}'
replacement_event_title = """.event-title {
      font-size: clamp(12.5px, 0.85vw, 14.5px);
      font-weight: 700;
      color: var(--deep-forest);
      line-height: 1.35;
      margin-top: 2px;
      transition: color 0.2s ease;
    }"""
content = re.sub(css_event_title, replacement_event_title, content)

# 5. Move Search to the right of Awards & Honors
search_html = """
        <!-- Search Bar at the bottom right -->
        <div class="portal-search-container">
          <form class="hero-search" action="{% url 'search' %}" method="get">
            <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input type="text" name="q" placeholder="Search journals, members, awards..." required>
            <button type="submit" class="btn-search">Search</button>
          </form>
        </div>"""

# Remove from current location
content = content.replace(search_html, "")

# Remove the CSS for portal-search-container
css_search = r'\.portal-search-container \{[\s\S]*?font-size: 14px;\s*\}'
content = re.sub(css_search, "", content)

# Add after Awards card inside f-pattern-grid
awards_end_idx = content.find('</a>', content.find('Awards &amp; Honors')) + len('</a>')

new_search_html = """
          <!-- Search Bar at the bottom right (inside grid) -->
          <div class="portal-search-container" style="grid-column: 2 / -1; display: flex; align-items: center; justify-content: flex-end;">
            <form class="hero-search" action="{% url 'search' %}" method="get" style="width: 100%; max-width: 500px; display: flex; align-items: center; background: #FFFFFF; border: 2px solid rgba(11, 36, 23, 0.16); border-radius: 100px; padding: 7px 9px 7px 26px; box-shadow: 0 8px 28px rgba(11, 36, 23, 0.09);">
              <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="color: var(--text-muted); margin-right: 14px;"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              <input type="text" name="q" placeholder="Search journals, members, awards..." required style="flex: 1; border: none; background: none; outline: none; font-size: 15px; font-weight: 500; min-width: 0; min-height: 48px;">
              <button type="submit" class="btn-search" style="padding: 10px 24px; border-radius: 100px; border: none; background: var(--vibrant-green); color: #FFF; font-weight: 800; font-size: 14px; cursor: pointer;">Search</button>
            </form>
          </div>
"""
content = content[:awards_end_idx] + "\n" + new_search_html + content[awards_end_idx:]

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
