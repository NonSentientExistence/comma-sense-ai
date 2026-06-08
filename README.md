# comma-sense-ai

Local LLM for querying an uploaded CSV dataset. Built with FastAPI, pandas,
and a SmolLM2 model running locally via HuggingFace transformers.

A REST API that takes a CSV upload, exposes statistics about it, and answers
natural-language questions about the data through a typed Runnable chain
(`PromptBuilder | LLMRunner | ResponseParser`).

## Requirements

- Python 3.14
- [uv](https://docs.astral.sh/uv/) for dependency management

## Installation

```bash
git clone https://github.com/NonSentientExistence/comma-sense-ai.git
cd comma-sense-ai
uv sync
```

## Running

```bash
uv run uvicorn app.main:app --reload
```

The API is then available at http://127.0.0.1:8000
Interactive Swagger docs at http://127.0.0.1:8000/docs

**Note:** the first call to `/ai/ask` downloads the model (~300 MB) and may
take a minute. Subsequent calls are faster.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/data/upload` | Upload a CSV (form-data) |
| GET | `/data/stats` | Descriptive statistics of the uploaded data |
| POST | `/ai/ask` | Ask a question about the data |

## Example usage

1. Start the server and open the Swagger docs at `/docs`
2. POST a CSV to `/data/upload` (you can choose the separator, e.g. `;`)
3. GET `/data/stats` to see descriptive statistics
4. POST a question to `/ai/ask`, e.g. `{"question": "Which game sold the most?"}`

## Running tests

```bash
uv run pytest app/tests/ -v
```

## Assumptions

- The uploaded data is stored in memory and cleared on server restart.
- Only the file extension is validated on upload
- Provided test data is fictional (game_data.csv)
- Default model is SmolLM2-135M

