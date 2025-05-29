# agents/compliance_auditor_agent.py
import os
import pandas as pd
import asyncio

from typing import Annotated
from openai import AsyncOpenAI
from dotenv import load_dotenv

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function

class ComplianceMonitorPlugin:
    """Plugin for compliance monitoring and auditing."""

    def __init__(self):
        self.data = pd.read_csv("mock_data/compliance_data.csv")

    @kernel_function(description="Get the next compliance reading from mock data.")
    def get_next_reading(self) -> Annotated[dict, "Returns the next compliance reading with timestamp."]:
        return self.data.iloc[0].to_dict()

    @kernel_function(description="Analyzes compliance metrics and provides status.")
    def analyze_compliance(self, energy_kwh: float,
                         carbon_emission: float,
                         renewable_percent: float,
                         policy_target: float,
                         anomaly: str) -> Annotated[str, "Returns compliance analysis and recommendations."]:
        if anomaly !="nan":
            return f"Violation Detected: {anomaly}"
        elif renewable_percent < policy_target:
            return f"Flag for Review: Renewable energy usage ({renewable_percent}%) below target ({policy_target}%)"
        
        return f"Compliant: All metrics are within acceptable limits."

async def monitor_compliance():
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
    compliance_plugin = ComplianceMonitorPlugin()
 # Create the energy monitor agent
    compliance_agent = ChatCompletionAgent(
        service=chat_completion_service,
        plugins=[compliance_plugin],
        name="ComplianceAuditor",
        instructions= """You are an AI agent specialized in compliance monitoring and auditing. 
        Your role is to evaluate compliance with energy regulations and sustainability goals. 
        Based on metrics, output: 'Compliant', 'Flag for Review', or 'Violation Detected'. 
        Use the available plugins to analyze compliance data and provide actionable insights.""",
    )

    thread = None
    try:
        #while True:
            # Get the next reading from mock data
            reading = compliance_plugin.get_next_reading()

            # Format the input for the agent
            user_input = (
                f"Analyze compliance metrics:\n"
                f"Energy Consumption: {reading['energy_kwh']} kWh\n"
                f"Carbon Emission: {reading['carbon_emission']} tons CO2\n"
                f"Renewable Energy: {reading['renewable_percent']}%\n"
                f"Policy Target: {reading['policy_target']}%\n"
                f"Anomaly: {reading['anomaly']}"
            )

            print(f"\n[Compliance Auditor] Processing: {user_input}")

            # Get agent's analysis
            response_text = ""
            async for response in compliance_agent.invoke_stream(
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
                response_text = "No response generated from compliance analysis."

            return response_text
    
    except KeyboardInterrupt:
        print("\n[Compliance Auditor] Shutting down...")
    finally:
        if thread:
            await thread.delete()

if __name__ == "__main__":
    asyncio.run(monitor_compliance())