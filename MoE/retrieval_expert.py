import requests


class RetrievalExpert:
    def __init__(self, model="llama3"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def solve(self, query: str):
        print("[RetrievalExpert] Generating answer...")

        prompt = f"""
Answer the question clearly and concisely.

Question:
{query}

Answer:
"""

        response = requests.post(self.url, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.3
        })

        result = response.json()["response"]

        return {
            "type": "retrieval",
            "answer": result.strip()
        }