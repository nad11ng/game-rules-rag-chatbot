import os
import sys

from retriever import search_rules
from generator import generate_answer

def main():
    print("="*60)
    print("Welcome to board game rag chat bot")
    print("="*60)
    print("Ask a question about the rules (e.g: How to win in Uno?)")
    print("Type 'exit' or 'quit' to end the conversation")
    print("="*60)

    while True:
        try:
            query = input("\n You: ")

            if query.lower().strip() in ['exit', 'quit']:
                print("GLHF!!")
                break

            if not query.strip():
                continue

            print("Looking for the answer...")
            retrieved_chunks = search_rules(query, n_results=3)

            if not retrieved_chunks:
                print("RAG bot: Sorry, I couldn't find any related information...")
                continue

            context = "\n\n".join(retrieved_chunks)

            print("Thinking...")

            response = generate_answer(question=query, context=context)
            print(f"\n RAG bot: {response}")

        except KeyboardInterrupt:
            print("\n Keyboard interrupted.")
            sys.exit(0)
        except Exception as e:
            print(f"\n Error: {e}")
            print(" Check the tunnel to see if everything is fine.")

if __name__ == "__main__":
    main()