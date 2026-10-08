import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Reduce height of left and right, remove strict 3:4 aspect ratio, force a reasonable fixed height
old_carousel = r'\.hero-carousel-container \{[\s\S]*?aspect-ratio: 3 / 4;\s*position: relative;\s*border: 1px solid rgba\(11, 36, 23, 0\.1\);\s*\}'
new_carousel = """.hero-carousel-container {
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(11, 36, 23, 0.1);
      background: #0B2417;
      width: 100%;
      height: clamp(380px, 50vh, 480px);
      position: relative;
      border: 1px solid rgba(11, 36, 23, 0.1);
    }"""
content = re.sub(old_carousel, new_carousel, content)

old_events = r'\.hero-events-card \{[\s\S]*?width: 100%;\s*height: auto;\s*aspect-ratio: 3 / 4;\s*box-sizing: border-box;\s*position: relative;\s*overflow: hidden;\s*\}'
new_events = """.hero-events-card {
      background: #FFFFFF;
      border: 1.5px solid rgba(11, 36, 23, 0.09);
      border-radius: 20px;
      padding: 16px 18px 8px 20px;
      box-shadow: 0 10px 30px rgba(11, 36, 23, 0.06);
      display: flex;
      flex-direction: column;
      width: 100%;
      height: clamp(380px, 50vh, 480px);
      box-sizing: border-box;
      position: relative;
      overflow: hidden;
    }"""
content = re.sub(old_events, new_events, content)

# 2. Enhance logo visibility EVEN MORE
old_emblem = r'\.hero-jubilee-emblem \{[\s\S]*?filter: drop-shadow\(0 10px 24px rgba\(217, 119, 6, 0\.5\)\);\s*\}'
new_emblem = """.hero-jubilee-emblem {
      height: clamp(120px, 14vh, 180px);
      width: auto;
      object-fit: contain;
      display: block;
      image-rendering: -webkit-optimize-contrast;
      filter: drop-shadow(0 14px 32px rgba(217, 119, 6, 0.8)) drop-shadow(0 4px 10px rgba(0,0,0,0.3));
      transform: scale(1.08);
    }"""
content = re.sub(old_emblem, new_emblem, content)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
