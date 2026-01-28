from typing import List
from app.data.courses import COURSES
from app.data.fields import FIELDS
from app.models.analysis import GradeInput, CategoryScore, FieldSignal

def signal_strength(score: float) -> str:
    if score >= 14:
        return "Strong"
    if score >= 11:
        return "Consistent"
    return "Emerging"

def calculate_confidence(coverage: float) -> str:
    """Derive confidence label from coverage."""
    if coverage >= 0.7:
        return "High"
    if coverage >= 0.4:
        return "Medium"
    return "Low"

def run_analysis(
    current_phase: int,
    grades: List[GradeInput]
) -> dict:

    warnings = []
    
    # Index grades by course name
    grade_map = {g.course_name: g.grade for g in grades}

    # Filter courses by phase
    eligible_courses = [
        c for c in COURSES if c.phase <= current_phase
    ]
    
    # Check if no eligible courses for phase
    if not eligible_courses:
        warnings.append(f"No courses available for phase {current_phase}")

    category_totals = {}
    category_credits = {}

    completed_credits = 0
    total_credits = sum(c.credits for c in eligible_courses)

    for course in eligible_courses:
        if course.course_name not in grade_map:
            continue

        grade = grade_map[course.course_name]
        completed_credits += course.credits

        category = course.category

        category_totals.setdefault(category, 0)
        category_credits.setdefault(category, 0)

        category_totals[category] += grade * course.credits
        category_credits[category] += course.credits
    
    # Check if grades submitted but none matched
    if grades and completed_credits == 0:
        warnings.append("Grades were submitted but none matched eligible courses for this phase")

    category_scores = []

    for category in category_totals:
        avg = category_totals[category] / category_credits[category]
        category_scores.append(
            CategoryScore(
                category=category,
                average_grade=round(avg, 2),
                total_credits=category_credits[category]
            )
        )

    coverage = round(
        completed_credits / total_credits, 2
    ) if total_credits > 0 else 0.0
    
    # Check for very low coverage
    if coverage < 0.2 and coverage > 0:
        warnings.append(f"Very low coverage ({coverage:.0%}): Results may not be representative")

    # Convert category scores to dict
    category_score_map = {
        cs.category: cs.average_grade
        for cs in category_scores
    }

    field_signals = []

    for field, weights in FIELDS.items():
        total_weight = 0
        weighted_sum = 0
        contributing_categories = []
        contributing_courses = []

        for category, weight in weights.items():
            if category in category_score_map:
                weighted_sum += category_score_map[category] * weight
                total_weight += weight
                contributing_categories.append(category)

        if total_weight == 0:
            continue

        score = weighted_sum / total_weight
        
        # Determine evidence level
        all_categories = set(weights.keys())
        present_categories = set(contributing_categories)
        evidence_level = "Complete" if present_categories == all_categories else "Partial"
        
        # Find contributing courses
        for course in eligible_courses:
            if course.category in contributing_categories:
                if course.course_name in grade_map:
                    contributing_courses.append(course.course_name)

        field_signals.append(
            FieldSignal(
                field=field,
                score=round(score, 2),
                signal_strength=signal_strength(score),
                contributors={
                    "categories": contributing_categories,
                    "courses": contributing_courses
                },
                evidence_level=evidence_level
            )
        )

    # Sort outputs for better UX (strongest signals first)
    category_scores.sort(key=lambda x: x.average_grade, reverse=True)
    field_signals.sort(key=lambda x: x.score, reverse=True)

    # Calculate confidence
    confidence = calculate_confidence(coverage)

    result = {
        "phase": current_phase,
        "coverage": coverage,
        "confidence": confidence,
        "category_scores": category_scores,
        "field_signals": field_signals
    }
    
    # Only include warnings if there are any
    if warnings:
        result["warnings"] = warnings
    
    return result
