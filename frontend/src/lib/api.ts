import type { Course, AnalysisRequest, AnalysisResponse } from '@/types/api';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * API client for Career Signals backend
 */
class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Fetch all courses from the catalogue
   */
  async getCourses(): Promise<Course[]> {
    const response = await fetch(`${this.baseUrl}/courses`);
      throw new Error(`Failed to fetch courses: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Fetch a single course by ID
   */
  async getCourse(id: number): Promise<Course> {
    const response = await fetch(`${this.baseUrl}/courses/${id}`);
      throw new Error(`Failed to fetch course: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Submit analysis request with student grades
   */
  async submitAnalysis(data: AnalysisRequest): Promise<AnalysisResponse> {
    const response = await fetch(`${this.baseUrl}/analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Analysis failed: ${response.statusText}`);
    }

    return response.json();
  }
}

// Export a singleton instance
export const api = new ApiClient();
