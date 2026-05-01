from services.model_connection.send_prompt import call_model

def extract_job_data(job_description: str) -> dict:

    with open('prompts/extract_job_details_prompt.txt', 'r') as f:
        sample_prompt = f.read()

    sample_prompt = sample_prompt.replace("[job_description]", job_description)
    
    prompt = f"""
{sample_prompt}
"""


    output = call_model(prompt)
    return output