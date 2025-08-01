# Install necessary libraries
!pip install PyMuPDF python-docx

import fitz  # PyMuPDF
from docx import Document

# Function to extract text from PDF and save to DOCX
def pdf_to_docx(pdf_path, docx_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Create a new Word document
    doc = Document()
    
    # Extract text from each page and add to the document
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        doc.add_paragraph(text)
        doc.add_page_break()
    
    # Save the Word document
    doc.save(docx_path)

# Example usage
pdf_to_docx("sample.pdf", "output.docx")