from typing import TypedDict, Annotated, Literal, Optional, List
from langchain_core.messages import BaseMessage
import operator

IntentType = Literal[
    "get_info",
    "book",
    "cancel",
    "reschedule",
    "unknown",
    "end",
]

RouteTarget = Literal[
    "info_agent",
    "booking_agent",
    "cancellation_agent",
    "rescheduling_agent",
    "end",
]


class AppointmentState(TypedDict):
    # Conversation history — appended by each node, never replaced
    messages: Annotated[List[BaseMessage], operator.add]

    # Supervisor routing
    intent: Optional[IntentType]
    next_agent: Optional[RouteTarget]

    # User-supplied booking parameters
    patient_id: Optional[str]
    requested_specialization: Optional[str]
    requested_doctor: Optional[str]
    requested_date_slot: Optional[str]

    # Rescheduling: old slot + new desired slot
    current_date_slot: Optional[str]
    new_date_slot: Optional[str]

    # Tool execution results
    available_slots: Optional[List[dict]]
    operation_success: Optional[bool]
    operation_message: Optional[str]

    # Final response assembled by the active agent
    final_response: Optional[str]
