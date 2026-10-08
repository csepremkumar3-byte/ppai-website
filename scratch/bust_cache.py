with open('templates/pages/editorial_board.html', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("dr_jose_romeno_faleiro.png' %}?v=20260929_1", "dr_jose_romeno_faleiro.png' %}?v=20261008_new")
with open('templates/pages/editorial_board.html', 'w', encoding='utf-8') as f:
    f.write(content)
