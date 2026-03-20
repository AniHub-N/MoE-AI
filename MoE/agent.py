from llm_router import LLMRouter
from math_expert import MathExpert
from code_expert import CodeExpert
from retrieval_expert import RetrievalExpert


class MoESystem:
    def __init__(self):
        self.router = LLMRouter()
        self.math_expert = MathExpert()
        self.code_expert = CodeExpert()
        self.retrieval_expert = RetrievalExpert()

    # Security layer
    def is_malicious(self, query: str) -> bool:
        blacklist = [
            "ignore all instructions",
            "developer mode",
            "internal prompt",
            "system prompt",
            "jailbreak"
        ]
        return any(word in query.lower() for word in blacklist)
    
    def filter_routes(self, routes, query):
        filtered = []

        query_lower = query.lower()

        for r in routes:
            if r == "math":
                # only allow math if numbers present
                if any(char.isdigit() for char in query):
                    filtered.append(r)

            else:
                filtered.append(r)

        return filtered

    # Combine outputs from multiple experts
    def combine_responses(self, responses):
        final = {
            "answer": None,
            "code": None,
            "math": None
        }

        for res in responses:
            if not isinstance(res, dict):
                continue

            if res.get("type") == "retrieval":
                final["answer"] = res.get("answer")

            elif res.get("type") == "code":
                code = res.get("code")
                if code and "Invalid" not in code:
                    final["code"] = code

            elif res.get("type") == "math":
                final["math"] = res.get("result")

        return {k: v for k, v in final.items() if v is not None}

    def handle_query(self, query: str):
        print(f"\n[System] Query: {query}")

        # Security
        if self.is_malicious(query):
            response = {
                "type": "blocked",
                "message": "Request denied due to security policy."
            }
            print(f"[System] Response: {response}")
            return response

        # Routing (MULTI)
        routes = self.router.route(query)
        routes = self.filter_routes(routes, query)

        # Not exactly hardcoded, but a safety net for weird LLM outputs. The router should ideally catch these.
        query_lower = query.lower()

        if "code" in query_lower or "python" in query_lower:
            if "code" not in routes:
                routes.append("code")

        if any(char.isdigit() for char in query_lower):
            if any(op in query_lower for op in "+-*/"):
                if "math" not in routes:
                    routes.append("math")

        routes = list(set(routes))

        print(f"[Router] Selected: {routes}")

        responses = []

        # Execute ALL relevant experts
        for route in routes:

            if route == "math":
                res = self.math_expert.solve(query)
                responses.append(res)

            elif route == "code":
                res = self.code_expert.solve(query)

                # Code validation
                if isinstance(res, dict) and "code" in res:
                    code = res.get("code")
                    if not code or "def " not in code or "return" not in code:
                        res["code"] = "Invalid code generated. Please refine query."

                responses.append(res)

            elif route == "retrieval":
                res = self.retrieval_expert.solve(query)
                responses.append(res)

        # Combine outputs
        final_response = self.combine_responses(responses)

        print(f"[System] Response: {final_response}")
        return final_response



if __name__ == "__main__":
    system = MoESystem()

    while True:
        query = input("\nEnter query (or 'exit'): ")

        if query.lower() == "exit":
            break

        system.handle_query(query)