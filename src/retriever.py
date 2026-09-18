import os
import chromadb
from chromadb.utils import embedding_functions

def search_rules(query: str, game_filter: str = None, n_results: int = 3 ) -> list:
    persist_directory = "storage/chroma"

    # test if database exists.
    if not os.path.exists(persist_directory):
        print("Database not found at '{persist_directory}', run ingest.py first.")
        return []

    try:
        # connect local database Chroma
        client = chromadb.PersistentClient(path=persist_directory)

        # use Chroma's default embedding model
        embedding_fn = embedding_functions.DefaultEmbeddingFunction()

        # get rules collection
        collection = client.get_collection(
            name="game_rules",
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
                game_name = meta.get("game", "unknown game")
                section_name = meta.get("section", "General")

                # format text for LLM
                source_info = f"[Game: {game_name} | Section: {section_name}]"
                formatted_chunk = f"{source_info}\n{doc}"
                retrieved_chunks.append(formatted_chunk)

        return retrieved_chunks

    except Exception as e:
        print(f"Error during retrieval with ChromaDB: {e}")
        return []


if __name__ == "__main__":
    print("Đang kiểm tra bộ truy xuất Retriever...")
    test_query = "Làm sao để chiến thắng?"
    
    # Lưu ý: Lúc này nếu chưa có database, code sẽ in ra dòng Cảnh báo và trả về list rỗng
    results = search_rules(test_query)
    
    print(f"\nTìm thấy {len(results)} kết quả cho câu hỏi: '{test_query}'")
    for i, res in enumerate(results, 1):
        print(f"\n--- Kết quả {i} ---")
        print(res)