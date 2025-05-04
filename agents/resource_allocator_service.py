# agents/resource_allocator_service.py

import pandas as pd
import time
from agents.resource_allocator_agent import ResourceAllocatorAgent
from utils.logger import log_decision

def run_resource_service():
    agent = ResourceAllocatorAgent()
    df = pd.read_csv("mock_data/resource_data.csv")

    print("?? Resource Allocator Agent starting...\n")
    for _, row in df.iterrows():
        data = row.to_dict()
        decision = agent.act(data)
        print(f"?? Resource Snapshot: {data}")
        print(f"?? Agent Decision: {decision}\n")
   log_decision(agent.name, data, decision 
        time.sleep(2)

if __name__ == "__main__":
    run_resource_service()