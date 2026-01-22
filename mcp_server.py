from fastapi import HTTPException
from fastapi.params import Header
import jwt
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from tools.advisor import advise_on_code
from tools.analyzer import analyze_code
from utils.jwt_token import ALGORITHM, SECRET_KEY

mcp = FastMCP()

@mcp.tool()
def analyze(code: str, authorization: str = Header(...)) -> list[TextContent]:
    """
    Seperate MCP server tool for the same logic.
    """
    token = authorization.replace("Bearer ", "")
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    static_feedback = analyze_code(code)
    ai_feedback = advise_on_code(code)

    combined = "\n".join([
        f"{item['message']}" for item in static_feedback + ai_feedback
    ])

    return [TextContent(type="text", text=combined)]

if __name__ == "__main__":
    mcp.run(host="0.0.0.0", port=9000)
