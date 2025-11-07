
import sys
import os

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(verbose=True)

OPENAI_API_KEY = os.environ.get("OPENAI_COMPATIBLE_API_KEY")
BASE_URL = os.environ.get("OPENAI_COMPATIBLE_BASE_URL")
MODEL = os.environ.get("DEFAULT_MODEL")

WELCOME = (
    "Hello — I am a chat assistant, but I have a fish-like memory. "
    "I can only answer what you say right now. I do not remember previous messages."
)
EXIT_WORDS = {"bye", "goodbye", "exit", "quit", "再见", "拜拜"}


if not OPENAI_API_KEY or not BASE_URL:
    print("Missing OPENAI_COMPATIBLE_API_KEY or OPENAI_COMPATIBLE_BASE_URL in environment.")
    sys.exit(1)

llm = ChatOpenAI(
  api_key=OPENAI_API_KEY,
  base_url=BASE_URL,
  model=MODEL,
  stream_usage=True
)

def main():
    print(WELCOME)
    input_tokens= 0
    output_tokens = 0
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        if user_input.lower() in EXIT_WORDS:
            print("Chatbot: Goodbye!")
            break
        try:
            response = llm.invoke([{"role": "user", "content": user_input}])
            input_tokens += response.usage_metadata['input_tokens']
            output_tokens += response.usage_metadata['output_tokens']
            print(f"Chatbot: {response.content} [Tokens used - Input: {input_tokens}, Output: {output_tokens}]")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
