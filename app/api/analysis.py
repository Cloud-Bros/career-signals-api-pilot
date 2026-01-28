from fastapi import APIRouter
from app.models.analysis import AnalysisRequest, AnalysisResponse
from app.services.analysis_service import run_analysis

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.post("/", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest):
    return run_analysis(
        current_phase=request.current_phase,
        grades=request.grades
    )
