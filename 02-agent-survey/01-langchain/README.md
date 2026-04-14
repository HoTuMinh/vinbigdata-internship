# 01 — LangChain Agent

**Framework**: LangChain 0.3.13  
**LLM backend**: Groq `llama-3.3-70b-versatile`  
**Pattern**: `@tool` decorator → `create_tool_calling_agent` → `AgentExecutor`

## How it works

```
User query
  └─> ChatPromptTemplate (system + human + scratchpad)
        └─> ChatGroq (tool_calling)
              └─> AgentExecutor loop
                    ├─> search_doctor(department, hospital)
                    ├─> book_appointment(doctor_id, datetime, patient_name, phone)
                    └─> cancel_appointment(booking_id)
```

## Setup

```bash
cd 01-langchain
uv venv && uv pip install -r requirements.txt
cp ../../.env.example ../../.env   # add GROQ_API_KEY
python example.py
```

## Pros

- **Massive ecosystem**: 500+ integrations (vector stores, memory, retrievers, callbacks).
- **Mature tool-calling**: `@tool` + type hints = auto-generated JSON schema. Zero boilerplate.
- **Observability**: LangSmith tracing, `return_intermediate_steps`, `verbose` mode baked in.
- **Flexible chaining**: LCEL lets you swap components (LLM, prompt, parser) independently.
- **Production patterns**: streaming, async, retry, fallback all first-class.

## Cons

- **Abstraction overhead**: Multiple layers (Runnable → Chain → Agent → Executor) confuse newcomers.
- **Verbose setup**: Even simple agents need prompt + agent + executor wiring.
- **Frequent breaking changes**: 0.1→0.2→0.3 migrations required significant rewrites.
- **Import confusion**: `langchain`, `langchain-core`, `langchain-community` split adds friction.
- **Overkill for simple tasks**: A 3-tool agent is ~80 lines; bare OpenAI SDK would be ~30.

## Scope & Limitations

- Mock tool implementations; no real Vinmec API integration.
- No conversation memory across sessions (stateless per call).
- Error handling is minimal (production would need retry + fallback logic).
