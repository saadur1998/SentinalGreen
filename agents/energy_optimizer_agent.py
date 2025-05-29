# sentinelgreen_project/agents/energy_optimizer_agent.py
import os
import pandas as pd
import asyncio

from typing import Annotated
from openai import AsyncOpenAI
from dotenv import load_dotenv

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function

class EnergyMonitorPlugin:
    """Plugin for energy monitoring and analysis."""
    
    def __init__(self, energy_threshold=70):
        self.energy_threshold = energy_threshold
        self.data = pd.read_csv('mock_data/energy_data.csv')

    @kernel_function(description="Get the next energy reading from mock data.")
    def get_next_reading(self) -> Annotated[dict, "Returns the next energy reading with timestamp."]:
        # This would be replaced with real sensor data in production
        return self.data.iloc[0].to_dict()

    @kernel_function(description="Analyzes energy usage and provides recommendations.")
    def analyze_energy(self, current_energy: float) -> Annotated[str, "Returns energy analysis and recommendations."]:
        if current_energy > self.energy_threshold:
            return (
                f"High energy detected ({current_energy} units).\n"
                f"Action: Reduce lighting, shift non-critical compute loads."
            )
        return f"Energy usage normal ({current_energy} units). No immediate action needed."

async def monitor_energy():
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
    energy_plugin = EnergyMonitorPlugin()
 # Create the energy monitor agent
    energy_agent = ChatCompletionAgent(
        service=chat_completion_service,
        plugins=[energy_plugin],
        name="EnergyMonitor",
        instructions="""You are an AI agent specialized in energy monitoring and optimization.
        Your role is to analyze energy usage data in real-time and provide intelligent recommendations for energy conservation and optimization. 
        Use the available plugins to analyze energy data and provide actionable insights.""",
    )

    thread = None
    try:
       # while True:
            # Get the next reading from mock data
            reading = energy_plugin.get_next_reading()
            
            # Format the input for the agent
            user_input = f"Analyze energy usage: {reading['energy_usage']} units at {reading['timestamp']}"
            
            print(f"\n[Energy Monitor] Processing: {user_input}")
            
            # Get agent's analysis
            response_text = ""
            async for response in energy_agent.invoke_stream(
                messages=user_input,
                thread=thread
            ):
                if thread is None:
                    thread = response.thread
                response_text += str(response)
                print(f"{response}", end="", flush=True)
            
            if not response_text:
                response_text = "No response generated from energy analysis."

            # Simulate real-time delay
            #await asyncio.sleep(1)
            
            return response_text
        
    except KeyboardInterrupt:
        print("\n[Energy Monitor] Shutting down...")
    finally:
        if thread:
            await thread.delete()

if __name__ == "__main__":
    asyncio.run(monitor_energy())