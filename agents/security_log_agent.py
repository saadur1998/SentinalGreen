# agents/security_sentinel_agent.py
import os
import pandas as pd
import asyncio

from typing import Annotated
from openai import AsyncOpenAI
from dotenv import load_dotenv

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function

class SecurityLogPlugin:
    """Plugin for security monitoring and alerting."""

    def __init__(self):
        self.data = pd.read_csv("mock_data/security_log_data.csv")

    @kernel_function(description="Get the next security reading from mock data.")
    def get_next_reading(self) -> Annotated[dict, "Returns the next security reading with timestamp."]:
        return self.data.iloc[0].to_dict()
    
    @kernel_function(description="Analyzes security metrics and provides recommendations.")
    def analyze_security(self,
                         access_time: str,
                         user_role: str,
                         location: str,
                         method: str,
                         failed_attempts: int,
                         alerts: bool) -> Annotated[str, "Returns security analysis and recommendations."]:
        if failed_attempts > 0:
            return f"Security Alert: {failed_attempts} failed login attempts from {location} using {method}."
        if alerts:
            return "Security Alert: Potential intrusion detected."
        return "All clear: No security issues detected."
    
async def monitor_security():
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
    security_plugin = SecurityLogPlugin()

    # Create the security sentinel agent
    sentinel_agent = ChatCompletionAgent(
        service=chat_completion_service,
        plugins=[security_plugin],
        name="SecurityLog",
        instructions="""You are an AI agent specialized in security monitoring and alerting.
        Your role is to analyze security metrics and provide intelligent recommendations for optimal security.
        Use the available plugins to analyze security metrics and provide actionable insights.
        Based on inputs and plugins, recommend 'Allow', 'Investigate', 'Alert Admin', or 'Block Access'.""",
    )

    thread = None
    try:
        #while True:
            # Get the next reading from mock data
            reading = security_plugin.get_next_reading()
            # Format the input for the agent
            user_input = (
                f"Access Time: {reading['access_time']}\n"
                f"User Role: {reading['user_role']}\n"
                f"Access Location: {reading['location']}\n"
                f"Entry Method: {reading['method']}\n"
                f"Failed Attempts: {reading['failed_attempts']}\n"
                f"Any security alerts?: {reading['alerts']}\n"
                "Based on the above, what action should be taken?"
            )

            print(f"\n[Security Sentinel] Processing: {user_input}")

            # Get agent's analysis
            response_text = ""
            async for response in sentinel_agent.invoke_stream(
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
                response_text = "No response generated from security analysis."

            return response_text
    
    except KeyboardInterrupt:
        print("\n[Security Sentinel] Shutting down...")
    finally:
        if thread:
            await thread.delete()   

if __name__ == "__main__":
    asyncio.run(monitor_security())