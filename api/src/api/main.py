"""Web Adapter"""

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Screening Tool")


@app.get("/applicants/", response_model=list[schemas.Applicant])
def read_applicants(db: Session = Depends(get_db)):
    return crud.get_applicants(db)


@app.post("/applicants/", response_model=schemas.Applicant)
def create_applicants(applicant: schemas.Applicant, db: Session = Depends(get_db)):
    return crud.create_applicant(db, applicant)
