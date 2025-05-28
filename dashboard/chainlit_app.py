# dashboard/chainlit_app.py

import chainlit as cl
import asyncio
import sys
import os
# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator_agent import OrchestratorPlugin, run_orchestrator

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="?? Welcome to **SentinelGreen** 🏭 AI Orchestrator for Secure & Sustainable Data Centers\n\n"
                "I can help you with:\n"
                "• Energy optimization and power management\n"
                "• Cooling system monitoring and control\n"
                "• Security monitoring and threat detection\n"
                "• Predictive maintenance and equipment health\n"
                "• Compliance and regulatory requirements\n"
                "• Resource allocation and optimization\n\n"
                "Just describe your issue or concern, and I'll route it to the appropriate specialist agent."
    ).send()

    # Initialize the orchestrator
    cl.user_session.set("orchestrator", OrchestratorPlugin())

@cl.on_message
async def on_message(msg: cl.Message):
    # Get the orchestrator instance
    orchestrator = cl.user_session.get("orchestrator")
    
    # Show thinking message
    thinking_msg = await cl.Message(content="?? Analyzing your request...").send()
    
    try:
        # Route the issue to the appropriate agent
        agent_name = orchestrator.route_issue(msg.content)
        
        if agent_name != "unknown":
            # Update thinking message
            thinking_msg.content = f"?? Routing to {agent_name} specialist..."
            await thinking_msg.update()
            
            # Execute the appropriate agent
            result = await orchestrator.execute_agent(agent_name, msg.content)
            
            # Send the response
            await cl.Message(
                content=f"?? **{agent_name.title()} Specialist Response:**\n{result}"
            ).send()
            
            # Add a separator for clarity
            await cl.Message(content="---").send()
        else:
            # If no specific agent is identified, use the orchestrator's analysis
            thinking_msg.content = "?? Analyzing with orchestrator..."
            await thinking_msg.update()
            
            # Get orchestrator's analysis
            async for response in orchestrator.orchestrator_agent.invoke_stream(
                message=msg.content,
                thread=orchestrator.thread
            ):
                if orchestrator.thread is None:
                    orchestrator.thread = response.thread
                await cl.Message(content=str(response)).send()
    
    except Exception as e:
        await cl.Message(
            content=f"?? Error: {str(e)}\nPlease try again or rephrase your request."
        ).send()

@cl.on_stop
async def on_stop():
    # Clean up any resources
    orchestrator = cl.user_session.get("orchestrator")
    if orchestrator and orchestrator.thread:
        await orchestrator.thread.delete()