# from langchain_xai import ChatXAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dental_agent.config.settings import GROQ_API_KEY, MODEL_NAME, TEMPERATURE
from dental_agent.models.state import AppointmentState, RouteTarget
from dental_agent.utils import sanitize_messages


class SupervisorDecision(BaseModel):
    """Routing decision produced by the supervisor."""
    intent: str = Field(
        description="Classified intent. One of: get_info, book, cancel, reschedule, unknown, end."
    )
    next_agent: RouteTarget = Field(
        description=(
            "The agent to route to. One of: info_agent, booking_agent, "
            "cancellation_agent, rescheduling_agent, end."
        )
    )
    reasoning: str = Field(description="Brief explanation of the routing decision.")


SUPERVISOR_SYSTEM = """You are the supervisor and router for a dental appointment management system.

Your ONLY job is to analyze the user's latest message and classify their intent, then route to the correct specialist agent.

## Routing Rules
- get_info      → info_agent          : User asks about available slots, doctors, specializations, schedules, or general queries.
- book          → booking_agent       : User wants to create / make / schedule a NEW appointment.
- cancel        → cancellation_agent  : User wants to cancel / remove an existing appointment.
- reschedule    → rescheduling_agent  : User wants to move / change an existing appointment to a different time.
- end           → end                 : User says goodbye, thanks, says they're done, or the conversation is fully resolved.
- unknown       → info_agent          : Ambiguous intent; default to info_agent for clarification.

## Important
- Do NOT answer the user directly. Only classify and route.
- If the user's message contains multiple intents, pick the PRIMARY action.
- If the last AI message already answered the user's question and the user has no follow-up, route to end.

Output ONLY valid JSON matching the SupervisorDecision schema.
"""

SUPERVISOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SUPERVISOR_SYSTEM),
    ("placeholder", "{messages}"),
])


def supervisor_node(state: AppointmentState) -> dict:
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    ).with_structured_output(SupervisorDecision)

    chain = SUPERVISOR_PROMPT | llm
    decision: SupervisorDecision = chain.invoke({"messages": sanitize_messages(state["messages"])})

    return {
        "intent": decision.intent,
        "next_agent": decision.next_agent,
    }
