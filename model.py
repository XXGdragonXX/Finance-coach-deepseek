from groq import Groq


# Initialize the Groq client

client = Groq(api_key="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")

class LLM_model():
    def __init__(self,prompt,model_name = "deepseek-r1-distill-llama-70b"):
        self.model_name = model_name
        self.prompt = prompt

    def llm_model(self):
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user", 
                    "content": self.prompt
                }
            ]
        )
        response_content = response.choices[0].message.content

        return response_content
