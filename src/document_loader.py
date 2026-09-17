from pathlib import Path
import pymupdf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIRECTORY = PROJECT_ROOT / "data" / "raw"

def load_pdf(file_path):
    file_path = Path(file_path)
    
    if not file_path.is_file():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    if file_path.suffix.lower() != ".pdf":
        raise ValueError(f"Unsupported file type: {file_path.suffix}")

    documents = []

    with pymupdf.open(file_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):

            # Extract text from the current page
            text = page.get_text("text").strip()

            # Ignore pages without extractable text
            if not text:
                continue

            document = {
                "text": text,
                "metadata": {
                    "source": file_path.name,
                    "page": page_number,
                },
            }

            documents.append(document)

    return documents

def load_documents(directory=DEFAULT_DATA_DIRECTORY):
    
    directory = Path(directory)
    
    if not directory.is_dir():
        raise NotADirectoryError(f"Data director not fount: {directory}")
    
    pdf_files = sorted(directory.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in: {directory}"
        )

    all_documents = []

    for pdf_file in pdf_files:
        print(f"Loading: {pdf_file.name}")

        pdf_documents = load_pdf(pdf_file)
        all_documents.extend(pdf_documents)

        print(
            f"Loaded {len(pdf_documents)} pages "
            f"from {pdf_file.name}"
        )

    return all_documents

def main():
    """
    Test the document loader.
    """
    documents = load_documents()

    print()
    print(f"Total loaded pages: {len(documents)}")

    if documents:
        first_document = documents[1]

        print()
        print("First document metadata:")
        print(first_document["metadata"])

        print()
        print("First 300 characters:")
        print(first_document["text"][:300])


if __name__ == "__main__":
    main()