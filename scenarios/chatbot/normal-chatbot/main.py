
import sys
import os

from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage, trim_messages
from dotenv import load_dotenv
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory

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
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

trimmer = trim_messages(
    max_tokens=300,
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

config = {"configurable": {"session_id": "abc2"}}

response = with_message_history.invoke(
    {"messages": [HumanMessage(content="hi! I'm todd")],
     "language": "Chinese"},
    config=config
)

for r in with_message_history.stream(
    {"messages": [HumanMessage(content="what's my name?")],
     "language": "Chinese"},
    config=config
):
    print(r.content, end="", flush=True)
