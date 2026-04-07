import fitz
doc = fitz.open('黄运添-AI产品经理.pdf')
text = ''
for page in doc:
    text += page.get_text()

with open('resume_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)
