import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from nemoguardrails import RailsConfig, LLMRails

load_dotenv()

# print("API_BASE:", os.getenv("OPENAI_API_BASE"))
# print("API_KEY:", os.getenv("OPENAI_API_KEY")[:10])
app = FastAPI()

config = RailsConfig.from_path("./config")
rails = LLMRails(config)
print(config.models)
# print("Loaded config successfully")
# print(config)
class PromptRequest(BaseModel):                       
    message: str

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