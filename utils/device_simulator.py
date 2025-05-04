# mock_data/device_simulator.py

import time
import random
import json
from azure.iot.device import IoTHubDeviceClient, Message

# Load device connection string from environment (set in .env)
import os
from dotenv import load_dotenv
load_dotenv()

CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
DEVICE_NAME = os.getenv("DEVICE_NAME", "sentinelgreen-energy-sensor")

client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

def simulate_energy_data():
    return {
        "type": "energy",
        "timestamp": time.time(),
        "usage_kw": random.randint(50, 100),
        "voltage": random.randint(210, 250),
        "load_percent": random.randint(60, 100)
    }

def simulate_cooling_data():
    return {
        "type": "cooling",
        "temperature": random.randint(22, 35),
        "humidity": random.randint(30, 60),
        "rack_load": random.randint(50, 95)
    }

def simulate_security_data():
    return {
        "type": "security",
        "access_time": f"{random.randint(0,23):02}:{random.randint(0,59):02}",
        "user_role": random.choice(["Technician", "Guest", "Admin", "Unknown"]),
        "location": random.choice(["Server Room", "Lobby", "Control Room"]),
        "method": random.choice(["Keycard", "QR", "Biometrics", "Unknown"]),
        "failed_attempts": random.randint(0, 5),
        "alerts": random.choice(["None", "Suspicious badge ID", "Repeated failures"])
    }

def simulate_maintenance_data():
    return {
        "type": "maintenance",
        "component": random.choice(["CPU Rack 12", "Cooling Pump A", "Power Unit 7"]),
        "uptime_hours": random.randint(2000, 20000),
        "spikes": random.randint(0, 5),
        "last_maintenance": random.randint(10, 180),
        "failure_history": random.choice(["Yes", "No"])
    }

def simulate_compliance_data():
    return {
        "type": "compliance",
        "energy_kwh": random.randint(90000, 200000),
        "carbon_emission": random.randint(25, 80),
        "renewable_percent": random.randint(30, 75),
        "policy_target": random.choice([50, 60]),
        "anomaly": random.choice(["None", "Overuse spike", "Emissions breach"])
    }

def simulate_resource_data():
    return {
        "type": "resource",
        "compute_load": random.randint(40, 95),
        "storage_utilization": random.randint(30, 90),
        "bandwidth": random.randint(100, 800),
        "cost": round(random.uniform(0.05, 0.25), 2),
        "status": random.choice(["Stable", "Overloaded", "Underutilized", "Balanced"])
    }

def send_message(payload):
    message = Message(json.dumps(payload))
    message.content_encoding = "utf-8"
    message.content_type = "application/json"
    print(f"?? Sending {payload['type']} data: {payload}")
    client.send_message(message)

if __name__ == "__main__":
    print(f"?? Starting IoT simulation for all agents using device: {DEVICE_NAME}")

    try:
        while True:
            send_message(simulate_energy_data())
            send_message(simulate_cooling_data())
            send_message(simulate_security_data())
            send_message(simulate_maintenance_data())
            send_message(simulate_compliance_data())
            send_message(simulate_resource_data())
            time.sleep(10)  # Simulate data every 10 seconds
    except KeyboardInterrupt:
        print("? Stopping simulation.")