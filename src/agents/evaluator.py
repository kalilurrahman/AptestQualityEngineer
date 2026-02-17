from src.state.state import AgentState, TestScenario

def evaluator_agent(state: AgentState) -> dict:
    """
    Evaluates the test execution against expected results.
    """
    print("[Evaluator] Evaluating results...")
    final_verdict = state.get("final_verdict", "unknown")
    logs = state.get("execution_logs", [])

    test_plan = state.get("test_plan", [])
    current_index = state.get("current_scenario_index", 0)

    scenario = None
    if current_index < len(test_plan):
        scenario_data = test_plan[current_index]
        scenario = TestScenario(**scenario_data)

    if final_verdict == "passed":
        print(f"[Evaluator] Scenario '{scenario.title}' PASSED.")
        logs.append(f"VERDICT: PASSED - {scenario.title}")
    elif final_verdict == "failed":
        print(f"[Evaluator] Scenario '{scenario.title}' FAILED.")
        logs.append(f"VERDICT: FAILED - {scenario.title}")
    else:
        print(f"[Evaluator] Scenario '{scenario.title}' UNKNOWN VERDICT.")

    return {
        "execution_logs": logs,
        "final_verdict": final_verdict
    }
