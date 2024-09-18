"""Database Adapter"""

from sqlalchemy.orm import Session

from . import schemas, models


def get_applicants(db: Session):
    return db.query(models.Applicant).all()


def create_applicant(db: Session, applicant: schemas.ApplicantCreate):
    db_applicant = models.Applicant(**applicant.dict())
    db.add(db_applicant)
    db.commit()
    db.refresh(db_applicant)

    return db_applicant
