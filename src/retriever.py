import os
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIRECTORY = PROJECT_ROOT / "storage" / "chroma"
COLLECTION_NAME = "game_rules"

def search_rules(query: str, game_filter: str = None, n_results: int = 3) -> list:
    if not CHROMA_DIRECTORY.exists():
        print(f"Database not found at '{CHROMA_DIRECTORY}', run ingest.py first.")
        return []

    try:
        client = chromadb.PersistentClient(path=str(CHROMA_DIRECTORY))
        embedding_fn = embedding_functions.DefaultEmbeddingFunction()

        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_fn
        )

        # filter metadata for a specific game
        where_condition = {"game": game_filter} if game_filter else None

        # query
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_condition
        )

        retrieved_chunks = []

        # extract and format results
        if results and "documents" in results and results["documents"]:
            documents = results["documents"][0]
            metadatas = results["metadatas"][0]

            # extract game name and rule from metadata
            for doc, meta in zip(documents,metadatas):
                game_name = meta.get("heading_1", "unknown game")
                section_name = meta.get("heading_2", "General")

                # format text for LLM
                source_info = f"[Game: {game_name} | Section: {section_name}]"
                formatted_chunk = f"{source_info}\n{doc}"
                retrieved_chunks.append(formatted_chunk)

        return retrieved_chunks

    except Exception as e:
        print(f"Error during retrieval with ChromaDB: {e}")
        return []


if __name__ == "__main__":
    print("Testing Retriever...")
    test_query = "How to win?"
    
    results = search_rules(test_query)
    
    print(f"\nFound {len(results)} for query: '{test_query}'")
    for i, res in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(res)