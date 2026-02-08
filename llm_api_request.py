import os
import base64
from enum import Enum
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam

load_dotenv()

class Model(Enum):
    DEEPSEEK_R1T2_CHIMERA = "tngtech/deepseek-r1t2-chimera:free"
    GEMMA_3_27B_IT = "google/gemma-3-27b-it:free"
    

class LLMsAPIRequests:
    def __init__(self, prompt: str, image_bytes = None, host_url: str = ""):
        self.host_url = host_url
        self.prompt: str = prompt
        self.image_path = image_bytes
        self.client = OpenAI(
            base_url=os.environ.get("API_BASE_URL"),
            api_key=os.getenv("API_KEY_2"),
        )
        if image_bytes is not None:
            self.model: str = Model.GEMMA_3_27B_IT.value
            base64_image = base64.b64encode(image_bytes).decode("utf-8")
            self.messages: list[ChatCompletionUserMessageParam] = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": self.prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url" : f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }]
        else:
            self.model: str = Model.DEEPSEEK_R1T2_CHIMERA.value
            self.messages: list[ChatCompletionUserMessageParam] = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": self.prompt
                    }
                ]
            }]



    def get_response(self):
        completion = self.client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": f"{self.host_url}", # Optional. Site URL for rankings on openrouter.ai.
                "X-Title": "Chemini", # Optional. Site title for rankings on openrouter.ai.
            },
            model=self.model,
            extra_body={"reasoning": {"enabled": True}},
            messages=self.messages,
        )
        return completion.choices[0].message.content