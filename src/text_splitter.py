def chunk_document(documents, chunk_size = 600, chunk_overlap = 100):
    chunks = []
    for doc in documents:
        text = doc["text"]
        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + chunk_size
            if end < len(text):
                while end > start and text[end] != ' ':
                    end -= 1

            split_text = text[start:end].strip()

            if split_text:
                chunk = {
                    "text": split_text,
                    "metadata": doc["metadata"].copy
                }
                chunk["metadata"]["chunk_id"] = f"{doc['metadata']['game'].replace(' ', '')}_p{doc['metadata']['page']}_c{chunk_index}"
                chunks.append(chunk)

        start = end - chunk_overlap
        chunk_index += 1

    return chunks


