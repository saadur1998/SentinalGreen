# agents/predictive_maintainer_agent.py

from autogen import ConversableAgent
from utils.llm_client import get_llm_response

class PredictiveMaintainerAgent(ConversableAgent):
    def __init__(self, name="PredictiveMaintainer", system_message=None):
        if system_message is None:
            system_message = (
                "You are a Predictive Maintainer AI Agent for a data center. "
                "You analyze sensor data and hardware records to anticipate failures. "
                "Based on inputs, recommend 'No Action', 'Schedule Maintenance', or 'Urgent Inspection'."
            )
        super().__init__(name=name, system_message=system_message)

    def act(self, data_row):
        prompt = (
            f"Component: {data_row['component']}\n"
            f"Uptime (hours): {data_row['uptime_hours']}\n"
            f"Temperature Spike Count: {data_row['spikes']}\n"
            f"Last Maintenance (days ago): {data_row['last_maintenance']}\n"
            f"Failure History: {data_row['failure_history']}\n"
            "Based on this, what is the maintenance recommendation?"
        )
        decision = get_llm_response(prompt)
        return decision