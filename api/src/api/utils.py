import PyPDF2
from docx import Document


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        full_text = ""

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            full_text += page.extract_text() + "\n"  # Add a new line after each page

    return full_text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)