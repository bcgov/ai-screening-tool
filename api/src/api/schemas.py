"""API Schemas"""

from pydantic import BaseModel


class JobDescriptionBase(BaseModel):
    data: dict


class JobDescription(JobDescriptionBase):
    id: int

    class Config:
        from_attributes = True


class JobDescriptionCreate(JobDescriptionBase): ...


class ApplicantBase(BaseModel):
    unique_id: str
    masked_info: dict
    resume_data: dict


class ApplicantCreate(ApplicantBase): ...


class Applicant(ApplicantBase):
    class Config:
        from_attributes = True


class AnalysisBase(BaseModel):
    job_description_id: int
    applicant_id: str
    data: dict


class AnalysisCreate(AnalysisBase): ...


class Analysis(AnalysisBase):
    id: int

    class Config:
        from_attributes = True
