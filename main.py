from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.model_connection.send_prompt import call_model
from services.scraper import extract_job
from services.ai_service import extract_job_data

app = FastAPI()

class ExtractRequest(BaseModel):
    url: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate")
async def generate(request: Request):
    body = await request.json()
    data = call_model(body.get("prompt"))
    return {"output": data}

@app.post("/extract-job-data")
async def extract_job_data_endpoint(request: Request):
    #body = await request.json()
    #print(body)
    #job_description = body.get("job_description")

    with open('prompts/sample_job_description.txt', 'r') as f:
        job_description = f.read()
    return extract_job_data(job_description)
    pass

@app.post("/extract-job")
async def extract(req: ExtractRequest):
    return extract_job(req.url)

@app.get("/hello")
async def read_root():
    return {"Hello": "World"}