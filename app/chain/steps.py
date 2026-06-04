from app.schemas import PromptBuilderInput, PromptBuilderOutput, LLMRunnerOutput, ResponseParserOutput
from app.chain.runnable import Runnable

class PromptBuilder(Runnable[PromptBuilderInput, PromptBuilderOutput]):
    name: str = "prompt_builder"

    def invoke(self, data: PromptBuilderInput) -> PromptBuilderOutput:
        # Format data stats dict into text.
        stats_text = f"\n Stats for the dataset\n"
        for column, values in data.stats.items():
            stats_text += f"\n{column}:\n"
            for stat_name, stat_value in values.items():
                stats_text += f"    {stat_name}: {stat_value}\n"
        
        instructions = "Du är en dataanalytiker som svarar på frågor om ett dataset."

        prompt = f"""{instructions}
        {stats_text}
        Question: {data.question}
        """
        return PromptBuilderOutput(prompt=prompt)