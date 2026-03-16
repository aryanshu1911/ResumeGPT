"""
app.py — Career Path Analyzer API (FastAPI) V2
Updated: 2026-03-16 22:53 (Streak Maintenance)
=============================================
Main entry point for the backend REST API.

Endpoints:
  POST /analyze  — Upload a resume file, returns JSON with categorized entities
                   and advanced career suggestions (matching, missing, roadmaps).
"""

import hashlib
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.resume_parser import parse_resume
from models.resume_ner_model.extractor import extract_entities
from models.career_match_model.matcher import match_career

app = FastAPI(
    title="Career Path Analyzer API",
    description="Upload a resume and get AI-powered career recommendations with deep skill analytics.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Simple In-Memory Cache for repeated file analysis (e.g., hard page reloads)
# ---------------------------------------------------------------------------
_ANALYSIS_CACHE = {}

@app.get("/")
def root():
    return {"status": "ok", "message": "Career Path Analyzer API running."}

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    allowed_extensions = {"pdf", "docx", "txt"}
    extension = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: .{extension}. Allowed: {allowed_extensions}",
        )

    try:
        file_bytes = await file.read()
        
        # Hash the file content for caching
        file_hash = hashlib.md5(file_bytes).hexdigest()
        if file_hash in _ANALYSIS_CACHE:
            print("Returning cached analysis for:", file.filename)
            return _ANALYSIS_CACHE[file_hash]

        resume_text = parse_resume(file_bytes, file.filename)

        if not resume_text or len(resume_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Could not extract meaningful text from the file.",
            )

        entities = extract_entities(resume_text)
        
        # pass the full extracted entities dictionary as the second parameter for holistic matching
        career_suggestions = match_career(resume_text, entities, top_n=5)

        # Handle fallback check
        is_fallback = False
        if not career_suggestions:
            is_fallback = True
            # We can optionally include a generic roadmap here if needed

        response_data = {
            "filename": file.filename,
            "skills": entities["skills"],
            "projects": entities["projects"],
            "achievements": entities["achievements"],
            "extracurriculars": entities["extracurriculars"],
            "career_suggestions": career_suggestions,
            "is_fallback": is_fallback,
        }

        # Save to cache
        _ANALYSIS_CACHE[file_hash] = response_data

        return response_data

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal error during analysis: {str(e)}",
        )
