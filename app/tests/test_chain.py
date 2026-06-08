from app.schemas import PromptBuilderInput, LLMRunnerOutput
from app.chain.steps import PromptBuilder, ResponseParser
from app.chain.pipeline import oraklet

def test_prompt_builder_has_user_question_and_stats():
    # Hardcoded input for test
    test_input = PromptBuilderInput(
        question="Which game had the highest review score?",
        stats = {"score": {"mean": "92.5", "max": "97"}}
    )

    result = PromptBuilder().invoke(test_input)
    assert "Which game had the highest review score?" in result.prompt
    assert "score" in result.prompt
    assert "mean" in result.prompt
    assert "92.5" in result.prompt

def test_PromptBuilderInput_gets_answer_from_LLM():
# Should mock LLMRunner, will fix later
    # Mocked response from LLMRunner
    mock_llm_output = LLMRunnerOutput(
        raw_response= "    Elden Ring sold the most with 61.0 million units.  ",
        question = "What game sold the most?"
    )

    # Run the parser step
    result = ResponseParser().invoke(mock_llm_output)

    # Can be shortened to assert result.answer as both are falsy
    assert result.answer is not None
    assert result.answer != ""
    # Assert that result has the expected response from mock LLM parser. Assert whitespace has been cleaned
    assert result.answer == "Elden Ring sold the most with 61.0 million units."
    assert result.question == "What game sold the most?"
    assert result.model == "HuggingFaceTB/SmolLM2-135M-Instruct"