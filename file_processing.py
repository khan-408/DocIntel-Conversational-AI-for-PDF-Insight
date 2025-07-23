import fitz
from PIL import Image
import pytesseract
from io import BytesIO
import os

def extract_pdf_text_with_metadata(content: bytes, filename:str):
    doc = fitz.open(stream=BytesIO(content), filetype="pdf")
    pages=[]
    for i,page in enumerate(doc, start=1):  
        text = page.get_text()
        if not text.strip():
            pass
        pages.append({'text':text,
                      'filename':filename,
                      'page_number':i
                      })  
    return pages

def process_files(file_dict:dict):
    all_docs=[]
    for filename, content in file_dict.items():
        if filename.endswith(".pdf"):
            all_docs.extend(extract_pdf_text_with_metadata(content,filename))
        else:
            print(f"Skipping unsupported file: {filename}")
    return all_docs

