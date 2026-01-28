from typing import List, Optional
from app.models.course import Course, CourseCategory

class CourseRepository:
    """Abstraction for data access—will make switching to DB painless."""
    
    @staticmethod
    def get_all() -> List[Course]:
        from app.data.courses import COURSES
        return COURSES
    
    @staticmethod
    def get_by_id(course_id: int) -> Optional[Course]:
        all_courses = CourseRepository.get_all()
        return next((c for c in all_courses if c.id == course_id), None)
    
    @staticmethod
    def filter(phase: Optional[int] = None, category: Optional[CourseCategory] = None) -> List[Course]:
        results = CourseRepository.get_all()
        if phase is not None:
            results = [c for c in results if c.phase == phase]
        if category is not None:
            results = [c for c in results if c.category == category]
        return results

def get_courses(
    phase: Optional[int] = None,
    category: Optional[CourseCategory] = None
) -> List[Course]:
    """Business logic wrapper around repository."""
    return CourseRepository.filter(phase=phase, category=category)

def get_course_by_id(course_id: int) -> Optional[Course]:
    """Fetch a single course by ID."""
    return CourseRepository.get_by_id(course_id)
