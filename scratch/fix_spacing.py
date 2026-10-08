import re

with open('templates/pages/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

css_updates = [
    # 1. Update the grid so it fills horizontal space perfectly
    # Use 'auto' for the left column so it perfectly wraps the carousel.
    # Use '1fr' for middle and right so they take up the ENTIRE remaining container width!
    # Also increase the max height of the hero panel on large screens.
    (r'\.hero-main-grid \{[\s\S]*?flex: 1 1 auto;\s*\}', """.hero-main-grid {
      --hero-panel-h: clamp(320px, calc(100vh - 450px), 650px);
      display: grid;
      grid-template-columns: auto 1.3fr 1fr;
      gap: clamp(24px, 3vw, 40px);
      width: 100%;
      min-height: 0;
      flex: 1 1 auto;
    }"""),

    # 2. Make the carousel flush left instead of margin-left: auto
    (r'\.hero-carousel-container \{[\s\S]*?margin-left: auto;\s*\}', """.hero-carousel-container {
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
      margin-right: auto;
    }"""),

    # 3. Events card should stretch to fill its column
    (r'\.hero-events-card \{[\s\S]*?overflow: hidden;\s*\}', """.hero-events-card {
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

    # 4. Middle Card should also stretch and be centered
    (r'\.hero-middle-card \{[\s\S]*?padding: 0 20px;\s*\}', """.hero-middle-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 0 clamp(20px, 3vw, 40px);
      width: 100%;
    }"""),

    # 5. Fix vertical spacing on large screens:
    (r'\.viewport-fold \{[\s\S]*?position: relative;\s*\}', """.viewport-fold {
      min-height: 100vh;
      min-height: 100dvh;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      background: linear-gradient(180deg, #FFFFFF 0%, #E1F0E8 100%);
      position: relative;
    }
    .hero {
      flex: 1 1 auto;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: clamp(20px, 4vh, 60px) 0;
    }""")
]

for pattern, repl in css_updates:
    content = re.sub(pattern, repl, content)

with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
