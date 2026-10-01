import re

with open("templates/pages/journal_current.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if '<div class="cover-action-btns">' in line:
        new_lines.append(line)
        new_lines.append("        <a href=\"{% static 'documents/IJPP_Vol_54_No_1_March_2026.pdf' %}\" target=\"_blank\" class=\"btn-emerald\">\n")
        new_lines.append("          <svg width=\"15\" height=\"15\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.2\"><path d=\"M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z\"/><circle cx=\"12\" cy=\"12\" r=\"3\"/></svg>\n")
        new_lines.append("          View Full Vol. 54 PDF\n")
        new_lines.append("        </a>\n")
        new_lines.append("        <a href=\"{% static 'documents/IJPP_Vol_54_No_1_March_2026.pdf' %}\" download=\"IJPP_Vol54_No1_March_2026.pdf\" class=\"btn-outline\" style=\"background: #FFF;\">\n")
        new_lines.append("          <svg width=\"15\" height=\"15\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4\"/><polyline points=\"7 10 12 15 17 10\"/><line x1=\"12\" y1=\"15\" x2=\"12\" y2=\"3\"/></svg>\n")
        new_lines.append("          Download Vol. 54 PDF\n")
        new_lines.append("        </a>\n")
        skip = True
    elif skip and '</div>' in line:
        new_lines.append(line)
        skip = False
    elif not skip:
        new_lines.append(line)

with open("templates/pages/journal_current.html", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("journal_current.html replaced cleanly!")
