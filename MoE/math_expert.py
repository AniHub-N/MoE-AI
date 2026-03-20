import re
import requests


class MathExpert:
    def __init__(self, model="llama3"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    # Fast path (regex)
    def extract_expression(self, query: str) -> str:
        matches = re.findall(r"[0-9\+\-\*\/\.\(\)\s]+", query)
        matches = [m.strip().replace(" ", "") for m in matches if m.strip()]

        if not matches:
            return ""

        return max(matches, key=len)

    # Detect weak extraction
    def is_weak_expression(self, expression: str) -> bool:
        numbers = re.findall(r"\d+", expression)
        has_operator = any(op in expression for op in "+-*/")

        return len(numbers) < 2 or not has_operator

    # LLM parsing (no hardcoding)
    def llm_parse_expression(self, query: str) -> str:
        print("[MathExpert] Using LLM to parse...")

        prompt = f"""
Convert the following into a valid Python arithmetic expression.

Rules:
- Return ONLY the expression
- No words
- No explanation
- No equals sign

Examples:
"10 boys and 5 girls" → 10 + 5
"50 divided by 5" → 50 / 5

Query:
{query}

Expression:
"""

        response = requests.post(self.url, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0
        })

        return response.json()["response"].strip()

    # Safety check
    def is_safe_expression(self, expr: str) -> bool:
        return all(c in "0123456789+-*/(). " for c in expr)

    # Clean expression
    def clean_expression(self, expression: str) -> str:
        return re.sub(r'\b0+(\d)', r'\1', expression)

    # Validate structure
    def is_valid_expression(self, expression: str) -> bool:
        operators = ["+", "-", "*", "/"]

        if not any(op in expression for op in operators):
            return False

        if expression[0] in operators:
            return False

        if expression[-1] in operators:
            return False

        return True


    def compute(self, expression: str):
        try:
            return eval(expression)
        except Exception as e:
            return f"Error: {str(e)}"


    def solve(self, query: str):
        print(f"[MathExpert] Query: {query}")

        # Step 1: regex extraction
        expression = self.extract_expression(query)

        # Step 2: fallback if weak
        if not expression or self.is_weak_expression(expression):
            expression = self.llm_parse_expression(query)

        print(f"[MathExpert] Expression: {expression}")

        # Step 3: safety
        if not self.is_safe_expression(expression):
            return "Unsafe or invalid expression."

        # Step 4: clean
        expression = self.clean_expression(expression)

        # Step 5: validate
        if not self.is_valid_expression(expression):
            return "Invalid or incomplete math expression."

        # Step 6: compute
        result = self.compute(expression)

        return {
            "type": "math",
            "input": expression,
            "result": result
        }


#Test
if __name__ == "__main__":
    m = MathExpert()

    tests = [
        "2+3*4",
        "There are 5 red and 7 blue crayons, total?",
        "50 divided by 5",
        "007 +",
        "hello"
    ]

    for t in tests:
        print("\n---")
        print(m.solve(t))