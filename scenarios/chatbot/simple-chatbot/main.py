
import sys
import os
import hashlib
import threading
import itertools
import time

from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage, trim_messages
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from operator import itemgetter

load_dotenv(verbose=True)

OPENAI_API_KEY = os.environ.get("OPENAI_COMPATIBLE_API_KEY")
BASE_URL = os.environ.get("OPENAI_COMPATIBLE_BASE_URL")
MODEL = os.environ.get("DEFAULT_MODEL")

if not OPENAI_API_KEY or not BASE_URL:
    print("Missing OPENAI_COMPATIBLE_API_KEY or OPENAI_COMPATIBLE_BASE_URL in environment.")
    sys.exit(1)


llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=BASE_URL,
    model=MODEL,
    stream_usage=True
)

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage("You are a helpful assistant"),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

trimmer = trim_messages(
    max_tokens=100,
    strategy="last",
    token_counter=len,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

chain = (
    RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer)
    | prompt
    | llm
)


with_message_history = RunnableWithMessageHistory(chain,
                                                  get_session_history,
                                                  input_messages_key="messages",)


def md5_session_id(username: str) -> str:
    return hashlib.md5(username.encode("utf-8")).hexdigest()


def print_help():
    print("Commands:")
    print("  login <username>   - login as <username> (no password)")
    print("  logout             - logout current user (history preserved)")
    print("  exit | quit | bye  - exit the program")
    print("After login, type messages to send to the assistant.")


def main():
    current_session = None
    current_username = None

    print("Welcome. Type 'login <username>' to login.")
    print_help()

    while True:
        try:
            user_input = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_input:
            continue

        lower = user_input.lower()

        if lower in {"exit", "quit", "bye"}:
            print("Goodbye.")
            break

        if lower.startswith("login "):
            parts = user_input.split(None, 1)
            if len(parts) < 2 or not parts[1].strip():
                print("Usage: login <username>")
                continue
            username = parts[1].strip()
            session_id = md5_session_id(username)
            current_session = session_id
            current_username = username
            print(f"Logged in as {username} (session {session_id})")
            continue

        if lower == "logout":
            if current_session is None:
                print("No user is currently logged in.")
            else:
                print(f"User {current_username} logged out.")
                current_session = None
                current_username = None
            continue

        if current_session is None:
            print("Please login first with: login <username>")
            continue

        # Send only the current message (no explicit conversation build here;
        # RunnableWithMessageHistory will manage history per session_id)
        human_msg = HumanMessage(content=user_input)
        config = {"configurable": {"session_id": current_session}}

        # ...existing code...
        try:
            # Start spinner and stream concurrently.
            print("Assistant: ", end="", flush=True)

            done_event = threading.Event()

            def spinner(ev: threading.Event):
                for ch in itertools.cycle("|/-\\"):
                    if ev.is_set():
                        break
                    sys.stdout.write(ch)
                    sys.stdout.flush()
                    time.sleep(0.12)
                    sys.stdout.write("\b")
                    sys.stdout.flush()

            spinner_thread = threading.Thread(
                target=spinner, args=(done_event,))
            spinner_thread.start()

            first_chunk = True
            for chunk in with_message_history.stream({"messages": [human_msg]}, config=config):
                if first_chunk:
                    # stop spinner before printing real content
                    done_event.set()
                    spinner_thread.join()
                    # clear any leftover spinner char
                    sys.stdout.write(" ")
                    sys.stdout.write("\b")
                    sys.stdout.flush()
                    first_chunk = False

                # print content as it's streamed
                sys.stdout.write(chunk.content)
                sys.stdout.flush()

            # ensure spinner stopped if no chunks produced
            if not first_chunk:
                print("")  # newline after finished streaming
            else:
                done_event.set()
                spinner_thread.join()
                print("")  # newline when nothing printed
        except Exception as e:
            done_event.set()
            try:
                spinner_thread.join(timeout=1)
            except Exception:
                pass
            print(f"\n[error calling model: {e}]")


if __name__ == "__main__":
    main()
