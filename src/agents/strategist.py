from src.state.state import AgentState, TestPlan, TestScenario
from src.utils.llm import call_llm
import uuid
import json

def strategist_agent(state: AgentState) -> dict:
    """
    Analyzes requirements and generates a test plan using the LLM.
    """
    print("[Strategist] Analyzing requirements with LLM...")
    requirements = state.get("user_requirements", "")

    prompt = f"""
    You are the Chief Architect of Quality Assurance (Strategist Agent).
    Your task is to analyze the following User Requirements and generate a comprehensive Test Plan.

    User Requirements:
    "{requirements}"

    Generate a JSON object containing a list of Test Scenarios.
    Each scenario must have:
    - id: A unique string
    - title: A short descriptive title
    - description: A detailed description of the objective
    - steps: A list of high-level steps (e.g., "Navigate to /login", "Enter valid credentials")
    - expected_result: The expected outcome
    - tags: A list of tags (e.g., "functional", "security", "smoke")

    Output Schema:
    {{
        "scenarios": [
            {{
                "id": "...",
                "title": "...",
                "description": "...",
                "steps": ["..."],
                "expected_result": "...",
                "tags": ["..."]
            }}
        ]
    }}

    Ensure the test plan covers:
    1. Happy Path (Functional)
    2. Edge Cases (Negative Testing)
    3. Security Considerations (if applicable)

    Return ONLY valid JSON.
    """

    try:
        response_text = call_llm(prompt, capability="planning", structured_output_schema=True)
        # Sanitize response (Gemini sometimes adds markdown blocks)
        cleaned_text = response_text.replace("```json", "").replace("```", "").strip()

        data = json.loads(cleaned_text)

        scenarios = []
        for s in data.get("scenarios", []):
            scenarios.append(TestScenario(
                id=s.get("id", str(uuid.uuid4())),
                title=s.get("title", "Untitled Scenario"),
                description=s.get("description", ""),
                steps=s.get("steps", []),
                expected_result=s.get("expected_result", ""),
                tags=s.get("tags", [])
            ))

        # Serialize scenarios to dicts for state compatibility
        test_plan_serialized = [s.model_dump() for s in scenarios]

        return {
            "test_plan": test_plan_serialized,
            "execution_logs": ["Generated test plan using LLM."]
        }

    except Exception as e:
        print(f"[Strategist] Error generating plan: {e}")
        # Fallback to empty or error state
        return {
            "test_plan": [],
            "execution_logs": [f"Error generating test plan: {e}"],
            "error": str(e)
        }
