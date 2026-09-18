from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

HEADER_TO_SPLIT = [
    ("#", "heading_1"),
    ("##", "heading_2"),
    ("###", "heading_3")
]

def chunk_pdf(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\\n\\n", "\\n", ". ", " ", ""]
    )
    chunks = []
    for document in documents:
        document_chunks = text_splitter.split_text(document.page_tent)
        
        for chunk in document_chunks:
            chunk.metadata = {**document.metadata, **chunk.metadata}
            
            chunks.append(chunk)

    for index, chunk in enumerate(chunks):
        source = chunk.metada.get("source", "unknown")
        filename = Path(source).stem
        
        chunk.metadata["chunk_id"] = (f"{filename}_chunk_{index}")
        
    return chunks


def chunk_documents(documents):
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADER_TO_SPLIT,
        strip_headers=False
    )
    
    chunks = []
    for document in documents:
        document_chunks = markdown_splitter.split_text(document.page_content)
    
        for chunk in document_chunks:
            chunk.metadata = {**document.metadata, **chunk.metadata}
            
            chunks.append(chunk)
    
    for index, chunk in enumerate(chunks):
        source = chunk.metadata.get("source", "unknown")
        filename = Path(source).stem
        
        chunk.metadata["chunk_id"] = (f"{filename}_chunk_{index}")
    
    
    return chunks

if __name__ == "__main__":
    from document_loader import load_markdown_documents

    documents = load_markdown_documents()
    chunks = chunk_documents(documents)

    print(f"Total documents: {len(documents)}")
    print(f"Total chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks):
        print("=" * 70)
        print(f"CHUNK {index + 1}")
        print("=" * 70)

        print("Metadata:")
        print(chunk.metadata)

        print("\nContent:")
        print(chunk.page_content)

        print(f"\nChunk length: {len(chunk.page_content)}")

