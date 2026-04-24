from fastmcp import Client
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



#  TOOL SCHEMA

async def get_tools_schema(client):
    tools = await client.list_tools()
    return [{"name": t.name, "description": t.description} for t in tools]



#  AGENT STEP (LLM DECISION)

def agent_step(messages, tools):
    prompt = f"""
You are an intelligent autonomous agent.

Available tools:
{tools}

IMPORTANT:
- Each tool includes its expected arguments
- Extract ONLY required arguments
- Do NOT include extra words
- Return STRICT JSON

Decide next step:
- If a tool is needed → return tool call
- If final answer is ready → return final answer

Format:
{{"tool": "...", "arguments": {{...}}}}
OR
{{"final_answer": "..."}}
"""

    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages + [{"role": "system", "content": prompt}],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)


#  AGENT LOOP

async def agent_loop(client, user_input, tools):
    messages = [{"role": "user", "content": user_input}]

    for _ in range(5):
        decision = agent_step(messages, tools)

        if "final_answer" in decision:
            final = decision["final_answer"]

            if isinstance(final, str):
                return final
            else:
                return json.dumps(final)

        tool_name = decision["tool"]
        arguments = decision.get("arguments", {})

        print("\nAgent chose:", tool_name)
        print("Arguments:", arguments)

        try:
            result = await client.call_tool(
                tool_name,
                {"input_data": arguments}
            )

            print("Tool Output:", result.data)

            messages.append({
                "role": "assistant",
                "content": json.dumps(decision)
            })

            messages.append({
                "role": "system",
                "content": f"Tool result: {result.data}"
            })

        except Exception as e:
            print("Tool failed:", str(e))

            messages.append({
                "role": "system",
                "content": f"Tool call failed: {str(e)}. Fix and retry."
            })

    return "Agent could not complete the task."



#  MAIN ENTRY (USED BY API)

async def run_agent_query(user_input: str):
    client = Client(transport="http://127.0.0.1:8011/mcp")

    async with client:
        tools = await get_tools_schema(client)
        return await agent_loop(client, user_input, tools)


