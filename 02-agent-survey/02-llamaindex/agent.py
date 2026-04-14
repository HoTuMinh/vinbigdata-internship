"""
LlamaIndex agent for Vinmec appointment booking.
Framework: llama-index-core 0.12.5 + Groq (llama-3.3-70b-versatile).
Pattern: FunctionTool x3 -> ReActAgent
"""
import json
import os
from dotenv import load_dotenv
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.groq import Groq

load_dotenv()

# ---------------------------------------------------------------------------
# Tool implementations (mocked)
# ---------------------------------------------------------------------------

MOCK_DOCTORS = {
    ("tim mạch", "vinmec hà nội"): [
        {"id": "D001", "name": "BS. Nguyễn Văn An", "specialty": "Tim mạch can thiệp"},
        {"id": "D002", "name": "BS. Trần Thị Bình", "specialty": "Siêu âm tim"},
        {"id": "D003", "name": "GS. Lê Quốc Cường", "specialty": "Rối loạn nhịp tim"},
    ],
    ("nhi khoa", "vinmec hà nội"): [
        {"id": "D010", "name": "BS. Phạm Thị Mai", "specialty": "Nhi tổng quát"},
    ],
}


def search_doctor(department: str, hospital: str) -> str:
    """Search for available doctors in a department at a Vinmec hospital.

    Args:
        department: Medical department in Vietnamese (e.g. 'tim mạch').
        hospital: Hospital branch (e.g. 'Vinmec Hà Nội').

    Returns:
        JSON string listing available doctors.
    """
    key = (department.lower().strip(), hospital.lower().strip())
    result = MOCK_DOCTORS.get(
        key,
        [{"id": "D999", "name": "BS. Trực ban", "specialty": department}],
    )
    return json.dumps(result, ensure_ascii=False)


def book_appointment(
    doctor_id: str,
    appointment_datetime: str,
    patient_name: str,
    patient_phone: str,
) -> str:
    """Book an appointment with a doctor.

    Args:
        doctor_id: Doctor ID from search_doctor (e.g. 'D001').
        appointment_datetime: Datetime string (e.g. '2026-04-25 09:00').
        patient_name: Patient's full name.
        patient_phone: Patient's phone number.

    Returns:
        Booking confirmation with booking_id, or error string.
    """
    if not all([doctor_id, appointment_datetime, patient_name, patient_phone]):
        return "ERROR: All fields are required."

    seed = doctor_id + appointment_datetime + patient_name
    booking_id = f"VN{abs(hash(seed)) % 100000:05d}"

    return (
        f"BOOKING CONFIRMED | ID: {booking_id} | "
        f"Doctor: {doctor_id} | Time: {appointment_datetime} | "
        f"Patient: {patient_name} ({patient_phone})"
    )


def cancel_appointment(booking_id: str) -> str:
    """Cancel an existing appointment.

    Args:
        booking_id: Booking ID to cancel (format: VN#####).

    Returns:
        Cancellation result string.
    """
    valid = booking_id.startswith("VN") and len(booking_id) == 7 and booking_id[2:].isdigit()
    if not valid:
        return f"ERROR: Invalid booking ID '{booking_id}'. Expected: VN##### format."
    return f"CANCELLED: Appointment {booking_id} successfully cancelled."


# ---------------------------------------------------------------------------
# FunctionTool wrappers
# ---------------------------------------------------------------------------

search_doctor_tool = FunctionTool.from_defaults(
    fn=search_doctor,
    name="search_doctor",
    description=(
        "Search for available doctors by department and hospital. "
        "Use before booking to get a valid doctor_id."
    ),
)

book_appointment_tool = FunctionTool.from_defaults(
    fn=book_appointment,
    name="book_appointment",
    description=(
        "Book a medical appointment. Requires doctor_id from search_doctor, "
        "appointment datetime, patient name, and phone number."
    ),
)

cancel_appointment_tool = FunctionTool.from_defaults(
    fn=cancel_appointment,
    name="cancel_appointment",
    description="Cancel an existing appointment using its booking_id (VN##### format).",
)

# ---------------------------------------------------------------------------
# Agent builder
# ---------------------------------------------------------------------------

def build_agent() -> ReActAgent:
    """Construct and return a LlamaIndex ReActAgent."""
    llm = Groq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
    )

    tools = [search_doctor_tool, book_appointment_tool, cancel_appointment_tool]

    agent = ReActAgent.from_tools(
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=8,
        system_prompt=(
            "You are a Vinmec hospital virtual assistant. "
            "Help patients find doctors and book appointments. "
            "Always search for a doctor before booking. "
            "Respond in Vietnamese."
        ),
    )
    return agent


if __name__ == "__main__":
    agent = build_agent()
    query = (
        "Đặt lịch khám tim mạch ngày 25/04/2026 lúc 9h sáng ở Vinmec Hà Nội. "
        "Tên: Nguyễn Minh Tuấn, SĐT: 0912345678."
    )
    print(f"USER: {query}\n")
    response = agent.chat(query)
    print("\n=== FINAL ANSWER ===")
    print(response)
