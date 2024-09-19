"""Database Adapter"""

from sqlalchemy.orm import Session

from . import schemas, models


def create_job_description(db: Session, job_description: schemas.JobDescriptionCreate):
    db_job_description = models.JobDescription(**job_description.dict())
    db.add(db_job_description)
    db.commit()
    db.refresh(db_job_description)

    return db_job_description


def get_job_descriptions(db: Session):
    return db.query(models.JobDescription).all()


def get_job_description_by_id(db: Session, id: int):
    return db.query(models.JobDescription).filter(models.JobDescription.id == id).first()


def create_applicant(db: Session, applicant: schemas.ApplicantCreate):
    db_applicant = models.Applicant(**applicant.dict())
    db.add(db_applicant)
    db.commit()
    db.refresh(db_applicant)

    return db_applicant


def get_applicants(db: Session):
    return db.query(models.Applicant).all()


def get_applicant_by_id(db: Session, unique_id: str):
    return (
        db.query(models.Applicant)
        .filter(models.Applicant.unique_id == unique_id)
        .first()
    )


def create_analysis(db: Session, analysis: schemas.AnalysisCreate):
    db_analysis = models.Analysis(**analysis.dict())
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    return db_analysis


def get_analyses(db: Session):
    return db.query(models.Analysis).all()
