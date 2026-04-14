"""
Example: Vinmec appointment booking — LlamaIndex ReActAgent trace.
Primary scenario: "Đặt lịch khám tim mạch ngày 25/04/2026 ở Vinmec Hà Nội"
"""
import time
from agent import build_agent

TEST_SCENARIOS = [
    {
        "name": "Full booking flow (primary use case)",
        "input": (
            "Đặt lịch khám tim mạch ngày 25/04/2026 lúc 9h sáng ở Vinmec Hà Nội. "
            "Tên tôi là Nguyễn Minh Tuấn, SĐT: 0912345678."
        ),
    },
    {
        "name": "Search doctors only",
        "input": "Cho tôi xem danh sách bác sĩ tim mạch ở Vinmec Hà Nội.",
    },
    {
        "name": "Cancel appointment",
        "input": "Hủy lịch khám VN54321 của tôi.",
    },
]


def run_scenario(agent, scenario: dict, index: int) -> None:
    print(f"\n{'=' * 62}")
    print(f"SCENARIO {index}: {scenario['name']}")
    print(f"{'=' * 62}")
    print(f"USER: {scenario['input']}\n")

    start = time.perf_counter()
    # ReActAgent.chat() returns a Response object; str() gives the answer text
    response = agent.chat(scenario["input"])
    elapsed = time.perf_counter() - start

    print(f"\n--- FINAL ANSWER ({elapsed:.2f}s) ---")
    print(str(response))

    # LlamaIndex exposes sources / tool calls via response.sources
    if hasattr(response, "sources") and response.sources:
        print(f"\n--- TOOL CALLS ---")
        for src in response.sources:
            print(f"  Tool: {src.tool_name}  |  Raw output: {str(src.raw_output)[:100]}")


def main() -> None:
    print("LlamaIndex ReActAgent — Vinmec Virtual Assistant")
    print("Model : llama-3.3-70b-versatile (Groq)")
    print("Tools : search_doctor | book_appointment | cancel_appointment\n")

    agent = build_agent()

    # Primary use case
    run_scenario(agent, TEST_SCENARIOS[0], 1)

    # Uncomment for full suite:
    # agent.reset()
    # for i, scenario in enumerate(TEST_SCENARIOS, 1):
    #     run_scenario(agent, scenario, i)
    #     agent.reset()  # clear conversation memory between scenarios


if __name__ == "__main__":
    main()
