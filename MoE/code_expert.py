import requests
import re


class CodeExpert:
    def __init__(self, model="deepseek-coder"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def extract_code_block(self, text: str) -> str:
        # Try markdown block first
        match = re.search(r"```python(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()

        # fallback: find lines that look like code
        lines = text.split("\n")
        code_lines = []

        for line in lines:
            if line.strip().startswith(("def ", "for ", "while ", "if ", "return", "print")):
                code_lines.append(line)

        return "\n".join(code_lines).strip()

    def generate_code(self, query: str):
        prompt = f"""
    You are a strict Python code generator.

    Return ONLY valid, complete Python code.

    Requirements:
    - Must include function definition if applicable
    - No explanations
    - No markdown
    - No comments
    - Code should be executable as-is

    Task:
    {query}

    Output:
    """

        response = requests.post(self.url, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0
        })

        result = response.json()

        return result["response"]
    

    def clean_code(self, response: str) -> str:
        import re

        # remove markdown
        response = re.sub(r"```.*?\n", "", response)
        response = response.replace("```", "")

        lines = response.split("\n")
        cleaned_lines = []

        for line in lines:
            # remove explanation lines
            if any(phrase in line.lower() for phrase in [
                "here is", "this is", "example", "solution"
            ]):
                continue

            # remove inline comments
            line = line.split("#")[0]

            # remove empty lines after cleaning
            if line.strip():
                cleaned_lines.append(line.rstrip())

        return "\n".join(cleaned_lines).strip()

    def solve(self, query: str):
        print("[CodeExpert] solve() CALLED")
        print("[CodeExpert] Generating code...")

        code = ""

        # First attempt
        raw_code = self.generate_code(query)
        code = self.extract_code_block(raw_code)
        code = self.strip_comments(code) 

        # Retry if invalid
        if not self.is_valid_code(code):
            print("[CodeExpert] Retrying with stricter prompt...")

            retry_prompt = f"""
    Return ONLY clean Python code.

    STRICT RULES:
    - No comments
    - No explanation
    - No extra text
    - Only function definition
    - Must include return

    Task:
    {query}
    """

            response = requests.post(self.url, json={
                "model": self.model,
                "prompt": retry_prompt,
                "stream": False,
                "temperature": 0
            })

            craw_code = response.json()["response"]
            code = self.extract_code_block(raw_code)
            code = self.strip_comments(code)

        # Final validation
        if not self.is_valid_code(code):
            return {
                "type": "code",
                "code": "Failed to generate clean code."
            }

        return {
            "type": "code",
            "code": code
        }
    def is_valid_code(self, code: str) -> bool:
        if not code:
            return False

        # must have function
        if "def " not in code:
            return False

        # must have return
        if "return" not in code:
            return False

        # try compiling
        try:
            compile(code, "<string>", "exec")
        except:
            return False

        return True
    
    def strip_comments(self, code: str) -> str:
        lines = code.split("\n")
        cleaned = []

        for line in lines:
            # remove inline comments
            line = line.split("#")[0]

            if line.strip():
                cleaned.append(line.rstrip())

        return "\n".join(cleaned)

    
    
    
    
if __name__ == "__main__":
    code_expert = CodeExpert()
    print(code_expert.solve("Write Python code to reverse a list"))