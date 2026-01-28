from pydantic import BaseModel
from typing import List

class GradeInput(BaseModel):
    course_name: str
    grade: float

class CategoryScore(BaseModel):
    category: str
    average_grade: float
    total_credits: int

class AnalysisRequest(BaseModel):
    current_phase: int
    grades: List[GradeInput]


class FieldSignal(BaseModel):
    field: str
    score: float
    signal_strength: str

class AnalysisResponse(BaseModel):
    phase: int
    coverage: float
    category_scores: List[CategoryScore]
    field_signals: List[FieldSignal]
    signal_strength: str


class AnalysisResponse(BaseModel):
    phase: int
    coverage: float
    category_scores: List[CategoryScore]
    field_signals: List[FieldSignal]

