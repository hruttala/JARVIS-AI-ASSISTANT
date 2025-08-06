# prompt_lab.py

from ollama_interface import ask_ollama


# ----------------------------------------
# 1. Run a single prompt directly
# ----------------------------------------
def run_prompt(prompt: str) -> str:
    response = ask_ollama(prompt)
    print("\n[🧠 Response]")
    print(response.strip())
    return response.strip()


# ----------------------------------------
# 2. Generate N variants of a base prompt
# ----------------------------------------
def compare_variants(prompt: str, n: int = 3) -> list:
    variant_prompt = f"""
Generate {n} different rewrites of the following prompt that vary in tone, phrasing, or structure but retain the same meaning.

Prompt:
{prompt}

Output:
"""
    response = ask_ollama(variant_prompt)
    variants = [line.strip("- ").strip() for line in response.strip().splitlines() if line.strip()]
    print("\n[🌀 Prompt Variants]")
    for i, variant in enumerate(variants[:n], start=1):
        print(f"{i}. {variant}")
    return variants[:n]


# ----------------------------------------
# 3. Evaluate multiple prompts (which is better?)
# ----------------------------------------
def evaluate_prompts(variants: list[str]) -> str:
    numbered = "\n".join([f"{i+1}. {v}" for i, v in enumerate(variants)])
    eval_prompt = f"""
You are a prompt engineering expert. Evaluate the following {len(variants)} prompt variants based on effectiveness, clarity, and detail.

{numbered}

Which one is best and why? Respond with a short evaluation.
"""
    response = ask_ollama(eval_prompt)
    print("\n[🔍 Evaluation]")
    print(response.strip())
    return response.strip()


# ----------------------------------------
# 4. Full cycle: generate + evaluate
# ----------------------------------------
def lab_test(prompt: str, n: int = 3) -> dict:
    variants = compare_variants(prompt, n)
    evaluation = evaluate_prompts(variants)
    return {
        "original": prompt,
        "variants": variants,
        "evaluation": evaluation
    }


# ----------------------------------------
# 5. Jarvis Intent Integration
# ----------------------------------------
def prompt_lab_from_intent(params: dict) -> dict:
    base_prompt = params.get("prompt", "")
    n = params.get("n", 3)
    return lab_test(base_prompt, n)