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
        return PromptBuilderOutput(prompt=prompt, question=data.question)
    
class LLMRunner:
    name: str = "llm_runner"
    model_name: str = "HuggingFaceTB/SmolLM2-135M-Instruct"
    pipe: object = None

    def model_post_init(self, __context) -> None:
        print(f"Loading {self.model_name} to memory")
        self.pipe = pipeline("text-generation", self.model_name)
        print("{self.model_name} loaded successfully")

    def invoke(self, data: PromptbuilderOutput) -> LLMRunnerOutput:
        message = [{"role": "user", "content": data.prompt}]
        output = self.pipe(messages, max_new_tokens=150)
        raw_response = output[0]["generated_text"][-1]["content"]
        return LLMRunnerOutput(raw_response=raw_response, question=data.question)