from app.schemas import PromptBuilderInput
from app.chain.steps import PromptBuilder

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