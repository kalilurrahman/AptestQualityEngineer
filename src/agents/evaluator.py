from src.state.state import AgentState, TestScenario
from src.utils.llm import call_llm
import json

def evaluator_agent(state: AgentState) -> dict:
    """
    Evaluates the test execution against expected results using LLM-as-a-Judge.
    """
    print("[Evaluator] Evaluating results with LLM...")
    final_verdict = state.get("final_verdict", "unknown")
    logs = state.get("execution_logs", [])
    screenshots = state.get("screenshots", [])

    test_plan = state.get("test_plan", [])
    current_index = state.get("current_scenario_index", 0)

    scenario = None
    if current_index < len(test_plan):
        scenario_data = test_plan[current_index]
        scenario = TestScenario(**scenario_data)

    if final_verdict == "failed" and state.get("retry_count", 0) >= 3:
        # If execution failed after retries, it's definitely a failure.
        print(f"[Evaluator] Scenario '{scenario.title}' FAILED (Execution Error).")
        logs.append(f"VERDICT: FAILED - {scenario.title}")
        return {
            "execution_logs": logs,
            "final_verdict": "failed"
        }

    # Use LLM to judge success based on logs/screenshots if execution didn't crash
    prompt = f"""
    You are an Expert QA Evaluator.
    Judge whether the test scenario passed or failed based on the execution logs and expected result.

    Scenario: {scenario.title}
    Expected Result: {scenario.expected_result}

    Execution Logs:
    {json.dumps(logs[-10:], indent=2)}

    Did the test pass?
    Return ONLY "PASSED" or "FAILED".
    If unclear, default to "FAILED".
    """

    try:
        # If we have screenshots, we could use vision too, but let's stick to logs for simplicity unless needed
        verdict = call_llm(prompt, capability="reasoning").strip().upper()

        if "PASSED" in verdict:
            print(f"[Evaluator] LLM Verdict: PASSED for '{scenario.title}'")
            final_verdict = "passed"
        else:
            print(f"[Evaluator] LLM Verdict: FAILED for '{scenario.title}'")
            final_verdict = "failed"

    except Exception as e:
        print(f"[Evaluator] Error evaluating: {e}")
        final_verdict = "failed"

    logs.append(f"VERDICT: {final_verdict.upper()} - {scenario.title}")

    return {
        "execution_logs": logs,
        "final_verdict": final_verdict
    }
