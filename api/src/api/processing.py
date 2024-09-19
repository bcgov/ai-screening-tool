"""Temp Functions to Produce Fake Data

Insert processing here or replace completely.
"""

from uuid import uuid4

from .openai.utils import parse_job_description_to_json, mask_pii_and_parse_resume_to_json


def process_job_description(text: str) -> dict:
    jd = parse_job_description_to_json(text)

    return jd


def process_resume(text: str) -> tuple[dict]:
    r = mask_pii_and_parse_resume_to_json(text)

    return r
