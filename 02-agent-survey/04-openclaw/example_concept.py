"""
OpenClaw Conceptual Implementation — Vinmec Appointment Booking
Reference: https://github.com/openclaw/openclaw

NOTE: This is a conceptual stub demonstrating how OpenClaw's
framework-agnostic tool specification would look in practice.
The `openclaw` package is not pip-installable as of writing;
this file shows the intended API design.

OpenClaw's core idea: define tools ONCE using a standardized JSON Schema spec,
then export them to ANY agent framework (LangChain, LlamaIndex, AutoGen, etc.)
via adapters — without rewriting tool logic per framework.
"""
from __future__ import annotations
from typing import Any, Callable

# ---------------------------------------------------------------------------
# Conceptual OpenClaw SDK (stubbed)
# ---------------------------------------------------------------------------

class ToolSpec:
    """Holds a declarative JSON Schema description of a single tool."""

    def __init__(self, name: str, description: str, parameters: dict):
        self.name = name
        self.description = description
        self.parameters = parameters

    def to_openai_schema(self) -> dict:
        """Export as OpenAI function-calling JSON schema."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


class ToolRegistry:
    """Bind Python implementations to OpenClaw tool specs."""

    def __init__(self):
        self._specs: dict[str, ToolSpec] = {}
        self._implementations: dict[str, Callable] = {}

    def register(self, spec: ToolSpec):
        """Decorator: bind a function to a named tool spec."""
        def decorator(fn: Callable) -> Callable:
            if spec.name in self._specs:
                raise ValueError(f"Tool '{spec.name}' already registered.")
            self._specs[spec.name] = spec
            self._implementations[spec.name] = fn
            return fn
        return decorator

    def call(self, name: str, **kwargs) -> Any:
        """Invoke a registered tool by name."""
        if name not in self._implementations:
            raise KeyError(f"Tool '{name}' not found in registry.")
        return self._implementations[name](**kwargs)

    def export_langchain(self):
        """
        Export all tools as LangChain StructuredTool objects.
        (Conceptual — requires openclaw.adapters.langchain)
        """
        raise NotImplementedError(
            "Install: uv pip install openclaw[langchain]\n"
            "Then: from openclaw.adapters.langchain import export_tools"
        )

    def export_llamaindex(self):
        """
        Export all tools as LlamaIndex FunctionTool objects.
        (Conceptual — requires openclaw.adapters.llamaindex)
        """
        raise NotImplementedError(
            "Install: uv pip install openclaw[llamaindex]\n"
            "Then: from openclaw.adapters.llamaindex import export_tools"
        )

    def list_tools(self) -> list[str]:
        return list(self._specs.keys())


# ---------------------------------------------------------------------------
# Vinmec tool specifications (framework-agnostic)
# ---------------------------------------------------------------------------

registry = ToolRegistry()

SEARCH_DOCTOR_SPEC = ToolSpec(
    name="search_doctor",
    description="Search for available doctors by department and hospital.",
    parameters={
        "type": "object",
        "properties": {
            "department": {
                "type": "string",
                "description": "Medical department in Vietnamese (e.g. 'tim mạch')",
            },
            "hospital": {
                "type": "string",
                "description": "Vinmec hospital branch (e.g. 'Vinmec Hà Nội')",
            },
        },
        "required": ["department", "hospital"],
    },
)

BOOK_APPOINTMENT_SPEC = ToolSpec(
    name="book_appointment",
    description="Book a medical appointment with a specific doctor.",
    parameters={
        "type": "object",
        "properties": {
            "doctor_id": {"type": "string"},
            "appointment_datetime": {"type": "string", "format": "date-time"},
            "patient_name": {"type": "string"},
            "patient_phone": {"type": "string"},
        },
        "required": ["doctor_id", "appointment_datetime", "patient_name", "patient_phone"],
    },
)

CANCEL_APPOINTMENT_SPEC = ToolSpec(
    name="cancel_appointment",
    description="Cancel an existing appointment by booking_id.",
    parameters={
        "type": "object",
        "properties": {
            "booking_id": {
                "type": "string",
                "pattern": "^VN[0-9]{5}$",
                "description": "Booking ID in VN##### format",
            }
        },
        "required": ["booking_id"],
    },
)


# ---------------------------------------------------------------------------
# Register implementations (the SAME functions used across all frameworks)
# ---------------------------------------------------------------------------

@registry.register(SEARCH_DOCTOR_SPEC)
def search_doctor(department: str, hospital: str) -> list[dict]:
    mock = {
        ("tim mạch", "vinmec hà nội"): [
            {"id": "D001", "name": "BS. Nguyễn Văn An", "specialty": "Tim mạch can thiệp"},
            {"id": "D002", "name": "BS. Trần Thị Bình", "specialty": "Siêu âm tim"},
        ]
    }
    return mock.get((department.lower(), hospital.lower()), [])


@registry.register(BOOK_APPOINTMENT_SPEC)
def book_appointment(
    doctor_id: str,
    appointment_datetime: str,
    patient_name: str,
    patient_phone: str,
) -> str:
    booking_id = f"VN{abs(hash(doctor_id + appointment_datetime + patient_name)) % 100000:05d}"
    return booking_id


@registry.register(CANCEL_APPOINTMENT_SPEC)
def cancel_appointment(booking_id: str) -> bool:
    return True


# ---------------------------------------------------------------------------
# Conceptual agent usage (requires openclaw package)
# ---------------------------------------------------------------------------
#
# from openclaw import Agent, GroqBackend
#
# agent = Agent(
#     backend=GroqBackend(
#         model="llama-3.3-70b-versatile",
#         api_key=os.getenv("GROQ_API_KEY"),
#     ),
#     tools=registry,
#     system_prompt="You are a Vinmec virtual assistant. Respond in Vietnamese.",
# )
#
# # Same registry, different runtime — no tool rewrites needed:
# langchain_agent = agent.export_langchain()
# llamaindex_agent = agent.export_llamaindex()
#
# response = agent.run("Đặt lịch khám tim mạch ngày 25/04/2026 ở Vinmec Hà Nội")
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    print("OpenClaw Concept Demo — registry only (no LLM)")
    print(f"Registered tools: {registry.list_tools()}\n")

    # Direct invocation (bypasses LLM — tests tool logic only)
    doctors = registry.call("search_doctor", department="tim mạch", hospital="vinmec hà nội")
    print(f"search_doctor result: {doctors}")

    booking_id = registry.call(
        "book_appointment",
        doctor_id="D001",
        appointment_datetime="2026-04-25 09:00",
        patient_name="Nguyễn Minh Tuấn",
        patient_phone="0912345678",
    )
    print(f"book_appointment result: {booking_id}")

    cancelled = registry.call("cancel_appointment", booking_id=booking_id)
    print(f"cancel_appointment result: {cancelled}")

    print("\nOpenAI-compatible schema for search_doctor:")
    import json
    print(json.dumps(SEARCH_DOCTOR_SPEC.to_openai_schema(), indent=2, ensure_ascii=False))
