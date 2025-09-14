import fitz  # PyMuPDF
import spacy
import json
import re
from pathlib import Path

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_education(text):
    # Simple regex-based extraction
    edu_keywords = ["Bachelor", "B.Tech", "B.Sc", "Master", "M.Tech", "M.Sc", "MBA"]
    education = []
    for line in text.split("\n"):
        if any(word in line for word in edu_keywords):
            education.append(line.strip())
    return education


def extract_experience(text):
    exp_keywords = ["experience", "worked at", "internship", "project"]
    experience = []
    for line in text.split("\n"):
        if any(word.lower() in line.lower() for word in exp_keywords):
            experience.append(line.strip())
    return experience


def extract_skills(text):
    doc = nlp(text)
    # Take nouns and proper nouns as potential skills
    skills = set()
    for token in doc:
        if token.pos_ in ["PROPN", "NOUN"] and len(token.text) > 1:
            skills.add(token.text)
    return list(skills)

def extract_projects(text):
    project_keywords = ["project", "projects", "github", "portfolio"]
    projects = []
    for line in text.split("\n"):
        if any(word.lower() in line.lower() for word in project_keywords):
            projects.append(line.strip())
    return projects



def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    resume_data = {
        "education": extract_education(text),
        "experience": extract_experience(text),
        "skills": extract_skills(text),
        "projects": extract_projects(text)
    }
    return resume_data


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parse PDF resume")
    parser.add_argument("pdf_path", type=str, help="Path to resume PDF")
    args = parser.parse_args()

    result = parse_resume(args.pdf_path)
    # Output JSON to same folder
    output_path = Path(args.pdf_path).with_suffix(".json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print(f"Parsed resume saved to {output_path}")
