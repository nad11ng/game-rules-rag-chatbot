# GameRules Library RAG Chatbot

## 1. Project overview
Build a chatbot that can answer questions about the rules of five games based entirely on provided documents.
Core features:
* Identify the correct game being asked about.
* Find the correct document segment and answer based on the retrieved context.
* Display sources.
* Do not invent rules when the document does not mention them.
* Support questions in Vietnamese and English.

## 2. Demo
*(Add screenshot or GIF demo here)*
![Demo](assets/demo.gif) 

## 3. Supported games
The project supports explaining the rules of 5 games:
* Battleship
* Tic-tac-toe
* UNO
* Pac-Man (Rules and gameplay mechanics of the classic arcade version)
* Connect Four

## 4. RAG Architecture
The system consists of two separate processes:
* **Ingestion:** Read game rule documents, clean, divide into chunks, create embeddings, and save to ChromaDB.
* **Question answering:** Receive user question, identify the game, search for relevant chunks in ChromaDB, combine into Prompt (question + context), and pass to LLM to generate an answer with sources.

## 5. Technologies used
* **Language:** Python
* **Interface:** Streamlit
* **Document reading:** PyMuPDF
* **Embedding:** OpenAI Embeddings or Sentence Transformers
* **Vector database:** ChromaDB
* **LLM:** OpenAI API or Ollama (currently configured for a custom LLM endpoint via Kaggle/Docker setup)
* **Environment & Source code management:** Git, GitHub, and python-dotenv
* **Testing:** pytest

## 6. Installation guide
If running locally without Docker:
```bash
git clone <repository-url>
cd game-rules-rag-chatbot
python -m venv .venv
.venv\Scripts\activate  # Or `source .venv/bin/activate` on Linux/Mac
pip install -r requirements.txt
```

## 7. Environment setup (.env)
Copy the example file to create the environment configuration:
```bash
copy .env.example .env  # Use `cp` on Linux/Mac
```
*Note: Add the `LLM_API_URL` from your Kaggle server to the `.env` file.*

## 8. Document ingestion
Before asking questions, you need to prepare the data and vector db (run only once):
```bash
python -m src.ingest
```

## 9. Running the CLI
Test the RAG logic without the UI:
```bash
python -m src.cli
```

## 10. Running Streamlit
To start the chatbot web interface:
```bash
streamlit run app.py
```
*(If using Docker: Run `docker-compose up --build`)*

## 11. Example questions
You can try the following questions:
* "How many ships does each Battleship player have?"
* "In Tic-tac-toe, when is the game a tie?"
* "Can a Wild Draw Four be played at any time?"
* "What is the effect of the Power Pellet in Pac-Man?"
* "In Connect Four, can a checker be placed in any slot?"
* "How do UNO and Battleship differ in the number of players?"

## 12. Evaluation results
The system uses a set of 50 test questions (stored in `evaluation/questions.json`) to evaluate: direct questions, rephrased questions, comparison questions, unanswerable questions, and wrong-game questions.
Evaluates Retrieval and Answer accuracy (e.g., source accuracy, refusal on missing data).

## 13. Current limitations
The current version does not support:
* User login and account database.
* Voice chatbot.
* Fine-tuning.
* Stable cloud deployment (currently using Kaggle session/Local).
* Real-time Internet search.

## 14. Roadmap
* **Version 0.2:** Hybrid search (keyword + vector), adjust chunk size, reranking, automatic game identification, cross-game rule comparison.
* **Version 0.3:** Docker deployment, Automated tests on GitHub Actions, deploy demo, evaluation dashboard, support uploading new documents.

## 15. Document sources
All rule documents are stored in `data/raw/` including: `battleship_rules.pdf`, `tic_tac_toe_rules.pdf`, `uno_rules.pdf`, `pacman_rules.pdf`, `connect_four_rules.pdf`.
*(Note: UNO uses official rules, not house rules).*

## 16. License
MIT License