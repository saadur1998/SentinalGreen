# agents/cooling_manager_service.py

import pandas as pd
import time
from agents.cooling_manager_agent import CoolingManagerAgent
from utils.logger import log_decision

def run_cooling_service():
    agent = CoolingManagerAgent()
    df = pd.read_csv("mock_data/cooling_data.csv")

    print("?? Cooling Manager Agent starting...\n")
    for _, row in df.iterrows():
        data = row.to_dict()
        decision = agent.act(data)
        print(f"?? Data: {data}")
        print(f"?? Agent Decision: {decision}\n")
log_decision(agent.name, data, decision)
        time.sleep(2)

if __name__ == "__main__":
    run_cooling_service()