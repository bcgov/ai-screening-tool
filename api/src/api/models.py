"""Database Models"""

from sqlalchemy import Column, ForeignKey, Integer, JSON, String, UniqueConstraint

from .database import Base


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)


class Applicant(Base):
    __tablename__ = "applicants"

    unique_id = Column(String, primary_key=True)
    masked_info = Column(JSON)
    resume_data = Column(JSON)


class Analysis(Base):
    __tablename__ = "analyses"
    __table_args__ = (UniqueConstraint("job_description_id", "applicant_id"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_description_id = Column(Integer, ForeignKey(JobDescription.id))
    applicant_id = Column(String, ForeignKey(Applicant.unique_id))
    data = Column(JSON)
