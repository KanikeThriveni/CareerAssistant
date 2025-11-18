import os

def parse_resume(filepath):
    """
    Extracts text from PDF or DOCX resume and returns a brief summary.
    """
    text = ""
    if filepath.lower().endswith('.pdf'):
        try:
            import pdfplumber
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            text = f"Error reading PDF: {e}"
    elif filepath.lower().endswith('.docx'):
        try:
            from docx import Document
            doc = Document(filepath)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            text = f"Error reading DOCX: {e}"
    else:
        text = "Unsupported file type."

    # Simple brief: first 500 characters
    brief = text[:500] + ("..." if len(text) > 500 else "")
    return {
        'file': os.path.basename(filepath),
        'brief': brief,
        'raw_text': text
    }

def match_experience_to_job(resume_data, job_description):
    """
    Simple placeholder: checks if any skill/experience from resume_data appears in job_description.
    """
    if not resume_data or not job_description:
        return "Insufficient data to compare."
    # Assume resume_data is a dict with 'skills' and 'experience' keys
    skills = resume_data.get('skills', [])
    experience = resume_data.get('experience', [])
    matches = []
    for skill in skills:
        if skill.lower() in job_description.lower():
            matches.append(skill)
    for exp in experience:
        if exp.lower() in job_description.lower():
            matches.append(exp)
    if matches:
        return f"Your resume matches these requirements: {', '.join(matches)}"
    else:
        return "No direct matches found between your experience and the job description."
