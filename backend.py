from fastapi import FastAPI, UploadFile, File, Form
from resume_parser import extract_text_from_pdf, extract_text_from_docx
from scoring_engine import calculate_scores
from skill_extractor import extract_skills

app = FastAPI()


@app.post("/screen_resume")
async def screen_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # -------- Extract Resume Text --------
    if resume_file.filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(resume_file.file)
    elif resume_file.filename.endswith(".docx"):
        resume_text = extract_text_from_docx(resume_file.file)
    else:
        return {"error": "Unsupported file format"}

    # -------- Extract Skills --------
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    matched_skills = list(set(resume_skills) & set(jd_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))

    # -------- Calculate Scores --------
    result = calculate_scores(
        resume_text,
        job_description,
        matched_skills,
        jd_skills
    )

    # -------- Return Full Data --------
    return {
        "accuracy_score": result["accuracy_score"],
        "confidence_score": result["confidence_score"],
        "confidence_level": result["confidence_level"],
        "job_fit_category": result["job_fit_category"],
        "skills_score": result["skills_score"],
        "projects_score": result["projects_score"],
        "experience_score": result["experience_score"],
        "ats_score": result["ats_score"],   # 🔥 THIS WAS MISSING
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "improvement_suggestions": result["improvement_suggestions"]
    }