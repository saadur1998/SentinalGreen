# agents/predictive_maintainer_agent.py
import os
import pandas as pd
import asyncio

from typing import Annotated
from openai import AsyncOpenAI
from dotenv import load_dotenv

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function

class PredictiveMaintainerPlugin:
    """Plugin for predictive maintenance analysis."""

    def __init__(self):
        self.data = pd.read_csv("mock_data/maintenance_data.csv")

    @kernel_function(description="Get the next maintenance reading from mock data.")
    def get_next_reading(self) -> Annotated[dict, "Returns the next maintenance reading with timestamp."]:
        return self.data.iloc[0].to_dict()
    
    @kernel_function(description="Analyzes maintenance data and provides recommendations.")
    def analyze_maintenance(self,
                            component: str,
                            uptime_hours: int,
                            spikes: int,
                            last_maintenance: int,
                            failure_history: str) -> Annotated[str, "Returns maintenance analysis and recommendations."]:
        if failure_history != "nan":
            return f" Past Failure detected: {component} has failed {failure_history} times in the last {uptime_hours} hours."
        elif spikes > 10:
            return f"Potential failure: {component} has {spikes} temperature spikes in the last {uptime_hours} hours."
        elif uptime_hours > 1000 and last_maintenance > 30:
            return f"Scheduled maintenance: {component} has been in operation for {uptime_hours} hours without maintenance."
        return f"No action needed: {component} is operating normally."
        
async def monitor_maintenance():
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
    maintenance_plugin = PredictiveMaintainerPlugin()

    # Create the predictive maintainer agent
    maintainer_agent = ChatCompletionAgent(
        service=chat_completion_service,
        plugins=[maintenance_plugin],
        name="PredictiveMaintainer",
         instructions="""You are an AI agent specialized in predictive maintenance.
        Your role is to analyze maintenance data and provide intelligent recommendations for proactive maintenance.
        
        IMPORTANT: You must ONLY analyze the data provided in the input. DO NOT make up or assume any data.
        The input will contain specific information about a single component including:
        - Component name
        - Uptime hours
        - Temperature spike count
        - Days since last maintenance
        - Failure history
        
        Based on ONLY these provided metrics, recommend one of:
        - 'No Action' if the component is operating normally
        - 'Schedule Maintenance' if maintenance is needed soon
        - 'Urgent Inspection' if immediate attention is required
        
        DO NOT analyze or mention any components that are not in the provided data.""",
    )

    thread = None
    try:
        #while True:
            # Get the next reading from mock data
            reading = maintenance_plugin.get_next_reading()

            # Format the input for the agent
            user_input = (
                "Analyze the following data and provide a maintenance recommendation:\n"
                "Use the data provided in the input to make a recommendation.\n"
                f"Component: {reading['component']}\n"
                f"Uptime (hours): {reading['uptime_hours']}\n"
                f"Temperature Spike Count: {reading['spikes']}\n"
                f"Last Maintenance (days ago): {reading['last_maintenance']}\n"
                f"Failure History: {reading['failure_history']}"
            )

            print(f"\n[Predictive Maintainer] Processing: {user_input}")

            # Get agent's analysis
            response_text = ""
            async for response in maintainer_agent.invoke_stream(
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
                response_text = "No response generated from predictive maintenance analysis."

            return response_text
    
    except KeyboardInterrupt:
        print("\n[Predictive Maintainer] Shutting down...")
    finally:
        if thread:
            await thread.delete()   

if __name__ == "__main__":
    asyncio.run(monitor_maintenance())