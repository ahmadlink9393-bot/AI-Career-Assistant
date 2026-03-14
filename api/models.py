from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String)
    content = Column(Text, nullable=False)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)

class Optimization(Base):
    __tablename__ = "optimizations"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    optimized_text = Column(Text)
    score = Column(Integer)
    suggestions = Column(Text)

    resume = relationship("Resume")
    job = relationship("Job")    
    


class JobDescription(Base):
    __tablename__ = "job_descriptions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description_text = Column(Text)    