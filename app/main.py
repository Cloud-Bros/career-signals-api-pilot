from fastapi import FastAPI
from app.api.courses import router as courses_router
from app.api.analysis import router as analysis_router


app = FastAPI(title="Career Signals API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Career Signals API"}

app.include_router(courses_router)
app.include_router(analysis_router)
