# AI Resume Analyzer

Automated resume parsing, job-fit analysis, and video interview insights — all in one free AI tool.

---

## Motivation

Job hunting can be tedious. This tool helps job seekers quickly assess their fit for job descriptions, saving time and improving their chances of success. Recruiters can also benefit from faster candidate evaluation.

---

## Features

- **Resume Parsing:** Extract skills, experience, education, and projects from PDF resumes into structured JSON.  
- **Job-fit Scoring:** Uses semantic similarity (Sentence Transformers) to evaluate how well your resume matches a job description.  
- **Video Interview Analysis:** Transcribe your video interviews using Whisper to identify keywords and speech patterns.  
- **Interactive Dashboard:** Streamlit dashboard for easy upload and instant results.

---

## Installation

1. Clone the repo:
```bash
git clone https://github.com/<your-username>/resume-analyzer-ai.git
cd resume-analyzer-ai

python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# OR for Mac/Linux
# source venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage

1. Run the dashboard:
```bash
streamlit run src/dashboard.py
```
2. Upload a PDF resume.
3. Upload a job description in plain text.
4. (Optional) Upload a video interview to generate transcript.

## Future work
!!This project is a work in progress, with many more features being added.!!

