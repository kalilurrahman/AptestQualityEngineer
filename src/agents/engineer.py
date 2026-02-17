from src.state.state import AgentState, TestScenario
from src.utils.llm import call_llm
import json

def engineer_agent(state: AgentState) -> dict:
    """
    Converts the current test scenario into tool calls using the LLM.
    """
    print("[Engineer] Generating execution steps with LLM...")

    test_plan_data = state.get("test_plan", [])
    current_index = state.get("current_scenario_index", 0)

    if current_index >= len(test_plan_data):
        return {"execution_logs": ["All scenarios completed or no scenarios found."]}

    scenario_data = test_plan_data[current_index]
    scenario = TestScenario(**scenario_data)

    print(f"[Engineer] Processing scenario: {scenario.title}")

    prompt = f"""
    You are an Expert Test Engineer.
    Convert the following Test Scenario into a sequence of Tool Calls for a browser automation agent.

    Scenario: {scenario.title}
    Steps: {scenario.steps}
    Expected Result: {scenario.expected_result}

    Available Tool:
    - interact_with_ui(action: str, description: str, value: Optional[str])

    Actions: "click", "type", "hover", "navigate", "wait"

    Output Format (JSON List of Tool Calls):
    [
        {{"tool": "interact_with_ui", "args": {{"action": "navigate", "description": "https://example.com/login"}}}},
        {{"tool": "interact_with_ui", "args": {{"action": "type", "description": "username field", "value": "testuser"}}}},
        {{"tool": "interact_with_ui", "args": {{"action": "click", "description": "login button"}}}}
    ]

    Rules:
    1. Use "navigate" for URLs.
    2. Use "type" for input fields. "description" should be a visual description (e.g., "blue search bar"). "value" is the text to type.
    3. Use "click" for buttons/links. "description" should describe the element visually or semantically.
    4. Return ONLY valid JSON.
    """

    try:
        response_text = call_llm(prompt, capability="coding", structured_output_schema=True)
        # Sanitize
        cleaned_text = response_text.replace("```json", "").replace("```", "").strip()

        tool_calls = json.loads(cleaned_text)

        current_test_context = state.get("current_test_context", {})
        current_test_context["execution_plan"] = tool_calls

        return {
            "current_test_context": current_test_context,
            "execution_logs": [f"Generated execution plan for scenario: {scenario.title}"]
        }
    except Exception as e:
        print(f"[Engineer] Error generating code: {e}")
        return {
            "execution_logs": [f"Error generating execution plan: {e}"],
            "error": str(e)
        }
