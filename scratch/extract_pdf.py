import PyPDF2

pdf_path2 = r"C:\Users\LENOVO\.gemini\antigravity\brain\c6878145-16c3-412a-830d-aeeb83c80302\.user_uploaded\media_1789939257188.pdf"
reader2 = PyPDF2.PdfReader(pdf_path2)
print(f"Second PDF pages: {len(reader2.pages)}")
for i, page in enumerate(reader2.pages):
    text = page.extract_text()
    if text and text.strip():
        print(f"\n--- Page {i+1} ---")
        print(text[:5000])
