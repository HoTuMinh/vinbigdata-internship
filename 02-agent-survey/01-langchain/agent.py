"""
LangChain agent for Vinmec appointment booking.
Framework: LangChain 0.3.13 + ChatGroq (llama-3.3-70b-versatile).
"""
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

SYSTEM_PROMPT = (
    "You are a Vinmec hospital virtual assistant. "
    "Help patients search for doctors and book appointments using available tools. "
    "Always confirm booking details before calling book_appointment. "
    "Respond in Vietnamese."
)

# ---------------------------------------------------------------------------
# Tool implementations (mocked — replace with real Vinmec API calls)
# ---------------------------------------------------------------------------

MOCK_DOCTORS = {
    ("tim mạch", "vinmec hà nội"): [
        {"id": "D001", "name": "BS. Nguyễn Văn An", "specialty": "Tim mạch can thiệp"},
        {"id": "D002", "name": "BS. Trần Thị Bình", "specialty": "Siêu âm tim"},
        {"id": "D003", "name": "GS. Lê Quốc Cường", "specialty": "Rối loạn nhịp tim"},
    ],
    ("nhi khoa", "vinmec hà nội"): [
        {"id": "D010", "name": "BS. Phạm Thị Mai", "specialty": "Nhi tổng quát"},
        {"id": "D011", "name": "BS. Vũ Đức Hùng", "specialty": "Sơ sinh"},
    ],
}


@tool
def search_doctor(department: str, hospital: str) -> str:
    """Search for available doctors in a department at a Vinmec hospital.

    Args:
        department: Medical department name in Vietnamese (e.g. 'tim mạch').
        hospital: Hospital branch name (e.g. 'Vinmec Hà Nội').

    Returns:
        JSON list of available doctors with id, name, specialty.
    """
    key = (department.lower().strip(), hospital.lower().strip())
    doctors = MOCK_DOCTORS.get(
        key,
        [{"id": "D999", "name": "BS. Trực ban", "specialty": department}],
    )
    return json.dumps(doctors, ensure_ascii=False)


@tool
def book_appointment(
    doctor_id: str,
    appointment_datetime: str,
    patient_name: str,
    patient_phone: str,
) -> str:
    """Book a medical appointment with a specific doctor.

    Args:
        doctor_id: Doctor ID from search_doctor result (e.g. 'D001').
        appointment_datetime: Date and time string (e.g. '2026-04-25 09:00').
        patient_name: Full name of the patient.
        patient_phone: Patient's contact phone number.

    Returns:
        Booking confirmation string with booking_id, or error message.
    """
    if not all([doctor_id, appointment_datetime, patient_name, patient_phone]):
        return "ERROR: All fields (doctor_id, datetime, patient_name, patient_phone) are required."

    seed = doctor_id + appointment_datetime + patient_name
    booking_id = f"VN{abs(hash(seed)) % 100000:05d}"

    return (
        f"BOOKING CONFIRMED\n"
        f"  Booking ID : {booking_id}\n"
        f"  Doctor     : {doctor_id}\n"
        f"  Date/Time  : {appointment_datetime}\n"
        f"  Patient    : {patient_name} ({patient_phone})\n"
        f"  Status     : Awaiting SMS confirmation"
    )


@tool
def cancel_appointment(booking_id: str) -> str:
    """Cancel an existing Vinmec appointment.

    Args:
        booking_id: The booking ID to cancel (format: VN#####).

    Returns:
        Cancellation confirmation or error message.
    """
    if not (booking_id.startswith("VN") and len(booking_id) == 7 and booking_id[2:].isdigit()):
        return f"ERROR: Invalid booking ID '{booking_id}'. Expected format: VN##### (e.g. VN12345)."
    return f"CANCELLED: Appointment {booking_id} has been successfully cancelled."


# ---------------------------------------------------------------------------
# Agent builder
# ---------------------------------------------------------------------------

def build_agent() -> AgentExecutor:
    """Construct and return a LangChain tool-calling AgentExecutor."""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY"),
    )

    tools = [search_doctor, book_appointment, cancel_appointment]

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=6,
        return_intermediate_steps=True,
    )


if __name__ == "__main__":
    executor = build_agent()
    query = (
        "Đặt lịch khám tim mạch ngày 25/04/2026 lúc 9h sáng ở Vinmec Hà Nội. "
        "Tên: Nguyễn Minh Tuấn, SĐT: 0912345678."
    )
    print(f"USER: {query}\n")
    result = executor.invoke({"input": query})
    print("\n=== FINAL ANSWER ===")
    print(result["output"])
