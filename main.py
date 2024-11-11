import re
import pdfplumber
import docx
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# read a PDF file and extract text
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:  # Check if text extraction is successful
                text += page_text + "\n"  # Add new line after each page
    return text.strip()  # Remove leading/trailing whitespace

# read a Word (.docx) file and extract text
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

# extract information based on section titles
def extract_info(text):
    info = {}

    # Extract Name
    name_match = re.search(r'^[A-Z][a-zA-Z]+\s[A-Z][a-zA-Z]+', text, re.MULTILINE)
    info['Name'] = name_match.group(0) if name_match else "Not found"

    # Extract Email
    email = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', text)
    info['Email'] = email[0] if email else "Not found"

    # Extract Phone Number
    phone = re.findall(r'\b(?:\+?\d{1,3}[-.\s]?)?\d{9,12}\b', text)
    info['Phone'] = phone[0] if phone else "Not found"

    # Extract Work Experience
    work_experience = extract_section(text, "WORK EXPERIENCE", ["EDUCATION", "CONTACT", "OBJEVTIVE", "LANGUAGES", "SKILLS"])
    info['Work Experience'] = work_experience.strip() if work_experience else "Not found"

    # Extract Education
    education = extract_section(text, "EDUCATION", ["WORK EXPERIENCE", "CONTACT", "SKILLS", "HOBBIES", "OBJEVTIVE", "LANGUAGES"])
    info['Education'] = education.strip() if education else "Not found"

    return info

def extract_section(text, start_keyword, end_keywords):
    start_idx = text.lower().find(start_keyword.lower())
    if start_idx == -1:
        return ""

    end_idx = len(text)  # Default to the end of the text
    for end_keyword in end_keywords:
        idx = text.lower().find(end_keyword.lower(), start_idx)
        if idx != -1 and idx < end_idx:
            end_idx = idx

    return text[start_idx:end_idx].strip()


# open a file chooser and get the file path
def get_file_path():
    Tk().withdraw()
    file_path = askopenfilename(
        title="Select a PDF or Word Document",
        filetypes=(("PDF files", "*.pdf"), ("Word files", "*.docx"))
    )
    return file_path

# determine the file type and extract data
def extract_cv_info():
    file_path = get_file_path()
    if not file_path:
        print("No file selected.")
        return

    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        print("Unsupported file format. Please provide a PDF or DOCX file.")
        return

    extracted_info = extract_info(text)
    for key, value in extracted_info.items():
        print(f"{key}: {value}")

# the main function
if __name__ == '__main__':
    extract_cv_info()
