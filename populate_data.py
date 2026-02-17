import json
import os

data = {
    # ------------------
    # Web & Mobile Apps
    # ------------------
    "fullstack_web": {
        "title": "Full-stack Web App Testing",
        "category": "Web & Mobile",
        "description": "Comprehensive test strategy for a modern full-stack web application, covering UI, API, and Database layers.",
        "prompt": "Act as an expert Quality Engineer. Generate a comprehensive test strategy for a Full-stack Web Application (React frontend, Python backend, PostgreSQL database). Include functional, API, and database test cases.",
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
        "category": "Web & Mobile",
        "description": "Testing strategy for a news aggregation application focusing on personalization and real-time updates.",
        "prompt": "Act as an expert Quality Engineer. Create a detailed test plan for a news aggregation app like Google News. Focus on personalization algorithms, real-time feed updates, and offline reading capabilities.",
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
        "category": "Web & Mobile",
        "description": "Testing a video streaming platform with focus on streaming quality, device compatibility, and recommendation engine.",
        "prompt": "Act as an expert Quality Engineer. Develop a test strategy for a video streaming platform like Netflix. Include scenarios for adaptive bitrate streaming, multi-device support, and content recommendation accuracy.",
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
    "social_network": {
        "title": "Social Network Feed Algorithm",
        "category": "Social Media",
        "description": "Testing the feed ranking algorithm and social interactions for a platform like Instagram or Facebook.",
        "prompt": "Act as an expert Quality Engineer. Design a test suite for a Social Network Feed Algorithm. Focus on content ranking, user engagement metrics, and edge cases like shadowbanning or content moderation.",
        "content": """
# Social Network Feed Algorithm Test Strategy

## 1. Test Strategy
*   **Algorithm Logic**: Verify that posts from close friends appear higher.
*   **Engagement**: Verify that likes/comments boost post visibility.
*   **Moderation**: Ensure flagged content is hidden or downranked.

## 2. Test Cases

| ID | Feature | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| SN01 | Feed | User A likes User B's posts frequently | User B's new post appears at top of User A's feed | High |
| SN02 | Ads | Ad frequency check | Ads appear every 5-10 posts, not consecutively | Medium |
| SN03 | Content | Post containing banned keywords | Post is automatically flagged/hidden | High |

## 3. Boundary Test Cases
*   User with 0 friends/follows.
*   User following 10,000 accounts.
*   Post with maximum character limit and 10+ images.
"""
    },
    "messaging_app": {
        "title": "Encrypted Messaging App",
        "category": "Social Media",
        "description": "Security and functionality testing for an end-to-end encrypted messaging application like WhatsApp or Signal.",
        "prompt": "Act as an expert Quality Engineer. Create a test plan for an End-to-End Encrypted Messaging App. Prioritize security, message delivery reliability, and media sharing.",
        "content": """
# Encrypted Messaging App Test Strategy

## 1. Test Strategy
*   **E2EE Verification**: Ensure messages cannot be intercepted or read by the server.
*   **Delivery**: Test message delivery statuses (Sent, Delivered, Read).
*   **Media**: Verify encryption of shared images and videos.

## 2. Test Cases

| ID | Feature | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| MA01 | Security | Intercept traffic with proxy | Message content is unreadable (encrypted) | Critical |
| MA02 | Chat | Send message in airplane mode | Message queues and sends upon reconnection | High |
| MA03 | Group | Add member to group | New member sees history (if enabled) or only new messages | Medium |

## 3. Critical Analysis
*   Key exchange mechanism robustness.
*   Battery usage during background sync.
"""
    },

    # ------------------
    # Finance & Banking
    # ------------------
    "mobile_banking": {
        "title": "Mobile Banking App",
        "category": "Finance",
        "description": "Security-focused testing for a mobile banking application including fund transfers and account management.",
        "prompt": "Act as an expert Quality Engineer. Generate a comprehensive test strategy for a Mobile Banking Application. Focus on security (MFA, Biometrics), transaction integrity, and compliance.",
        "content": """
# Mobile Banking App Test Strategy

## 1. Test Strategy
*   **Security**: Biometric login, 2FA, Session timeout.
*   **Transactions**: ACIDE properties for fund transfers.
*   **Compliance**: KYC/AML checks.

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| MB01 | Auth | Login with Fingerprint | Access granted within 2 seconds | High |
| MB02 | Transfer | Transfer > Account Balance | Transaction failed, error shown | Critical |
| MB03 | BillPay | Schedule future payment | Payment deducted on scheduled date | High |

## 3. Security Tests
*   SQL Injection on search fields.
*   Man-in-the-Middle (MitM) attack simulation.
*   Data leakage in background mode (screenshot prevention).
"""
    },
    "atm_software": {
        "title": "ATM Software",
        "category": "Finance",
        "description": "Hardware-software integration testing for Automated Teller Machines.",
        "prompt": "Act as an expert Quality Engineer. detailed test cases for ATM Software. Include hardware interaction scenarios (card reader, cash dispenser), network failures, and security protocols.",
        "content": """
# ATM Software Test Strategy

## 1. Test Strategy
*   **Hardware Integration**: Card reader, PIN pad, Cash dispenser, Receipt printer.
*   **Network**: Handling transaction timeouts and connection loss.
*   **Security**: PIN encryption, Physical tampering alerts.

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| ATM01 | Auth | Insert invalid card | Card ejected, error message shown | High |
| ATM02 | Withdraw | Request amount > daily limit | Transaction declined | High |
| ATM03 | Hardware | Cash dispenser jam simulation | Error log generated, onscreen apology | Critical |

## 3. Boundary Test Cases
*   Withdrawal of $0.
*   Withdrawal of maximum possible amount.
*   3 incorrect PIN attempts (Card block).
"""
    },
    "trading_platform": {
        "title": "High-Frequency Trading Platform",
        "category": "Finance",
        "description": "Performance and accuracy testing for a stock trading platform where latency is critical.",
        "prompt": "Act as an expert Quality Engineer. Design a test strategy for a High-Frequency Trading Platform. Focus on low-latency execution, real-time data accuracy, and failover mechanisms.",
        "content": """
# High-Frequency Trading Platform Test Strategy

## 1. Test Strategy
*   **Latency**: Ensure order execution < 1ms.
*   **Concurrency**: Handle 100k+ orders per second.
*   **Data Integrity**: Real-time stock price accuracy.

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| TR01 | Order | Place Market Order | Executed at best available price immediately | Critical |
| TR02 | Feed | Price update latency | Update received within defined SLA | Critical |
| TR03 | Risk | Margin check failure | Order rejected if insufficient margin | High |

## 3. Stress Testing
*   Simulate market crash (sudden volume spike).
*   Network packet loss simulation.
"""
    },
    "car_insurance": {
        "title": "Car Insurance Industry Testing",
        "category": "Finance",
        "description": "Domain-specific testing for insurance policy lifecycle, claims processing, and premium calculation.",
        "prompt": "Act as an expert Quality Engineer. Create a domain-specific test plan for a Car Insurance Application. Include Premium Calculation logic, Claims Processing workflows, and Regulatory Compliance.",
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

    # ------------------
    # Retail & E-commerce
    # ------------------
    "online_marketplace": {
        "title": "Online Marketplace (E-commerce)",
        "category": "Retail",
        "description": "Testing a multi-vendor marketplace focusing on search, cart, checkout, and vendor management.",
        "prompt": "Act as an expert Quality Engineer. Develop a test strategy for a Multi-vendor E-commerce Marketplace (like Amazon). Cover Product Search, Shopping Cart, Payment Gateway integration, and Vendor Portals.",
        "content": """
# Online Marketplace Test Strategy

## 1. Test Strategy
*   **Search**: Relevance and filtering accuracy.
*   **Checkout**: Transaction flow and payment gateway integration.
*   **Vendor**: Product listing and inventory updates.

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| EC01 | Search | Filter by Price (Low to High) | Results sorted correctly | Medium |
| EC02 | Cart | Add out-of-stock item | 'Notify me' option shown, cannot add | High |
| EC03 | Checkout | Payment with expired card | Transaction declined | High |

## 3. Boundary Test Cases
*   Buying 999 units of a product.
*   Coupon code usage limits.
"""
    },
    "pos_system": {
        "title": "Point of Sale (POS) System",
        "category": "Retail",
        "description": "Testing physical POS software used in retail stores, including hardware integration and offline capability.",
        "prompt": "Act as an expert Quality Engineer. Create test cases for a Retail Point of Sale (POS) System. Include barcode scanning, receipt printing, cash drawer operation, and offline transaction handling.",
        "content": """
# POS System Test Strategy

## 1. Test Strategy
*   **Hardware**: Barcode scanner, Receipt printer, Cash drawer.
*   **Offline Mode**: Transaction storage when network is down.
*   **Inventory**: Real-time stock deduction.

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| POS01 | Scan | Scan valid barcode | Item added to bill with correct price | Critical |
| POS02 | Payment | Split payment (Cash + Card) | Both payments processed, total balances | High |
| POS03 | Returns | Process refund | Inventory updated, cash/credit returned | High |

## 3. Error Handling
*   Scanner failure (manual entry fallback).
*   Printer out of paper.
"""
    },
    "inventory_mgmt": {
        "title": "Inventory Management System",
        "category": "Retail",
        "description": "Testing backend inventory tracking, reorder points, and supply chain integration.",
        "prompt": "Act as an expert Quality Engineer. Design a test plan for an Inventory Management System. Focus on Stock Level tracking, Reorder Point logic, and Warehouse Management integration.",
        "content": """
# Inventory Management Test Strategy

## 1. Test Strategy
*   **Accuracy**: Stock count matches physical reality.
*   **Forecasting**: Reorder alerts triggered at correct thresholds.
*   **Integration**: Sync with POS and E-commerce.

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| INV01 | Stock | Receive shipment | Stock count increases by received amount | High |
| INV02 | Alert | Stock falls below threshold | Low stock alert generated | High |
| INV03 | Report | Generate monthly valuation | Accurate value based on FIFO/LIFO | Medium |

## 3. Data Integrity
*   Concurrent updates from multiple warehouses.
"""
    },

    # ------------------
    # Healthcare
    # ------------------
    "hospital_mgmt": {
        "title": "Hospital Management System",
        "category": "Healthcare",
        "description": "Testing critical healthcare workflows including patient admission, scheduling, and electronic health records (EHR).",
        "prompt": "Act as an expert Quality Engineer. Create a comprehensive test strategy for a Hospital Management System. Prioritize Patient Safety, Data Privacy (HIPAA), and interoperability (HL7).",
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
    },
    "telemedicine_app": {
        "title": "Telemedicine App",
        "category": "Healthcare",
        "description": "Testing video consultation, appointment scheduling, and remote prescription features.",
        "prompt": "Act as an expert Quality Engineer. Develop a test plan for a Telemedicine Application. Focus on Video Call Quality, Appointment Scheduling, and Secure Prescription transmission.",
        "content": """
# Telemedicine App Test Strategy

## 1. Test Strategy
*   **Video Quality**: WebRTC stability, low bandwidth handling.
*   **Scheduling**: Time zone management for doctor/patient.
*   **Prescriptions**: Digital signature and pharmacy forwarding.

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| TM01 | Video | Connect call with poor network | Audio remains clear, video degrades gracefully | High |
| TM02 | Schedule | Book slot across time zones | Correct local time shown for both parties | High |
| TM03 | Rx | Doctor issues prescription | Patient receives PDF, Pharmacy notified | Critical |

## 3. Security
*   End-to-end encryption of video stream.
"""
    },
    "health_tracker": {
        "title": "Wearable Health Tracker",
        "category": "Healthcare",
        "description": "Testing data synchronization between wearable hardware and mobile app (IoT/Healthcare).",
        "prompt": "Act as an expert Quality Engineer. Create test cases for a Wearable Health Tracker (like Fitbit) and its companion app. Cover Data Synchronization, Step Counting accuracy, and Battery optimization.",
        "content": """
# Wearable Health Tracker Test Strategy

## 1. Test Strategy
*   **Sensor Accuracy**: Step count, Heart rate monitoring.
*   **Sync**: Bluetooth data transfer reliability.
*   **Battery**: Power consumption optimization.

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| WT01 | Pedometer | Walk 100 steps | Counter shows 95-105 steps | High |
| WT02 | Sync | Sync after 3 days offline | All historical data transferred | High |
| WT03 | Pairing | Pair with new phone | Secure bonding, old data preserved | Medium |

## 3. Environmental Tests
*   Water resistance (if applicable).
*   Extreme temperature performance.
"""
    },

    # ------------------
    # Travel & Transport
    # ------------------
    "airline_booking": {
        "title": "Airline Booking System",
        "category": "Travel",
        "description": "Testing complex reservation systems, seat selection, and GDS integration.",
        "prompt": "Act as an expert Quality Engineer. Design a test strategy for an Airline Booking System. Include Flight Search, Seat Selection, Payment Processing, and PNR generation.",
        "content": """
# Airline Booking System Test Strategy

## 1. Test Strategy
*   **Search Engine**: Handling complex routes and multi-city flights.
*   **Inventory**: Real-time seat availability (prevention of double booking).
*   **Integration**: GDS (Global Distribution System) connectivity.

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| AB01 | Search | Search Round Trip | Valid flights shown for both legs | High |
| AB02 | Booking | Book last available seat | Booking confirmed, seat map updated | Critical |
| AB03 | Check-in | Online check-in < 24hrs | Boarding pass generated | High |

## 3. Negative Testing
*   Booking a flight in the past.
*   Payment failure handling.
"""
    },
    "ride_sharing": {
        "title": "Ride Sharing App",
        "category": "Travel",
        "description": "Testing location-based services, driver-rider matching, and dynamic pricing.",
        "prompt": "Act as an expert Quality Engineer. Create a test plan for a Ride Sharing App (like Uber/Lyft). Focus on GPS Accuracy, Driver-Rider Matching, and Surge Pricing logic.",
        "content": """
# Ride Sharing App Test Strategy

## 1. Test Strategy
*   **Geolocation**: Accurate pickup/drop-off point detection.
*   **Matching Algorithm**: Nearest driver allocation.
*   **Pricing**: Surge pricing calculation based on demand.

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| RS01 | GPS | Request ride at current location | Correct address detected | High |
| RS02 | Matching | Driver accepts ride | Rider notified, ETA shown | High |
| RS03 | Payment | Trip completion | Card charged, driver paid | Critical |

## 3. Edge Cases
*   GPS signal loss during trip.
*   Rider cancels 1 minute after driver arrival.
"""
    },

    # ------------------
    # Telecom
    # ------------------
    "telecom_oms": {
        "title": "Telecom Order Management",
        "category": "Telecom",
        "description": "Testing complex order workflows, provisioning, and billing integration for telecom services.",
        "prompt": "Act as an expert Quality Engineer. Generate a test strategy for a Telecom Order Management System. Cover Order Capture, Service Provisioning, and Billing Activation workflows.",
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

    # ------------------
    # Education
    # ------------------
    "lms": {
        "title": "Learning Management System (LMS)",
        "category": "Education",
        "description": "Testing educational platforms for course delivery, grading, and student management.",
        "prompt": "Act as an expert Quality Engineer. Develop a test plan for a Learning Management System (LMS). Include Course Content delivery, Quiz/Exam modules, and Gradebook calculation.",
        "content": """
# LMS Test Strategy

## 1. Test Strategy
*   **Content Delivery**: Video streaming, PDF rendering.
*   **Assessment**: Quiz timing, auto-grading logic.
*   **User Roles**: Student vs. Teacher vs. Admin permissions.

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| LMS01 | Quiz | Submit quiz after time limit | Auto-submit triggered, answers saved | High |
| LMS02 | Gradebook | Teacher updates grade | Student sees new grade immediately | High |
| LMS03 | Access | Student accesses unpublished course | Access denied | Medium |

## 3. Compatibility
*   Mobile browser support.
*   Screen reader accessibility (WCAG).
"""
    },

    # ------------------
    # IoT
    # ------------------
    "smart_thermostat": {
        "title": "Smart Home Thermostat",
        "category": "IoT",
        "description": "Testing embedded systems, sensor accuracy, and remote control via mobile app.",
        "prompt": "Act as an expert Quality Engineer. Create test cases for a Smart Thermostat IoT device. Cover Temperature Sensor accuracy, Remote Control via App, and Connectivity resilience.",
        "content": """
# Smart Thermostat Test Strategy

## 1. Test Strategy
*   **Sensor Calibration**: Accuracy within +/- 0.5 degrees.
*   **Connectivity**: WiFi reconnection logic.
*   **Automation**: Schedule adherence (Day/Night modes).

## 2. Test Cases

| ID | Module | Test Scenario | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| IOT01 | Sensor | Room temp increases | Thermostat reading updates | High |
| IOT02 | App | Change temp remotely | Device responds within 3 seconds | High |
| IOT03 | Firmware | OTA Update | Update installs, device reboots, config saved | Critical |

## 3. Safety
*   Overheat protection cutoff.
"""
    }
}

os.makedirs('app/data', exist_ok=True)
with open('app/data/repo_data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Expanded Data populated successfully.")
