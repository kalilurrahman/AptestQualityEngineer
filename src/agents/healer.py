from src.state.state import AgentState
from src.utils.llm import call_llm
import os
import json

def healer_agent(state: AgentState) -> dict:
    """
    Analyzes failures using Multimodal LLM (Vision) and attempts to heal the test.
    """
    print("[Healer] Analyzing failure with Vision LLM...")
    error = state.get("error", "")
    retry_count = state.get("retry_count", 0)

    if retry_count >= 3:
        print("[Healer] Max retries reached. Cannot heal.")
        return {"final_verdict": "failed", "retry_count": retry_count}

    print(f"[Healer] Attempting to heal error: {error}. Retry {retry_count + 1}/3")

    current_test_context = state.get("current_test_context", {})
    failed_step_index = current_test_context.get("failed_step_index", 0)
    execution_plan = current_test_context.get("execution_plan", [])

    if execution_plan and failed_step_index < len(execution_plan):
        step = execution_plan[failed_step_index]
        original_desc = step['args'].get('description', '')

        # Get latest screenshot
        screenshots = state.get("screenshots", [])
        latest_screenshot = screenshots[-1] if screenshots else None

        if latest_screenshot and os.path.exists(latest_screenshot):
            prompt = f"""
            You are a Self-Healing Test Agent.
            The following test step failed:
            Action: {step['args'].get('action')}
            Target Description: "{original_desc}"
            Error: "{error}"

            Analyze the attached screenshot of the application state.
            Identify the correct element that matches the intent of the original step.

            Provide a new, more robust visual description or selector for this element.

            Return ONLY the new description string.
            """
            try:
                new_description = call_llm(prompt, capability="vision", image_path=latest_screenshot)
                print(f"[Healer] LLM suggested new description: {new_description}")

                step['args']['description'] = new_description.strip()
                execution_plan[failed_step_index] = step
                current_test_context["execution_plan"] = execution_plan

            except Exception as e:
                print(f"[Healer] Vision analysis failed: {e}")
        else:
            print("[Healer] No screenshot available for analysis.")

    return {
        "retry_count": retry_count + 1,
        "current_test_context": current_test_context,
        "error": None, # Reset error
        "final_verdict": "in_progress", # Reset verdict so we can loop back
        "execution_logs": [f"Healed step {failed_step_index + 1} with LLM guidance. Retrying..."]
    }
