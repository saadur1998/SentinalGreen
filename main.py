from agents.energy_optimizer_agent import EnergyOptimizerAgent
import pandas as pd
import time

# Load mock data
data = pd.read_csv('mock_data/energy_data.csv')

# Initialize agent
energy_agent = EnergyOptimizerAgent()

# Simulate reading and agent action
for _, row in data.iterrows():
    decision = energy_agent.act(row)
    print(f"Timestamp: {row['timestamp']} | Decision: {decision}")
    time.sleep(2)