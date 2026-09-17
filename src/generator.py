import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env variables
load_dotenv()

# get URL from ngrok on kaggle
LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:11434/v1")

# initialize OpenAI client that points to the endpoint of Kaggle
client = OpenAI(
    base_url=LLM_API_URL,
    api_key="ollama",
    
)

def generate_answer(question: str, context: str, model_name: str = "llama3") -> str:
    #system prompt to avoid hallucination
    system_prompt = (
        "You are an expert board game rules assistant. "
        "Answer the user's question using ONLY the provided context. "
        "Strict Rules:\n"
        "1. Do not use any external knowledge or information not present in the context.\n"
        "2. If the context does not contain the answer, explicitly state that the answer could not be found in the provided rule documents.\n"
        "3. Always mention which game or section the rule belongs to if specified in the context.\n"
        "4. Respond in the same language as the user's question (e.g., if asked in Vietnamese, reply in Vietnamese).\n"
        "5. Be concise, clear, and direct."
    )
    user_prompt = f"Context:\n{context}\n\nQuestion:\n{question}"

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1, #low temparature to stick with the retrieved documents
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error found. No connection to LLM server: {e}"

#test
if __name__ == "__main__":
    print("Đang kiểm tra generator với dữ liệu mẫu...")
    sample_context = "[Game: Battleship, Section: Components]\nEach player has 5 ships: Carrier (5), Battleship (4), Cruiser (3), Submarine (3), Destroyer (2)."
    sample_question = "Mỗi người chơi Battleship có bao nhiêu tàu?"
    
    result = generate_answer(sample_question, sample_context)
    print("\n--- KẾT QUẢ TEST ---")
    print(result)

