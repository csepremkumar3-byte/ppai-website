import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make only the carousel 3:4 aspect ratio
old_carousel = r'\.hero-carousel-container \{[\s\S]*?height: clamp\(380px, 50vh, 480px\);\s*position: relative;\s*border: 1px solid rgba\(11, 36, 23, 0\.1\);\s*\}'
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
    }"""
content = re.sub(old_carousel, new_carousel, content)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
