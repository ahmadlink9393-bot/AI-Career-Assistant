from sqlalchemy.orm import Session
import models, schemas # استوردنا models بدلاً من database هنا

def create_resume(db: Session, resume: schemas.ResumeCreate):
    # نستخدم models.Resume لأن الكلاس موجود هناك الآن
    db_resume = models.Resume(
        candidate_name=resume.candidate_name,
        content=resume.content
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def create_job_description(db: Session, job: schemas.JobDescriptionCreate):
    # نستخدم models.JobDescription
    db_job = models.JobDescription(
        title=job.title,
        description_text=job.description_text
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


# لجلب كل السير الذاتية
def get_resumes(db: Session):
    return db.query(models.Resume).all()

# لجلب كل الوظائف
def get_jobs(db: Session):
    return db.query(models.JobDescription).all()