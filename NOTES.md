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

Added model_name without hardcoded value, intent is to allow user to choose model for the response. Initial default will be SmolLM2-135M-Instruct.
Want to test other models such as SmolLM2-360M-Instruct, Qwen2.5-0.5B-Instruct, Qwen2.5-1.5B-Instruct which are still runnable on CPU. 

### Testing

- 1. First test ensure that question and stats are included in the Promptbuilder
- 2. LLM response includes answer works but is prompting the real model. Changed to mocked LLMRunner

### Idea notes
- Test other tasks for pupteline such as sentiment-analysis or translation

### Notes for self

Transformers needs torch or a differemt backend installed to actually run the models.

First response from LLM, mostly rambles but a response still. 
    question='What game sold the most?' answer="1. Sales-Millions: This dataset shows the total number of units sold for the 22.93 million units of the company's sales-millions dataset.\n\n2. Mean: The mean of the sales-millions dataset is 22.93 million units sold.\n\n3. Max: The maximum number of units sold is also 61.0 million units.\n\nSo, the dataset shows the average number of units sold per customer for the company's sales-millions dataset, which are 22.93 million units." model='HuggingFaceTB/SmolLM2-135M-Instruct'
