# 02 — LlamaIndex Agent

**Framework**: llama-index-core 0.12.5  
**LLM backend**: Groq `llama-3.3-70b-versatile`  
**Pattern**: `FunctionTool` x3 → `ReActAgent.from_tools`

## How it works

```
User query
  └─> ReActAgent (ReAct loop: Thought → Action → Observation)
        ├─> search_doctor   (FunctionTool)
        ├─> book_appointment (FunctionTool)
        └─> cancel_appointment (FunctionTool)
```

ReAct loop runs until agent emits a final answer or `max_iterations` is hit.

## Setup

```bash
cd 02-llamaindex
uv venv && uv pip install -r requirements.txt
cp ../../.env.example ../../.env   # add GROQ_API_KEY
python example.py
```

## Pros

- **RAG-first design**: Deep integration with vector stores, document loaders, and query engines — ideal when tools need to retrieve from knowledge bases.
- **ReAct transparency**: Thought/Action/Observation printed verbosely; easy to debug reasoning chain.
- **Built-in conversation memory**: `agent.chat()` maintains turn history automatically.
- **Structured output**: `QueryEngineTool` wraps RAG pipelines as first-class agent tools.
- **Strong async support**: `agent.achat()` for production async workloads.

## Cons

- **Less mature for pure tool-calling**: ReAct can be slower than direct tool-use (LangChain) due to additional reasoning steps.
- **Verbose FunctionTool wiring**: Requires explicit `FunctionTool.from_defaults()` vs LangChain's `@tool` decorator.
- **Smaller ecosystem**: Fewer third-party integrations than LangChain.
- **Breaking API changes**: Package restructure (`llama_index` → `llama_index.core`) required full migration.
- **Overkill without RAG**: For pure tool-calling without document retrieval, LangChain is lighter.

## Scope & Limitations

- Mock tool implementations; no real Vinmec API integration.
- FunctionTool docstrings serve as tool descriptions — quality affects agent reasoning.
- No streaming support in this example.
