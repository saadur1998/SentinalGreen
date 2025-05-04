# sentinelgreen_project/agents/energy_optimizer_service.py

from agents.energy_optimizer_agent import EnergyOptimizerAgent
import pandas as pd
import time
from utils.logger import log_decision

class EnergyOptimizerService:
    def __init__(self):
        self.agent = EnergyOptimizerAgent()

    def serve(self):
        """
        Main service loop for Energy Optimizer Agent.
        Reads from mock sensor data every few seconds.
        """
        data = pd.read_csv('mock_data/energy_data.csv')

        print("[Energy Optimizer Service] Starting...\n")
        
        while True:
            for _, row in data.iterrows():
                result = self.agent.act(row)
                print(f"[Energy Optimizer Service] {row['timestamp']} | Decision: {result}")

log_decision(agent.name, data, decision)

                time.sleep(2)  # Simulating real-time stream

if __name__ == "__main__":
    service = EnergyOptimizerService()
    service.serve()