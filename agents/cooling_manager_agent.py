# agents/cooling_manager_agent.py
import os
import pandas as pd
import asyncio

from typing import Annotated
from openai import AsyncOpenAI
from dotenv import load_dotenv

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function

class CoolingMonitorPlugin:
    """Plugin for cooling monitoring and management."""

    def __init__(self):
        self.data = pd.read_csv("mock_data/cooling_data.csv")

    @kernel_function(description="Get the next cooling reading from mock data.")
    def get_next_reading(self) -> Annotated[dict, "Returns the next cooling reading with timestamp."]:
        return self.data.iloc[0].to_dict()

    @kernel_function(description="Analyzes cooling metrics and provides recommendations.")
    def analyze_cooling(self, temperature: float,
                        humidity: float,
                        rack_load: float) -> Annotated[str, "Returns cooling analysis and recommendations."]:
        if temperature > 27:
            return f"Temperature ({temperature} �C) above optimal. Increase cooling output."
        elif humidity > 60:
            return f"Humidity ({humidity}%) above optimal. Increase cooling output."
        elif rack_load > 80:
            return f"Rack load ({rack_load}%) above optimal. Increase cooling output."
        
        return f"Optimal cooling conditions. No action needed."
    
async def monitor_cooling():
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
    cooling_plugin = CoolingMonitorPlugin()

    # Create the cooling manager agent
    cooling_agent = ChatCompletionAgent(
        service=chat_completion_service,
        plugins=[cooling_plugin],
        name="CoolingManager",
        instructions="""You are an AI agent specialized in cooling monitoring and management.
        Your role is to analyze cooling metrics and provide intelligent recommendations for cooling optimization.
        Use the available plugins to analyze cooling data and provide actionable insights.
        Your goal is to maintain optimal temperature while minimizing energy consumption.""",
    )

    thread = None
    try:
        #while True:
            # Get the next reading from mock data
            reading = cooling_plugin.get_next_reading()

            # Format the input for the agent
            user_input = (
                f"Analyze cooling metrics:\n"
                f"Temperature: {reading['temperature']} �C\n"
                f"Humidity: {reading['humidity']} %\n"
                f"Rack Load: {reading['rack_load']} %\n"
                "Should the cooling be increased, decreased, or maintained?"
            )

            print(f"\n[Cooling Manager] Processing: {user_input}")

            # Get agent's analysis
            response_text = ""
            async for response in cooling_agent.invoke_stream(
                message = user_input,
                thread=thread
            ):
                if thread is None:
                    thread = response.thread
                response_text += str(response)
                print(f"{response}", end="", flush=True)
            
            # Simulate real-time delay
            #await asyncio.sleep(0.5)

            if not response_text:
                response_text = "No response generated from cooling analysis."

            return response_text
    
    except KeyboardInterrupt:
        print("\n[Cooling Manager] Shutting down...")
    finally:
        if thread:
            await thread.delete()

if __name__ == "__main__":
    asyncio.run(monitor_cooling())
