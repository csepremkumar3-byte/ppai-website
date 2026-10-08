import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Grid
old_grid = r'\.hero-main-grid \{[\s\S]*?align-items: center;\s*\}'
new_grid = """.hero-main-grid {
      --hero-panel-h: clamp(320px, calc(100vh - 450px), 540px);
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      width: 100%;
      min-height: 0;
      flex: 1 1 auto;
      align-items: stretch;
    }"""
content = re.sub(old_grid, new_grid, content)

# 2. Carousel
old_carousel = r'\.hero-carousel-container \{[\s\S]*?flex-shrink: 0;\s*\}'
new_carousel = """.hero-carousel-container {
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(11, 36, 23, 0.1);
      background: #0B2417;
      width: 100%;
      height: auto;
      aspect-ratio: 3 / 4;
      position: relative;
      border: 1px solid rgba(11, 36, 23, 0.1);
    }
    .hero-carousel-container .carousel-slide img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }"""
content = re.sub(old_carousel, new_carousel, content)

# 3. Events Card
old_events = r'\.hero-events-card \{[\s\S]*?height: var\(--hero-panel-h\);[\s\S]*?\}'
new_events = """.hero-events-card {
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
content = re.sub(old_events, new_events, content)

# 4. Title CSS
old_title_css = r'\.hero-main-title \{[\s\S]*?font-size: clamp\(18px, 1\.7vw, 26px\);[\s\S]*?\}'
new_title_css = """.hero-main-title {
      font-size: clamp(15px, 1.4vw, 21px);
      font-weight: 800;
      color: var(--deep-forest);
      line-height: 1.15;
      letter-spacing: -0.03em;
      margin-bottom: 6px;
      text-align: left;
    }"""
content = re.sub(old_title_css, new_title_css, content)

# 5. Tagline CSS
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
content = content.replace('.hero-main-subtitle {', tagline_css + '    .hero-main-subtitle {')

# 6. Tagline HTML (ensuring white-space: nowrap stays on the title)
old_html = '<h1 class="hero-main-title"><span style="white-space: nowrap;">Fifty decades of Excellence in plant</span><br>Protection.</h1>'
new_html = '<h1 class="hero-main-title"><span style="white-space: nowrap;">Fifty decades of Excellence in plant</span><br>Protection.</h1>\n            <h4 class="hero-tagline">Advancing Science, Safeguarding Crops, Sustaining Agriculture</h4>'
content = content.replace(old_html, new_html)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
