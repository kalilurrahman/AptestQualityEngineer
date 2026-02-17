from src.state.state import AgentState

def healer_agent(state: AgentState) -> dict:
    """
    Analyzes failures and attempts to heal the test.
    """
    print("[Healer] Analyzing failure...")
    error = state.get("error", "")
    retry_count = state.get("retry_count", 0)

    if retry_count >= 3:
        print("[Healer] Max retries reached. Cannot heal.")
        return {"final_verdict": "failed", "retry_count": retry_count}

    print(f"[Healer] Attempting to heal error: {error}. Retry {retry_count + 1}/3")

    # Mock healing logic:
    # If error is about an element not found, we update the plan with a new selector.
    # Here we just retry.

    current_test_context = state.get("current_test_context", {})
    failed_step_index = current_test_context.get("failed_step_index", 0)
    execution_plan = current_test_context.get("execution_plan", [])

    if execution_plan and failed_step_index < len(execution_plan):
        step = execution_plan[failed_step_index]
        # Simulate updating selector using VLM
        original_desc = step['args'].get('description', '')
        print(f"[Healer] Adjusting selector for step {failed_step_index + 1}: {original_desc}")

        # Simple heuristic for demo: append "(healed)"
        step['args']['description'] = f"{original_desc} (healed)"
        execution_plan[failed_step_index] = step
        current_test_context["execution_plan"] = execution_plan

    return {
        "retry_count": retry_count + 1,
        "current_test_context": current_test_context,
        "error": None, # Reset error
        "final_verdict": "in_progress", # Reset verdict so we can loop back
        "execution_logs": [f"Healed step {failed_step_index + 1}. Retrying..."]
    }
