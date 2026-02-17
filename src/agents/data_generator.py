from src.state.state import AgentState, TestScenario
from src.utils.llm import call_llm
import json
import csv
from io import StringIO

def data_generator_agent(state: AgentState) -> dict:
    """
    Generates realistic test data for the test scenarios.
    """
    print("[Data Generator] Generating test data...")
    test_plan = state.get("test_plan", [])

    # Analyze the scenarios to determine data needs
    prompt = f"""
    You are a Test Data Architect.
    Analyze the following Test Scenarios and generate a CSV dataset needed to execute them.

    Scenarios:
    {[s['title'] for s in test_plan]}

    For example, if a scenario is "User Login", generate columns for 'username', 'password', 'role'.
    If "Checkout", generate 'product_id', 'quantity', 'payment_method'.

    Generate 5 rows of realistic, diverse test data.
    Include edge cases (e.g., long strings, special characters) where appropriate.

    Return ONLY the CSV content.
    """

    try:
        csv_content = call_llm(prompt, capability="coding")
        # Sanitize
        csv_content = csv_content.replace("```csv", "").replace("```", "").strip()

        # Parse CSV to validate
        f = StringIO(csv_content)
        reader = csv.DictReader(f)
        data = list(reader)

        print(f"[Data Generator] Generated {len(data)} rows of test data.")

        current_context = state.get("current_test_context", {})
        current_context["test_data"] = data

        return {
            "current_test_context": current_context,
            "execution_logs": ["Generated synthetic test data (5 rows)."]
        }
    except Exception as e:
        print(f"[Data Generator] Error: {e}")
        return {
            "execution_logs": [f"Error generating test data: {e}"]
        }
