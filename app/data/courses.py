from app.models.course import Course, CourseCategory

COURSES = [
    Course(id=1, course_name="Databases", category=CourseCategory.DATA, phase=1, credits=6),
    Course(id=2, course_name="Data Processing & Analysis", category=CourseCategory.DATA, phase=1, credits=3),
    Course(id=3, course_name="Programming Fundamentals", category=CourseCategory.PROGRAMMING, phase=1, credits=6),
    Course(id=4, course_name="Scripting", category=CourseCategory.PROGRAMMING, phase=1, credits=6),
    Course(id=5, course_name="Computing Fundamentals", category=CourseCategory.SECURITY, phase=1, credits=6),
    Course(id=6, course_name="Business Fundamentals", category=CourseCategory.BUSINESS, phase=1, credits=3),

    Course(id=7, course_name="Data Science Fundamentals", category=CourseCategory.DATA, phase=2, credits=6),
    Course(id=8, course_name="Programming Advanced", category=CourseCategory.PROGRAMMING, phase=2, credits=6),
    Course(id=9, course_name="Identity & Access Management", category=CourseCategory.SECURITY, phase=2, credits=3),

    Course(id=10, course_name="Machine Learning & Forecasting", category=CourseCategory.DATA, phase=3, credits=6),
    Course(id=11, course_name="DevOps", category=CourseCategory.PROGRAMMING, phase=3, credits=3),
    Course(id=12, course_name="Cyber Resilience", category=CourseCategory.SECURITY, phase=3, credits=3),
]
