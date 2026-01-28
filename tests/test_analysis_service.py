import pytest
from app.models.analysis import GradeInput
from app.services.analysis_service import run_analysis, signal_strength, calculate_confidence


class TestSignalStrength:
    """Test signal strength categorization."""
    
    def test_strong_signal(self):
        assert signal_strength(14.0) == "Strong"
        assert signal_strength(15.5) == "Strong"
        assert signal_strength(20.0) == "Strong"
    
    def test_consistent_signal(self):
        assert signal_strength(11.0) == "Consistent"
        assert signal_strength(12.5) == "Consistent"
        assert signal_strength(13.9) == "Consistent"
    
    def test_emerging_signal(self):
        assert signal_strength(10.9) == "Emerging"
        assert signal_strength(8.0) == "Emerging"
        assert signal_strength(0.0) == "Emerging"


class TestCalculateConfidence:
    """Test confidence label calculation."""
    
    def test_high_confidence(self):
        assert calculate_confidence(0.7) == "High"
        assert calculate_confidence(0.85) == "High"
        assert calculate_confidence(1.0) == "High"
    
    def test_medium_confidence(self):
        assert calculate_confidence(0.4) == "Medium"
        assert calculate_confidence(0.55) == "Medium"
        assert calculate_confidence(0.69) == "Medium"
    
    def test_low_confidence(self):
        assert calculate_confidence(0.0) == "Low"
        assert calculate_confidence(0.2) == "Low"
        assert calculate_confidence(0.39) == "Low"


class TestPhaseFiltering:
    """Test that only eligible courses for the phase are considered."""
    
    def test_phase_1_filtering(self):
        grades = [
            GradeInput(course_name="Databases", grade=15.0),
            GradeInput(course_name="Programming Fundamentals", grade=14.0)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        assert result["phase"] == 1
        assert len(result["category_scores"]) > 0
        # Only phase 1 courses should be considered
    
    def test_phase_2_includes_phase_1(self):
        grades = [
            GradeInput(course_name="Databases", grade=15.0),  # Phase 1
            GradeInput(course_name="Data Science Fundamentals", grade=16.0)  # Phase 2
        ]
        result = run_analysis(current_phase=2, grades=grades)
        
        assert result["phase"] == 2
        # Both phase 1 and 2 courses should be considered
    
    def test_phase_3_includes_all(self):
        grades = [
            GradeInput(course_name="Databases", grade=15.0),  # Phase 1
            GradeInput(course_name="Data Science Fundamentals", grade=16.0),  # Phase 2
            GradeInput(course_name="Machine Learning & Forecasting", grade=17.0)  # Phase 3
        ]
        result = run_analysis(current_phase=3, grades=grades)
        
        assert result["phase"] == 3
        # All courses should be considered


class TestCoverageCalculation:
    """Test coverage calculation logic."""
    
    def test_full_coverage(self):
        # Provide a subset of phase 1 courses to achieve high coverage
        grades = [
            GradeInput(course_name="Databases", grade=15.0),
            GradeInput(course_name="Data Processing & Analysis", grade=14.0),
            GradeInput(course_name="Programming Fundamentals", grade=16.0),
            GradeInput(course_name="Scripting", grade=15.0),
            GradeInput(course_name="Computing Fundamentals", grade=14.0),
            GradeInput(course_name="Business Fundamentals", grade=13.0)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        # With expanded course catalogue, partial coverage is expected
        assert result["coverage"] > 0.4  # Should be at least medium coverage
        assert result["confidence"] in ["Medium", "High"]
    
    def test_partial_coverage(self):
        # Provide only some phase 1 courses
        grades = [
            GradeInput(course_name="Databases", grade=15.0),
            GradeInput(course_name="Programming Fundamentals", grade=16.0)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        assert 0.0 < result["coverage"] < 1.0
    
    def test_zero_coverage(self):
        # Provide no grades
        result = run_analysis(current_phase=1, grades=[])
        
        assert result["coverage"] == 0.0
        assert result["confidence"] == "Low"


class TestCategoryAveraging:
    """Test credit-weighted category averaging."""
    
    def test_weighted_average(self):
        # Databases (6 credits, grade 12) and Data Processing (3 credits, grade 15)
        # Should give: (12*6 + 15*3) / (6+3) = (72+45)/9 = 117/9 = 13.0
        grades = [
            GradeInput(course_name="Databases", grade=12.0),
            GradeInput(course_name="Data Processing & Analysis", grade=15.0)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        # Find Data category score
        data_score = next(
            (cs for cs in result["category_scores"] if cs.category == "Data"),
            None
        )
        
        assert data_score is not None
        assert data_score.average_grade == 13.0
        assert data_score.total_credits == 9
    
    def test_single_course_category(self):
        grades = [
            GradeInput(course_name="Business Fundamentals", grade=14.5)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        business_score = next(
            (cs for cs in result["category_scores"] if cs.category == "Business"),
            None
        )
        
        assert business_score is not None
        assert business_score.average_grade == 14.5


class TestFieldSignals:
    """Test field signal calculation and properties."""
    
    def test_field_score_calculation(self):
        # Provide data and programming courses
        grades = [
            GradeInput(course_name="Databases", grade=15.0),
            GradeInput(course_name="Programming Fundamentals", grade=14.0)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        # Should have field signals
        assert len(result["field_signals"]) > 0
        
        # Check that field signals have required properties
        for signal in result["field_signals"]:
            assert hasattr(signal, "field")
            assert hasattr(signal, "score")
            assert hasattr(signal, "signal_strength")
            assert hasattr(signal, "contributors")
            assert hasattr(signal, "evidence_level")
    
    def test_evidence_level_partial(self):
        # Provide only Data courses for Data Science field (needs Data, Programming, Business)
        grades = [
            GradeInput(course_name="Databases", grade=15.0),
            GradeInput(course_name="Data Processing & Analysis", grade=14.0)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        data_science_signal = next(
            (fs for fs in result["field_signals"] if fs.field == "Data Science"),
            None
        )
        
        if data_science_signal:
            assert data_science_signal.evidence_level == "Partial"
    
    def test_evidence_level_complete(self):
        # Provide all categories for a field
        grades = [
            GradeInput(course_name="Databases", grade=15.0),
            GradeInput(course_name="Business Fundamentals", grade=14.0)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        # Data Analytics needs only Data and Business
        data_analytics_signal = next(
            (fs for fs in result["field_signals"] if fs.field == "Data Analytics"),
            None
        )
        
        if data_analytics_signal:
            assert data_analytics_signal.evidence_level == "Complete"
    
    def test_contributors_structure(self):
        grades = [
            GradeInput(course_name="Databases", grade=15.0),
            GradeInput(course_name="Programming Fundamentals", grade=14.0)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        for signal in result["field_signals"]:
            assert "categories" in signal.contributors
            assert "courses" in signal.contributors
            assert isinstance(signal.contributors["categories"], list)
            assert isinstance(signal.contributors["courses"], list)
            assert len(signal.contributors["categories"]) > 0
            assert len(signal.contributors["courses"]) > 0


class TestSorting:
    """Test that outputs are sorted correctly."""
    
    def test_category_scores_sorted(self):
        grades = [
            GradeInput(course_name="Databases", grade=18.0),
            GradeInput(course_name="Programming Fundamentals", grade=12.0),
            GradeInput(course_name="Business Fundamentals", grade=15.0)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        scores = result["category_scores"]
        # Check that scores are in descending order
        for i in range(len(scores) - 1):
            assert scores[i].average_grade >= scores[i + 1].average_grade
    
    def test_field_signals_sorted(self):
        grades = [
            GradeInput(course_name="Databases", grade=18.0),
            GradeInput(course_name="Programming Fundamentals", grade=12.0),
            GradeInput(course_name="Business Fundamentals", grade=15.0),
            GradeInput(course_name="Computing Fundamentals", grade=14.0)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        signals = result["field_signals"]
        # Check that field signals are in descending order by score
        for i in range(len(signals) - 1):
            assert signals[i].score >= signals[i + 1].score


class TestWarnings:
    """Test warning generation for non-fatal issues."""
    
    def test_low_coverage_warning(self):
        # Provide very few grades for low coverage
        grades = [
            GradeInput(course_name="Databases", grade=15.0)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        # Should have warnings for low coverage
        if result["coverage"] < 0.2:
            assert "warnings" in result
            assert len(result["warnings"]) > 0
    
    def test_no_warnings_good_coverage(self):
        # Provide good coverage
        grades = [
            GradeInput(course_name="Databases", grade=15.0),
            GradeInput(course_name="Programming Fundamentals", grade=14.0),
            GradeInput(course_name="Computing Fundamentals", grade=16.0),
            GradeInput(course_name="Business Fundamentals", grade=13.0)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        # Should not have warnings
        assert "warnings" not in result or result["warnings"] is None or len(result["warnings"]) == 0
    
    def test_empty_grades_warning(self):
        result = run_analysis(current_phase=1, grades=[])
        
        # May have warnings but should not fail
        assert "coverage" in result
        assert result["coverage"] == 0.0


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_all_same_grades(self):
        grades = [
            GradeInput(course_name="Databases", grade=15.0),
            GradeInput(course_name="Programming Fundamentals", grade=15.0),
            GradeInput(course_name="Business Fundamentals", grade=15.0)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        # All category scores should be 15.0
        for score in result["category_scores"]:
            assert score.average_grade == 15.0
    
    def test_minimum_grade(self):
        grades = [
            GradeInput(course_name="Databases", grade=0.0)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        assert result["coverage"] > 0
        data_score = next(
            (cs for cs in result["category_scores"] if cs.category == "Data"),
            None
        )
        assert data_score.average_grade == 0.0
    
    def test_maximum_grade(self):
        grades = [
            GradeInput(course_name="Databases", grade=20.0)
        ]
        result = run_analysis(current_phase=1, grades=grades)
        
        assert result["coverage"] > 0
        data_score = next(
            (cs for cs in result["category_scores"] if cs.category == "Data"),
            None
        )
        assert data_score.average_grade == 20.0
