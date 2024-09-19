import json
import os

import openai
from prompts import RESUME_PARSER_SYSTEM_PROMPT, JOB_DESCRIPTION_SYSTEM_PROMPT, RESUME_COMPARISON_SYSTEM_PROMPT

MODEL = "gpt-4o-mini"
openai.api_key = os.getenv('OPENAI_KEY')

def mask_pii_and_parse_resume_to_json(text):
    client = openai.OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
    model=MODEL,
    response_format={"type": "json_object"},
    temperature=0,
    messages=[
        {"role": "system", "content": RESUME_PARSER_SYSTEM_PROMPT},
        {"role": "user", "content": text}
        ]
    )
    return json.loads(response.choices[0].message.content)

def parse_job_description_to_json(text):
    client = openai.OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
    model=MODEL,
    response_format={"type": "json_object"},
    temperature = 0,
    messages=[
        {"role": "system", "content": JOB_DESCRIPTION_SYSTEM_PROMPT},
        {"role": "user", "content": text}
        ]
    )
    return json.loads(response.choices[0].message.content)

def analyze_resume(job_description_json, resume_json):
    text = f"""
    The job description is as follows:
    `job_description: {job_description_json}`
    The applicant resume is as follows:
    `resume: {resume_json}`
    """
    client = openai.OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
    model=MODEL,
    response_format={"type": "json_object"},
    temperature = 0,
    messages=[
        {"role": "system", "content": RESUME_COMPARISON_SYSTEM_PROMPT},
        {"role": "user", "content": text}
        ]
    )
    return json.loads(response.choices[0].message.content)