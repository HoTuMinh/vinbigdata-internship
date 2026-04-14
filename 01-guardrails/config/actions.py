"""
Actions for Vinmec NeMo Guardrails — function-call rail.
Extracts appointment info from user messages using Groq LLM.
"""
import json
import os

from groq import Groq
from nemoguardrails.actions import action
from pydantic import BaseModel


EXTRACT_SYSTEM_PROMPT = """
Bạn là hệ thống trích xuất thông tin đặt lịch khám tại Vinmec.
Từ tin nhắn của người dùng, hãy trích xuất các trường sau (nếu có):
- customer_name: tên khách hàng
- customer_phone: số điện thoại
- medical_department: khoa khám (ví dụ: tim mạch, da liễu, nhi)
- hospital_name: tên cơ sở / chi nhánh Vinmec
- appointment_date: ngày hẹn (định dạng DD/MM/YYYY hoặc như người dùng nói)
- appointment_time: giờ hẹn
- symptoms: triệu chứng / lý do khám
- customer_dob: ngày sinh khách hàng
- customer_place: địa chỉ / tỉnh thành
- relationship: quan hệ với bệnh nhân (bản thân, con, vợ/chồng, ...)
- cancel_num: số lịch cần hủy (integer, null nếu không hủy)
- is_yes: true/false/null — xác nhận đặt lịch của người dùng

Trả về JSON hợp lệ, chỉ JSON, không thêm bất kỳ văn bản nào khác.
Các trường không có thông tin thì để null.
"""


class AppointmentInfo(BaseModel):
    customer_name: str | None = None
    customer_phone: str | None = None
    medical_department: str | None = None
    hospital_name: str | None = None
    appointment_date: str | None = None
    appointment_time: str | None = None
    symptoms: str | None = None
    customer_dob: str | None = None
    customer_place: str | None = None
    relationship: str | None = None
    cancel_num: int | None = None
    is_yes: bool | None = None


@action(is_system_action=False)
async def extract_appointment_info(context: dict, **kwargs) -> dict:
    """Extract appointment info from the latest user message via Groq."""
    user_message = context.get("user_message", "")

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": EXTRACT_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.0,
        max_tokens=512,
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    try:
        data = json.loads(raw)
        info = AppointmentInfo(**data)
    except Exception:
        info = AppointmentInfo()

    return info.model_dump()
