import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the entire hero-header-row
start_hdr = content.find('<div class="hero-header-row">')
end_hdr = content.find('<!-- Main 2-Column Grid', start_hdr)
content = content[:start_hdr] + content[end_hdr:]

# 2. Re-insert the middle column text inside the hero-main-grid
right_col_marker = '<!-- Right Column: Matching Upcoming Events Card (Exact Photo Layout) -->'
middle_col_html = """
          <!-- Middle Column: Title & Text (No Card Background, Left Aligned) -->
          <div class="hero-middle-content">
            <div class="hero-jubilee-wrapper">
              <img src="{% static 'images/golden_jubilee_emblem.png' %}?v=20261008_2" alt="PPAI Golden Jubilee 1972 - 2022" class="hero-jubilee-emblem">
            </div>
            <h1 class="hero-main-title">Fifty decades of Excellence in plant<br>Protection.</h1>
            <p class="hero-main-subtitle">PPAI celebrated its landmark Golden Jubilee (1972&ndash;2022), commemorating fifty years of continuous contributions to Indian agricultural science. Over the decades, the Association has evolved into a multidisciplinary body encompassing Agricultural Entomology, Plant Pathology, Nematology, Weed Science, Plant Biosecurity, and Pesticide Chemistry.</p>
          </div>
"""
content = content.replace(right_col_marker, middle_col_html + "\n          " + right_col_marker)

# 3. Change "Upcoming Events" to "Key Events"
content = content.replace('<h2 class="events-card-title">Upcoming Events</h2>', '<h2 class="events-card-title">Key Events</h2>')

# 4. Change the Search Bar position
portal_start = content.find('<div class="f-pattern-grid">')
portal_end_sec = content.find('</section>', portal_start)
search_html = """
        <!-- Search Bar at the bottom right -->
        <div class="portal-search-container">
          <form class="hero-search" action="{% url 'search' %}" method="get">
            <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input type="text" name="q" placeholder="Search journals, members, awards..." required>
            <button type="submit" class="btn-search">Search</button>
          </form>
        </div>
"""
content = content[:portal_end_sec] + search_html + content[portal_end_sec:]

# 5. CSS Updates
css_updates = [
    # Main Grid to 3 Columns
    (r'\.hero-main-grid \{[\s\S]*?flex: 1 1 auto;\s*\}', """.hero-main-grid {
      --hero-panel-h: clamp(320px, calc(100vh - 450px), 540px);
      display: grid;
      grid-template-columns: 1fr 1.3fr 1.1fr;
      gap: clamp(24px, 3vw, 48px);
      width: 100%;
      min-height: 0;
      flex: 1 1 auto;
      align-items: center;
    }"""),
    
    (r'/\* --- Left-Aligned 2-Column', """.hero-middle-content {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      justify-content: center;
      text-align: left;
    }
    
    /* --- Left-Aligned 2-Column"""),

    # Title Styling
    (r'\.hero-main-title \{[\s\S]*?margin-bottom: 3px;\s*\}', """.hero-main-title {
      font-size: clamp(24px, 2.2vw, 34px);
      font-weight: 800;
      color: var(--deep-forest);
      line-height: 1.15;
      letter-spacing: -0.03em;
      margin-bottom: 12px;
      text-align: left;
    }"""),
    
    # Subtitle Styling
    (r'\.hero-main-subtitle \{[\s\S]*?text-justify: inter-word;\s*\}', """.hero-main-subtitle {
      font-size: clamp(13px, 0.9vw, 15px);
      color: var(--text-muted);
      line-height: 1.6;
      max-width: 100%;
      text-align: left;
    }"""),

    # Jubilee emblem wrapper
    (r'\.hero-jubilee-wrapper \{[\s\S]*?margin-bottom: 2px;\s*\}', """.hero-jubilee-wrapper {
      display: inline-flex;
      align-items: flex-start;
      margin-bottom: 16px;
    }"""),

    # Remove right column fixed widths so it fits the grid
    (r'\.hero-events-card \{[\s\S]*?max-width: 820px;[\s\S]*?\}', """.hero-events-card {
      background: #FFFFFF;
      border: 1.5px solid rgba(11, 36, 23, 0.09);
      border-radius: 20px;
      padding: 16px 18px 8px 20px;
      box-shadow: 0 10px 30px rgba(11, 36, 23, 0.06);
      display: flex;
      flex-direction: column;
      height: var(--hero-panel-h);
      width: 100%;
      box-sizing: border-box;
      position: relative;
      overflow: hidden;
    }"""),

    # Event Title Font size reduction
    (r'\.event-title \{[\s\S]*?font-size: clamp\(16\.5px, 1\.15vw, 19px\);[\s\S]*?\}', """.event-title {
      font-size: clamp(13px, 0.95vw, 15px);
      font-weight: 700;
      color: var(--deep-forest);
      line-height: 1.35;
      margin-top: 2px;
      transition: color 0.2s ease;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }"""),

    # Event Item padding reduction
    (r'\.event-item \{[\s\S]*?padding: 6px 6px;[\s\S]*?\}', """.event-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 6px 8px;
      border-bottom: 1px solid #EDF1EF;
      text-decoration: none;
      transition: background 0.15s ease;
      cursor: pointer;
      background: #FFFFFF;
      width: 100%;
      box-sizing: border-box;
      border-radius: 6px;
    }""")
]

for pattern, repl in css_updates:
    content = re.sub(pattern, repl, content)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
