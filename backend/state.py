# state.py
from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage

class State(TypedDict, total=False):
    messages: List[BaseMessage]

    # tool interface
    tool_query: Optional[str]
    tool_result: Optional[str]

    done: bool
