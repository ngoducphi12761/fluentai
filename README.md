# FluentAI – Autonomous CFD Simulation Assistant Powered by RAG, LLMs, and Rule-Based Reasoning

> Created by **Duc Phi Ngo (Mr. Bill)** — a highly experienced CFD/FEA engineer and AI/ML software developer, FluentAI bridges physics-based simulation with intelligent automation through structured reasoning and multimodal control.

---

## Project Vision

**FluentAI** redefines how engineers interact with simulation platforms like **Ansys Fluent**, **STAR-CCM+**, and **OpenFOAM**. By replacing GUI-based workflows with **natural language interaction**, FluentAI empowers users to control and automate simulation tasks using:

- 🔍 **Retrieval-Augmented Generation (RAG)** for context-aware knowledge recall  
- 🧠 **LLM-driven reasoning (LLaMA 3 / GPT)** for understanding simulation logic  
- ⚙️ **Rule-based action planning** to ensure reliable and deterministic execution  

**FluentAI** is more than a chatbot — it's a decision-making agent capable of understanding, planning, and executing complete CFD workflows from voice or text input.

---

## Why It Matters

In modern simulation workflows, engineers lose productivity to:
- Repetitive GUI operations across platforms
- Manual setup of simulation parameters and post-processing
- Lack of intelligent interfaces for engineering software

**FluentAI** eliminates these pain points by introducing:
- A **multi-intent voice/text interface**
- A **domain-aware LLM engine** that understands simulation language
- A **deterministic automation layer** built on PyFluent and structured decision rules

---

## Key Capabilities

### Multimodal user input
- Accepts both voice (via Google Speech-to-Text) and typed commands
- Classifies intent as question, knowledge query, or action plan

### Retrieval-Augmented Generation (RAG)
- Uses FAISS/ChromaDB to retrieve relevant engineering documents (YAML, PDFs, Fluent settings)
- Employs LangChain for structured RAG integration

### AI and natural language processing
- Powered by LLaMA 3 (or GPT-4) for contextual understanding and planning
- Generates JSON-formatted **action plans** using deterministic prompt logic and condition-action rules

### Deterministic simulation control
- Executes structured commands through PyFluent API:
  - Inlet velocity/temperature settings
  - Turbulence model configuration
  - Solver iteration count
  - Post-processing (contours, plane slicing)
- Currently supports **steady-state flow simulations**

### Modular CFD automation
- Uses a declarative `input.yaml` to define geometry, boundary conditions, solver settings, and outputs
- Translates LLM decisions into **safe, auditable Fluent operations**

### Software engineering stack
- Python 3.10+, modular architecture
- CLI + voice support for flexibility in demos and real use
- Logs, temp files, and YAML for traceability and reproducibility

---

## 📐 Architecture Overview

```text
            ┌──────────────────────┐
            │  User Input (Voice/Text)
            └──────────┬───────────┘
                     ↓
        ┌────────────────────────────┐
        │ Vector Search (FAISS + LangChain)
        └────────┬───────────────────┘
                 ↓
       ┌───────────────────────────────┐
       │ Prompt Template + Rule Engine │
       └────────┬──────────────────────┘
                ↓
           ┌────────────────────┐
           │  LLM (LLaMA 3 / GPT) │
           └────────┬───────────┘
                    ↓
      ┌──────────────────────────────┐
      │ JSON Action Plan Generator   │
      └────────┬─────────────────────┘
               ↓
     ┌───────────────────────────────┐
     │ Action Dispatcher (PyFluent)  │
     └───────────────────────────────┘

```
### Voice Output
Currently powered by **Google Text-to-Speech (GTTS)** for demo simplicity.
Will be upgraded to **Bark or ElevenLabs** in future versions for more natural, production-ready voice output