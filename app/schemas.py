from pydantic import BaseModel

# Prompt for AI, user input
class PromptBuilderInput(BaseModel):
    question: str
    stats: dict
# Completed user input prompt
class PromptBuilderOutput(BaseModel):
    prompt: str
    question: str
# Raw output from the AI
class LLMRunnerOutput(BaseModel):
    raw_response: str
    question: str
# Cleaned response to user
class ResponseParserOutput(BaseModel):
    question: str
    answer: str
    model: str