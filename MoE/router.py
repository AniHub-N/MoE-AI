class Router:
    def __init__(self):
        # simple keyword rules
        self.math_keywords = ["calculate", "solve", "equation", "+", "-", "*", "/"]
        self.code_keywords = ["code", "python", "java", "function", "bug", "program"]
    
    def route(self, query: str) -> str:
        query_lower = query.lower()

        # math routing
        if any(word in query_lower for word in self.math_keywords):
            return "math"

        # code routing
        if any(word in query_lower for word in self.code_keywords):
            return "code"

        # default to retrieval
        return "retrieval"
    

router = Router()

from math_expert import MathExpert

math_expert = MathExpert()


print(math_expert.solve("What is 2 + 3 * 4?"))
print(math_expert.solve("Hello"))