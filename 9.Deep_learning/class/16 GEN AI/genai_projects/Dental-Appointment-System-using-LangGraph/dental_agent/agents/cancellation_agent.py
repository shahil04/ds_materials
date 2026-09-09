# from langchain_xai import ChatXAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import ToolNode
from dental_agent.config.settings import GROQ_API_KEY, MODEL_NAME, TEMPERATURE
from dental_agent.models.state import AppointmentState
from dental_agent.tools.csv_reader import get_patient_appointments
from dental_agent.tools.csv_writer import cancel_appointment
from dental_agent.utils import sanitize_messages

CANCEL_TOOLS = [get_patient_appointments, cancel_appointment]

CANCEL_SYSTEM = """You are the Cancellation Agent for a dental appointment management system.

Your ONLY job is to cancel existing appointments.

## Workflow
1. Collect REQUIRED information:
   - patient_id  : numeric patient ID
   - date_slot   : the specific slot to cancel in M/D/YYYY H:MM format

2. If the patient does not know the exact slot, call get_patient_appointments(patient_id)
   to list their bookings, then ask which one to cancel.

3. Confirm with the user before proceeding:
   "Are you sure you want to cancel the appointment at {date_slot} with {doctor_name}? (yes/no)"

4. On user confirmation, call cancel_appointment(patient_id, date_slot).

5. Inform the user of the outcome.

## Rules
- Always confirm before cancelling — ask "yes/no" explicitly.
- If the patient has no appointments, inform them kindly.
- Do NOT cancel if the patient_id does not match the booking.
- If the user already confirmed in their message (e.g. "yes, cancel it"), skip asking again.

## Date Format
M/D/YYYY H:MM (e.g., 5/8/2026 8:30)
"""

CANCEL_PROMPT = ChatPromptTemplate.from_messages([
    ("system", CANCEL_SYSTEM),
    ("placeholder", "{messages}"),
])

cancellation_tool_node = ToolNode(tools=CANCEL_TOOLS)


def cancellation_agent_node(state: AppointmentState) -> dict:
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    ).bind_tools(CANCEL_TOOLS)

    chain = CANCEL_PROMPT | llm
    response = chain.invoke({"messages": sanitize_messages(state["messages"])})
    return {
        "messages": [response],
        "final_response": response.content if not response.tool_calls else None,
    }
