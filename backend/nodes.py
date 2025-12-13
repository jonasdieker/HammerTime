# nodes.py
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, AIMessage
from backend.state import State
from backend.tools import search_suppliers
from backend.read_api_key import read_api_key

SYSTEM_PROMPT = (
    "You are a procurement agent for a construction company.\n"
    "You help foremen order parts by finding suppliers with the best price.\n"
    "Always base decisions on the supplier database results.\n"
    "If you need supplier information, request a database search."
)

read_api_key()
print(f"Using Anthropic API Key: {os.environ.get('ANTHROPIC_API_KEY')}")

llm = ChatAnthropic(
    model="claude-sonnet-4-5",
    temperature=0,
)

def agent_node(state: State) -> State:
    messages = state["messages"]

    # Inject system prompt exactly once
    if not any(m.type == "system" for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm.invoke(messages)
    print(f"Agent response!: {response.content}")

    if "search" in response.content.lower():
        return {
            "messages": messages + [response],
            "tool_query": response.content,
        }

    return {
        "messages": messages + [response],
        "done": True,
    }


def tool_node(state: State) -> State:
    result = search_suppliers(state["tool_query"])

    return {
        "messages": state["messages"] + [
            AIMessage(content=f"Supplier results:\n{result}")
        ],
        "tool_result": result,
    }
