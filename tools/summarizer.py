from openai import OpenAI
import os
import json
import sys
from dotenv import load_dotenv

load_dotenv()

TOOL_NAME = "summarizer"
TOOL_DESCRIPTION = "Summarize text using OpenAI"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def execute(input_data):
    text = input_data.get("text", "")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful summarization assistant."},
            {"role": "user", "content": f"Summarize:\n\n{text}"}
        ],
        temperature=0.2
    )

    summary = response.choices[0].message.content or ""

    return {"summary": summary}


if __name__ == "__main__":
    input_json = json.loads(sys.stdin.read())
    output = execute(input_json)

    # 🔥 CRITICAL LINE
    print(json.dumps(output))