import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
    default_headers={"User-Agent": "python-app"}
)

def ask_llm(messages):

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=messages
    )

    return response.choices[0].message.content