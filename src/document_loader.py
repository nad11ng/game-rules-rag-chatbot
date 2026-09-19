from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyMuPDFLoader, UnstructuredFileLoader

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIRECTORY = PROJECT_ROOT / "data" / "raw"


def load_markdown_documents(directory=DEFAULT_DATA_DIRECTORY):
    
    directory = Path(directory)
    
    loader = DirectoryLoader(
        path=str(directory),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={
            "encoding": "utf-8",
        },
        show_progress=True,
        use_multithreading=False       
    )
    
    documents = loader.load()
    
    return documents
    
if __name__ == "__main__":
    
    documents = load_markdown_documents()
    print(f"Total Markdown documents: {len(documents)}")
    print(f"Total PDF documents: {len(documents)}")
    
    
    for document in documents:
        print("=" * 70)
        print(f"DOCUMENT: {document}")
        print("-" * 70)

        print("\nMetadata:")
        print(document.metadata)
        print("-" * 70)
        
        print("\nContent:")
        print(document.metadata)