# Agent Framework Comparison Report

**Use case**: Vinmec virtual assistant — search doctors, book/cancel appointments  
**Test query**: "Đặt lịch khám tim mạch ngày 25/04/2026 ở Vinmec Hà Nội"  
**LLM**: Groq `llama-3.3-70b-versatile` (same model across all code-based frameworks)  
**Reference**: [A Survey of AI Agents (arXiv 2503.21460)](https://arxiv.org/pdf/2503.21460)

---

## Scoring rubric (1 = worst, 5 = best)

| Dimension | Description |
|-----------|-------------|
| Setup complexity | 1 = many steps/concepts; 5 = minimal friction to first working agent |
| Tool-calling | 1 = manual JSON wiring; 5 = clean declarative API, auto schema generation |
| Multi-step reasoning | 1 = single-turn only; 5 = robust multi-hop planning with memory |
| Production readiness | 1 = prototype only; 5 = battle-tested in production |
| Community/ecosystem | 1 = solo project; 5 = thousands of integrations and contributors |
| Vinmec fit (this use case) | 1 = poor fit; 5 = ideal fit |

---

## Comparison table

| Dimension | LangChain | LlamaIndex | n8n | OpenClaw |
|-----------|:---------:|:----------:|:---:|:--------:|
| Setup complexity | 3 | 3 | 5 | 2 |
| Tool-calling abstraction | 5 | 4 | 3 | 4 |
| Multi-step reasoning | 5 | 4 | 3 | 3 |
| Production readiness | 5 | 4 | 4 | 1 |
| Community / ecosystem | 5 | 4 | 3 | 1 |
| Vinmec fit | 5 | 4 | 3 | 2 |
| **Total / 30** | **28** | **23** | **21** | **13** |

---

## Dimension deep-dives

### 1. Setup complexity

**LangChain (3/5)** — pip install is straightforward, but newcomers are confused by the `langchain` / `langchain-core` / `langchain-community` split. Prompt templates, agent constructors, and executor wiring add ~50 lines of boilerplate before a single tool runs.

**LlamaIndex (3/5)** — Similar complexity. `FunctionTool.from_defaults()` is explicit but verbose. The package restructure (`llama_index` → `llama_index.core`) caused widespread migration pain.

**n8n (5/5)** — Import a JSON file, add credentials, click Activate. No coding, no environment setup beyond running the n8n server. Fastest time-to-first-run by far.

**OpenClaw (2/5)** — The conceptual API is clean, but the package isn't pip-installable. Requires understanding both the spec pattern and adapters before anything runs.

---

### 2. Tool-calling abstraction

**LangChain (5/5)** — `@tool` decorator with type-annotated function signature auto-generates the JSON schema. Docstring becomes the tool description. Cleanest DX of the code-based options.

```python
@tool
def search_doctor(department: str, hospital: str) -> str:
    """Search for available doctors."""
    ...
```

**LlamaIndex (4/5)** — `FunctionTool.from_defaults(fn=..., name=..., description=...)` works well but requires explicit wiring. No decorator magic.

**n8n (3/5)** — Tool descriptions are strings typed into GUI fields. No type system; the LLM receives a plain-text description and must infer structure. Brittle for complex schemas.

**OpenClaw (4/5)** — Explicit JSON Schema per tool. Verbose but maximally portable. `to_openai_schema()` works with any model that accepts function-calling format.

---

### 3. Multi-step reasoning

**LangChain (5/5)** — `AgentExecutor` with `max_iterations`, intermediate steps tracking, and configurable stopping conditions. Supports parallel tool calling in newer versions.

**LlamaIndex (4/5)** — ReAct loop with explicit Thought/Action/Observation trace. Good for debugging; slightly slower than direct tool-calling due to extra reasoning steps. Conversation memory via `agent.chat()` is a strength.

**n8n (3/5)** — n8n's AI Agent node supports up to 10 iterations, but the visual graph structure makes it hard to inspect intermediate reasoning. No native conversation memory across webhook calls (requires external storage node).

**OpenClaw (3/5)** — Conceptually supports any reasoning loop via the backend abstraction, but no reference implementation to evaluate.

---

### 4. Production readiness

**LangChain (5/5)** — LangSmith for observability, streaming, async, rate limiting, fallbacks — all first-class. Used at scale by thousands of companies.

**LlamaIndex (4/5)** — Solid but fewer battle-tested production patterns than LangChain. Strong for RAG-heavy workloads. LlamaCloud provides hosted evaluation/tracing.

**n8n (4/5)** — n8n is production-ready as a workflow platform. Healthcare deployments require careful data handling (HIPAA/GDPR). No audit trail for LLM reasoning steps by default.

**OpenClaw (1/5)** — Not production-ready. No known deployments, no SLA, no support. Risk of API changes.

---

### 5. Community / ecosystem

**LangChain (5/5)** — 90k+ GitHub stars, 500+ integrations, active Discord, weekly releases. Largest agent framework ecosystem.

**LlamaIndex (4/5)** — 35k+ stars, strong RAG community, LlamaHub for community integrations. Smaller but focused.

**n8n (3/5)** — 45k+ stars as a workflow tool, but AI Agent nodes are newer and have smaller community than code-based frameworks.

**OpenClaw (1/5)** — < 500 stars (estimated), no community forum, documentation sparse.

---

### 6. Vinmec appointment booking — fit analysis

**LangChain (5/5)** — Best overall fit. Clean tool-calling, easy to add EHR/CRM integrations later, production-grade observability for healthcare compliance.

**LlamaIndex (4/5)** — Good fit if Vinmec needs doctor knowledge-base RAG (e.g., "Bác sĩ nào chuyên về...?"). Tool-calling works but ReAct adds latency.

**n8n (3/5)** — Good for PoC and stakeholder demos. Non-technical hospital staff can modify workflows. Poor fit for complex multi-step reasoning or custom validation logic.

**OpenClaw (2/5)** — Good architectural idea for long-term portability, but not viable today due to ecosystem immaturity.

---

## Recommendation

| Scenario | Recommended framework |
|----------|-----------------------|
| Production Vinmec chatbot | **LangChain** — ecosystem, observability, tool-calling maturity |
| Doctor knowledge-base Q&A + booking | **LlamaIndex** — RAG + tool-calling in one framework |
| Internal PoC for non-technical stakeholders | **n8n** — no-code, fast demo, easy to modify |
| Multi-framework tooling standardization | **OpenClaw** — watch for 2026 roadmap; not ready yet |

**Bottom line**: For the Vinmec use case as specified (3 tools, production intent), **LangChain is the pragmatic choice today**. LlamaIndex is the right call if the scope expands to include document retrieval from medical records. n8n excels for rapid internal demos but cannot replace code-based agents in production healthcare systems.
