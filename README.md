# SentinelGreen: Autonomous AI Agent System for Secure & Sustainable Data Centers

## 🌱 Overview
**SentinelGreen** is a multi-agent, LLM-integrated AI system designed to optimize energy consumption, cooling, compliance, and cybersecurity within modern data centers. BuiSentinelGreen is an intelligent, multi-agent system designed to transform how modern data centers manage their resources, respond to operational risks, and achieve environmental sustainability goals. Data centers are among the most energy-intensive infrastructures globally, contributing significantly to electricity consumption and carbon emissions. At the same time, they are highly vulnerable to cybersecurity threats, hardware failures, and inefficiencies in cooling, resource allocation, and compliance.

SentinelGreen addresses these challenges using a team of six autonomous AI agents that work collaboratively to continuously optimize data center operations. By leveraging Microsoft Azure services and lightweight language models like Phi-3 Mini, SentinelGreen combines real-time sensor telemetry with natural language reasoning to deliver proactive insights and autonomous decision-making.

The system provides full flexibility—agents can operate locally for testing via FastAPI and Chainlit, or scale to production using Azure’s IoT, AI, and analytics ecosystem. It supports live telemetry ingestion, real-time data processing, predictive analytics, compliance checks, and actionable recommendations—all orchestrated by AutoGen-based intelligent agents. Built with a modular architecture, SentinelGreen serves as both a hackathon prototype and a blueprint for future-ready, sustainable, and secure digital infrastructure.

lt for the Microsoft AI Agents Hackathon 2025, SentinelGreen leverages the power of real-time telemetry, modular autonomous agents, Azure cloud services, and lightweight LLMs (like Phi-3 Mini) to deliver actionable insights and sustainability-driven automation.

This system demonstrates a complete end-to-end intelligent agent pipeline with flexible options for both local simulation and cloud-scale deployment using Microsoft Azure services and AutoGen/Chainlit frameworks.

---

🧠 System Architecture

🔧 Layered Architecture (Logical View)

[Physical World]
  └── Sensors → Energy / Cooling / Access Logs
       ↓
[Sensing & Ingestion Layer]
  └── Azure IoT Hub
       ↓
[Processing & Transformation Layer]
  └── Azure Stream Analytics
       ↓
[Storage & Modeling Layer]
  ├── Azure Data Lake Gen2 (Raw Data Storage)
  └── Azure Synapse Analytics (Query + ML Ready)
       ↓
[Intelligent Agent Layer]
  └── AutoGen Framework + Phi-3 Mini LLM
       ├── Energy Optimizer Agent
       ├── Cooling Manager Agent
       ├── Security Sentinel Agent
       ├── Predictive Maintainer Agent
       ├── Compliance Auditor Agent
       └── Resource Allocator Agent
       ↓
[Interaction Layer]
  ├── Chainlit Dashboard (UI)
  └── main.py CLI Interface


```

---

🤖 Agent Lineup (All Autonomous)

1. Energy Optimizer Agent

Analyzes real-time power usage (kWh), voltage levels, and peak load data from energy sensors. Based on this, it recommends actions like reducing load, scheduling redistribution, or deferring non-critical operations to off-peak hours — driving both energy efficiency and cost reduction.

2. Cooling Manager Agent

Monitors environmental factors like temperature, humidity, and rack-level heat distribution. It decides whether to increase/decrease cooling or maintain current HVAC output to ensure thermal efficiency, reduce energy waste, and prevent overheating.

3. Security Sentinel Agent

Continuously analyzes access logs, failed entry attempts, time-of-access patterns, and flagged badge activities. It determines whether to allow access, flag for review, alert security personnel, or block unauthorized entries — proactively enhancing physical data center security.

4. Predictive Maintainer Agent

Processes equipment lifecycle data such as uptime hours, temperature spikes, failure history, and time since last maintenance. It recommends maintenance actions like urgent inspection, scheduled servicing, or no action, helping prevent outages before they occur.

5. Compliance & Green Auditor Agent

Audits operational metrics such as carbon emissions, renewable energy usage, energy efficiency targets, and ESG policy adherence. It identifies violations, flags areas for review, and helps maintain alignment with sustainability regulations.

6. Resource Allocator Agent

Analyzes compute load, storage utilization, bandwidth usage, and unit cost in real-time. Based on current performance and workload patterns, it suggests scaling up/down, reallocating resources, or maintaining current levels for optimal performance and cost control.

Each agent operates independently yet follows the same logic backbone: receive structured data → convert into prompt → get recommendation from Phi-3 LLM → act/log/respond.

---

## 🛠️ Technologies Used

### 🌐 Microsoft Azure
- Azure IoT Hub
- Azure Stream Analytics
- Azure Synapse Analytics
- Azure Data Lake Gen2 Storage
- Azure Digital Twins *(optional)*
- Azure AI Studio (AI Foundry) – Phi-3 Mini deployment
- Azure OpenAI Service *(for production LLM scaling)*

### 🧩 LLMs and Agents
- [Phi-3 Mini (Azure AI Foundry)](https://github.com/microsoft/phi-3)
- AutoGen Framework (ConversableAgent)
- Local LLM FastAPI fallback for offline testing

### 📊 Frontend & CLI
- Chainlit UI (interactive agent testing)
- `main.py` CLI switchboard for terminal testing
- `logger.py` for unified logs
- `data_streamer.py` for testing agents from CSVs
- `device_simulator.py` for mock telemetry into Azure

### 📚 Learning Resources (Microsoft Reactor)
- [AI Agents Hackathon Page](https://microsoft.github.io/AI_Agents_Hackathon/)
- [Azure AI Agent Services Demo Code](https://github.com/Azure-Samples/python-ai-agent-frameworks-demos)
- [Phi-3 Mini Launch](https://github.com/microsoft/phi-3)
- [AI Foundry Deployment Guide](https://learn.microsoft.com/en-us/azure/ai-services/studio/overview)

---

## 🔄 End-to-End Flow (Step-by-Step)

1. Simulate IoT Telemetry:The process begins with generating mock telemetry data using device_simulator.py. This script simulates energy usage, temperature, access logs, component uptime, and more—representing live sensor readings in a data center. These JSON-formatted telemetry messages are continuously pushed into Azure IoT Hub to mimic real-time sensor behavior.

2. Stream Analytics → Storage:Once data arrives at the IoT Hub, an Azure Stream Analytics job picks it up and routes it to two storage destinations: Azure Data Lake Storage Gen2 for archival and bulk analysis, and Azure Synapse Analytics for querying and joining with historical or policy datasets. This forms the data backbone upon which all intelligent decisions are made.

3. Agent Activation (Local or Cloud):Agents can be run either through main.py (CLI) or data_streamer.py (batch simulation). Depending on the selected agent (e.g., Cooling Manager or Compliance Auditor), the system reads relevant inputs from mock CSVs (in development) or directly from Synapse (in production). These values are then passed into the agent’s logic via AutoGen’s ConversableAgent.

4. LLM Decisioning:Each agent crafts a structured prompt using its system message and the live input data. This prompt is sent to either the locally hosted FastAPI LLM (local_llm_service.py) or the cloud-hosted Phi-3 Mini deployed on Azure AI Foundry. The LLM processes the prompt and returns a decision such as "Scale Up Resources" or "Violation Detected" based on semantic understanding.

5. Response Logging & UI:Agent decisions are displayed on the terminal or in Chainlit’s browser-based UI. Every action is logged using the centralized logger.py module, storing time-stamped entries under /logs/. Users can also interactively test different agents using Chainlit’s sidebar dropdown menu, with real-time insights powered by LLM responses.

---

🧪 How to Run Locally and Live

🖥️ Local Mode (Offline Testing with Mock Data)

1. Set up your environment

Clone the repo

Create a .env file and configure:

USE_LOCAL_LLM=True
LOCAL_LLM_ENDPOINT=http://localhost:8000/query

Install dependencies:

pip install -r requirements.txt

2. Start the Local LLM Server

Run your mock FastAPI server:

uvicorn llm_service.local_llm_service:app --reload --port 8000

3. Simulate Data and Run Agents

Push mock data:

python mock_data/device_simulator.py

Launch agents using CLI:

python utils/data_streamer.py

Or test with interactive Chainlit UI:

chainlit run dashboard/chainlit_app.py -w

☁️ Live Mode (End-to-End Azure Pipeline)

1. Deploy Azure Resources

Create:

Azure IoT Hub + registered device (e.g. sentinelgreen-energy-sensor)

Azure Stream Analytics job (input: IoT Hub, output: Storage + Synapse)

Azure Synapse workspace and Lake Storage container

Azure AI Foundry project with Phi-3 Mini deployed as endpoint

2. Update .env Configuration

USE_LOCAL_LLM=False
AZURE_FOUNDRY_ENDPOINT=https://your-foundry-endpoint/models
AZURE_FOUNDRY_API_KEY=your_api_key_here
IOTHUB_DEVICE_CONNECTION_STRING=your_azure_iot_device_connection

3. Run Live Simulation

Start telemetry stream:

python mock_data/device_simulator.py

Confirm data flows into Azure via IoT → Stream Analytics → Storage/Synapse

4. Activate Agents

Same as local, but agents pull real-time synced data

Use main.py, data_streamer.py, or Chainlit for execution

5. Monitor Logs and Output

View .log files under /logs/

Optionally integrate dashboards or alerts (Teams/Slack/Power BI)

```

---

🌐 How It Works – Explained

1. ConversableAgent Pattern (AutoGen):  Each agent inherits from the ConversableAgent class in the AutoGen framework. This makes every agent modular, reusable, and capable of rich multi-turn interactions using a consistent message interface. The architecture lets each agent define its own system prompt and behavior logic using the act() method.

2. Data Flow and Input Handling: Each agent receives structured input from simulated sensor telemetry or Azure ingestion points. Inputs are preprocessed into Python dictionaries containing key metrics (e.g., temperature, access time, emissions) which are then used to generate prompts for the LLMs. The same logic applies whether running locally or in the cloud.

3. Prompt Engineering per Agent: Every agent encodes its real-world reasoning into a specific system prompt and user input template. This design ensures that Cooling Manager gets HVAC logic, while Resource Allocator gets compute/bandwidth info. Prompt formats are customized but share a reusable backend to ensure modularity.

4. LLM Decisioning Engine: These prompts are routed through llm_client.py to either the Azure-hosted Phi-3 Mini model or a local FastAPI mock LLM. The engine interprets natural language requests and returns minimal, actionable recommendations. This design keeps inference lightweight and transparent.

5. Output Management and Logging: All agent outputs (e.g., "Scale Down", "Alert Admin") are captured in CLI/Chainlit as well as written to rotating log files under /logs/. These logs help ensure traceability and auditing of decision pathways — critical for regulated environments and post-incident analysis.

6. Chainlit UI and Interactivity: A no-code interactive layer is built with Chainlit, providing a live dropdown for switching agents and sending data. This user-friendly interface enables rapid prototyping, demo delivery, and human-in-the-loop review without writing Python code.

7. Azure Wiring and Integration Flow: All data streaming is orchestrated through Azure services:

IoT devices send telemetry to Azure IoT Hub.

Stream Analytics reads incoming messages and applies transformation queries.

Output is delivered to Azure Data Lake Gen2 or Synapse Analytics for long-term storage.

Agents can be extended to query Synapse for real-time metrics (SQL-on-demand or Spark pool).

In production, this makes SentinelGreen cloud-scale and event-triggered — capable of taking action on every message as it enters the Azure edge pipeline.

---

## 📁 Directory Structure


sentinelgreen_project/
├── agents/                     # Contains all 6 agent classes and their service loops
│   ├── *_agent.py              # Each agent's LLM logic with prompt formatting
│   ├── *_service.py            # Loops through mock CSVs and streams data to the agent
│
├── dashboard/
│   └── chainlit_app.py         # Chainlit UI with agent dropdown + message interface
│
├── llm_service/
│   └── local_llm_service.py    # FastAPI server for local mock LLM response simulation
│
├── mock_data/                  # CSV mock datasets + IoT simulator
│   ├── *_data.csv              # Energy, cooling, security, compliance, etc.
│   └── device_simulator.py     # Pushes JSON sensor data to Azure IoT Hub
│
├── utils/
│   ├── logger.py               # Central logging utility for all agent outputs
│   ├── llm_client.py           # Unified LLM call logic for Azure or local LLM
│   └── data_streamer.py        # Agent runner CLI for any agent with mock data
│
├── main.py                     # Optional entry point to select and run any agent
├── .env                        # Environment variables for endpoints, keys, etc.
├── requirements.txt            # Python dependencies list
├── README.md                   # Complete documentation (this file)

Each folder serves a modular purpose to ensure testability, scalability, and clean structure for LLM + IoT + agentic AI development.

---

## ✅ Status
- [x] 6 Autonomous Agents implemented
- [x] Real-time simulation via IoT + Stream Analytics
- [x] Fully working LLM integration with Phi-3 Mini (Azure Foundry)
- [x] Chainlit interactive UI and CLI
- [x] Logging and modular services

---

## 🏁 Next Steps (After Hackathon)
- Integrate alerts via Microsoft Teams / Azure Functions
- Extend agent-to-agent communication
- Auto-remediation actions (HVAC API, VM scaling, etc.)
- Production deployment with Azure Kubernetes Service (AKS)

---

## 📞 Contact
**Team:** SentinelGreen  
Built by Neha Pawar and Saad Ur Rahman for Microsoft AI Agents Hackathon 2025

LinkedIn Neha: [https://www.linkedin.com/in/neha-pawar86]

LinkedIn Saad: [https://www.linkedin.com/in/saadurrahman]

---

> "Making data centers greener, smarter, and safer — one autonomous agent at a time."

