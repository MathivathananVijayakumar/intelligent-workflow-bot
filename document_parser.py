import fitz  # PyMuPDF
import docx
import os

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Main parser function
def parse_attachments(attachments):
    extracted_info = []
    for file in attachments:
        filename, file_extension = os.path.splitext(file)
        if file_extension.lower() == '.pdf':
            content = extract_text_from_pdf(file)
        elif file_extension.lower() == '.docx':
            content = extract_text_from_docx(file)
        else:
            content = "Unsupported file type."
        extracted_info.append({"file": file, "content": content})
    return extracted_info
