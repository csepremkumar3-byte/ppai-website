import pymupdf
import os
import io

pdf1_path = r"C:\Users\LENOVO\.gemini\antigravity\brain\c6878145-16c3-412a-830d-aeeb83c80302\.user_uploaded\media_1791270236975.pdf"
pdf2_path = r"C:\Users\LENOVO\.gemini\antigravity\brain\c6878145-16c3-412a-830d-aeeb83c80302\.user_uploaded\media_1791270237039.pdf"

print("--- PDF 1 (Dr Bajaru Bhaskar) ---")
doc1 = pymupdf.open(pdf1_path)
for i, page in enumerate(doc1):
    for img_idx, img in enumerate(page.get_images()):
        xref = img[0]
        base_img = doc1.extract_image(xref)
        img_bytes = base_img["image"]
        img_ext = base_img["ext"]
        out_name = f"scratch/dr_b_bhaskar_extracted.{img_ext}"
        with open(out_name, "wb") as f:
            f.write(img_bytes)
        print(f"Extracted image {img_idx}: {out_name} ({len(img_bytes)} bytes)")

print("\n--- PDF 2 (Dr Johnson Stanley) ---")
doc2 = pymupdf.open(pdf2_path)
for i, page in enumerate(doc2):
    for img_idx, img in enumerate(page.get_images()):
        xref = img[0]
        base_img = doc2.extract_image(xref)
        img_bytes = base_img["image"]
        img_ext = base_img["ext"]
        out_name = f"scratch/dr_j_stanley_extracted.{img_ext}"
        with open(out_name, "wb") as f:
            f.write(img_bytes)
        print(f"Extracted image {img_idx}: {out_name} ({len(img_bytes)} bytes)")

