def generate_ai_recommendations(resume_text, job_description, missing_skills):

    recommendations = []

    for skill in missing_skills:

        recommendations.append(
            f"Develop hands-on projects demonstrating your proficiency in {skill}."
        )

        recommendations.append(
            f"Take an online course or certification focused on {skill}."
        )

    recommendations.append(
        "Build an end-to-end project combining multiple required skills from the job description."
    )

    recommendations.append(
        "Deploy one project on cloud platforms like AWS or Render to show production readiness."
    )

    return recommendations