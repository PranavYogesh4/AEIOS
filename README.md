# AEIOS – Autonomous Explainable Intelligent Orchestration System

**A Multi-Agent AI System for Cybersecurity Analysis and Intelligent Decision Support**

## 1. Project Overview

AEIOS (Autonomous Explainable Intelligent Orchestration System) is a Python-based multi-agent AI system designed to perform cybersecurity analysis and generate structured, explainable decision-support reports.

The system coordinates multiple specialized AI agents through a central orchestrator. Each agent performs a specific task, such as research, threat analysis, report generation, planning, confidence evaluation, and explainability.

AEIOS combines agent collaboration, adaptive execution, memory management, knowledge retrieval, and performance monitoring to produce structured and actionable results.

## 2. Key Features

- **Multi-Agent Architecture:** Multiple specialized agents collaborate to complete complex tasks.
- **Centralized Orchestration:** Coordinates agent execution, task routing, and workflow management.
- **Cybersecurity Research:** Gathers and analyzes relevant information.
- **Threat Analysis:** Examines potential cybersecurity threats and risks.
- **Intelligent Report Generation:** Produces structured reports and recommendations.
- **Consensus Mechanism:** Coordinates outputs from different analysis stages.
- **Adaptive Execution:** Supports dynamic workflow execution and retry handling.
- **Memory Management:** Maintains relevant conversational context.
- **Knowledge Retrieval:** Uses RAG-based context retrieval to support agent responses.
- **Confidence Evaluation:** Assesses the quality and reliability of generated responses.
- **Explainable Decisions:** Provides decision traces and explanations.
- **Performance Monitoring:** Tracks execution progress and system performance.
- **Interactive Dashboard:** Provides a Streamlit-based interface for interacting with the system.

## 3. System Architecture

AEIOS follows a layered multi-agent architecture.

### Main Components

1. **Frontend Layer:** Streamlit interface containing Dashboard, Chat, Memory, Analytics, Decision Trace, and Settings.
2. **Backend Layer:** Handles application services, execution management, progress tracking, and analytics.
3. **Orchestration Layer:** Coordinates agents, workflows, retries, evaluation, and final responses.
4. **Specialized Agent Layer:** Performs individual research, threat analysis, reporting, planning, and evaluation tasks.
5. **Execution and Collaboration Layer:** Supports parallel execution, task routing, adaptive execution, and retry management.
6. **Memory and Knowledge Layer:** Manages conversation history, knowledge retrieval, and execution logs.
7. **External Services Layer:** Integrates the Groq LLM API and web search capabilities.

## 4. Specialized AI Agents

| Agent | Responsibility |
|---|---|
| Research Agent | Performs research and gathers relevant information. |
| Threat Agent | Analyzes potential threats and security risks. |
| Report Agent | Generates structured analytical reports. |
| Consensus Agent | Coordinates and consolidates agent outputs. |
| Planning Agent | Supports planning and task organization. |
| Reconstruction Agent | Supports reconstruction of relevant analysis context. |
| Self-Evaluation Agent | Evaluates generated results. |
| Reflection Agent | Performs reflective analysis of outputs. |
| Confidence Agent | Estimates response confidence. |
| Explainability Agent | Provides explanations and decision traces. |

## 5. Technology Stack

- **Programming Language:** Python
- **Frontend Framework:** Streamlit
- **LLM Integration:** Groq API
- **Language Model:** `openai/gpt-oss-120b`
- **AI Architecture:** Multi-Agent System
- **Knowledge Support:** Retrieval-Augmented Generation (RAG)
- **Version Control:** Git and GitHub

## 6. Project Structure

```text
AEIOS/
│
├── agents/
│   ├── orchestrator.py
│   ├── research_agent.py
│   ├── threat_agent.py
│   ├── report_agent.py
│   ├── consensus_agent.py
│   ├── planning_agent.py
│   ├── reconstruction_agent.py
│   ├── self_evaluation_agent.py
│   ├── reflection_agent.py
│   ├── confidence_agent.py
│   └── explainability_agent.py
│
├── backend/
│   ├── service.py
│   ├── progress_tracker.py
│   ├── execution_manager.py
│   └── analytics_manager.py
│
├── collaboration/
├── engine/
├── execution/
├── frontend/
│   ├── app.py
│   └── views/
│
├── knowledge_base/
├── memory/
├── tools/
├── utils/
├── workflows/
│
├── config.py
├── ingest.py
├── main.py
├── .gitignore
└── README.md
```

## 7. Installation and Setup

### Prerequisites

- Python 3.10 or later (use the version compatible with your dependencies).
- Git
- A Groq API key

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AEIOS
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root and configure the API credentials required by the application.

Example:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Use the exact variable names expected by your `config.py`. Never upload your actual `.env` file or API key to GitHub.

### Step 5: Run the Application

From the project root, execute:

```bash
streamlit run frontend/app.py
```

The application will open in your browser through Streamlit.

## 8. How AEIOS Works

The general processing workflow is:

1. The user submits a cybersecurity-related query through the Streamlit interface.
2. The backend receives the request and forwards it to the orchestrator.
3. The orchestrator identifies and coordinates the required agents.
4. Specialized agents perform research, threat analysis, and other assigned tasks.
5. The execution layer manages collaboration, task routing, and retries.
6. Memory and knowledge retrieval provide relevant contextual information.
7. The reporting and evaluation stages process the generated results.
8. Confidence and explainability components assess and explain the response.
9. The final decision-support output is returned to the user.

## 9. Expected Outputs

Depending on the request and successful execution of the relevant components, AEIOS can produce:

- Structured cybersecurity analysis reports.
- Threat assessments.
- Actionable recommendations.
- Confidence scores.
- Agent execution information.
- Decision traces and explanations.
- Evaluation results.

## 10. Security and Configuration

- Store API keys and credentials in environment variables.
- Never commit `.env` files or other sensitive information.
- Keep virtual environments and generated cache files out of version control.
- Review external inputs and generated reports before using them for operational security decisions.

## 11. Future Enhancements

Potential future improvements include:

- Additional specialized cybersecurity agents.
- Enhanced knowledge retrieval and contextual memory.
- Improved agent coordination and evaluation.
- More advanced explainability and visualization.
- Expanded performance analytics.
- Integration with additional security intelligence sources.

