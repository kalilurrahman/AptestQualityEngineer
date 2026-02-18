from src.state.state import AgentState
from src.utils.llm import call_llm

def reporter_agent(state: AgentState) -> dict:
    """
    Generates a comprehensive markdown report of the test execution.
    """
    print("[Reporter] Generating final report...")
    logs = state.get("execution_logs", [])
    test_plan = state.get("test_plan", [])
    verdict = state.get("final_verdict", "unknown")

    prompt = f"""
    You are a Quality Assurance Reporter.
    Generate a professional Markdown Test Report based on the following execution logs.

    Test Plan Summary:
    {len(test_plan)} Scenarios Planned.

    Final Verdict: {verdict.upper()}

    Execution Logs:
    {logs}

    The report should include:
    1. Executive Summary
    2. Test Scope
    3. Detailed Results (Pass/Fail per scenario)
    4. Issues Found (if any)
    5. Recommendations

    Return ONLY the Markdown content.
    """

    try:
        report = call_llm(prompt, capability="reasoning")
        # Sanitize
        report = report.replace("```markdown", "").replace("```", "").strip()

        # Save report to file
        with open("test_report.md", "w") as f:
            f.write(report)

        return {
            "execution_logs": ["Final Test Report generated: test_report.md"]
        }
    except Exception as e:
        print(f"[Reporter] Error: {e}")
        return {
            "execution_logs": [f"Error generating report: {e}"]
        }
