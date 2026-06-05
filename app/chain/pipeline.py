from app.chain.steps import PromptBuilder, LLMRunner, ResponseParser

oraklet = PromptBuilder() | LLMRunner() | ResponseParser()

if __name__ == "__main__":
    from app.schemas import PromptBuilderInput

    test_input = PromptBuilderInput(
        question="What game sold the most?",
        stats={"sales_millions": {"mean": 22.93, "max": 61.0}}
    )
    result = oraklet.invoke(test_input)
    print(result)