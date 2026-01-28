from enum import Enum
from pydantic import BaseModel, Field

class CourseCategory(str, Enum):
    DATA = "Data"
    PROGRAMMING = "Programming"
    SECURITY = "Security"
    BUSINESS = "Business"

class Course(BaseModel):
    id: int = Field(description="Unique course identifier")
    course_name: str
    category: CourseCategory
    phase: int
    credits: int
