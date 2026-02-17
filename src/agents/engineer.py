from src.state.state import AgentState, TestScenario

def engineer_agent(state: AgentState) -> dict:
    """
    Converts the current test scenario into tool calls.
    (Mocked: Maps steps to tool calls)
    """
    print("[Engineer] Generating execution steps...")

    test_plan_data = state.get("test_plan", [])
    current_index = state.get("current_scenario_index", 0)

    if current_index >= len(test_plan_data):
        return {"execution_logs": ["All scenarios completed or no scenarios found."]}

    scenario_data = test_plan_data[current_index]
    scenario = TestScenario(**scenario_data)

    print(f"[Engineer] Processing scenario: {scenario.title}")

    # Generate tool calls based on steps (Mock Logic)
    # The output format will be a list of dictionaries that the Executor can iterate over.
    tool_calls = []
    for step in scenario.steps:
        if step.startswith("Navigate to "):
            url = step.replace("Navigate to ", "").strip()
            tool_calls.append({"tool": "interact_with_ui", "args": {"action": "navigate", "description": url}})
        elif step.startswith("Enter "):
            desc = step.replace("Enter ", "").strip()
            tool_calls.append({"tool": "interact_with_ui", "args": {"action": "type", "description": desc, "value": "test_value"}})
        elif step.startswith("Click "):
            desc = step.replace("Click ", "").strip()
            tool_calls.append({"tool": "interact_with_ui", "args": {"action": "click", "description": desc}})
        elif step.startswith("Wait "):
             tool_calls.append({"tool": "interact_with_ui", "args": {"action": "wait", "description": "Wait for element", "value": "2"}})

    current_test_context = state.get("current_test_context", {})
    current_test_context["execution_plan"] = tool_calls

    return {
        "current_test_context": current_test_context,
        "execution_logs": [f"Generated execution plan for scenario: {scenario.title}"]
    }
