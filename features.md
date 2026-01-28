
## Career Signals Backend (FastAPI)

### Purpose

This document defines the **functional and non-functional features** of the Career Signals backend API.

The backend analyzes **academic transcript data** (courses + grades) and produces **explainable academic strength signals** across categories and higher-level technical fields.

The system **must not**:

* recommend jobs
* make career decisions
* assess employability

It only surfaces **directional academic signals**.

---

## 1. Core Design Principles

* **Stateless**: No user data persistence in V1
* **Explainable**: Every signal must be traceable to data
* **Phase-aware**: Students are only evaluated on courses they could have taken
* **Signal-based**: Outputs indicate *alignment*, not readiness or prescriptions
* **Composable**: New fields, courses, or mappings can be added without refactoring

---

## 2. Data Model (Static Curriculum)

### Course Catalogue

The backend maintains a **canonical list of courses**.

Each course has:

* `course_name` (string, unique)
* `category` (string)
* `phase` (int, 1–3)
* `credits` (int)

The course catalogue is **read-only** and acts as a validation source.

---

## 3. API Endpoints

### 3.1 `GET /courses`

#### Description

Returns the full course catalogue or a filtered subset.

#### Query Parameters

* `phase` (optional, int, 1–3)
* `category` (optional, string)

#### Response

```json
[
  {
    "course_name": "Databases",
    "category": "Data",
    "phase": 1,
    "credits": 6
  }
]
```

#### Requirements

* Filtering must be case-insensitive
* Endpoint must be read-only
* No authentication in V1

---

### 3.2 `POST /analysis`

#### Description

Performs **pure computation** on user-supplied grades and returns:

* category-level academic signals
* field-level academic signals
* coverage and confidence indicators

This endpoint **does not store data**.

---

## 4. Analysis Input

### Request Body

```json
{
  "current_phase": 2,
  "grades": [
    { "course_name": "Databases", "grade": 15 }
  ]
}
```

### Validation Rules

* `current_phase` must be between **1 and 3**
* `grade` must be between **0 and 20**
* `course_name` must exist in the course catalogue
* Grades for courses above `current_phase` must be ignored

Invalid input must result in a **422 error** with a clear message.

---

## 5. Analysis Logic

### 5.1 Phase Filtering

Only courses with:

```
course.phase <= current_phase
```

are eligible for analysis.

---

### 5.2 Category Scoring

For each category:

* Use **credit-weighted averaging**
* Only include completed courses

Formula:

```
average_grade =
  Σ(grade × credits) / Σ(credits)
```

---

### 5.3 Coverage Calculation

Coverage indicates how much of the expected curriculum has grade data.

```
coverage = completed_credits / total_eligible_credits
```

Coverage must be a float between `0.0` and `1.0`.

---

### 5.4 Confidence Label

Derived from coverage:

| Coverage | Confidence |
| -------- | ---------- |
| ≥ 0.7    | High       |
| ≥ 0.4    | Medium     |
| < 0.4    | Low        |

Confidence must be included in the response.

---

## 6. Field Signals

### 6.1 Field Definitions

Fields are defined as **weighted combinations of categories**.

Example:

```python
FIELDS = {
  "Data Science": {
    "Data": 0.6,
    "Programming": 0.3,
    "Business": 0.1
  }
}
```

* Weights do **not** imply requirements
* Fields represent **directional academic alignment**

---

### 6.2 Field Score Calculation

For each field:

1. Use only available category scores
2. Renormalize weights if categories are missing
3. Compute weighted average

Formula:

```
field_score =
  Σ(category_score × weight) / Σ(weights_used)
```

---

### 6.3 Signal Strength Labels

| Score | Label      |
| ----- | ---------- |
| ≥ 14  | Strong     |
| ≥ 11  | Consistent |
| < 11  | Emerging   |

---

## 7. Explainability (Required)

Each field signal must include:

* contributing categories
* contributing courses
* whether evidence is **partial** or **complete**

Example:

```json
{
  "field": "Data Science",
  "score": 14.33,
  "signal_strength": "Strong",
  "contributors": {
    "categories": ["Data", "Programming"],
    "courses": ["Databases", "Programming Fundamentals"]
  },
  "evidence_level": "Partial"
}
```

---

## 8. Analysis Response Schema

```json
{
  "phase": 2,
  "coverage": 0.56,
  "confidence": "Medium",
  "category_scores": [
    {
      "category": "Data",
      "average_grade": 14.6,
      "total_credits": 15
    }
  ],
  "field_signals": [
    {
      "field": "Data Science",
      "score": 14.33,
      "signal_strength": "Strong",
      "contributors": {
        "categories": ["Data", "Programming"],
        "courses": ["Databases", "Programming Fundamentals"]
      },
      "evidence_level": "Partial"
    }
  ]
}
```

---

## 9. Non-Goals (Explicit)

The backend must **not**:

* recommend jobs
* rank users
* predict salaries
* store personal data
* claim employability or readiness

---

## 10. Implementation Constraints

* FastAPI
* Pydantic models
* No database in V1
* Logic must live in `services/`
* Endpoints must be thin wrappers
* Analysis logic must be unit-testable

---

## 11. Definition of Done (V1)

The backend is considered **complete** when:

* `/courses` returns a validated curriculum
* `/analysis`:

  * validates input
  * computes category scores
  * computes field signals
  * includes confidence & explainability
* No business logic exists in API routes
* No career/job claims appear anywhere

---

## 12. Future Extensions (Out of Scope)

* PDF transcript ingestion
* User authentication
* Persistence
* Frontend visualization
* ML-based clustering

---

### Final Note

This backend is an **academic signal engine**, not a recommender system.
All outputs must remain **directional, explainable, and non-prescriptive**.

---