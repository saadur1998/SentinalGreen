# dashboard/chainlit_app.py

import chainlit as cl
from utils.llm_client import get_llm_response

AGENT_SYSTEM_MESSAGES = {
    "Energy Optimizer": "You are a data center Energy Optimizer AI. Analyze energy usage and recommend energy-saving decisions.",
    "Cooling Manager": "You are a Cooling Manager AI. Adjust cooling based on temperature, humidity, and load.",
    "Security Sentinel": "You are a Security Sentinel AI. Review access logs and alert about unauthorized activity.",
    "Predictive Maintainer": "You are a Predictive Maintainer AI. Predict potential hardware failures and recommend maintenance.",
    "Compliance Auditor": "You are a Compliance & Green Auditor. Check environmental compliance and carbon targets.",
    "Resource Allocator": "You are a Resource Allocator AI. Optimize compute, storage, and bandwidth use."
}

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="?? Welcome to **SentinelGreen** – AI Agents for Secure & Sustainable Data Centers").send()

    # Sidebar dropdown
    await cl.ChatSettings(
        [
            cl.Dropdown(
                id="agent_selector",
                label="Select Agent",
                values=list(AGENT_SYSTEM_MESSAGES.keys()),
                initial_value="Energy Optimizer"
            )
        ]
    ).send()

@cl.on_message
async def on_message(msg: cl.Message):
    agent_choice = cl.user_session.get("agent_selector", "Energy Optimizer")
    system_msg = AGENT_SYSTEM_MESSAGES.get(agent_choice, "You are a helpful AI agent.")

    full_prompt = f"{system_msg}\n\nUser Input:\n{msg.content}"

    cl.user_session.set("last_prompt", full_prompt)

    await cl.Message(content="?? Thinking...").send()

    # LLM Response
    reply = get_llm_response(full_prompt)

    await cl.Message(content=f"?? **{agent_choice} Response:**\n{reply}").send()

@cl.on_settings_update
async def on_settings_update(settings):
    if "agent_selector" in settings:
        cl.user_session.set("agent_selector", settings["agent_selector"])