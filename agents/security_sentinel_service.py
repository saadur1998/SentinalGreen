# agents/security_sentinel_service.py

import pandas as pd
import time
from agents.security_sentinel_agent import SecuritySentinelAgent
from utils.logger import log_decision

def run_security_service():
    agent = SecuritySentinelAgent()
    df = pd.read_csv("mock_data/security_log_data.csv")

    print("??? Security Sentinel Agent starting...\n")
    for _, row in df.iterrows():
        data = row.to_dict()
        decision = agent.act(data)
        print(f"?? Log Entry: {data}")
        print(f"?? Agent Decision: {decision}\n"

  log_decision(agent.name, data, decision)

        time.sleep(2)

if __name__ == "__main__":
    run_security_service()