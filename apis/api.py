from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import sys
import uvicorn

# Fix import path (so client.py and add_tools can be imported)
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import your existing logic
from add_tools import add_tool
from client import run_agent_query

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development, allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows POST, GET, etc.
    allow_headers=["*"], # Allows Content-Type, Authorization, etc.
)

# dynamic correct path to server.py
SERVER_PATH = str(Path(__file__).resolve().parent.parent / "server.py")


# Request Models
class ToolRequest(BaseModel):
    tool_name: str
    description: str
    code: str


class AgentRequest(BaseModel):
    query: str



# Routes

# Add new tool dynamically
@app.post("/add-tool")
def add_tool_api(tool: ToolRequest):
    result = add_tool(
        name=tool.tool_name,
        description=tool.description,
        code=tool.code,
        server_path=SERVER_PATH
    )
    return result


# Run autonomous agent
@app.post("/ask")
async def run_agent(req: AgentRequest):
    try:
        response = await run_agent_query(req.query)
        return {
            "status": "success",
            "query": req.query,
            "answer": response
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


#  Run Server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
