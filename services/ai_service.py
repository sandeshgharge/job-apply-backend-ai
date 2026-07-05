from services.model_connection import send_prompt
import json

def extract_job_data(job_description: str) -> dict:

    with open('prompts/extract_job_details_prompt.txt', 'r') as f:
        sample_prompt = f.read()

    sample_prompt = sample_prompt.replace("[job_description]", job_description)
    
    prompt = f"""
{sample_prompt}
"""


    output = send_prompt.call_model(prompt)
    print("Extracted job data:", output)
    return json.loads(output)