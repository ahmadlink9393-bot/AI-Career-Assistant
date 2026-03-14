from pydantic import BaseModel

# 1. هذا الكلاس يحدد شكل البيانات التي نتوقعها من المستخدم (Frontend)
class ResumeCreate(BaseModel):
    candidate_name: str
    content: str

# 2. هذا الكلاس يحدد شكل البيانات التي سنرسلها للمستخدم بعد الحفظ
class ResumeResponse(BaseModel):
    id: int
    candidate_name: str
    content: str

    class Config:
        # هذا السطر ضروري ليتمكن Pydantic من قراءة البيانات من SQLAlchemy
        from_attributes = True

class JobDescriptionCreate(BaseModel):
    title: str
    description_text: str

class JobDescriptionResponse(BaseModel):
    id: int
    title: str
    description_text: str

    class Config:
        from_attributes = True        