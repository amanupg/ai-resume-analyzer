import streamlit as st
from resume_parser import parse_resume
from job_matcher import compute_job_fit
from video_analysis import analyze_video
from pathlib import Path
import json

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("🎯 AI Resume Analyzer")

# ---- Resume Parsing ----
st.header("1️⃣ Upload Resume")
resume_file = st.file_uploader("Upload PDF Resume", type=["pdf"])
if resume_file:
    resume_path = Path("data") / resume_file.name
    with open(resume_path, "wb") as f:
        f.write(resume_file.getbuffer())
    resume_data = parse_resume(resume_path)
    resume_json_path = resume_path.with_suffix(".json")
    with open(resume_json_path, "w", encoding="utf-8") as f:
        json.dump(resume_data, f, indent=4)

    st.subheader("Parsed Resume Data")
    st.json(resume_data)

# ---- Job Fit ----
st.header("2️⃣ Job Description")
job_file = st.file_uploader("Upload Job Description (txt)", type=["txt"])
if job_file and resume_file:
    job_path = Path("data") / job_file.name
    with open(job_path, "wb") as f:
        f.write(job_file.getbuffer())
    with open(job_path, "r", encoding="utf-8") as f:
        job_text = f.read()
    job_fit_result = compute_job_fit(resume_json_path, job_text)
    st.subheader("Job Fit Analysis")
    st.metric("Job Fit Score (%)", job_fit_result["job_fit_score"])
    st.write("Missing Skills:", job_fit_result["missing_skills"])

# ---- Video Pitch Analysis ----
st.header("3️⃣ Upload Video Pitch")
uploaded_video = st.file_uploader("Upload your video", type=["mp4", "mov", "mkv"])
if uploaded_video is not None:
    # Save to disk
    video_path = Path("data") / uploaded_video.name
    with open(video_path, "wb") as f:
        f.write(uploaded_video.getbuffer())

    # Now pass the actual file path to analyze_video
    video_result = analyze_video(video_path)

    st.subheader("Video Analysis Result")
    st.write("Transcript:", video_result["transcript"])
    st.write("Speech Features:", video_result["speech_features"])
    st.write("Facial Emotions:", video_result["facial_emotions"])
