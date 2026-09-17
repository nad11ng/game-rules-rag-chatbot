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


def chunk_document(documents, chunk_size = 600, chunk_overlap = 100):
    chunks = []
    for doc in documents:
        text = doc["text"]
        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            if end < len(text):
                split_at = end
                while split_at > start and text[split_at] != ' ':
                    split_at -= 1
                if split_at > start:
                    end = split_at

            split_text = text[start:end].strip()

            if split_text:
                chunk = {
                    "text": split_text,
                    "metadata": doc["metadata"].copy()
                }
                chunk["metadata"]["chunk_id"] = f"{doc['metadata']['source'].replace(' ', '')}_p{doc['metadata']['page']}_c{chunk_index}"
                chunks.append(chunk)
                chunk_index += 1

            if end >= len(text):
                break

            start = max(end - chunk_overlap, start + 1)

    return chunks

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

        print(chunk_document(documents, chunk_size = 600, chunk_overlap= 100))

if __name__ == "__main__":
    main()