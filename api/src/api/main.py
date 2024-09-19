"""Web Adapter"""

from fastapi import Depends, FastAPI, UploadFile
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import get_db, engine
from .file_utils import extract_text_from_docx, extract_texts_from_resume_batch
from .openai.utils import analyze_resume
from .processing import process_job_description, process_resume

from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Screening Tool")


@app.post("/job-descriptions/")
async def upload_job_description(
    job_description: UploadFile, db: Session = Depends(get_db)
) -> dict:
    job_description_text = extract_text_from_docx(job_description.file)
    data = process_job_description(job_description_text)
    crud.create_job_description(db, schemas.JobDescriptionCreate(data=data))

    return {"status": "success"}


@app.get("/job-descriptions/", response_model=list[schemas.JobDescription])
def read_job_descriptions(db: Session = Depends(get_db)):
    return crud.get_job_descriptions(db)


@app.post("/resumes/batch/")
async def upload_resume_batch(
    resume_batch: UploadFile, db: Session = Depends(get_db)
) -> dict:
    processed_resumes = list(
        map(
            process_resume,
            extract_texts_from_resume_batch(resume_batch.file),
        )
    )

    for processed_resume in processed_resumes:
        crud.create_applicant(
            db,
            schemas.ApplicantCreate(
                unique_id=processed_resume["unique_id"],
                masked_info=processed_resume["masked_info"],
                resume_data=processed_resume["resume_data"],
            ),
        )

    return {"status": "success", "num_found": len(processed_resumes)}


@app.get("/applicants/", response_model=list[schemas.Applicant])
def read_applicants(db: Session = Depends(get_db)):
    return crud.get_applicants(db)


@app.post("/analyses/")
async def create_analysis(
    job_description_id: int, applicant_id: str, db: Session = Depends(get_db)
):
    job_description = crud.get_job_description_by_id(db, job_description_id)
    applicant = crud.get_applicant_by_id(db, applicant_id)

    s = {
        "unique_id": applicant.unique_id,
        "masked_info": applicant.masked_info,
        "resume_data": applicant.resume_data,
}
    print(job_description)
    print(applicant.resume_data)
    data = analyze_resume(job_description.data, s)

    # data = {"comparison": "between resume and job description"}

    crud.create_analysis(
        db,
        schemas.AnalysisCreate(
            job_description_id=job_description_id,
            applicant_id=applicant_id,
            data=data,
        ),
    )

    return {"status": "success"}


@app.get("/analyses/", response_model=list[schemas.Analysis])
async def read_analyses(db: Session = Depends(get_db)):
    return crud.get_analyses(db)
