import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Align hero-main-grid exactly with f-pattern-grid
old_hero_grid = r'\.hero-main-grid \{[\s\S]*?align-items: center;\s*\}'
new_hero_grid = """.hero-main-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      width: 100%;
      min-height: 0;
      flex: 1 1 auto;
      align-items: stretch;
    }"""
content = re.sub(old_hero_grid, new_hero_grid, content)

# 2. Adjust Carousel to fill width and determine height
old_carousel = r'\.hero-carousel-container \{[\s\S]*?margin: 0 auto;\s*\}'
new_carousel = """.hero-carousel-container {
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(11, 36, 23, 0.1);
      background: #0B2417;
      width: 100%;
      height: 100%;
      min-height: 350px;
      position: relative;
      border: 1px solid rgba(11, 36, 23, 0.1);
    }
    .hero-carousel-container .carousel-slide img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }"""
content = re.sub(old_carousel, new_carousel, content)

# Remove the hardcoded aspect-ratio if necessary, or just rely on height:100% and object-fit: cover.
# Wait, if height is 100%, it will match the tallest column (Events or Text).
# This perfectly aligns start and end vertically!

# 3. Adjust Events Card to stretch
old_events_card = r'\.hero-events-card \{[\s\S]*?height: var\(--hero-panel-h\);[\s\S]*?\}'
new_events_card = """.hero-events-card {
      background: #FFFFFF;
      border: 1.5px solid rgba(11, 36, 23, 0.09);
      border-radius: 20px;
      padding: 16px 18px 8px 20px;
      box-shadow: 0 10px 30px rgba(11, 36, 23, 0.06);
      display: flex;
      flex-direction: column;
      height: 100%;
      width: 100%;
      box-sizing: border-box;
      position: relative;
      overflow: hidden;
    }"""
content = re.sub(old_events_card, new_events_card, content)

# 4. Add the Tagline CSS
tagline_css = """
    .hero-tagline {
      font-size: clamp(14px, 1.1vw, 16px);
      font-weight: 700;
      color: var(--deep-forest);
      margin-bottom: 16px;
      line-height: 1.4;
      text-align: left;
    }
"""
content = content.replace('.hero-main-subtitle {', tagline_css + '\n    .hero-main-subtitle {')

# 5. Add the Tagline HTML
old_title_html = '<h1 class="hero-main-title"><span style="white-space: nowrap;">Fifty decades of Excellence in plant</span><br>Protection.</h1>'
new_title_html = '<h1 class="hero-main-title"><span style="white-space: nowrap;">Fifty decades of Excellence in plant</span><br>Protection.</h1>\n            <h4 class="hero-tagline">Advancing Science, Safeguarding Crops, Sustaining Agriculture</h4>'
content = content.replace(old_title_html, new_title_html)

# Also fix the nowrap since 1fr might be narrow
new_title_css = r'\.hero-main-title \{[\s\S]*?font-size: clamp\(18px, 1\.7vw, 26px\);[\s\S]*?\}'
replacement_title_css = """.hero-main-title {
      font-size: clamp(18px, 1.7vw, 26px);
      font-weight: 800;
      color: var(--deep-forest);
      line-height: 1.15;
      letter-spacing: -0.03em;
      margin-bottom: 8px;
      text-align: left;
    }"""
content = re.sub(new_title_css, replacement_title_css, content)

# Let's remove white-space: nowrap just in case 1fr column is too narrow and overflows
content = content.replace('<span style="white-space: nowrap;">Fifty decades of Excellence in plant</span>', 'Fifty decades of Excellence in plant')

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
