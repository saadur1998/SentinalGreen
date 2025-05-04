# agents/resource_allocator_agent.py

from autogen import ConversableAgent
from utils.llm_client import get_llm_response

class ResourceAllocatorAgent(ConversableAgent):
    def __init__(self, name="ResourceAllocator", system_message=None):
        if system_message is None:
            system_message = (
                "You are a Resource Allocator AI Agent for a data center. "
                "You analyze compute usage, storage pressure, and bandwidth demand "
                "to recommend optimal scaling decisions. Output one of the following: "
                "'Scale Up', 'Scale Down', 'Reallocate', or 'Maintain Current Allocation'."
            )
        super().__init__(name=name, system_message=system_message)

    def act(self, data_row):
        prompt = (
            f"Compute Load (%): {data_row['compute_load']}\n"
            f"Storage Utilization (%): {data_row['storage_utilization']}\n"
            f"Bandwidth Usage (Mbps): {data_row['bandwidth']}\n"
            f"Cost per Unit ($): {data_row['cost']}\n"
            f"Current Allocation Status: {data_row['status']}\n"
            "What is the recommended resource allocation action?"
        )
        decision = get_llm_response(prompt)
        return decision