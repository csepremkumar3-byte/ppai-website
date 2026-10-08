import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('<section class="hero">')
end_idx = content.find('</section>', start_idx) + len('</section>')

new_hero = """<section class="hero">
  <div class="container hero-container">
    <!-- Main 3-Column Grid -->
    <div class="hero-main-grid">

      <!-- Left Column: Carousel Card -->
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
              <div class="carousel-slide" data-title="Indian Journal of Plant Protection &ndash; Vol 54 (1)">
                <img src="{% static 'images/journal_cover.png' %}" alt="Indian Journal of Plant Protection Cover Vol 54 No 1">
              </div>
              <div class="carousel-slide" data-title="PPAI Golden Jubilee &ndash; Celebrating 50 Years">
                <img src="{% static 'images/golden_jubilee_banner.png' %}" alt="PPAI Golden Jubilee 1972 - 2022 Celebrating 50 Years">
              </div>
              <div class="carousel-slide" data-title="Agricultural Entomology &amp; Pest Surveillance">
                <img src="{% static 'images/slide1.jpg' %}" alt="Agricultural Entomology & Pest Surveillance">
              </div>
              <div class="carousel-slide" data-title="Biological Control &amp; Natural Predators">
                <img src="{% static 'images/slide2.jpg' %}" alt="Biological Control & Natural Predators">
              </div>
              <div class="carousel-slide" data-title="Plant Pathology &amp; Disease Diagnostics">
                <img src="{% static 'images/slide3.jpg' %}" alt="Plant Pathology & Disease Diagnostics">
              </div>
              <div class="carousel-slide" data-title="Sustainable Crop Protection &amp; Biosecurity">
                <img src="{% static 'images/slide4.jpg' %}" alt="Sustainable Crop Protection & Biosecurity">
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
                <span class="dot" data-slide="2"></span>
                <span class="dot" data-slide="3"></span>
                <span class="dot" data-slide="4"></span>
                <span class="dot" data-slide="5"></span>
              {% endif %}
            </div>
          </div>
        </div>
      </div>

      <!-- Center Column: Logo & Text -->
      <div class="hero-middle-card">
        <div class="hero-jubilee-wrapper">
          <img src="{% static 'images/golden_jubilee_emblem.png' %}?v=20261008_2" alt="PPAI Golden Jubilee 1972 - 2022" class="hero-jubilee-emblem">
        </div>
        <h1 class="hero-main-title">Fifty decades of Excellence in plant Protection.</h1>
        <p class="hero-main-subtitle">PPAI celebrated its landmark Golden Jubilee (1972&ndash;2022), commemorating fifty years of continuous contributions to Indian agricultural science. Over the decades, the Association has evolved into a multidisciplinary body encompassing Agricultural Entomology, Plant Pathology, Nematology, Weed Science, Plant Biosecurity, and Pesticide Chemistry.</p>
      </div>

      <!-- Right Column: Events Card -->
      <div class="hero-events-card">
        <div class="events-card-header">
          <div class="events-header-title-group">
            <span class="events-live-pulse"></span>
            <h2 class="events-card-title">Key Events.</h2>
          </div>
          <a href="{% url 'conferences' %}" class="view-all-events-link">
            <span>Event &gt;</span>
          </a>
        </div>
        <div class="events-list" id="heroEventsList">
          {% for ev in events %}
            <a href="{% if ev.doc_file %}{% static ev.doc_file %}{% else %}#{% endif %}" class="event-item" target="_blank" rel="noopener noreferrer" onclick="handleEventDocClick(event, '{{ ev.title|escapejs }}', '{% if ev.doc_file %}{% static ev.doc_file %}{% endif %}')">
              <div class="event-date-badge">
                <span class="event-day">{{ ev.day }}</span>
                <span class="event-month">{{ ev.month }}</span>
              </div>
              <div class="event-info">
                <div class="event-tags-row">
                  <span class="event-category-badge">{{ ev.category }}</span>
                  <span class="event-year-tag">{{ ev.year }}</span>
                </div>
                <div class="event-title">{{ ev.title }}</div>
              </div>
              <svg class="event-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </a>
          {% empty %}
            <div class="event-item">
              <div class="event-date-badge">
                <span class="event-day">15</span>
                <span class="event-month">NOV</span>
              </div>
              <div class="event-info">
                <div class="event-tags-row">
                  <span class="event-category-badge">International Conference</span>
                  <span class="event-year-tag">2023</span>
                </div>
                <div class="event-title">ICPHM 2023 International Conference on Plant Health Management</div>
              </div>
              <svg class="event-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </div>
          {% endfor %}
        </div>
      </div>

    </div>
  </div>
</section>"""

content = content[:start_idx] + new_hero + content[end_idx:]

# Move search bar to bottom
portal_start = content.find('<div class="f-pattern-grid">')
p_sec = content.find('</section>', portal_start)
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
content = content[:p_sec] + search_html + content[p_sec:]

css_updates = [
    (r'\.hero-main-grid \{[\s\S]*?flex: 1 1 auto;\s*\}', """.hero-main-grid {
      --hero-panel-h: clamp(280px, calc(100vh - 580px), 480px);
      display: grid;
      grid-template-columns: minmax(auto, 1fr) minmax(auto, 1.4fr) minmax(auto, 1.2fr);
      gap: clamp(16px, 1.8vw, 24px);
      width: 100%;
      min-height: 0;
      flex: 1 1 auto;
    }
    .hero-middle-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 0 20px;
    }"""),
    
    (r'\.hero-header-right \{[\s\S]*?padding-top: 2px;\s*\}', ""),
    (r'\.hero-quick-pills \{[\s\S]*?justify-content: flex-end;\s*\}', ""),
    (r'\.quick-pill \{[\s\S]*?text-decoration: none;\s*\}', ""),
    (r'\.quick-pill:hover \{[\s\S]*?box-shadow: 0 4px 12px rgba\(0, 178, 114, 0\.25\);\s*\}', ""),

    (r'\.hero-carousel-container \{[\s\S]*?flex-shrink: 0;\s*\}', """.hero-carousel-container {
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(11, 36, 23, 0.1);
      background: #0B2417;
      height: var(--hero-panel-h);
      aspect-ratio: 1 / 1;
      width: auto;
      position: relative;
      border: 1px solid rgba(11, 36, 23, 0.1);
      flex-shrink: 0;
      margin-left: auto;
    }"""),
    
    (r'\.hero-events-card \{[\s\S]*?overflow: hidden;\s*\}', """.hero-events-card {
      background: #FFFFFF;
      border: 1.5px solid rgba(11, 36, 23, 0.09);
      border-radius: 20px;
      padding: 16px 18px 8px 20px;
      box-shadow: 0 10px 30px rgba(11, 36, 23, 0.06);
      display: flex;
      flex-direction: column;
      height: var(--hero-panel-h);
      flex: 1 1 auto;
      min-width: 0;
      box-sizing: border-box;
      position: relative;
      overflow: hidden;
    }"""),

    (r'\.event-title \{[\s\S]*?transition: color 0\.2s ease;\s*\}', """.event-title {
      font-size: clamp(14px, 1vw, 16px);
      font-weight: 700;
      color: var(--deep-forest);
      line-height: 1.35;
      margin-top: 2px;
      transition: color 0.2s ease;
    }"""),

    (r'\.portal-section \{[\s\S]*?margin-bottom: clamp\(60px, 8vh, 100px\);\s*\}', """.portal-section {
      position: relative;
      z-index: 10;
      margin-top: clamp(40px, 6vh, 60px);
      margin-bottom: clamp(60px, 8vh, 100px);
    }
    .portal-search-container {
      display: flex;
      justify-content: flex-end;
      margin-top: 32px;
    }
    .portal-search-container .hero-search {
      max-width: 450px;
      min-height: 48px;
    }
    .portal-search-container .btn-search {
      padding: 10px 24px;
      font-size: 14px;
    }""")
]

for pattern, repl in css_updates:
    content = re.sub(pattern, repl, content)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
