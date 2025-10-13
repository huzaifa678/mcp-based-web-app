import ast

def analyze_code(code: str):
    """
    Perform static analysis on Python code.
    Returns a list of feedback messages.
    """
    feedback = []

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        feedback.append({
            "type": "error",
            "message": f"Syntax error: {e}"
        })
        return feedback

    # Check all functions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not ast.get_docstring(node):
                feedback.append({
                    "type": "warning",
                    "message": f"Function '{node.name}' has no docstring."
                })
            if len(node.body) > 30:
                feedback.append({
                    "type": "suggestion",
                    "message": f"Function '{node.name}' is too long (>30 lines). Consider refactoring."
                })

    # Check for TODO comments
    if "TODO" in code:
        feedback.append({
            "type": "reminder",
            "message": "Your code contains TODO comments. Consider completing them."
        })

    return feedback
