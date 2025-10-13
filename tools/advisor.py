from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def advise_on_code(code: str):
    """
    Send the code to OpenAI to get AI-powered advice.
    Returns a list of suggestions.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Python code reviewer. Provide clear, concise suggestions and improvements."},
            {"role": "user", "content": f"Review the following Python code and give advice:\n\n{code}"}
        ],
        temperature=0.3
    )

    advice_text = response.choices[0].message.content.strip()

    return [{"type": "ai", "message": advice_text}]
