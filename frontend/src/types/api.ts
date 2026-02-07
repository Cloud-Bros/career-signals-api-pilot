// TypeScript types matching the FastAPI backend models

export type CourseCategory = 
  | 'Data'
  | 'Programming'
  | 'Security'
  | 'Business'
  | 'Communication'
  | 'Business Intelligence'
  | 'Hands-On Experience';

export interface Course {
  id: number;
  course_name: string;
  category: CourseCategory;
  phase: number;
  credits: number;
}

export interface GradeInput {
  course_name: string;
  grade: number; // 0-20
}

export interface CategoryScore {
  category: string;
  average_grade: number;
  total_credits: number;
}

export interface AnalysisRequest {
  current_phase: number; // 1-3
  grades: GradeInput[];
}

export interface FieldSignal {
  field: string;
  score: number;
  signal_strength: string;
  contributors: {
    categories: string[];
    courses: string[];
  };
  evidence_level: string; // "Complete" or "Partial"
}

export interface AnalysisResponse {
  phase: number;
  coverage: number;
  confidence: string;
  category_scores: CategoryScore[];
  field_signals: FieldSignal[];
  warnings?: string[];
}
