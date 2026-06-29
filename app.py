import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from nemoguardrails import RailsConfig, LLMRails

load_dotenv()

app = FastAPI()

config = RailsConfig.from_path("./config")

config.models[0].parameters["api_key"] = os.getenv("GROQ_API_KEY")
config.models[0].parameters["base_url"] = os.getenv("GROQ_BASE_URL")

rails = LLMRails(config)
print(config.models)

class PromptRequest(BaseModel):                       
    message: str

@app.get("/")
async def home():
    return {
        "status": "running",
        "message": "NeMo Guardrails API is running"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }

@app.post("/guard")
async def guard(req: PromptRequest):

    response = await rails.generate_async(
        messages=[
            {
                "role": "user",
                "content": req.message
            }
        ]
    )
    info = rails.explain()
    return {
        "response": response,
        "trace": info
    }
