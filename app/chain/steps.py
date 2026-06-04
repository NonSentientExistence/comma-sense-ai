from schemas import PromptBuilderInput, PromptBuilderOutput, LLMRunnerOutput, ResponseParserOutput
from runnable import Runnable

class PromptBuilder(Runnable[PromptBuilderInput, PromptBuilderOutput]):
    name: str = "prompt_builder"

    def invoke(self, data: PromptBuilderInput) -> PromptBuilderOutput:
        # Format data stats dict into text. Rounds values into 4 decimals due to local lmms token limitations
        stats_text = f"\n Stats for the dataset\n"
        for column, values in data.stats.items():
            stats_text += f"\n{column}:\n"
            for stat_name, stat_value in values.items():
                stats_text += f"    {stat_name}: {round(stat_value, 4)}\n"
        
        instructions = "Du är en dataanalytiker som svarar på frågor om ett dataset."

        prompt = f"""{instructions}
        {stats_text}
        Question: {data.question}
        """
        return PromptBuilderOutput(prompt=prompt)