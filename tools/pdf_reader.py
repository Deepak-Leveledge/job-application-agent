import PyPDF2
import os

def read_pdf(pdf_path: str) -> str:
    print(f"📖 Reading PDF: {pdf_path}")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at: {pdf_path}")

    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()

    print(f"✅ PDF read successfully! {len(text)} characters extracted.")
    return text
