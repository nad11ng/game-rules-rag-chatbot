from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from document_loader import load_markdown_documents
from text_splitter import chunk_documents

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIRECTORY = PROJECT_ROOT / "storage" / "chroma"

COLLECTION_NAME = "game_rules"

def ingest_documents():
    # Load markdown documents
    documents = load_markdown_documents()
    
    # Split documents into chunks
    chunks = chunk_documents(documents)
    
    # Create storage/chroma directory
    CHROMA_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )
    
    client = chromadb.PersistentClient(path=str(CHROMA_DIRECTORY))
    
    embedding_function = DefaultEmbeddingFunction()
    
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )
    
    chunk_texts = []
    chunk_metadatas = []
    chunk_ids = []
    
    for chunk in chunks:
        chunk_texts.append(chunk.page_content)
        chunk_metadatas.append(chunk.metadata)
        chunk_ids.append(chunk.metadata["chunk_id"])
        
    collection.upsert(
        ids=chunk_ids,
        documents=chunk_texts,
        metadatas=chunk_metadatas
    )
    
    return documents, chunks, collection
    
if __name__ == "__main__":
    documents, chunks, collection = ingest_documents()

    print(f"Total documents: {len(documents)}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Stored chunks: {collection.count()}")
    print(f"Collection name: {collection.name}")
    print(f"Database directory: {CHROMA_DIRECTORY}")