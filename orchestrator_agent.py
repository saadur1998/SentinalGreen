import asyncio
from typing import Dict, List
import os
import sys

from typing import Annotated
from openai import AsyncOpenAI
from dotenv import load_dotenv

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function

# Import specialized agents
from agents.energy_optimizer_agent import EnergyMonitorPlugin, monitor_energy
from agents.cooling_manager_agent import CoolingMonitorPlugin, monitor_cooling
from agents.security_log_agent import SecurityLogPlugin, monitor_security
from agents.predictive_maintainer_agent import PredictiveMaintainerPlugin, monitor_maintenance
from agents.compliance_auditor_agent import ComplianceMonitorPlugin, monitor_compliance
from agents.resource_allocator_agent import ResourceAllocatorPlugin, allocate_resources

class OrchestratorPlugin:
    """Plugin for orchestrating different datacenter monitoring agents."""
    
    def __init__(self):
        # Initialize all agent plugins
        self.agents = {
            "energy": EnergyMonitorPlugin(),
            "cooling": CoolingMonitorPlugin(),
            "security": SecurityLogPlugin(),
            "maintenance": PredictiveMaintainerPlugin(),
            "compliance": ComplianceMonitorPlugin(),
            "resource": ResourceAllocatorPlugin()
        }
        
        # Define agent responsibilities
        self.agent_responsibilities = {
            "energy": "Monitor and optimize energy usage, power consumption, and efficiency",
            "cooling": "Manage cooling systems, temperature monitoring, and thermal optimization",
            "security": "Monitor security logs, access attempts, and potential threats",
            "maintenance": "Predict and schedule maintenance, monitor equipment health",
            "compliance": "Ensure regulatory compliance and audit requirements",
            "resource": "Optimize resource allocation and utilization"
        }

    @kernel_function(description="Get the list of available agents and their responsibilities.")
    def get_available_agents(self) -> Dict[str, str]:
        return self.agent_responsibilities

    @kernel_function(description="Route an issue to the appropriate agent based on the problem description.")
    def route_issue(self, problem_description: str) -> str:
        if "power" in problem_description.lower() or "energy" in problem_description.lower():
            return "energy"
        elif "temperature" in problem_description.lower() or "cooling" in problem_description.lower():
            return "cooling"
        elif "security" in problem_description.lower() or "access" in problem_description.lower():
            return "security"
        elif "maintenance" in problem_description.lower() or "equipment" in problem_description.lower():
            return "maintenance"
        elif "compliance" in problem_description.lower() or "audit" in problem_description.lower():
            return "compliance"
        elif "resource" in problem_description.lower() or "allocation" in problem_description.lower():
            return "resource"
        else:
            return "unknown"

    @kernel_function(description="Execute the appropriate agent based on the issue.")
    async def execute_agent(self, agent_name: str, issue: str) -> str:
        if agent_name in self.agents:
            print(f"\n[Orchestrator] Executing {agent_name} agent...")
            
            try:
                # Execute the appropriate monitoring function based on agent name
                if agent_name == "energy":
                    result = await monitor_energy()
                    return f"Energy Analysis: {result}"
                elif agent_name == "cooling":
                    result = await monitor_cooling()
                    return f"Cooling Analysis: {result}"
                elif agent_name == "security":
                    result = await monitor_security()
                    return f"Security Analysis: {result}"
                elif agent_name == "maintenance":
                    result = await monitor_maintenance()
                    return f"Maintenance Analysis: {result}"
                elif agent_name == "compliance":
                    result = await monitor_compliance()
                    return f"Compliance Analysis: {result}"
                elif agent_name == "resource":
                    result = await allocate_resources()
                    return f"Resource Analysis: {result}"
            except Exception as e:
                return f"Error executing {agent_name} agent: {str(e)}"
        return "No appropriate agent found for this issue."

async def run_orchestrator():
    # Initialize the environment and client
    load_dotenv()
    client = AsyncOpenAI(
        api_key="", #Use your own API key
        base_url="https://models.inference.ai.azure.com/",
    )

    # Create the chat completion service
    chat_completion_service = OpenAIChatCompletion(
        ai_model_id="gpt-4o-mini",
        async_client=client,
    )

    # Create orchestrator plugin instance
    orchestrator_plugin = OrchestratorPlugin()

    # Create the orchestrator agent
    orchestrator_agent = ChatCompletionAgent(
        service=chat_completion_service,
        plugins=[orchestrator_plugin],
        name="DatacenterOrchestrator",
        instructions="""You are an AI orchestrator specialized in datacenter monitoring and management.
        Your role is to:
        1. Analyze incoming issues and events
        2. Determine which specialized agent should handle each issue
        3. Coordinate between different agents when needed
        4. Ensure comprehensive monitoring of the datacenter
        5. Make decisions about agent prioritization and resource allocation
        
        When routing issues, consider:
        - The nature of the problem
        - The severity of the issue
        - The current workload of each agent
        - The interdependencies between different systems
        - The priority of different monitoring tasks
        
        You can route issues to:
        - Energy Optimizer: For power and efficiency issues
        - Cooling Manager: For temperature and cooling system issues
        - Security Sentinel: For security and access control issues
        - Predictive Maintainer: For maintenance and equipment health issues
        - Compliance Auditor: For regulatory and compliance issues
        - Resource Allocator: For resource utilization and allocation issues.
        
        IMPORTANT: Make sure to route the issue to the correct agent. Do not make up an agent that is not listed. 
        If the route_issue function returns "unknown", then decide yourself which agent should handle the issue.
        """,
    )

    thread = None
    try:
        while True:
            # Get input from monitoring systems or user
            user_input = input("\nEnter issue or event to analyze (or 'quit' to exit): ")
            if user_input.lower() == 'quit':
                break

            print(f"\n[Orchestrator] Analyzing: {user_input}")

            # First, get the orchestrator's analysis
            async for response in orchestrator_agent.invoke_stream(
                message=user_input,
                thread=thread
            ):
                if thread is None:
                    thread = response.thread
                print(f"{response}", end="", flush=True)
            
            # Then, route and execute the appropriate agent
            agent_name = orchestrator_plugin.route_issue(user_input)
            if agent_name != "unknown":
                print(f"\n[Orchestrator] Routing to {agent_name} agent...")
                result = await orchestrator_plugin.execute_agent(agent_name, user_input)
                print(f"\n[Orchestrator] Agent response: {result}")
            else:
                print("\n[Orchestrator] Could not determine appropriate agent for this issue.")
            
            # Simulate real-time delay
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        print("\n[Orchestrator] Shutting down...")
    finally:
        if thread:
            await thread.delete()

if __name__ == "__main__":
    asyncio.run(run_orchestrator())