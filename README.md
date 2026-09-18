# Board Game Rules RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about board game rules using only the provided rule documents as context, so it does not hallucinate rules that aren't in the source material.

## 1. Project overview

Core features:
* Load board game rule documents (Markdown) and split them into structured chunks.
* Embed and store chunks in a local vector database (ChromaDB).
* Retrieve the most relevant rule chunks for a user's question.
* Generate an answer using an LLM, grounded strictly in the retrieved context.
* Simple CLI chat interface for testing the full pipeline end to end.

## 2. Current supported games

Based on the documents currently ingested from `data/raw/`:
* Battleship (`battleship.md`)
* UNO (`uno.md`)

> Only `.md` files are picked up by the ingestion pipeline. `battleship.pdf` and `uno.pdf` are kept in `data/raw/` for reference but are **not** read by `document_loader.py` (it only globs `**/*.md`).

## 3. Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Document loading | LangChain (`langchain-community`) `DirectoryLoader` + `TextLoader` |
| Chunking | LangChain `MarkdownHeaderTextSplitter` (splits on `#`, `##`, `###`) |
| Embeddings | ChromaDB's built-in `DefaultEmbeddingFunction` (ONNX `all-MiniLM-L6-v2`, downloaded automatically on first run) |
| Vector database | ChromaDB (`PersistentClient`, stored locally in `storage/chroma/`) |
| LLM serving | Ollama running on a Kaggle notebook (GPU), exposed publicly via a local tunnel |
| LLM client | `openai` Python SDK configured with a custom `base_url` (OpenAI-compatible endpoint) |
| CLI | Plain Python (`src/main.py`) |
| Web UI (planned) | Streamlit (`app.py` — not implemented yet) |
| Config | `python-dotenv` (`.env`) |
| Containerization | Docker / docker-compose (targets the Streamlit app) |
| Testing | pytest |

## 4. Project structure

```
src/
  document_loader.py   # Loads *.md files from data/raw/
  text_splitter.py      # Splits documents into chunks by Markdown headers
  ingest.py              # Orchestrates load -> chunk -> embed -> store in ChromaDB
  retriever.py           # Queries ChromaDB and returns formatted context chunks
  generator.py           # Calls the LLM (Ollama via OpenAI-compatible API) to generate the final answer
  main.py                 # CLI chat loop tying retriever + generator together
data/raw/                # Source rule documents (.md used, .pdf kept for reference)
storage/chroma/          # Local persistent vector database (auto-created by ingest.py)
app.py                    # Streamlit entry point (currently empty, not implemented)
requirements.txt
.env                       # LLM_API_URL and other environment config
```

## 5. Prerequisites

* Python 3.11+ (project has been run successfully on 3.12/3.13)
* Windows users on **ARM64** machines: use an **x64 (amd64) Python interpreter**, not an ARM64 one. `pyarrow` (a ChromaDB dependency) has no prebuilt wheel for Windows ARM64 and will fail to build from source. An x64 interpreter runs fine under emulation and has full wheel support.
* A Kaggle account (for running the LLM with free GPU access)

## 6. Installation

```bash
git clone <repository-url>
cd game-rules-rag-chatbot
python -m venv .venv
.venv\Scripts\activate        # On Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
```

## 7. Setting up the LLM server (Ollama on Kaggle + tunnel)

The chatbot does not call OpenAI — it calls a **local Ollama server running inside a Kaggle notebook**, exposed to the internet through a tunnel. This step is required before the chatbot can generate answers (retrieval still works without it).

1. Open a Kaggle notebook with GPU enabled.
2. Install and start Ollama inside the notebook, then pull the model you intend to use (e.g. `llama3`).
3. Start the Ollama server so it listens locally inside the Kaggle kernel (default port `11434`).
4. Expose that local port publicly using a tunnel tool (e.g. `localtunnel`) run from inside the Kaggle notebook. This gives you a public forwarding URL, for example:
   ```
   https://gold-hoops-sit.loca.lt
   ```
5. Copy that URL into your `.env` file as `LLM_API_URL`, and make sure to **append `/v1`** at the end, since `generator.py` talks to Ollama's OpenAI-compatible API:
   ```
   LLM_API_URL=https://gold-hoops-sit.loca.lt/v1
   ```
6. Every time you restart the Kaggle notebook/tunnel, the URL changes — update `.env` again with the new URL before testing.
7. Once `.env` is updated, run `main.py` from inside `src/` (see step 9 below) to confirm the connection works end to end.

> If `LLM_API_URL` is not set, `generator.py` falls back to `http://localhost:11434/v1`, i.e. an Ollama instance running on your own machine.

## 8. Environment setup (`.env`)

Create/edit `.env` in the project root:
```
LLM_API_URL=https://<your-tunnel-url>/v1
```

## 9. Running the pipeline

All scripts currently use direct (non-package) imports, so they must be run **from inside the `src/` folder**, not with `python -m`.

### 9.1 Ingest the documents (run once, or whenever `data/raw/*.md` changes)
```bash
cd src
python ingest.py
```
This loads the Markdown files, splits them into chunks, generates embeddings, and stores everything in `storage/chroma/` under the collection `game_rules`.

### 9.2 Test retrieval only (optional, no LLM needed)
```bash
python retriever.py
```
Runs a sample query against the local vector database and prints the matched chunks.

### 9.3 Test generation only (optional, requires `LLM_API_URL` to be reachable)
```bash
python generator.py
```
Sends a sample context + question to the configured LLM endpoint and prints the answer.

### 9.4 Run the full chatbot (CLI)
```bash
python main.py
```
Then type a question, e.g.:
```
You: How to win in Battleship?
```
Type `exit` or `quit` to end the conversation.

> `app.py` (Streamlit web UI) is not implemented yet — use `main.py` for now.

## 10. Example questions

* "How many ships does each Battleship player have?"
* "Can a Wild Draw Four be played at any time in UNO?"
* "How to win in Battleship?"

## 11. Troubleshooting

* **`ModuleNotFoundError` when running a script** — make sure you `cd src` first; these scripts rely on the current working directory being `src/` for their imports to resolve.
* **`Database not found` from `retriever.py`/`main.py`** — run `python ingest.py` first to create `storage/chroma/`.
* **`Error: No connection to LLM server`** — your Kaggle notebook/tunnel is not running, or `LLM_API_URL` in `.env` is stale/missing the `/v1` suffix.
* **`pyarrow` fails to install on Windows ARM64** — see the Prerequisites section; switch to an x64 Python interpreter.

## 12. Current limitations

* Only 2 games ingested so far (Battleship, UNO); PDFs are not parsed yet.
* No Streamlit web UI yet (`app.py` is empty).
* No automatic game detection/filtering wired into the CLI (`game_filter` exists in `retriever.py` but is unused by `main.py`).
* Depends on a Kaggle notebook + tunnel staying online; the LLM endpoint is not persistent.
* No automated tests yet (`tests/` is an empty package).

## 13. Roadmap

* Wire up `game_filter` in the CLI for per-game filtering.
* Implement the Streamlit UI (`app.py`).
* Add more games and parse the existing PDFs.
* Add automated tests and CI.
* Move to a more stable LLM hosting setup (replace the Kaggle tunnel).

## 14. License

MIT License
