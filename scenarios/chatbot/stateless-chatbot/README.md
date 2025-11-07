# Stateless Chatbot

A basic chatbot implementation using LangChain and OpenAI-compatible APIs that demonstrates stateless conversation capabilities.

## Features

- Single-turn conversations (stateless chat)
- Token usage tracking for both input and output
- Support for OpenAI-compatible APIs
- Graceful exit handling with multiple exit commands
- Environment variable configuration

## Prerequisites

- Python 3.12+
- OpenAI-compatible API access
- Required environment variables:
  - `OPENAI_COMPATIBLE_API_KEY`: Your API key
  - `OPENAI_COMPATIBLE_BASE_URL`: Base URL for the API
  - `DEFAULT_MODEL`: Model name to use

## Installation

1. Ensure you have Python 3.12+ installed
2. Install uv if you haven't:
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```
3. Install dependencies using uv:
```sh
uv pip install .
```
4. Copy `.env.sample` to `.env` and fill in your API credentials


## Usage

Run the chatbot:
```sh
uv run main.py
```

To exit the chat, type any of these commands:
- "bye"
- "goodbye"
- "exit"
- "quit"
- "再见"
- "拜拜"

## LangChain Implementation Details

The chatbot uses several key LangChain concepts:

1. **ChatOpenAI Integration**
   - Uses `langchain_openai.ChatOpenAI` for interaction with OpenAI-compatible APIs
   - Configures model settings through environment variables

2. **Message Handling**
   - Implements basic chat using the `invoke` method
   - Messages are formatted using the standard role/content structure

3. **Token Usage Tracking**
   - Leverages `stream_usage=True` for real-time token counting
   - Tracks both input and output tokens separately

4. **Stateless Design**
   - Each interaction is independent
   - No conversation history is maintained between turns
