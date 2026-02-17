from typing import List, Dict, Optional, Annotated, Any
from enum import Enum
from pathlib import Path
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
import operator

class TestStatus(str, Enum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"

class TestScenario(BaseModel):
    id: str = Field(description="Unique identifier for the test scenario")
    title: str = Field(description="Title of the test scenario")
    description: str = Field(description="Detailed description of the test scenario")
    steps: List[str] = Field(description="High-level steps for the test")
    expected_result: str = Field(description="Expected outcome")
    status: TestStatus = TestStatus.PENDING
    tags: List[str] = Field(default_factory=list, description="Tags for categorization (e.g., 'compliance', 'security')")

class TestPlan(BaseModel):
    scenarios: List[TestScenario] = Field(default_factory=list, description="List of test scenarios")

class AgentState(TypedDict):
    user_requirements: str
    test_plan: List[Dict[str, Any]] # Serialized TestScenario objects
    current_test_context: Dict[str, Any]
    execution_logs: Annotated[List[str], operator.add]
    screenshots: Annotated[List[str], operator.add] # Storing paths as strings for JSON serialization
    retry_count: int
    final_verdict: str # "passed", "failed", "in_progress"
    current_scenario_index: int
    error: Optional[str]
