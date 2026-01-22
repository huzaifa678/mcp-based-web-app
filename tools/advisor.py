import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MCP_URL = "http://localhost:8000/mcp/analyze"

def advise_on_code(code: str, token: str):
    """
    Let the agent decide whether to call MCP tool. 
    """
    
    decision_prompt = (
        "You are a Python code reviewer. "
        "Given the following code, should you use the MCP analysis tool "
        "to get more detailed feedback? Answer only 'yes' or 'no'.\n\n"
        f"Code:\n{code}"
    )
    
    decision_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": decision_prompt}],
        temperature=0
    )
    
    decision_text = decision_resp.choices[0].message.content.strip().lower()
    
    mcp_feedback = None
    if decision_text.startswith("yes"):
        response = requests.post(
            MCP_URL,
            headers={"Authorization": f"Bearer {token}"},
            json={"code": code}
        )
        response.raise_for_status()
        mcp_feedback = response.json()
    
    final_prompt = (
        "You are a Python code reviewer. "
        "Provide clear, concise suggestions and improvements.\n\n"
        f"Code:\n{code}"
    )
    if mcp_feedback:
        final_prompt += f"\n\nMCP feedback:\n{mcp_feedback}"
    
    final_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": final_prompt}],
        temperature=0.3
    )
    
    advice_text = final_resp.choices[0].message.content.strip()
    return [{"type": "ai", "message": advice_text}]
