# agents/cooling_manager_agent.py

from autogen import ConversableAgent
from utils.llm_client import get_llm_response

class CoolingManagerAgent(ConversableAgent):
    def __init__(self, name="CoolingManager", system_message=None):
        if system_message is None:
            system_message = (
                "You are a Cooling Manager AI Agent for a data center. "
                "Given real-time temperature, humidity, and rack load info, "
                "decide whether to increase, decrease, or maintain cooling output. "
                "Your goal is to maintain optimal temperature while minimizing energy consumption."
            )
        super().__init__(name=name, system_message=system_message)

    def act(self, data_row):
        prompt = (
            f"Temperature: {data_row['temperature']} °C\n"
            f"Humidity: {data_row['humidity']} %\n"
            f"Rack Load: {data_row['rack_load']} %\n"
            "Should the cooling be increased, decreased, or maintained?"
        )
        decision = get_llm_response(prompt)
        return decision