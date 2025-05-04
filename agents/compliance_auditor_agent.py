# agents/compliance_auditor_agent.py

from autogen import ConversableAgent
from utils.llm_client import get_llm_response

class ComplianceAuditorAgent(ConversableAgent):
    def __init__(self, name="ComplianceAuditor", system_message=None):
        if system_message is None:
            system_message = (
                "You are a Compliance & Green Auditor AI Agent for a data center. "
                "You evaluate compliance with energy regulations and sustainability goals. "
                "Based on metrics, output: 'Compliant', 'Flag for Review', or 'Violation Detected'."
            )
        super().__init__(name=name, system_message=system_message)

    def act(self, data_row):
        prompt = (
            f"Energy Consumption (kWh): {data_row['energy_kwh']}\n"
            f"Carbon Emission (tons CO2): {data_row['carbon_emission']}\n"
            f"Renewable Energy Usage (%): {data_row['renewable_percent']}\n"
            f"Policy Target: {data_row['policy_target']}\n"
            f"Reported Anomaly?: {data_row['anomaly']}\n"
            "What is your compliance status recommendation?"
        )
        decision = get_llm_response(prompt)
        return decision