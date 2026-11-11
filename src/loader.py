
from pathlib import Path
from pypdf import PdfReader


def load_pdf(file_path):

    reader = PdfReader(file_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text:
            documents.append({
                "source": Path(file_path).name,
                "page": page_number,
                "text": text
            })

    return documents


def load_all_pdfs(directory):

    all_documents = []

    pdf_files = list(Path(directory).glob("*.pdf"))

    for pdf_file in pdf_files:

        print(f"Loading: {pdf_file.name}")

        documents = load_pdf(pdf_file)

        all_documents.extend(documents)

    return all_documents
