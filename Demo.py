import fitz  # PyMuPDF

# Replace this with the path to your PDF file
pdf_path = "KBB.pdf"

# Open the PDF
doc = fitz.open(pdf_path)

# Extract and print text from each page
for page_num, page in enumerate(doc, start=1):
    text = page.get_text()
    print(f"\n--- Page {page_num} ---\n{text}")
