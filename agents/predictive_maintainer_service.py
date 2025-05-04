# agents/predictive_maintainer_service.py

import pandas as pd
import time
from agents.predictive_maintainer_agent import PredictiveMaintainerAgent
from utils.logger import log_decision

def run_maintenance_service():
    agent = PredictiveMaintainerAgent()
    df = pd.read_csv("mock_data/maintenance_data.csv")

    print("??? Predictive Maintainer Agent starting...\n")
    for _, row in df.iterrows():
        data = row.to_dict()
        decision = agent.act(data)
        print(f"?? Maintenance Record: {data}")
        print(f"?? Agent Decision: {decision}\n")

  log_decision(agent.name, data, decision)
        time.sleep(2)

if __name__ == "__main__":
    run_maintenance_service()