from src.state.state import AgentState, TestPlan, TestScenario
import uuid

def strategist_agent(state: AgentState) -> dict:
    """
    Analyzes requirements and generates a test plan.
    (Mocked: Returns a fixed test plan for demonstration)
    """
    print("[Strategist] Analyzing requirements...")
    requirements = state.get("user_requirements", "")

    # Mock generation logic based on keywords in requirements
    scenarios = []
    if "login" in requirements.lower():
        scenarios.append(TestScenario(
            id=str(uuid.uuid4()),
            title="Valid Login",
            description="Verify user can login with valid credentials.",
            steps=["Navigate to https://example.com/login", "Enter valid username", "Enter valid password", "Click Login"],
            expected_result="User is redirected to dashboard",
            tags=["functional", "happy_path"]
        ))
        scenarios.append(TestScenario(
            id=str(uuid.uuid4()),
            title="Invalid Login",
            description="Verify login fails with invalid credentials.",
            steps=["Navigate to https://example.com/login", "Enter invalid username", "Enter valid password", "Click Login"],
            expected_result="Error message is displayed",
            tags=["functional", "negative"]
        ))
    else:
        # Default scenario
        scenarios.append(TestScenario(
            id=str(uuid.uuid4()),
            title="General Navigation",
            description="Verify homepage loads.",
            steps=["Navigate to https://example.com"],
            expected_result="Homepage is visible",
            tags=["smoke"]
        ))

    # Serialize scenarios to dicts for state compatibility
    test_plan_serialized = [s.model_dump() for s in scenarios]

    return {
        "test_plan": test_plan_serialized,
        "execution_logs": ["Generated test plan based on requirements."]
    }
