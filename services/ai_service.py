from services.model_connection.factory import get_model_connection
import json

def extract_job_data(job_description: str) -> dict:

    with open('prompts/extract_job_details_prompt.txt', 'r') as f:
        sample_prompt = f.read()

    sample_prompt = sample_prompt.replace("[job_description]", job_description)
    
    prompt = f"""
{sample_prompt}
"""


    connection = get_model_connection()
    output = connection.call_model(prompt)
    print("Extracted job data:", output)
    return json.loads(output)