# VinBigdata Internship — AI Safety & Agent Systems

12/2024 - 06/2025 | NLP Team @ VinBigdata

## Overview

During my internship at VinBigdata's NLP team, I worked on two main initiatives:

1. **Customizing NeMo Guardrails for Vietnamese SLM (vigpt)** — input rails + function-call rails
2. **AI Agent framework comparative study** — evaluated LangChain, LlamaIndex, n8n, OpenClaw for Vinmec virtual assistant use case

## Projects

### [01-guardrails/](./01-guardrails/)
NeMo Guardrails customization for vigpt (T5-based Vietnamese SLM).

**Sub-tasks:**
- Function-call rail with synthetic noisy data (Gemini API generated 14,471 samples)
- Input rail with Colang flows for sensitive topics (politics, history opinions)

**Tech:** NeMo Guardrails 0.11, Colang 2.0, Gemini API, Groq llama-3.1-8b (proxy for vigpt)

[→ Project details](./01-guardrails/README.md)

### [02-agent-survey/](./02-agent-survey/)
Comparative analysis of 4 agent frameworks on Vinmec appointment booking use case.

**Frameworks evaluated:**
- LangChain (28/30) — winner for production
- LlamaIndex (23/30) — best for RAG-heavy
- n8n (21/30) — best for non-developers
- OpenClaw (13/30) — promising future-proof spec

**Reference:** [arXiv:2503.21460](https://arxiv.org/pdf/2503.21460)

[→ Full report](./02-agent-survey/REPORT.md)

## Author

**Ho Tu Minh** | Final-year AI undergrad @ UET-VNU  
htm93313@gmail.com | [LinkedIn](https://www.linkedin.com/in/ho-tu-minh/)
