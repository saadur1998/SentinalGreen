# agents/security_sentinel_agent.py

from autogen import ConversableAgent
from utils.llm_client import get_llm_response

class SecuritySentinelAgent(ConversableAgent):
    def __init__(self, name="SecuritySentinel", system_message=None):
        if system_message is None:
            system_message = (
                "You are a Security Sentinel AI Agent for a data center. "
                "Your job is to analyze access logs and security events to detect anomalies. "
                "Recommend one of the following actions: 'Allow', 'Investigate', 'Alert Admin', or 'Block Access'."
            )
        super().__init__(name=name, system_message=system_message)

    def act(self, data_row):
        prompt = (
            f"Access Time: {data_row['access_time']}\n"
            f"User Role: {data_row['user_role']}\n"
            f"Access Location: {data_row['location']}\n"
            f"Entry Method: {data_row['method']}\n"
            f"Failed Attempts: {data_row['failed_attempts']}\n"
            f"Any security alerts?: {data_row['alerts']}\n"
            "Based on the above, what action should be taken?"
        )
        decision = get_llm_response(prompt)
        return decision