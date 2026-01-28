from app.models.course import Course, CourseCategory

COURSES = [

    # =========================
    # BUSINESS
    # =========================
    Course(id=1, course_name="Entrepreneurial Management", category=CourseCategory.BUSINESS, phase=1, credits=3),
    Course(id=2, course_name="Business Fundamentals", category=CourseCategory.BUSINESS, phase=1, credits=3),
    Course(id=3, course_name="Introduction to Financial Management", category=CourseCategory.BUSINESS, phase=1, credits=3),

    Course(id=4, course_name="Financial Management", category=CourseCategory.BUSINESS, phase=2, credits=6),
    Course(id=5, course_name="Management Skills", category=CourseCategory.BUSINESS, phase=2, credits=3),
    Course(id=6, course_name="Procurement & Supply Chain", category=CourseCategory.BUSINESS, phase=2, credits=3),

    Course(id=7, course_name="Corporate Social Responsibility", category=CourseCategory.BUSINESS, phase=3, credits=3),
    Course(id=8, course_name="Project Management", category=CourseCategory.BUSINESS, phase=3, credits=3),

    # =========================
    # COMMUNICATION
    # =========================
    Course(id=9, course_name="Personal Development", category=CourseCategory.COMMUNICATION, phase=1, credits=3),
    Course(id=10, course_name="Dutch", category=CourseCategory.COMMUNICATION, phase=1, credits=6),

    Course(id=11, course_name="Professional Communication", category=CourseCategory.COMMUNICATION, phase=2, credits=3),
    Course(id=12, course_name="French", category=CourseCategory.COMMUNICATION, phase=2, credits=6),

    # =========================
    # PROGRAMMING
    # =========================
    Course(id=13, course_name="Programming Fundamentals", category=CourseCategory.PROGRAMMING, phase=1, credits=6),
    Course(id=14, course_name="Scripting", category=CourseCategory.PROGRAMMING, phase=1, credits=6),

    Course(id=15, course_name="Programming Advanced", category=CourseCategory.PROGRAMMING, phase=2, credits=6),
    Course(id=16, course_name="Web Fundamentals", category=CourseCategory.PROGRAMMING, phase=2, credits=3),

    Course(id=17, course_name="DevOps", category=CourseCategory.PROGRAMMING, phase=3, credits=3),
    Course(id=18, course_name="Artificial Intelligence", category=CourseCategory.PROGRAMMING, phase=3, credits=3),

    # =========================
    # BUSINESS INTELLIGENCE
    # =========================
    Course(id=19, course_name="AI Tools", category=CourseCategory.BUSINESS_INTELLIGENCE, phase=1, credits=3),
    Course(id=20, course_name="Digital Skills", category=CourseCategory.BUSINESS_INTELLIGENCE, phase=1, credits=3),
    Course(id=21, course_name="Business Intelligence Fundamentals", category=CourseCategory.BUSINESS_INTELLIGENCE, phase=1, credits=3),

    Course(id=22, course_name="Business Intelligence Advanced", category=CourseCategory.BUSINESS_INTELLIGENCE, phase=2, credits=3),

    Course(id=23, course_name="Business Intelligence Lab", category=CourseCategory.BUSINESS_INTELLIGENCE, phase=3, credits=3),

    # =========================
    # DATA
    # =========================
    Course(id=24, course_name="Databases", category=CourseCategory.DATA, phase=1, credits=6),
    Course(id=25, course_name="Data Processing & Analysis", category=CourseCategory.DATA, phase=1, credits=3),

    Course(id=26, course_name="Data Science Fundamentals", category=CourseCategory.DATA, phase=2, credits=6),
    Course(id=27, course_name="Data Engineering", category=CourseCategory.DATA, phase=2, credits=6),

    Course(id=28, course_name="Machine Learning & Forecasting", category=CourseCategory.DATA, phase=3, credits=6),

    # =========================
    # SECURITY
    # =========================
    Course(id=29, course_name="Computing Fundamentals", category=CourseCategory.SECURITY, phase=1, credits=6),
    Course(id=30, course_name="Computer Toolkit", category=CourseCategory.SECURITY, phase=1, credits=3),

    Course(id=31, course_name="Cyber Crime Fundamentals", category=CourseCategory.SECURITY, phase=2, credits=3),
    Course(id=32, course_name="Legal Frameworks", category=CourseCategory.SECURITY, phase=2, credits=3),
    Course(id=33, course_name="Governance & Risk Management Frameworks", category=CourseCategory.SECURITY, phase=2, credits=3),
    Course(id=34, course_name="Identity & Access Management", category=CourseCategory.SECURITY, phase=2, credits=3),

    Course(id=35, course_name="Cyber Resilience", category=CourseCategory.SECURITY, phase=3, credits=3),
    Course(id=36, course_name="Hacking AI Systems", category=CourseCategory.SECURITY, phase=3, credits=3),
    Course(id=37, course_name="Privacy & Security by Design", category=CourseCategory.SECURITY, phase=3, credits=3),

    # =========================
    # HANDS-ON EXPERIENCE
    # =========================
    Course(id=38, course_name="Inspiration Lab", category=CourseCategory.HANDS_ON, phase=1, credits=3),
    Course(id=39, course_name="Project Lab", category=CourseCategory.HANDS_ON, phase=2, credits=3),

    Course(id=40, course_name="Internship", category=CourseCategory.HANDS_ON, phase=3, credits=21),
    Course(id=41, course_name="Integrated Lab", category=CourseCategory.HANDS_ON, phase=3, credits=9),
]
