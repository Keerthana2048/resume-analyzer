from sentence_transformers import SentenceTransformer, util
from ai_recommender import generate_ai_recommendations
import re

# Better semantic model for resume-job similarity
model = SentenceTransformer("all-mpnet-base-v2")


def calculate_scores(resume_text, job_description, matched_skills, jd_skills):

    # ---------------- SEMANTIC SIMILARITY ----------------

    embeddings = model.encode(
        [resume_text, job_description],
        convert_to_tensor=True
    )

    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()

    semantic_score = similarity * 100

    # ---------------- SKILLS SCORE ----------------

    if jd_skills:
        skills_score = (len(matched_skills) / len(jd_skills)) * 100
    else:
        skills_score = 0

    # ---------------- PROJECT DETECTION ----------------

    project_keywords = [
        "project",
        "developed",
        "built",
        "system",
        "application",
        "model"
    ]

    project_presence = any(
        k in resume_text.lower() for k in project_keywords
    )

    projects_score = 100 if project_presence else 50

    # ---------------- EXPERIENCE DETECTION ----------------

    experience_keywords = [
        "intern",
        "experience",
        "worked",
        "collaborated",
        "team"
    ]

    experience_presence = any(
        k in resume_text.lower() for k in experience_keywords
    )

    experience_score = 100 if experience_presence else 50

    # ---------------- QUANTIFIED ACHIEVEMENTS ----------------

    quantified = re.search(r"\d+%|\d+\+?", resume_text)

    quantified_score = 100 if quantified else 60

    # ---------------- ATS SCORE ----------------

    ats_score = (

        skills_score * 0.5 +
        projects_score * 0.2 +
        experience_score * 0.2 +
        quantified_score * 0.1

    )

    # ---------------- ACCURACY SCORE (Improved Formula) ----------------

    accuracy_score = (

        skills_score * 0.55 +
        ats_score * 0.30 +
        semantic_score * 0.25

    )

    # prevent score >100
    accuracy_score = min(accuracy_score, 100)

    # ---------------- CONFIDENCE SCORE ----------------

    confidence_score = (

        semantic_score * 0.6 +
        skills_score * 0.4

    )

    confidence_score = min(confidence_score, 100)

    # ---------------- RESUME STRENGTH ----------------

    resume_strength = (

        skills_score * 0.4 +
        projects_score * 0.3 +
        experience_score * 0.3

    )

    # ---------------- GRADE ----------------

    if accuracy_score >= 90:
        grade = "A+"
    elif accuracy_score >= 80:
        grade = "A"
    elif accuracy_score >= 70:
        grade = "B"
    elif accuracy_score >= 60:
        grade = "C"
    else:
        grade = "Needs Improvement"

    # ---------------- JOB FIT STATEMENT ----------------

    if accuracy_score >= 90:
        job_fit_statement = "⭐ Excellent Match — Best Fit for the Job"
    elif accuracy_score >= 80:
        job_fit_statement = "✅ Strong Match — Very Good Fit"
    elif accuracy_score >= 70:
        job_fit_statement = "👍 Moderate Match — Good Fit"
    elif accuracy_score >= 60:
        job_fit_statement = "⚠ Partial Match — Needs Skill Improvements"
    else:
        job_fit_statement = "❌ Low Match — Resume Needs Major Improvements"

    # ---------------- MISSING SKILLS ----------------

    missing_skills = list(set(jd_skills) - set(matched_skills))

    # ---------------- AI RECOMMENDATIONS ----------------

    ai_recommendations = generate_ai_recommendations(
        resume_text,
        job_description,
        missing_skills
    )

    ai_recommendations = ai_recommendations[:10]

    # ---------------- RETURN RESULTS ----------------

    return {

        "accuracy_score": round(accuracy_score, 2),
        "confidence_score": round(confidence_score, 2),

        "resume_grade": grade,
        "job_fit_statement": job_fit_statement,

        "resume_strength": round(resume_strength, 2),

        "skills_score": round(skills_score, 2),
        "projects_score": projects_score,
        "experience_score": experience_score,

        "ats_score": round(ats_score, 2),

        "missing_skills": missing_skills,
        "ai_recommendations": ai_recommendations

    }