# FluentAI – Autonomous CFD Simulation Assistant Powered by RAG, LLMs, and Rule-Based Reasoning

> Created by **Duc Phi Ngo (Mr. Bill)** — a senior CFD/FEA engineer and AI/ML software developer, FluentAI bridges physics-based simulation with intelligent automation through structured reasoning and multimodal control.

---

## Project Vision

**FluentAI** redefines how engineers interact with simulation platforms like **Ansys Fluent**, **STAR-CCM+**, and **OpenFOAM**. By replacing GUI-based workflows with **natural language interaction**, FluentAI empowers users to control and automate simulation tasks using:

- **Retrieval-Augmented Generation (RAG)** for context-aware knowledge recall  
- **LLM-driven reasoning (LLaMA 3 / GPT)** for understanding simulation logic  
- **Rule-based action planning** to ensure reliable and deterministic execution  

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

## Fluentai Architecture Overview
```
User (Voice/Text)
    ↓
[1] Whisper (Speech-to-Text)
    ↓
[2] RAG Engine
    - Retrieves relevant CFD context from Vector Store (FAISS/Chroma)
    - Combines with command to form enriched prompt
    ↓
[3] LLM (LLaMA 3 / GPT-4)
    - Interprets enriched prompt
    - Generates YAML modifications or Fluent instructions
    ↓
[4] YAML Editor
    - Updates input.yaml dynamically
    ↓
[5] PyFluent Automation
    - Runs geometry → mesh → setup → solve → post-process
    ↓
[6] Output
    - Contour plots, reports
    - Voice status updates via gTTS
```
### Voice Output
Currently powered by **Google Text-to-Speech (GTTS)** for demo simplicity.
Will be upgraded to **Bark or ElevenLabs** in future versions for more natural, production-ready voice output

---

## How to Run FluentAI

### 1. Install dependencies

Make sure you have Python 3.10+ installed. Then run:

```bash
pip install -r requirements.txt

Optional (recommended): Create and activate a virtual environment

python -m venv pyfluent-env
pyfluent-env\Scripts\activate  # On Windows only

```
2. Configure Simulation in input.yaml
Edit the input.yaml file to define:

- Geometry path
- Boundary conditions
- Iterations, solver model
- Post-processing outputs

```yaml
geometry_file: geometry/Static Mixer geometry.dsco
iterations: 50
velocity_inlets:
  - inlet_name: velocity-inlet-1
    velocity: 3.0
```
3. Run 
```bash
py ./launch_fluentai.py

Run steady-state simulation for 50 iterations and set inlet temperature to 300 K
```
4. View Results
After a run, check:
- output_*/: for contour images

