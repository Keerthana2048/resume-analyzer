import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import random

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from resume_parser import parse_resume
from skill_extractor import extract_skills
from scoring_engine import calculate_scores

st.set_page_config(page_title="AuroraCV", layout="wide")

# ---------------- Sparkles ----------------

sparkles = ""

for i in range(30):
    x = random.randint(0,100)
    y = random.randint(0,100)
    delay = random.uniform(0,4)

    sparkles += f'<div class="sparkle" style="left:{x}%; top:{y}%; animation-delay:{delay}s"></div>'

# ---------------- UI ----------------

st.markdown(f"""
<style>

.stApp {{
background: linear-gradient(135deg,#020617,#0f172a,#1e293b);
color:white;
}}

.title {{
font-size:70px;
font-weight:900;
text-align:center;
background: linear-gradient(90deg,#22d3ee,#a78bfa,#f472b6);
-webkit-background-clip:text;
color:transparent;
}}

.subtitle {{
text-align:center;
font-size:22px;
margin-bottom:50px;
color:#cbd5f5;
}}

[data-testid="stMetric"] {{
background: rgba(255,255,255,0.05);
padding:20px;
border-radius:15px;
transition:0.3s;
}}

[data-testid="stMetric"]:hover {{
transform:scale(1.08);
box-shadow:0 0 20px #22d3ee;
}}

[data-testid="stFileUploader"] {{
background:rgba(255,255,255,0.05);
padding:25px;
border-radius:16px;
transition:0.3s;
}}

[data-testid="stFileUploader"]:hover {{
transform:scale(1.08);
box-shadow:0 0 25px #22d3ee;
}}

.sparkle {{
position:fixed;
width:4px;
height:4px;
background:white;
border-radius:50%;
animation:sparkleAnim 3s infinite ease-in-out;
}}

@keyframes sparkleAnim {{
0%{{transform:scale(0);opacity:0}}
50%{{transform:scale(1.6);opacity:1}}
100%{{transform:scale(0);opacity:0}}
}}

</style>

{sparkles}
""", unsafe_allow_html=True)

# ---------------- Title ----------------

st.markdown("""
<div class="title">✨ AuroraCV</div>
<div class="subtitle">
AI Resume Analyzer • ATS Scoring • Skill Gap Detection
</div>
""", unsafe_allow_html=True)

# ---------------- PDF Generator ----------------

def generate_pdf(result, matched):

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    y = 750
    pdf.setFont("Helvetica-Bold",18)
    pdf.drawString(170,y,"AuroraCV Resume Analysis Report")

    pdf.setFont("Helvetica",12)

    pdf.drawString(50,700,f"Accuracy Score: {result['accuracy_score']}%")
    pdf.drawString(50,680,f"Confidence Score: {result['confidence_score']}%")
    pdf.drawString(50,660,f"ATS Score: {result['ats_score']}%")
    pdf.drawString(50,640,f"Resume Grade: {result['resume_grade']}")

    y = 600
    pdf.drawString(50,y,"Matched Skills")

    for skill in matched:
        y -= 20
        pdf.drawString(70,y,f"- {skill}")

    y -= 40
    pdf.drawString(50,y,"Missing Skills")

    for skill in result["missing_skills"]:
        y -= 20
        pdf.drawString(70,y,f"- {skill}")

    y -= 40
    pdf.drawString(50,y,"AI Recommendations")

    for rec in result["ai_recommendations"]:
        y -= 20
        pdf.drawString(70,y,f"- {rec}")

    pdf.save()
    buffer.seek(0)

    return buffer

# ---------------- Inputs ----------------

col1,col2 = st.columns(2)

with col1:
    resume = st.file_uploader("📄 Upload Resume (PDF/DOCX)")

with col2:
    job_description = st.text_area("📝 Enter Job Description", height=200)

# ---------------- Analyze ----------------

if st.button("🔍 Analyze Resume", use_container_width=True):

    resume_text = parse_resume(resume)

    jd_skills = extract_skills(job_description)

    matched_skills = [
        skill for skill in jd_skills
        if skill.lower() in resume_text.lower()
    ]

    result = calculate_scores(
        resume_text,
        job_description,
        matched_skills,
        jd_skills
    )

    st.header("📊 Resume Analysis Dashboard")

    m1,m2,m3,m4 = st.columns(4)

    m1.metric("Accuracy", f"{result['accuracy_score']}%")
    m2.metric("Confidence", f"{result['confidence_score']}%")
    m3.metric("ATS Score", f"{result['ats_score']}%")
    m4.metric("Grade", result["resume_grade"])

    # ---------------- Job Fit Statement ----------------

    if "job_fit_statement" in result:

        st.markdown(f"""
        <div style="
        background:rgba(34,211,238,0.15);
        padding:18px;
        border-radius:12px;
        font-size:20px;
        text-align:center;
        border:1px solid rgba(34,211,238,0.4);
        margin-bottom:20px;
        ">
        {result["job_fit_statement"]}
        </div>
        """, unsafe_allow_html=True)

    # ---------------- ATS Gauge ----------------

    ats_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=result["ats_score"],
        title={'text':"ATS Score"},
        gauge={'axis':{'range':[0,100]}}
    ))

    st.plotly_chart(ats_fig)

    # ---------------- Confidence Gauge ----------------

    conf_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=result["confidence_score"],
        title={'text':"AI Confidence"}
    ))

    st.plotly_chart(conf_fig)

    # ---------------- Radar ----------------

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(
        r=[
            result["skills_score"],
            result["projects_score"],
            result["experience_score"],
            result["ats_score"]
        ],
        theta=["Skills","Projects","Experience","ATS"],
        fill="toself"
    ))

    st.plotly_chart(radar)

    # ---------------- Skill Heatmap ----------------

    st.subheader("Skill Gap Heatmap")

    skill_status = []

    for skill in jd_skills:
        if skill in matched_skills:
            skill_status.append(1)
        else:
            skill_status.append(0)

    heatmap_df = pd.DataFrame({
        "Skill": jd_skills,
        "Match": skill_status
    })

    fig, ax = plt.subplots(figsize=(10,2))

    sns.heatmap(
        [heatmap_df["Match"]],
        cmap="RdYlGn",
        cbar=False,
        xticklabels=heatmap_df["Skill"],
        yticklabels=["Skill Match"],
        ax=ax
    )

    st.pyplot(fig)

    # ---------------- Recruiter Score ----------------

    recruiter_score = round(
        result["accuracy_score"]*0.4 +
        result["ats_score"]*0.4 +
        result["confidence_score"]*0.2,2
    )

    st.subheader("Recruiter Recommendation Score")

    st.progress(recruiter_score/100)

    # ---------------- AI Recommendations ----------------

    st.subheader("AI Job Readiness Recommendations")

    for rec in result["ai_recommendations"]:
        st.info(rec)

    # ---------------- Download PDF ----------------

    pdf = generate_pdf(result, matched_skills)

    st.download_button(
        label="⬇ Download Full Report",
        data=pdf,
        file_name="AuroraCV_Report.pdf",
        mime="application/pdf"
    )