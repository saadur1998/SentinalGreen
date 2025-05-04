# llm_service/local_llm_service.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

class QueryRequest(BaseModel):
    input: str
    parameters: dict = {}

@app.post("/query")
async def query_llm(request: QueryRequest):
    prompt = request.input.strip().lower()

    # Simulated responses based on keywords
    if "cooling" in prompt:
        output = "Increase cooling to handle rising temperatures." if "30" in prompt else "Maintain current cooling settings."
    elif "access" in prompt or "failed attempts" in prompt:
        output = "Alert Admin due to repeated failed access attempts." if "4" in prompt else "Allow access."
    elif "maintenance" in prompt or "uptime" in prompt:
        output = "Schedule Maintenance soon." if "16000" in prompt else "No Action required."
    elif "carbon" in prompt or "compliance" in prompt:
        output = "Violation Detected." if "80" in prompt else "Compliant"
    elif "resource" in prompt or "bandwidth" in prompt:
        output = "Scale Down." if "underutilized" in prompt else "Maintain Current Allocation"
    elif "energy" in prompt:
        output = "Reduce load during peak hours to save energy." if "95" in prompt else "No action needed."
    else:
        output = "Maintain default operation."

    return JSONResponse(content={"output": output})

if __name__ == "__main__":
    uvicorn.run("llm_service.local_llm_service:app", host="127.0.0.1", port=8000, reload=True)