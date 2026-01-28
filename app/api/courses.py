from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from app.models.course import Course, CourseCategory
from app.services.course_service import get_courses, get_course_by_id

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=List[Course])
def list_courses(
    phase: Optional[int] = Query(None, ge=1, le=3),
    category: Optional[CourseCategory] = None,
):
    return get_courses(phase=phase, category=category)

@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    """Fetch a single course by ID."""
    course = get_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
