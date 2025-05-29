# agents/resource_allocator_agent.py
import os
import pandas as pd
import asyncio

from typing import Annotated
from openai import AsyncOpenAI
from dotenv import load_dotenv

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function

class ResourceAllocatorPlugin:
    """Plugin for resource allocation and scaling recommendations."""

    def __init__(self):
        self.data = pd.read_csv("mock_data/resource_data.csv")

    @kernel_function(description="Get the next resource allocation reading from mock data.")
    def get_next_reading(self) -> Annotated[dict, "Returns the next resource allocation reading with timestamp."]:
        return self.data.iloc[0].to_dict()
    
    @kernel_function(description="Analyzes resource usage and provides recommendations.")
    def analyze_resource(self,
                         compute_load: float,
                         storage_utilization: float,
                         bandwidth: float,
                         cost: float,
                         status: str) -> Annotated[str, "Returns resource allocation analysis and recommendations."]:
        if status == "Overloaded":
            return "Scale Up Immediately! : Increase resources."
        if compute_load > 80:
            return "Suggestion: Scale Up, Increase compute resources."
        if storage_utilization > 90:
                return "Suggestion: Scale Up, Add more storage."
        if status == "Underutilized":
                return "Scale Down: Reduce compute resources."
        return "Maintain Current Allocation."

async def allocate_resources():
    # Initialize the environment and client
    load_dotenv()
    client = AsyncOpenAI(
        api_key="", #Use your own token or api key
        base_url="https://models.inference.ai.azure.com/",
    )

    # Create the chat completion service
    chat_completion_service = OpenAIChatCompletion(
        ai_model_id="gpt-4o-mini",
        async_client=client,
    )

    # Create plugin instance
    resource_plugin = ResourceAllocatorPlugin()

    # Create the resource allocator agent
    allocator_agent = ChatCompletionAgent(
        service=chat_completion_service,
        plugins=[resource_plugin],
        name="ResourceAllocator",
        instructions="""You are an AI agent specialized in resource allocation and scaling recommendations.
        Your role is to analyze resource usage and provide intelligent recommendations for optimal resource allocation.
        Use the available plugins to analyze resource usage and provide actionable insights.
        Based on inputs and plugins, recommend 'Scale Up', 'Scale Down', 'Reallocate', or 'Maintain Current Allocation'.""",
    )

    thread = None
    try:
        #while True:
            # Get the next reading from mock data
            reading = resource_plugin.get_next_reading()
            
            # Format the input for the agent
            user_input = (
                f"Compute Load (%): {reading['compute_load']}\n"
                f"Storage Utilization (%): {reading['storage_utilization']}\n"
                f"Bandwidth Usage (Mbps): {reading['bandwidth']}\n"
                f"Cost per Unit ($): {reading['cost']}\n"
                f"Current Allocation Status: {reading['status']}\n"
                "What is the recommended resource allocation action?"
            )

            print(f"\n[Resource Allocator] Processing: {user_input}")
            
            # Get agent's analysis
            response_text = ""
            async for response in allocator_agent.invoke_stream(
                message=user_input,
                thread=thread
            ):
                if thread is None:
                    thread = response.thread
                response_text += str(response)
                print(f"{response}", end="", flush=True)
            
            # Simulate real-time delay
            #await asyncio.sleep(0.5)

            if not response_text:
                response_text = "No response generated from resource allocation analysis."

            return response_text
    
    except KeyboardInterrupt:
        print("\n[Resource Allocator] Shutting down...")
    finally:
        if thread:
            await thread.delete()

if __name__ == "__main__":
    asyncio.run(allocate_resources())