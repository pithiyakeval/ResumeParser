import pdfplumber
import re
import spacy

nlp = spacy.load("en_core_web_sm")

def parse_resume(filepath):
    text = ""

    if filepath.endswith(".pdf"):
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    elif filepath.endswith(".docx"):
        import docx2txt
        text = docx2txt.process(filepath)
    else:
        return {"error": "Unsupported format"}

    doc = nlp(text)

    # Extract using REGEX and NLP
    name = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    email = re.findall(r'\S+@\S+', text)
    phone = re.findall(r'\b\d{10}\b', text)
    dob = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)

    # Extract technologies used (basic)
    tech_keywords = ['python', 'java', 'sql', 'mongodb', 'excel', 'react', 'node', 'pandas']
    tech_used = [tech for tech in tech_keywords if tech.lower() in text.lower()]

    # Very basic experience extraction (you can improve it)
    experience_match = re.findall(r'(\d+)\+?\s+years?', text.lower())

    return {
        "name": name[0] if name else "Not Found",
        "email": email[0] if email else "Not Found",
        "contact": phone[0] if phone else "Not Found",
        "dob": dob[0] if dob else "Not Found",
        "experience": experience_match[0] + " years" if experience_match else "Not Found",
        "technologies": ", ".join(tech_used) if tech_used else "Not Found"
    }
