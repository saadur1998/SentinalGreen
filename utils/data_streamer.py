# utils/data_streamer.py

import random
import pandas as pd
import time
from agents.energy_optimizer_agent import EnergyOptimizerAgent
from agents.cooling_manager_agent import CoolingManagerAgent
from agents.security_sentinel_agent import SecuritySentinelAgent
from agents.predictive_maintainer_agent import PredictiveMaintainerAgent
from agents.compliance_auditor_agent import ComplianceAuditorAgent
from agents.resource_allocator_agent import ResourceAllocatorAgent
from utils.logger import log_decision

# Simulated CSV paths (adjust as needed)
AGENT_CONFIG = {
    "energy": {
        "agent": EnergyOptimizerAgent(),
        "csv": "mock_data/energy_data.csv"
    },
    "cooling": {
        "agent": CoolingManagerAgent(),
        "csv": "mock_data/cooling_data.csv"
    },
    "security": {
        "agent": SecuritySentinelAgent(),
        "csv": "mock_data/security_log_data.csv"
    },
    "maintenance": {
        "agent": PredictiveMaintainerAgent(),
        "csv": "mock_data/maintenance_data.csv"
    },
    "compliance": {
        "agent": ComplianceAuditorAgent(),
        "csv": "mock_data/compliance_data.csv"
    },
    "resource": {
        "agent": ResourceAllocatorAgent(),
        "csv": "mock_data/resource_data.csv"
    }
}

def stream_agent(agent_type):
    config = AGENT_CONFIG.get(agent_type)
    if not config:
        print(f"? Unknown agent type: {agent_type}")
        return

    agent = config["agent"]
    df = pd.read_csv(config["csv"])

    print(f"\n?? Streaming data to {agent.name}...\n")
    for _, row in df.iterrows():
        data = row.to_dict()
        decision = agent.act(data)
        print(f"?? {agent_type.upper()} Input: {data}")
        print(f"?? Decision: {decision}\n")
        log_decision(agent.name, data, decision)
        time.sleep(2)

if __name__ == "__main__":
    print("Choose an agent to stream:")
    print("1. Energy Optimizer")
    print("2. Cooling Manager")
    print("3. Security Sentinel")
    print("4. Predictive Maintainer")
    print("5. Compliance Auditor")
    print("6. Resource Allocator")

    choice_map = {
        "1": "energy",
        "2": "cooling",
        "3": "security",
        "4": "maintenance",
        "5": "compliance",
        "6": "resource"
    }

    choice = input("Enter your choice (1-6): ")
    agent_key = choice_map.get(choice)
    if agent_key:
        stream_agent(agent_key)
    else:
        print("? Invalid choice.")