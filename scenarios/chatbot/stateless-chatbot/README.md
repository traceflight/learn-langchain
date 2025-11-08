# Stateless Chatbot

A basic chatbot implementation using LangChain and OpenAI-compatible APIs that demonstrates stateless conversation capabilities.

## Features

- Single-turn conversations (stateless chat)
- Token usage tracking for both input and output
- Support for OpenAI-compatible APIs
- Graceful exit handling with multiple exit commands
- Environment variable configuration

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
