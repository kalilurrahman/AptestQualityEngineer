from langgraph.graph import StateGraph, END
from src.state.state import AgentState
from src.agents.strategist import strategist_agent
from src.agents.engineer import engineer_agent
from src.agents.executor import executor_agent
from src.agents.healer import healer_agent
from src.agents.evaluator import evaluator_agent

def should_heal(state: AgentState):
    """
    Decide whether to heal or evaluate based on verdict and retry count.
    """
    if state.get("final_verdict") == "failed":
        if state.get("retry_count", 0) < 3:
            return "healer"
        else:
            return "evaluator"
    return "evaluator"

def check_next_scenario(state: AgentState):
    """
    Check if there are more scenarios to run.
    """
    test_plan = state.get("test_plan", [])
    current_index = state.get("current_scenario_index", 0)

    if current_index + 1 < len(test_plan):
        return "increment_index"
    return END

def increment_index_node(state: AgentState):
    """
    Prepare state for the next scenario.
    """
    return {
        "current_scenario_index": state.get("current_scenario_index", 0) + 1,
        "retry_count": 0,
        "final_verdict": "in_progress",
        "current_test_context": {},
        "error": None
    }

# Graph Construction
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("strategist", strategist_agent)
workflow.add_node("engineer", engineer_agent)
workflow.add_node("executor", executor_agent)
workflow.add_node("healer", healer_agent)
workflow.add_node("evaluator", evaluator_agent)
workflow.add_node("increment_index", increment_index_node)

# Set Entry Point
workflow.set_entry_point("strategist")

# Add Edges
workflow.add_edge("strategist", "engineer")
workflow.add_edge("engineer", "executor")

# Conditional Edge from Executor
workflow.add_conditional_edges(
    "executor",
    should_heal,
    {
        "healer": "healer",
        "evaluator": "evaluator"
    }
)

# Edge from Healer back to Executor
workflow.add_edge("healer", "executor")

# Conditional Edge from Evaluator
workflow.add_conditional_edges(
    "evaluator",
    check_next_scenario,
    {
        "increment_index": "increment_index",
        END: END
    }
)

# Edge from Increment to Engineer
workflow.add_edge("increment_index", "engineer")

# Compile the graph
# Note: interrupt_before=["executor"] allows HITL review before execution.
# To actually use this, we need a checkpointer.
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()

app = workflow.compile(checkpointer=checkpointer, interrupt_before=["executor"])
