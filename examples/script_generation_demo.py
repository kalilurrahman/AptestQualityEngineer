import os
import sys

# Add src to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.llm import call_llm

def generate_script(scenario_desc: str):
    print(f"Generating Playwright script for: {scenario_desc}")

    prompt = f"""
    You are an Expert Automation Engineer.
    Write a complete, executable Python script using Playwright (sync API) to automate the following test scenario.

    Scenario: {scenario_desc}

    Requirements:
    - Use `sync_playwright`.
    - Include comments explaining the steps.
    - Use robust selectors (e.g., get_by_role, get_by_label).
    - Handle potential timeouts or errors gracefully.
    - Assert the expected outcome.

    Return ONLY the Python code. Do not include markdown blocks.
    """

    try:
        script_content = call_llm(prompt, capability="coding")
        script_content = script_content.replace("```python", "").replace("```", "").strip()

        filename = f"examples/scripts/generated_test_{os.urandom(4).hex()}.py"
        with open(filename, "w") as f:
            f.write(script_content)

        print(f"Script generated successfully: {filename}")
        print("-" * 40)
        print(script_content)
        print("-" * 40)

    except Exception as e:
        print(f"Error generating script: {e}")

if __name__ == "__main__":
    scenario = "Login to https://saucedemo.com with standard_user / secret_sauce, add the first item to cart, and verify cart badge shows '1'."
    generate_script(scenario)
