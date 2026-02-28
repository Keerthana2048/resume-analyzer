import re

TECH_SKILLS = [
    "python", "java", "c++", "sql", "machine learning",
    "deep learning", "nlp", "tensorflow", "pytorch",
    "aws", "docker", "flask", "fastapi", "react",
    "node", "mongodb", "data analysis", "pandas",
    "numpy", "excel", "power bi"
]

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in TECH_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))