import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from tools.analyzer import analyze_code
from tools.advisor import advise_on_code
from pydantic import BaseModel

mcp = FastMCP("MCP server")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@mcp.tool()
def analyze(code: str) -> list[TextContent]:
    """
    Analyze the given Python code and return feedback.
    """
    static_feedback = analyze_code(code)
    ai_feedback = advise_on_code(code)

    combined = "\n".join([
        f"{item['message']}" for item in static_feedback + ai_feedback
    ])

    return [TextContent(type="text", text=combined)]

class CodeRequest(BaseModel):
    code: str

@app.post("/analyze")
def analyze_endpoint(request: CodeRequest):
    results = analyze(request.code)  
    return {"feedback": [r.text for r in results]}

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
