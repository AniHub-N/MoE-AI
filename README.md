# Mixture of Experts (MoE) AI System

A modular AI system inspired by
**Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity**
*(Journal of Machine Learning Research 23 (2022) 1–40)*


---

## Core Idea

Instead of using one monolithic model:

```
Input → One Model → Output 
```

I built a **Mixture of Experts system**:

```
User Query
    ↓
LLM Router (decision)
    ↓
 ┌───────────────┬───────────────┬───────────────┐
 ↓               ↓               ↓
Math Expert   Code Expert   Retrieval Expert     ...
    ↓               ↓               ↓
        Combined Final Response
```

---

## What This Project Demonstrates

This is NOT just a project — it’s a **systems-level implementation of MoE principles**:

*  Learned routing (LLM as gating network)
*  Specialized experts
*  Parallel execution
*  Output aggregation
*  Validation + retry loops
*  Hybrid (neural + symbolic) reasoning

---

## Features

### Intelligent Routing

* LLM-based router (`llama3`)
* Multi-label classification (multiple experts per query)
* Hybrid routing (LLM + rule-based boosting)

---

### Math Expert

* Regex-based fast extraction
* LLM fallback for word problems
* Safe execution
* Expression validation

---

### Code Expert

* Uses `deepseek-coder`
* Strict prompting
* Code extraction layer
* Comment stripping
* Compile validation
* Retry mechanism for bad generations

---

### Retrieval Expert

* General-purpose reasoning
* Explanation generation

---

### Output Pipeline

```
Generate → Extract → Clean → Validate → Retry → Return
```

---

### Safety Layer

* Basic prompt injection detection
* Output validation to prevent malformed responses

---

## System Architecture

```
Query
  ↓
LLM Router (llama3)
  ↓
Route Filtering + Boosting
  ↓
Parallel Expert Execution
  ↓
Response Combination
  ↓
Final Structured Output
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/moe-ai-system.git
cd moe-ai-system
```

---

### 2. Install Dependencies

```bash
pip install requests
```

---

### 3. Install Ollama (Local LLMs)

Download and install: https://ollama.com/

---

### 4. Pull Required Models

```bash
ollama pull llama3 (preffered)
ollama pull deepseek-coder
```

---

### 5. Run the System

```bash
python agent.py
```

---

## Example Usage

### Input:

```
Explain recursion and give Python code
```

### Output:

```json
{
  "answer": "\n\nRecursion is a programming technique where a function calls itself repeatedly until it reaches a base case that stops the recursion.
             In other words, a function solves a problem by breaking it down into smaller instances of the same problem,
             which are then solved using the same function.",
  "code": "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
}
```

---

## Key Learnings & Insights

### 1. **LLMs ≠ Systems**

A single LLM is not enough. Real power comes from:

> routing + specialization + control

---

### 2. **Routing is the Core of MoE**

The hardest problem wasn’t generation — it was:

> deciding *which expert(s)* should handle the query

---

### 3. **Model Specialization Matters**

* `deepseek-coder` → great for code (but always chose math or code routes)
* `llama3` → better for reasoning/routing

 Different tasks require different models

---

### 4. **LLMs Are Stochastic**

Same input ≠ same output
→ Needed temperature control + validation

---

### 5. **Output Cannot Be Trusted**

LLMs:

* ignore instructions
* mix text with code
* hallucinate syntax

Solution:

```
Extract → Clean → Validate → Retry
```

---

### 6. **Validation > Prompting**

Prompt engineering alone is NOT enough.

Real systems:

* enforce structure
* verify correctness
* reject bad outputs

---

### 7. **Neuro-Symbolic Systems Are Powerful**

Math expert combines:

* LLM understanding
* Python execution

Best of both worlds

---

### 8. **Multi-Expert > Single Expert**

Queries often require:

* explanation + code
* reasoning + computation

---

### 9. **Over-Triggering vs Under-Triggering**

We faced:

* too many experts firing
  (or)
* too few experts firing 

Finally:

> Hybrid routing (LLM + heuristics)

---

### 10. **Retry Loops Are Essential**

Bad outputs are normal.

Good systems:

```
Generate → Check → Fix → Return
```

---

## Problems Faced (and Solved)

### Router Misclassification

* Everything routed to math initially
* Fixed via better prompts + model switch + boosting

---

### Code Generation Noise

* Explanations inside code
* Fixed via extraction + comment stripping

---

### Invalid Code

* Broken syntax
* Fixed via `compile()` validation

---

### Incomplete Logic

* Missing return statements
* Fixed via structural validation

---

### Double Execution Bug

* Caused by self-import
* Fixed using `if __name__ == "__main__"`

---

### Over-Reliance on Regex

* Failed on word problems
* Fixed via LLM parsing

---

### Prompt Injection Risk

* Basic filtering added

---

## Interesting Observations

* LLMs follow instructions **probabilistically**, not deterministically
* Strict prompts can cause **under-generation**
* Loose prompts cause **over-generation**
* The real solution is **post-processing, not prompting**
* Combining simple components creates powerful systems

---

## What This Project Really Is

This is a simplified version of:

* ChatGPT tool usage
* LangChain agents
* Production AI pipelines
* Switch Transformer routing (conceptually)

---

## Future Improvements

* Expert collaboration (not just parallel execution)
* Memory layer (context awareness)
* Confidence-based routing
* Code execution sandbox
* RAG-based retrieval expert
* Evaluation framework

---

## Inspiration

Based on:

> **Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity**
    Journal of Machine Learning Research 23 (2022) 1–40
> Refer to it here : https://arxiv.org/pdf/2101.03961

---

## ⭐ If You Found This Useful

 - Star the repo :)
 - Try out the system
 - Share and insights
 - Connect :)

