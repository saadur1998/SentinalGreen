# agents/compliance_auditor_service.py

import pandas as pd
import time
from agents.compliance_auditor_agent import ComplianceAuditorAgent
from utils.logger import log_decision

def run_compliance_service():
    agent = ComplianceAuditorAgent()
    df = pd.read_csv("mock_data/compliance_data.csv")

    print("?? Compliance & Green Auditor Agent starting...\n")
    for _, row in df.iterrows():
        data = row.to_dict()
        decision = agent.act(data)
        print(f"?? Metrics: {data}")
        print(f"?? Agent Decision: {decision}\n")

   log_decision(agent.name, data, decision)
        time.sleep(2)

if __name__ == "__main__":
    run_compliance_service()