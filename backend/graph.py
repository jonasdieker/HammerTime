# graph.py
from langgraph.graph import StateGraph, END
from backend.state import State
from backend.nodes import agent_node, tool_node


def route(state: State) -> str:
    if state.get("tool_query"):
        return "tool"
    if state.get("done"):
        return END
    return "agent"

def build_graph():
    graph = StateGraph(State)

    graph.add_node("agent", agent_node)
    graph.add_node("tool", tool_node)

    graph.set_entry_point("agent")

    graph.add_conditional_edges(
        "agent",
        route,
        {
            "tool": "tool",
            "agent": "agent",
            END: END,
        },
    )

    graph.add_edge("tool", "agent")

    return graph.compile()
