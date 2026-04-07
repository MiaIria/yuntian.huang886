import fitz
import sys

try:
    doc = fitz.open('黄运添-AI产品经理.pdf')
    print("Number of pages:", len(doc))
    for i in range(len(doc)):
        page = doc[i]
        # Check text
        text = page.get_text()
        print(f"Page {i} text length: {len(text)}")
        # Check images
        images = page.get_images(full=True)
        print(f"Page {i} images count: {len(images)}")
except Exception as e:
    print("Error:", e)
