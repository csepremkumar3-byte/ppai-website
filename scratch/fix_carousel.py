with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_c = """    .hero-carousel-container {
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
new_c = """    .hero-carousel-container {
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(11, 36, 23, 0.1);
      background: #0B2417;
      height: 100%;
      width: 100%;
      min-height: 400px;
      position: relative;
      border: 1px solid rgba(11, 36, 23, 0.1);
      flex-shrink: 0;
    }
    .hero-carousel-container .carousel-slide img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }"""
content = content.replace(old_c, new_c)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
