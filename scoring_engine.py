from sentence_transformers import SentenceTransformer, util
import re

model = SentenceTransformer('all-MiniLM-L6-v2')


def calculate_scores(resume_text, job_description, matched_skills, jd_skills):

    embeddings = model.encode([resume_text, job_description])
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()

    resume_lower = resume_text.lower()

    # ---------------- Skills Score ----------------
    if len(jd_skills) > 0:
        skills_score = round((len(matched_skills) / len(jd_skills)) * 100, 2)
    else:
        skills_score = 0

    # ---------------- Accuracy Score (NOW AFTER skills_score) ----------------
    accuracy_score = round((similarity * 70) + (skills_score * 0.3), 2)
    confidence_score = round((similarity ** 2) * 100, 2)

    # ---------------- Projects Score ----------------
    project_keywords = ["project", "developed", "built", "created"]
    project_presence = any(word in resume_lower for word in project_keywords)
    projects_score = 100 if project_presence else 30

    # ---------------- Experience Score ----------------
    exp_keywords = ["experience", "intern", "worked", "company"]
    experience_presence = any(word in resume_lower for word in exp_keywords)
    experience_score = 100 if experience_presence else 30

    # ---------------- Quantified Achievement Detection ----------------
    quantified = re.search(r"\d+%", resume_text)
    quantified_score = 100 if quantified else 40

    # ---------------- ATS Score ----------------
    ats_score = round(
        (skills_score * 0.4 +
         projects_score * 0.2 +
         experience_score * 0.2 +
         quantified_score * 0.2), 2
    )

    # ---------------- Job Fit ----------------
    if skills_score >= 75 and similarity >= 0.7:
        job_fit = "Strong Fit"
    elif skills_score >= 40:
        job_fit = "Moderate Fit"
    else:
        job_fit = "Weak Fit"

    # ---------------- Missing Skills ----------------
    missing_skills = list(set(jd_skills) - set(matched_skills))

    # ---------------- Suggestions ----------------
    suggestions = []

    if missing_skills:
        for skill in missing_skills:
            suggestions.append(f"Add practical experience in '{skill}' to match job requirements.")

    if not project_presence:
        suggestions.append("Include detailed project descriptions.")

    if not experience_presence:
        suggestions.append("Add internships or work experience.")

    if not quantified:
        suggestions.append("Quantify achievements (e.g., improved accuracy by 20%).")

    if ats_score < 60:
        suggestions.append("Improve ATS compatibility by aligning resume keywords with JD.")

    if not suggestions:
        suggestions.append("Resume is well aligned with job requirements.")

    return {
        "accuracy_score": accuracy_score,
        "confidence_score": confidence_score,
        "confidence_level": "High" if confidence_score > 60 else "Medium" if confidence_score > 30 else "Low",
        "job_fit_category": job_fit,
        "skills_score": skills_score,
        "projects_score": projects_score,
        "experience_score": experience_score,
        "ats_score": ats_score,
        "improvement_suggestions": suggestions
    }