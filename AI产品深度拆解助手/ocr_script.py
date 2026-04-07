import fitz
from rapidocr_onnxruntime import RapidOCR
import sys

try:
    ocr = RapidOCR()
    doc = fitz.open('黄运添-AI产品经理.pdf')
    result_text = []

    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(dpi=300)
        img_path = f"page_{i}.png"
        pix.save(img_path)
        print(f"Saved {img_path}, running OCR...")
        
        result, elapse = ocr(img_path)
        if result:
            for line in result:
                text = line[1]
                result_text.append(text)

    with open('resume_text.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(result_text))

    print("OCR complete. Length of text:", len('\n'.join(result_text)))
except Exception as e:
    print("Error:", e)
    sys.exit(1)
