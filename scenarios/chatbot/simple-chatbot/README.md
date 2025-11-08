# Simple Multi-User Chatbot

A chat application demonstrating multi-user session management and conversation history using LangChain and OpenAI-compatible APIs.

## Features

- Multi-user support with session management
- Persistent conversation history per user
- Support for OpenAI-compatible APIs
- Interactive streaming responses with loading indicator
- MD5-based session identification
- Login/logout functionality

## Usage

Run the chatbot:
```sh
uv run main.py
```

Available commands:
- `login <username>` - Login as specified user
- `logout` - Logout current user (preserves chat history)
- `exit`, `quit`, `bye` - Exit the program

## LangChain Implementation Details

The chatbot leverages several key LangChain concepts:

1. **Session Management**
   - Uses `InMemoryChatMessageHistory` for per-user history
   - Implements MD5-based session identification
   - Maintains separate conversation contexts per user

2. **Message Handling**
   - Uses `RunnableWithMessageHistory` for history management
   - Implements streaming responses with progress indicator
   - Maintains conversation context between messages

3. **Chat Components**
   - `ChatPromptTemplate` for message formatting
   - `MessagesPlaceholder` for history injection
   - `trim_messages` for managing context window

4. **Interactive Features**
   - Real-time streaming output
   - Visual loading indicator during model responses
   - Session-based user management

## Limitations

- In-memory storage only (history cleared on restart)
- No password authentication
- Requires constant API connection