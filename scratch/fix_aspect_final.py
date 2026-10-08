import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Grid alignment and add Tagline HTML/CSS
# First we must change the grid to repeat(3, 1fr)
old_grid = """    .hero-main-grid {
      --hero-panel-h: clamp(320px, calc(100vh - 450px), 540px);
      display: grid;
      grid-template-columns: 0.9fr 1.6fr 1fr;
      gap: clamp(24px, 3vw, 48px);
      width: 100%;
      min-height: 0;
      flex: 1 1 auto;
      align-items: center;
    }"""
new_grid = """    .hero-main-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      width: 100%;
      align-items: center;
    }"""
content = content.replace(old_grid, new_grid)

# 2. Fix Carousel Aspect Ratio to 4/3 so it's landscape and not huge
old_carousel = """    .hero-carousel-container {
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
    }"""
new_carousel = """    .hero-carousel-container {
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(11, 36, 23, 0.1);
      background: #0B2417;
      width: 100%;
      height: auto;
      aspect-ratio: 4 / 3;
      position: relative;
      border: 1px solid rgba(11, 36, 23, 0.1);
    }
    .hero-carousel-container .carousel-slide img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }"""
content = content.replace(old_carousel, new_carousel)

# 3. Fix Events Card to also be 4/3 aspect ratio
old_events = """    .hero-events-card {
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
    }"""
new_events = """    .hero-events-card {
      background: #FFFFFF;
      border: 1.5px solid rgba(11, 36, 23, 0.09);
      border-radius: 20px;
      padding: 16px 18px 8px 20px;
      box-shadow: 0 10px 30px rgba(11, 36, 23, 0.06);
      display: flex;
      flex-direction: column;
      width: 100%;
      height: auto;
      aspect-ratio: 4 / 3;
      box-sizing: border-box;
      position: relative;
      overflow: hidden;
    }"""
content = content.replace(old_events, new_events)

# 4. Add Tagline CSS
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
content = content.replace('    .hero-main-subtitle {', tagline_css + '    .hero-main-subtitle {')

# 5. Add Tagline HTML (and keep nowrap!)
old_title_html = '<h1 class="hero-main-title"><span style="white-space: nowrap;">Fifty decades of Excellence in plant</span><br>Protection.</h1>'
new_title_html = '<h1 class="hero-main-title"><span style="white-space: nowrap;">Fifty decades of Excellence in plant</span><br>Protection.</h1>\n            <h4 class="hero-tagline">Advancing Science, Safeguarding Crops, Sustaining Agriculture</h4>'
content = content.replace(old_title_html, new_title_html)

# 6. Reduce title font slightly to fit the narrower column
old_title_css = """    .hero-main-title {
      font-size: clamp(20px, 1.9vw, 29px);
      font-weight: 800;
      color: var(--deep-forest);
      line-height: 1.15;
      letter-spacing: -0.03em;
      margin-bottom: 12px;
      text-align: left;
    }"""
new_title_css = """    .hero-main-title {
      font-size: clamp(16px, 1.4vw, 22px);
      font-weight: 800;
      color: var(--deep-forest);
      line-height: 1.15;
      letter-spacing: -0.03em;
      margin-bottom: 8px;
      text-align: left;
    }"""
content = content.replace(old_title_css, new_title_css)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
