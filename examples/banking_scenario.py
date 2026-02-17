from src.state.state import TestScenario

# FinTech Scenarios (KYC, Compliance, Security)

banking_scenarios = [
    TestScenario(
        id="FT-001",
        title="KYC Document Upload",
        description="Verify that a user can upload a valid ID document (Passport) and pass verification.",
        steps=[
            "Navigate to /kyc-portal",
            "Login as 'pending_user'",
            "Click 'Start Verification'",
            "Select 'Passport' from Document Type",
            "Upload 'valid_passport.jpg'",
            "Click 'Submit for Review'",
            "Wait for verification status to change to 'In Review'"
        ],
        expected_result="Verification status is 'In Review' and success message is shown.",
        tags=["functional", "KYC", "compliance"]
    ),
    TestScenario(
        id="FT-002",
        title="Fund Transfer Limit Check",
        description="Verify that a transfer exceeding the daily limit is blocked.",
        steps=[
            "Navigate to /transfers",
            "Select 'External Transfer'",
            "Enter amount '10001' (limit is 10000)",
            "Enter recipient details",
            "Click 'Transfer'"
        ],
        expected_result="Error 'Transaction exceeds daily limit' is displayed.",
        tags=["functional", "negative", "security"]
    ),
    TestScenario(
        id="FT-003",
        title="2FA Enforcement on Login",
        description="Verify that 2FA is required for login from a new device.",
        steps=[
            "Open Incognito/New Browser Context",
            "Navigate to /login",
            "Enter valid credentials",
            "Click 'Login'",
            "Verify redirect to /2fa-verification",
            "Enter invalid code '000000'",
            "Click 'Verify'"
        ],
        expected_result="Error 'Invalid Code' is displayed; user is not logged in.",
        tags=["security", "auth"]
    )
]

def run_banking_example():
    print("Running FinTech Banking Scenarios...")
    for scenario in banking_scenarios:
        print(f"Scenario: {scenario.title}")
        print(f"  Steps: {scenario.steps}")
        print(f"  Expected: {scenario.expected_result}")

if __name__ == "__main__":
    run_banking_example()
