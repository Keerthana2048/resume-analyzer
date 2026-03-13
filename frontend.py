import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(page_title="AI Resume Screening", layout="wide")

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.hero {
    background: linear-gradient(90deg, #1f2937, #111827);
    padding: 30px;
    border-radius: 15px;
    margin-bottom: 20px;
}
.hero h1 {
    color: #4ade80;
    font-size: 42px;
}
.skill-badge {
    background: linear-gradient(90deg,#2563eb,#1d4ed8);
    padding: 8px 14px;
    border-radius: 20px;
    margin: 5px;
    display: inline-block;
    color: white;
    font-size: 14px;
}
.missing-badge {
    background: linear-gradient(90deg,#ef4444,#dc2626);
    padding: 8px 14px;
    border-radius: 20px;
    margin: 5px;
    display: inline-block;
    color: white;
    font-size: 14px;
}
.section-title {
    font-size: 22px;
    font-weight: bold;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Hero Section ----------------
st.markdown("""
<div class="hero">
<h1>🚀 AI Resume Intelligence System</h1>
<p>Advanced ATS Analysis • Section Scoring • Smart Skill Gap Detection</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Input Section ----------------
col1, col2 = st.columns(2)

with col1:
    resume = st.file_uploader("📄 Upload Resume (PDF/DOCX)")

with col2:
    job_description = st.text_area("📝 Enter Job Description", height=150)

# ---------------- Analyze Button ----------------
if st.button("🔍 Analyze Resume", use_container_width=True):

    if resume is None or job_description.strip() == "":
        st.warning("⚠ Please upload resume and enter job description")
    else:
        with st.spinner("Analyzing Resume with AI Engine..."):
            try:
                files = {"resume_file": resume}
                data = {"job_description": job_description}

                response = requests.post(
                    "http://127.0.0.1:8000/screen_resume",
                    files=files,
                    data=data
                )

                # -------- Proper Error Handling --------
                if response.status_code != 200:
                    st.error(f"❌ Backend Error: {response.status_code}")
                    st.write(response.text)
                    st.stop()

                result = response.json()

                # Safety check
                if "accuracy_score" not in result:
                    st.error("❌ Invalid response from backend.")
                    st.write(result)
                    st.stop()

                # ---------------- Dashboard ----------------
                st.markdown("---")
                st.markdown("## 📊 Resume Analysis Dashboard")

                colA, colB, colC = st.columns(3)

                colA.metric("🎯 Accuracy", f"{result['accuracy_score']} %")
                colB.metric("🔒 Confidence", f"{result['confidence_score']} %")
                colC.metric("📈 ATS Score", f"{result['ats_score']} %")

                st.progress(result["accuracy_score"] / 100)

                # ---------------- Section Scores ----------------
                st.markdown("### 📌 Section Performance")

                s1, s2, s3 = st.columns(3)
                s1.metric("Skills Score", f"{result['skills_score']}%")
                s2.metric("Projects Score", f"{result['projects_score']}%")
                s3.metric("Experience Score", f"{result['experience_score']}%")

                # ---------------- Radar Chart ----------------
                fig = go.Figure()

                fig.add_trace(go.Scatterpolar(
                    r=[
                        result['skills_score'],
                        result['projects_score'],
                        result['experience_score'],
                        result['ats_score']
                    ],
                    theta=["Skills", "Projects", "Experience", "ATS"],
                    fill='toself'
                ))

                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    showlegend=False,
                    height=400
                )

                st.plotly_chart(fig, use_container_width=True)

                # ---------------- Job Fit ----------------
                st.markdown("### 🏷 Job Fit Category")

                if result["job_fit_category"] == "Strong Fit":
                    st.success("🟢 Strong Fit")
                elif result["job_fit_category"] == "Moderate Fit":
                    st.warning("🟡 Moderate Fit")
                else:
                    st.error("🔴 Weak Fit")

                # ---------------- Matched Skills ----------------
                st.markdown('<div class="section-title">✅ Matched Skills</div>', unsafe_allow_html=True)

                if result["matched_skills"]:
                    for skill in result["matched_skills"]:
                        st.markdown(
                            f'<span class="skill-badge">{skill}</span>',
                            unsafe_allow_html=True
                        )
                else:
                    st.info("No matched skills found.")

                # ---------------- Missing Skills ----------------
                st.markdown('<div class="section-title">❌ Missing Skills</div>', unsafe_allow_html=True)

                if result["missing_skills"]:
                    for skill in result["missing_skills"]:
                        st.markdown(
                            f'<span class="missing-badge">{skill}</span>',
                            unsafe_allow_html=True
                        )
                else:
                    st.success("🎉 No missing skills! Candidate matches all required skills.")

                # ---------------- Suggestions ----------------
                st.markdown('<div class="section-title">🚀 Smart Improvement Suggestions</div>', unsafe_allow_html=True)

                for suggestion in result["improvement_suggestions"]:
                    st.info("👉 " + suggestion)

            except Exception as e:
                st.error("❌ Failed to connect to backend.")
                st.write(str(e))