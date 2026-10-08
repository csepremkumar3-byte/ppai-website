import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the entire <section class="hero"> to its closing tag with a new structure
# First find the boundary of hero section
start_idx = content.find('<section class="hero">')
end_idx = content.find('</section>', start_idx) + len('</section>')

new_hero = """<section class="hero">
  <div class="container hero-container">
    <!-- Main 3-Column Grid -->
    <div class="hero-main-grid">

      <!-- Left Column: Carousel (Square) -->
      <div class="hero-carousel-card">
        <div class="hero-carousel-container" id="heroCarousel">
          <div class="carousel-track" id="carouselTrack">
            {% if slides %}
              {% for slide in slides %}
                <div class="carousel-slide" data-title="{{ slide.title|default:'Plant Protection Research' }}">
                  <img src="{{ slide.image.url }}" alt="{{ slide.title|default:"Indian Journal Cover" }}">
                </div>
              {% endfor %}
            {% else %}
              <div class="carousel-slide" data-title="Indian Journal of Plant Protection  Vol 54 (1)">
                <img src="{% static 'images/journal_cover.png' %}" alt="Indian Journal of Plant Protection Cover Vol 54 No 1">
              </div>
              <div class="carousel-slide" data-title="PPAI Golden Jubilee  Celebrating 50 Years">
                <img src="{% static 'images/golden_jubilee_banner.png' %}" alt="PPAI Golden Jubilee 1972 - 2022 Celebrating 50 Years">
              </div>
            {% endif %}
          </div>
          <div class="carousel-overlay-bar">
            <div class="carousel-dots" id="carouselDots">
              {% if slides %}
                {% for slide in slides %}
                  <span class="dot {% if forloop.first %}active{% endif %}" data-slide="{{ forloop.counter0 }}"></span>
                {% endfor %}
              {% else %}
                <span class="dot active" data-slide="0"></span>
                <span class="dot" data-slide="1"></span>
              {% endif %}
            </div>
          </div>
        </div>
      </div>

      <!-- Middle Column: Logo & Text -->
      <div class="hero-middle-card">
        <div class="hero-jubilee-wrapper">
          <img src="{% static 'images/golden_jubilee_emblem.png' %}?v=20261008_2" alt="PPAI Golden Jubilee 1972 - 2022" class="hero-jubilee-emblem">
        </div>
        <h1 class="hero-main-title">Fifty decades of Excellence in plant Protection.</h1>
        <hr class="hero-divider">
        <hr class="hero-divider">
        <hr class="hero-divider">
        <hr class="hero-divider">
      </div>

      <!-- Right Column: Events Card -->
      <div class="hero-events-card">
        <div class="events-card-header">
          <div class="events-header-title-group">
            <h2 class="events-card-title">Key Events.</h2>
          </div>
          <a href="{% url 'conferences' %}" class="view-all-events-link">
            <span>Event &gt;</span>
          </a>
        </div>
        <div class="events-list" id="heroEventsList">
          {% for ev in events %}
            <a href="{% if ev.doc_file %}{% static ev.doc_file %}{% else %}#{% endif %}" class="event-item" target="_blank" rel="noopener noreferrer">
              <div class="event-date-badge">
                <span class="event-day">{{ ev.date_from|date:"d" }}</span>
              </div>
              <div class="event-info">
                <span class="event-title">{{ ev.title }}</span>
              </div>
            </a>
          {% empty %}
            <!-- Fallback Static Events -->
            <a href="#" class="event-item">
              <div class="event-date-badge"><span class="event-day">19</span></div>
              <div class="event-info"><span class="event-title">Plant Protection Workshop</span></div>
            </a>
            <a href="#" class="event-item">
              <div class="event-date-badge"><span class="event-day">12</span></div>
              <div class="event-info"><span class="event-title">Annual General Meeting</span></div>
            </a>
            <a href="#" class="event-item">
              <div class="event-date-badge"><span class="event-day">05</span></div>
              <div class="event-info"><span class="event-title">Golden Jubilee Celebration</span></div>
            </a>
          {% endfor %}
        </div>
      </div>

    </div>
  </div>
</section>"""

content = content[:start_idx] + new_hero + content[end_idx:]

# 2. Add search bar below portal-section grid
portal_start = content.find('<div class="f-pattern-grid">')
portal_end = content.find('</div>', content.find('</div>', content.find('</div>', content.find('</div>', portal_start)+1)+1)+1)+1

search_html = """
        <!-- Search Bar at the bottom right -->
        <div class="portal-search-container">
          <form class="hero-search" action="{% url 'search' %}" method="get">
            <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input type="text" name="q" placeholder="Search..." required>
          </form>
        </div>
"""

# Actually, I'll just find </section> for portal-section and add it before it.
p_sec = content.find('</section>', portal_start)
content = content[:p_sec] + search_html + content[p_sec:]

# 3. Update CSS
css_updates = {
    r'\.hero-main-title \{.*?\s*margin-bottom: 3px;\s*\}': """.hero-main-title { font-size: clamp(16px, 1.5vw, 22px); font-weight: 700; color: var(--deep-forest); line-height: 1.2; text-align: center; margin-bottom: 8px; }
    .hero-divider { border: 0; border-top: 1px solid rgba(11, 36, 23, 0.2); width: 80%; margin: 6px auto; }""",
    r'\.hero-main-grid \{.*?\s*flex: 1 1 auto;\s*\}': """.hero-main-grid { --hero-panel-h: clamp(220px, calc(100vh - 650px), 320px); display: grid; grid-template-columns: minmax(auto, 1fr) minmax(auto, 1.2fr) minmax(auto, 1.2fr); gap: clamp(12px, 1.5vw, 20px); width: 100%; min-height: 0; flex: 1 1 auto; }
    .hero-middle-card { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 10px; }""",
    r'\.hero-carousel-container \{.*?\s*flex-shrink: 0;\s*\}': """.hero-carousel-container { border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(11, 36, 23, 0.1); background: #0B2417; height: var(--hero-panel-h); aspect-ratio: 1 / 1; width: auto; position: relative; border: 1px solid rgba(11, 36, 23, 0.1); flex-shrink: 0; margin-left: auto; }""",
    r'\.hero-events-card \{.*?\s*overflow: hidden;\s*\}': """.hero-events-card { background: #FFFFFF; border: 1.5px solid rgba(11, 36, 23, 0.09); border-radius: 12px; padding: 12px 14px 6px 14px; box-shadow: 0 4px 12px rgba(11, 36, 23, 0.06); display: flex; flex-direction: column; height: var(--hero-panel-h); box-sizing: border-box; position: relative; overflow: hidden; }""",
    r'\.events-card-title \{.*?\}': """.events-card-title { font-size: clamp(16px, 1.2vw, 18px); font-weight: 700; color: var(--deep-forest); }""",
    r'\.view-all-events-link \{.*?\}': """.view-all-events-link { font-size: 13px; font-weight: 700; color: var(--vibrant-green); text-decoration: none; }""",
    r'\.event-item \{.*?border-radius: 8px;\s*\}': """.event-item { display: flex; align-items: center; gap: 12px; padding: 6px; border-bottom: 1px solid #EDF1EF; text-decoration: none; transition: background 0.15s ease; cursor: pointer; background: #FFFFFF; width: 100%; box-sizing: border-box; border-radius: 6px; }""",
    r'\.event-date-badge \{.*?box-shadow.*?\}': """.event-date-badge { width: 28px; height: 28px; background: transparent; border: 1px solid var(--deep-forest); border-radius: 4px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: var(--deep-forest); font-weight: 700; font-size: 14px; }""",
    r'\.event-title \{.*?\}': """.event-title { font-size: 14px; font-weight: 600; color: var(--deep-forest); }""",
    r'\.hero-jubilee-emblem \{.*?filter:.*?\}': """.hero-jubilee-emblem { height: clamp(40px, 5vh, 60px); width: auto; object-fit: contain; display: block; margin-bottom: 10px; }""",
    r'\.portal-section \{.*?\}': """.portal-section { position: relative; z-index: 10; margin-top: clamp(24px, 3vh, 32px); margin-bottom: clamp(24px, 3vh, 32px); }
    .portal-search-container { display: flex; justify-content: flex-end; margin-top: 20px; }
    .portal-search-container .hero-search { max-width: 300px; border-radius: 100px; padding: 5px 15px; border: 1px solid var(--deep-forest); box-shadow: none; min-height: 36px; }
    .portal-search-container .hero-search input { font-size: 14px; padding: 4px 8px; }""",
}

for pattern, repl in css_updates.items():
    content = re.sub(pattern, repl, content, flags=re.DOTALL)


with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)

