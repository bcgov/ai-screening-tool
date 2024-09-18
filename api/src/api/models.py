"""Database Models"""

from sqlalchemy import Column, String, Integer, JSON

from .database import Base


class Applicant(Base):
    __tablename__ = "applicants"

    uuid = Column(String, primary_key=True)
    score = Column(Integer, unique=True, index=True)
    details = Column(JSON)
