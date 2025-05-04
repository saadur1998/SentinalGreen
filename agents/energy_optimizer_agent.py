# sentinelgreen_project/agents/energy_optimizer_agent.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autogen import Agent
from utils.llm_client import get_energy_recommendation

class EnergyOptimizerAgent(Agent):
    def __init__(self, name="EnergyOptimizer", energy_threshold=70):
        super().__init__(name=name)
        self.energy_threshold = energy_threshold

    def act(self, sensor_data):
        current_energy = sensor_data.get("energy_usage", 0)
        llm_recommendation = get_energy_recommendation(current_energy)

        if current_energy > self.energy_threshold:
            action = (
                f"?? High energy detected ({current_energy} units).\n"
                f"?? Action: Reduce lighting, shift non-critical compute loads.\n"
                f"?? LLM Suggestion: {llm_recommendation}"
            )
        else:
            action = (
                f"? Energy usage normal ({current_energy} units). No immediate action needed.\n"
                f"?? LLM Suggestion: {llm_recommendation}"
            )
        return action