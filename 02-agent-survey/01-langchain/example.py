"""
Example: Vinmec appointment booking — step-by-step trace.
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
        "input": "Cho tôi xem danh sách bác sĩ nhi khoa tại Vinmec Hà Nội.",
    },
    {
        "name": "Cancel appointment",
        "input": "Hủy lịch khám VN54321 của tôi.",
    },
]


def run_scenario(executor, scenario: dict, index: int) -> None:
    print(f"\n{'=' * 62}")
    print(f"SCENARIO {index}: {scenario['name']}")
    print(f"{'=' * 62}")
    print(f"USER: {scenario['input']}\n")

    start = time.perf_counter()
    result = executor.invoke({"input": scenario["input"]})
    elapsed = time.perf_counter() - start

    steps = result.get("intermediate_steps", [])

    print(f"\n--- TOOL TRACE ({len(steps)} call(s), {elapsed:.2f}s) ---")
    for i, (action, observation) in enumerate(steps, 1):
        obs_preview = str(observation).replace("\n", " ")[:100]
        print(f"  Step {i}: {action.tool}({action.tool_input})")
        print(f"         -> {obs_preview}")

    print(f"\n--- FINAL ANSWER ---")
    print(result["output"])


def main() -> None:
    print("LangChain Agent — Vinmec Virtual Assistant")
    print("Model : llama-3.3-70b-versatile (Groq)")
    print("Tools : search_doctor | book_appointment | cancel_appointment\n")

    executor = build_agent()

    # Run only the primary use case; comment in others for extended testing
    run_scenario(executor, TEST_SCENARIOS[0], 1)

    # Uncomment to run all scenarios:
    # for i, scenario in enumerate(TEST_SCENARIOS, 1):
    #     run_scenario(executor, scenario, i)


if __name__ == "__main__":
    main()
