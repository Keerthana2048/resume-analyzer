import re

# Master skill list
SKILLS_DB = [

    "python",
    "machine learning",
    "data analysis",
    "deep learning",
    "computer vision",
    "neural networks",
    "streamlit",
    "sql",
    "git",
    "github",
    "linux",
    "tensorflow",
    "pytorch",
    "opencv",
    "pandas",
    "numpy",
    "scikit-learn",
    "matplotlib",
    "seaborn",
    "fastapi",
    "flask",
    "statistics",
    "data science"

]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))