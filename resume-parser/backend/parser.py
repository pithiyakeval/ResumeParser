import pdfplumber
import re
import spacy
import docx2txt  # Move this to the top for cleanliness

nlp = spacy.load("en_core_web_sm")

# ✅ Put this helper function ABOVE parse_resume()
def extract_name_from_text(lines):
    # 1. Try spaCy
    first_lines_text = "\n".join(lines[:5])
    doc = nlp(first_lines_text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    if names:
        return names[0]

    # 2. Try regex pattern like "Name: Keval Ahir"
    name_regex = r'(?:Name\s*[:\-]?\s*)([A-Z][a-z]+\s+[A-Z][a-z]+)'
    for line in lines[:5]:
        match = re.search(name_regex, line)
        if match:
            return match.group(1)

    # 3. Fallback: first non-header line
    for line in lines[:5]:
        line = line.strip()
        if line and not re.search(r'(resume|curriculum vitae|email|phone|contact)', line, re.IGNORECASE):
            return line

    return "Not Found"


# ✅ Main parser function
def parse_resume(filepath):
    text = ""

    # Extract text
    if filepath.endswith(".pdf"):
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    elif filepath.endswith(".docx"):
        text = docx2txt.process(filepath)
    else:
        return {"error": "Unsupported file format"}

    # Clean text
    text = re.sub(r'\n+', '\n', text).strip()
    lines = text.split('\n')

    # ✅ Name extraction (using helper)
    name = extract_name_from_text(lines)

    # Email
    email_regex = r'[\w\.-]+@[\w\.-]+\.\w+'
    emails = re.findall(email_regex, text)
    email = emails[0] if emails else "Not Found"

    # Contact
    phone_regex = r'(\+?\d{1,3}[-.\s]?)?(\d{10})'
    phones = re.findall(phone_regex, text)
    contact = "".join(phones[0]) if phones else "Not Found"

    # DOB
    dob_regex = r'\b(?:DOB|Date of Birth|Birth Date|D\.O\.B)[\s:]*([0-9]{1,2}[-/\s]?(?:[A-Za-z]+|[0-9]{1,2})[-/\s]?[0-9]{2,4})'
    dob_matches = re.findall(dob_regex, text, flags=re.IGNORECASE)
    dob = dob_matches[0] if dob_matches else "Not Found"

    # Experience
    experience_regex = r'(?:(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years|yrs|year))'
    experience_matches = re.findall(experience_regex, text.lower())
    experience = experience_matches[0] + " years" if experience_matches else "Not Found"

    # Technologies
    tech_keywords = [
        'python', 'java', 'sql', 'mongodb', 'excel', 'react', 'node', 'pandas',
        'docker', 'aws', 'azure', 'git', 'javascript', 'html', 'css', 'flask',
        'django', 'tensorflow', 'keras', 'c++', 'c#'
    ]
    tech_used = [tech for tech in tech_keywords if re.search(r'\b' + re.escape(tech) + r'\b', text, re.IGNORECASE)]
    technologies = ", ".join(tech_used) if tech_used else "Not Found"

    return {
        "name": name,
        "email": email,
        "contact": contact,
        "dob": dob,
        "experience": experience,
        "technologies": technologies
    }
