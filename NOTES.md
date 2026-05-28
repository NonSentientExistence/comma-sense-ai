## Comma sense AI
#### Small local LMM that analyzes an uploaded CSV and lets you query the AI on the CSV data

### Structure

Initial structure idea for the project. Keeping the chain and LLM integration isolated from the start allows me to work on it separately without touching routes. This should make it easier for me to progress and avoiding troubleshooting several parts of the projects simultaneously. I.e, is it the route or the LLM integration. 

```
    comma-sense/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── data.py
│   └── chain/
├── pyproject.toml
├── README.md
├── .gitignore
└── .env
```