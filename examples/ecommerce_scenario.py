from src.state.state import TestScenario

# Example Test Scenario for E-Commerce Checkout

ecommerce_scenarios = [
    TestScenario(
        id="EC-001",
        title="Guest Checkout Flow",
        description="Verify a guest user can complete a purchase without creating an account.",
        steps=[
            "Navigate to /product/123",
            "Click 'Add to Cart'",
            "Click 'Checkout'",
            "Select 'Guest Checkout'",
            "Enter shipping details",
            "Enter payment details",
            "Click 'Place Order'"
        ],
        expected_result="Order confirmation page is displayed with Order ID.",
        tags=["functional", "critical"]
    ),
    TestScenario(
        id="EC-002",
        title="Discount Code Validation",
        description="Verify that an invalid discount code displays an error.",
        steps=[
            "Navigate to /cart",
            "Enter code 'INVALID2025'",
            "Click 'Apply'"
        ],
        expected_result="Error message 'Invalid Code' is displayed.",
        tags=["functional", "negative"]
    )
]

def run_ecommerce_example():
    print("Running E-Commerce Checkout Example...")
    for scenario in ecommerce_scenarios:
        print(f"Scenario: {scenario.title}")
        print(f"  Description: {scenario.description}")
        print(f"  Tags: {scenario.tags}")

if __name__ == "__main__":
    run_ecommerce_example()
