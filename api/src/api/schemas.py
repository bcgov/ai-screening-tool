"""API Schemas"""

from typing import Any
from pydantic import BaseModel


class ApplicantBase(BaseModel):
    uuid: str
    score: int
    details: Any


class Applicant(ApplicantBase):
    class Config:
        from_attributes = True


class ApplicantCreate(ApplicantBase): ...
