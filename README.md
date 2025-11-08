

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
3. Go to specific dir
4. Install dependencies using uv:
```sh
uv pip install .
```
5. Copy `.env.example` to `.env` and fill in your API credentials
