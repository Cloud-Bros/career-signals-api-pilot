Perfect — below is a **`tasks.md` written specifically for GitHub Copilot / Cursor**, **continuing from your current state**, not from scratch.

It assumes:

* FastAPI app already exists
* `/courses` and `/analysis` endpoints already implemented
* Category scores + field signals already working
* No database
* No auth

You can paste this directly into `tasks.md`.

---

# 🧩 tasks.md

## Career Signals Backend — Implementation Tasks (Continuation)

> This file defines **incremental implementation tasks** for GitHub Copilot.
> The core backend already exists.
> Do **not** re-architect or rewrite existing logic unless explicitly instructed.

---

## ✅ CURRENT STATE (DO NOT REDO)

The backend already includes:

* FastAPI project structure
* Static course catalogue
* `/courses` endpoint (GET)
* `/analysis` endpoint (POST)
* Phase-aware category scoring
* Credit-weighted averages
* Field signals derived from categories
* Signal strength labels (`Strong`, `Consistent`, `Emerging`)

The following tasks **extend and harden** the system.

---

## TASK 1 — Add strict input validation to `/analysis`

### Goal

Reject invalid analysis requests early and explicitly.

### Requirements

* Enforce `current_phase` ∈ `{1, 2, 3}`
* Enforce `grade` ∈ `[0, 20]`
* Reject unknown `course_name`
* Ignore grades for courses above `current_phase`

### Instructions for Copilot

* Update Pydantic models in `models/analysis.py`
* Use `Field(..., ge=?, le=?)` where appropriate
* Raise `HTTPException(status_code=422)` for invalid course names
* Validation logic must live **before** computation begins

### Acceptance Criteria

* Invalid phase → 422
* Grade < 0 or > 20 → 422
* Unknown course name → 422 with clear error message

---

## TASK 2 — Add confidence label to analysis response

### Goal

Contextualize results based on how much data is available.

### Rules

Use `coverage` to derive confidence:

| Coverage | Confidence |
| -------- | ---------- |
| ≥ 0.7    | High       |
| ≥ 0.4    | Medium     |
| < 0.4    | Low        |

### Instructions for Copilot

* Implement confidence derivation in `analysis_service.py`
* Add `confidence: str` to `AnalysisResponse`
* Confidence must be included in the final response

### Acceptance Criteria

* Confidence label matches coverage
* No confidence logic in API routes

---

## TASK 3 — Add field contributors (explainability)

### Goal

Explain **why** each field signal exists.

### Requirements

Each field signal must include:

* contributing categories
* contributing courses
* evidence level: `Partial` or `Complete`

### Definitions

* **Contributing category**: category used in field calculation
* **Contributing course**: any course that contributed to those categories
* **Evidence level**:

  * `Complete` → all categories defined for the field are present
  * `Partial` → one or more categories missing

### Instructions for Copilot

* Extend `FieldSignal` model to include:

  ```python
  contributors: {
    categories: List[str],
    courses: List[str]
  }
  evidence_level: str
  ```
* Determine contributors during analysis
* Do not hardcode contributors

### Acceptance Criteria

* Each field signal lists at least one category and course
* Evidence level is correct
* Logic remains deterministic and explainable

---

## TASK 4 — Sort outputs by strength

### Goal

Improve UX by surfacing strongest signals first.

### Instructions for Copilot

* Sort:

  * `category_scores` by `average_grade` (descending)
  * `field_signals` by `score` (descending)
* Sorting must occur in `analysis_service.py`

### Acceptance Criteria

* Strongest categories and fields appear first
* No sorting logic in API routes

---

## TASK 5 — Add warning support (non-fatal issues)

### Goal

Surface issues without failing analysis.

### Examples

* No valid courses for phase
* Grades submitted but none match catalogue
* Very low coverage (< 0.2)

### Instructions for Copilot

* Add optional `warnings: List[str]` to response
* Warnings must be informational only
* Do not block valid responses

### Acceptance Criteria

* Warnings appear only when relevant
* Core response remains unchanged

---

## TASK 6 — Add unit tests for analysis logic

### Goal

Ensure correctness and stability.

### Instructions for Copilot

* Add tests for:

  * Phase filtering
  * Coverage calculation
  * Category averaging
  * Field renormalization
  * Partial vs complete evidence
* Tests must target `run_analysis` directly
* Do not spin up FastAPI in tests

### Acceptance Criteria

* All tests pass
* No API-level tests required yet

---

## TASK 7 — Freeze backend (definition of V1 complete)

### Goal

Prevent scope creep.

### Instructions for Copilot

* Do **not** add:

  * authentication
  * databases
  * job recommendations
  * ML models
* Ensure documentation reflects:

  * signal-based design
  * non-prescriptive outputs

### Acceptance Criteria

* Backend behavior matches `features.md`
* No new endpoints added
* Logic remains stateless

---

## 🛑 OUT OF SCOPE (DO NOT IMPLEMENT)

* PDF transcript parsing
* User accounts
* Persistence
* Frontend UI
* Career/job recommendations
* Ranking or scoring users against others

---

## ✅ FINAL CHECKLIST (V1 DONE WHEN TRUE)

* [ ] Input validation enforced
* [ ] Confidence label present
* [ ] Field contributors implemented
* [ ] Evidence level included
* [ ] Outputs sorted
* [ ] Warnings supported
* [ ] Tests passing

---

### Closing Note

This backend is an **academic signal engine**, not a recommender system.
All outputs must remain **directional, explainable, and phase-aware**.

---

