from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class GradeInput(BaseModel):
    course_name: str
    grade: float = Field(ge=0, le=20, description="Grade must be between 0 and 20")

class CategoryScore(BaseModel):
    category: str
    average_grade: float
    total_credits: int

class AnalysisRequest(BaseModel):
    current_phase: int = Field(ge=1, le=3, description="Phase must be 1, 2, or 3")
    grades: List[GradeInput]
    
    @field_validator('grades')
    @classmethod
    def validate_course_names(cls, grades: List[GradeInput]):
        from app.data.courses import COURSES
        valid_course_names = {c.course_name for c in COURSES}
        
        for grade_input in grades:
            if grade_input.course_name not in valid_course_names:
                raise ValueError(
                    f"Unknown course name: '{grade_input.course_name}'. "
                    f"Must be one of the courses in the catalogue."
                )
        return grades


class FieldSignal(BaseModel):
    field: str
    score: float
    signal_strength: str
    contributors: dict  # {"categories": [...], "courses": [...]}
    evidence_level: str  # "Complete" or "Partial"

class AnalysisResponse(BaseModel):
    phase: int
    coverage: float
    confidence: str
    category_scores: List[CategoryScore]
    field_signals: List[FieldSignal]
    warnings: Optional[List[str]] = None

