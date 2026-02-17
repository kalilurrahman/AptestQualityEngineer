import os
import sys
import uuid
import time
from typing import List, Dict, Any

# Add src to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.workflows.graph import app
from src.state.state import AgentState, TestScenario

def run_banking_test_workflow():
    print("Initializing Autonomous Banking QA Workflow...")

    # Requirements that should trigger Strategist -> Engineer -> Executor for Banking scenarios
    requirements = """
    Test the Fund Transfer functionality for a FinTech app.
    Specifically:
    1. Verify a transfer within limits passes.
    2. Verify a transfer exceeding the daily limit ($10,000) is blocked.
    3. Ensure 2FA is prompted for high-value transactions.
    """

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # Initial State
    state: AgentState = {
        "user_requirements": requirements,
        "test_plan": [],
        "current_test_context": {},
        "execution_logs": [],
        "screenshots": [],
        "retry_count": 0,
        "final_verdict": "in_progress",
        "current_scenario_index": 0,
        "error": None
    }

    print("-" * 60)
    print(f"THREAD ID: {thread_id}")
    print(f"REQUIREMENTS: {requirements.strip()}")
    print("-" * 60)

    # Run Graph
    step_count = 0
    try:
        # We manually iterate to demonstrate the step-by-step progress
        for event in app.stream(state, config=config):
            for node, output in event.items():
                step_count += 1
                print(f"\n[STEP {step_count}] Completed Node: {node.upper()}")

                if node == "strategist":
                    plan = output.get("test_plan", [])
                    print(f"  > Generated Test Plan with {len(plan)} scenarios:")
                    for s in plan:
                        title = s.get('title', 'Untitled')
                        print(f"    - {title}")

                elif node == "engineer":
                    context = output.get("current_test_context", {})
                    steps = context.get("execution_plan", [])
                    print(f"  > Generated {len(steps)} Tool Calls (Playwright steps).")
                    # print(f"    Sample: {steps[0] if steps else 'None'}")

                elif node == "executor":
                    logs = output.get("execution_logs", [])
                    verdict = output.get("final_verdict", "unknown")
                    print(f"  > Execution Verdict: {verdict}")
                    print(f"  > Logs (Last 3): {logs[-3:] if logs else 'None'}")

                elif node == "healer":
                    logs = output.get("execution_logs", [])
                    print(f"  > Self-Healing Triggered!")
                    print(f"  > Logs: {logs}")

                elif node == "evaluator":
                    verdict = output.get("final_verdict", "unknown")
                    print(f"  > Final Evaluator Verdict: {verdict.upper()}")

        # Check final state
        final_state = app.get_state(config).values
        print("-" * 60)
        print("WORKFLOW COMPLETE")
        print(f"Final Outcome: {final_state.get('final_verdict', 'unknown')}")
        print("-" * 60)

    except Exception as e:
        print(f"Workflow Error: {e}")

if __name__ == "__main__":
    run_banking_test_workflow()
