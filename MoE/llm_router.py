import requests


class LLMRouter:
    def __init__(self, model="llama3"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def route(self, query: str) -> str:
        prompt = f"""
    You are an AI query router.

    Classify the query into ALL applicable categories:

Options:
- math
- code
- retrieval

Return as comma-separated list.

Examples:
"2+2" → math
"Explain recursion with code" → retrieval,code
"Write Python code" → code
"What is Python?" → retrieval

    ---

    Now classify:

    Return as comma-separated list.

    Query:
    {query}

    Answer:
    """

        response = requests.post(self.url, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0
        })

        result = response.json()["response"].strip().lower()

        routes = [r.strip() for r in result.split(",")]

        valid = {"math", "code", "retrieval"}

        return [r for r in routes if r in valid] or ["retrieval"]