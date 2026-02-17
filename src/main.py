from src.workflows.graph import app
from src.state.state import AgentState
import uuid

def main():
    # Initial State
    state: AgentState = {
        "user_requirements": "Test the login functionality on https://example.com",
        "test_plan": [],
        "current_test_context": {},
        "execution_logs": [],
        "screenshots": [],
        "retry_count": 0,
        "final_verdict": "in_progress",
        "current_scenario_index": 0,
        "error": None
    }

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    print(f"Starting QA Workflow (Thread ID: {thread_id})...")

    # Start execution
    # Since we have an interrupt before "executor", it should pause there.
    # Note: Using recursion_limit just in case
    try:
        for event in app.stream(state, config=config):
            for key, value in event.items():
                print(f"Finished Step: {key}")
                # Optional: Print partial state updates
                if key == "strategist":
                    print(f"  Generated {len(value.get('test_plan', []))} scenarios.")
                elif key == "engineer":
                    print(f"  Generated execution plan.")
    except Exception as e:
        print(f"Stream interrupted or error: {e}")

    # Check if we are paused
    snapshot = app.get_state(config)
    if snapshot.next:
        print(f"\nPaused before: {snapshot.next}")
        print("User Checkpoint Reached. Reviewing Plan...")

        # Simulate User Approval
        user_input = "yes" # In real app, verify user input
        if user_input == "yes":
            print("User Approved. Resuming execution...")

            # Resume execution
            # Pass None as input to resume from checkpoint
            for event in app.stream(None, config=config):
                 for key, value in event.items():
                    print(f"Finished Step: {key}")
                    if key == "evaluator":
                        logs = value.get("execution_logs", [])
                        verdict = value.get("final_verdict", "unknown")
                        print(f"  Evaluator Verdict: {verdict}")

    final_snapshot = app.get_state(config)
    print("\nWorkflow Complete.")
    print("Final Verdict:", final_snapshot.values.get("final_verdict", "N/A"))
    # print("Full Logs:", final_snapshot.values.get("execution_logs", []))

if __name__ == "__main__":
    main()
