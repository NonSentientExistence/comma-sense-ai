## Comma sense AI
#### Small local LMM that analyzes an uploaded CSV and lets you query the AI on the CSV data

### Structure

Initial structure idea for the project. Keeping the chain and LLM integration isolated from the start allows me to work on it separately without touching routes. This should make it easier for me to progress and avoiding debugging several parts of the projects at the same time. I.e, is it the route or the LLM integration. Separation of concerns, each module has one clear responsibility. 

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

Validation could have been its own file but seems like over engeenering for this project. Since the validation is straight forward for now, validation will be kept close to use point.

