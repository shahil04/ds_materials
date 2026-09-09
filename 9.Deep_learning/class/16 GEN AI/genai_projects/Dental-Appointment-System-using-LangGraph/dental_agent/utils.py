from typing import List
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)


def sanitize_messages(messages: List[BaseMessage]) -> List[BaseMessage]:
    """
    xAI (grok) API rejects any message with empty/null content.
    Replace empty content (None, "", or []) with a single space so the API
    accepts the message while preserving all other metadata.
    """
    result = []
    for msg in messages:
        content = msg.content
        is_empty = content is None or content == "" or content == []
        if is_empty:
            if isinstance(msg, AIMessage):
                result.append(
                    AIMessage(
                        content=" ",
                        tool_calls=getattr(msg, "tool_calls", None),
                        id=getattr(msg, "id", None),
                        response_metadata=getattr(msg, "response_metadata", {}),
                        usage_metadata=getattr(msg, "usage_metadata", None),
                    )
                )
            elif isinstance(msg, HumanMessage):
                result.append(
                    HumanMessage(
                        content=" ",
                        id=getattr(msg, "id", None),
                        response_metadata=getattr(msg, "response_metadata", {}),
                        usage_metadata=getattr(msg, "usage_metadata", None),
                    )
                )
            elif isinstance(msg, SystemMessage):
                result.append(
                    SystemMessage(
                        content=" ",
                        id=getattr(msg, "id", None),
                        response_metadata=getattr(msg, "response_metadata", {}),
                        usage_metadata=getattr(msg, "usage_metadata", None),
                    )
                )
            elif isinstance(msg, ToolMessage):
                result.append(
                    ToolMessage(
                        content=" ",
                        tool_call_id=getattr(msg, "tool_call_id", None),
                        id=getattr(msg, "id", None),
                        response_metadata=getattr(msg, "response_metadata", {}),
                        usage_metadata=getattr(msg, "usage_metadata", None),
                    )
                )
            else:
                msg_type = type(msg)
                result.append(
                    msg_type(
                        content=" ",
                        **{k: v for k, v in msg.__dict__.items() if k != "content"},
                    )
                )
        else:
            result.append(msg)
    return result
