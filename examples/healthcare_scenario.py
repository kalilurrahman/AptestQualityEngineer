from src.state.state import TestScenario

# Example Test Scenario for Healthcare (HIPAA Compliance)
# This simulates a test case that checks for proper PHI masking.

healthcare_scenarios = [
    TestScenario(
        id="HC-001",
        title="Patient Data Masking",
        description="Verify that patient Social Security Numbers are masked in the UI.",
        steps=[
            "Navigate to /patient-dashboard",
            "Search for patient 'John Doe'",
            "Verify SSN field displays as '***-**-****'",
            "Click 'Reveal' button (requires admin)",
            "Verify error 'Access Denied' for standard user"
        ],
        expected_result="SSN is masked by default and unmasking is restricted.",
        tags=["compliance", "HIPAA", "security"]
    ),
    TestScenario(
        id="HC-002",
        title="Audit Log Verification",
        description="Verify that accessing a patient record creates an audit log entry.",
        steps=[
            "Login as Doctor",
            "View patient 'Jane Smith'",
            "Logout",
            "Login as Admin",
            "Navigate to /audit-logs",
            "Search for 'Jane Smith' access event"
        ],
        expected_result="Access event is logged with timestamp and user ID.",
        tags=["compliance", "audit"]
    )
]

def run_healthcare_example():
    print("Running Healthcare Compliance Example...")
    # In a real run, these would be fed into the Strategist's context or directly into the Engineer.
    for scenario in healthcare_scenarios:
        print(f"Scenario: {scenario.title}")
        print(f"  Description: {scenario.description}")
        print(f"  Tags: {scenario.tags}")

if __name__ == "__main__":
    run_healthcare_example()
