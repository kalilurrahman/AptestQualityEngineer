import json
import os

data = {
    "fullstack_web": {
        "title": "Full-stack Web App Testing",
        "description": "Comprehensive test strategy for a modern full-stack web application, covering UI, API, and Database layers.",
        "content": """
# Full-stack Web App Test Strategy

## 1. Test Strategy
Testing a full-stack web application requires a layered approach:
*   **Unit Testing**: For backend logic (Python/Node.js) and frontend components (React/Angular).
*   **Integration Testing**: verifying API endpoints and database interactions.
*   **E2E Testing**: simulating user flows using tools like Cypress or Selenium.

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC01 | Auth | User Registration | User created in DB, confirmation email sent | High |
| TC02 | Auth | Login with invalid credentials | Error message displayed | High |
| TC03 | Dashboard | Load dashboard data | Data fetched from API and displayed correctly | Medium |
| TC04 | Profile | Update user profile | Changes saved to DB and reflected in UI | Medium |

## 3. Test Conditions
*   Browser compatibility (Chrome, Firefox, Safari).
*   Mobile responsiveness.
*   Network latency simulation.

## 4. Boundary Test Cases
*   Input fields max length.
*   Zero/Negative values in numeric fields.
*   Concurrent user load.
"""
    },
    "google_news": {
        "title": "Google News App Testing",
        "description": "Testing strategy for a news aggregation application focusing on personalization and real-time updates.",
        "content": """
# Google News App Test Strategy

## 1. Test Strategy
*   **Personalization Algorithm**: Verify news feed relevance based on user interests.
*   **Real-time Updates**: Verify breaking news alerts and feed refresh rates.
*   **Offline Mode**: Verify content caching and reading without internet.

## 2. Test Cases

| ID | Feature | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| GN01 | Feed | New user onboarding | Default news categories shown | High |
| GN02 | Search | Search for specific topic | Relevant articles displayed | High |
| GN03 | Offline | Read saved article offline | Article content loads from cache | Medium |

## 3. Critical Analysis
*   Latency in news delivery can impact user retention.
*   Accuracy of recommendation engine is critical.
"""
    },
    "netflix": {
        "title": "Netflix Testing",
        "description": "Testing a video streaming platform with focus on streaming quality, device compatibility, and recommendation engine.",
        "content": """
# Netflix Test Strategy

## 1. Test Strategy
*   **Streaming Quality**: Adaptive bitrate testing under various network conditions.
*   **Device Compatibility**: Smart TVs, Mobile, Web, Consoles.
*   **DRM**: Content protection verification.

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| NF01 | Player | Play video on 4G network | Video starts with appropriate resolution | High |
| NF02 | Search | Search for 'Stranger Things' | Correct title appears in results | High |
| NF03 | Profile | Switch profile | Recommendations update for selected profile | High |

## 3. Boundary Test Cases
*   Maximum number of concurrent streams per account.
*   Download limit for offline viewing.
"""
    },
    "car_insurance": {
        "title": "Car Insurance Industry Testing",
        "description": "Domain-specific testing for insurance policy lifecycle, claims processing, and premium calculation.",
        "content": """
# Car Insurance Application Test Strategy

## 1. Test Strategy
*   **Premium Calculation**: Verify complex algorithms for quote generation.
*   **Compliance**: Ensure adherence to state/federal regulations.
*   **Data Security**: PII protection.

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| CI01 | Quote | Generate quote for new driver | High premium calculated correctly | High |
| CI02 | Policy | Renew policy | Policy date extended, new premium applied | High |
| CI03 | Claims | File a claim | Claim ID generated, status 'Pending' | High |

## 3. Test Data
*   Driver Age: 18, 25, 40, 70.
*   Vehicle Type: Sedan, SUV, Truck.
*   History: 0 accidents, 1 accident, DUI.
"""
    },
    "telecom_oms": {
        "title": "Telecom Order Management Testing",
        "description": "Testing complex order workflows, provisioning, and billing integration for telecom services.",
        "content": """
# Telecom Order Management System (OMS) Test Strategy

## 1. Test Strategy
*   **Order Orchestration**: Verify order flow from capture to fulfillment.
*   **Provisioning**: Integration with network elements to activate service.
*   **Billing**: Correct charging initiation.

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| TO01 | Order Capture | Create new fiber connection order | Order created, status 'Submitted' | High |
| TO02 | Provisioning | Activate service | Network status 'Active', signal live | High |
| TO03 | Billing | First bill generation | Pro-rated charges applied correctly | High |

## 3. Complex Scenarios
*   Order modification during flight (MACD).
*   Order cancellation handling.
"""
    },
    "hospital_mgmt": {
        "title": "Hospital Management System Testing",
        "description": "Testing critical healthcare workflows including patient admission, scheduling, and electronic health records (EHR).",
        "content": """
# Hospital Management System Test Strategy

## 1. Test Strategy
*   **Patient Safety**: Critical focus on data accuracy (medications, allergies).
*   **Privacy**: HIPAA compliance.
*   **Workflow**: Seamless transition between departments (ER -> Ward -> Billing).

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| HM01 | Admission | Register new patient | Patient ID generated, band printed | High |
| HM02 | EHR | Update patient allergy | Alert shown when prescribing conflicting med | Critical |
| HM03 | Billing | Discharge patient | Final bill generated including all services | High |

## 3. Acceptance Criteria
*   System must handle 1000 concurrent users.
*   Zero data loss during failover.
"""
    }
}

os.makedirs('app/data', exist_ok=True)
with open('app/data/repo_data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Data populated successfully.")
