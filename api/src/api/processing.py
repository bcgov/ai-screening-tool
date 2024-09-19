"""Temp Functions to Produce Fake Data

Insert processing here or replace completely.
"""

from uuid import uuid4


def process_job_description(text: str) -> dict:
    # TODO: add actual processing here

    return {"job": "description"}


def process_resume(text: str) -> tuple[dict]:
    # TODO: add actual processing here

    return {
        "unique_id": str(uuid4()),
        "masked_info": {"masked": "info"},
        "resume_data": {"other": "jazz"},
    }
