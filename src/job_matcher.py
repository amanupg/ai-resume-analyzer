import json
from sentence_transformers import SentenceTransformer, util

# Load a small, fast Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')


def load_resume(resume_json_path):
    with open(resume_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def combine_resume_text(resume_data):
    text_parts = []
    for section in ["skills", "experience", "education", "projects"]:
        section_data = resume_data.get(section, [])
        if isinstance(section_data, list):
            # Flatten list items
            text_parts.extend([str(item) for item in section_data])
        elif isinstance(section_data, str):
            text_parts.append(section_data)
    return " ".join(text_parts)


def compute_job_fit(resume_json_path, job_description_text):
    resume_data = load_resume(resume_json_path)
    resume_text = combine_resume_text(resume_data)

    # Encode texts
    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    job_emb = model.encode(job_description_text, convert_to_tensor=True)

    # Compute cosine similarity (0–1)
    similarity = util.cos_sim(resume_emb, job_emb).item()
    # Convert to percentage
    score = round(similarity * 100, 2)

    # Optional: list missing skills
    resume_skills = set([s.lower() for s in resume_data.get("skills", [])])
    job_skills = set([s.lower() for s in job_description_text.split() if len(s) > 1])
    missing_skills = list(job_skills - resume_skills)

    return {"job_fit_score": score, "missing_skills": missing_skills}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compute job fit score")
    parser.add_argument("resume_json", type=str, help="Path to parsed resume JSON")
    parser.add_argument("job_description", type=str, help="Path to job description txt file")
    args = parser.parse_args()

    # Load job description
    with open(args.job_description, "r", encoding="utf-8") as f:
        job_text = f.read()

    result = compute_job_fit(args.resume_json, job_text)
    print(f"✅ Job Fit Score: {result['job_fit_score']}%")
    print(f"Missing skills: {result['missing_skills']}")
