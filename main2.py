import spacy
import docx
import pdfplumber
import re
from tkinter import Tk, Label, Text, Scrollbar, Button, filedialog, END, Toplevel

class DocumentAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.nlp = spacy.load("en_core_web_sm")

    def extract_text_from_docx(self):
        doc = docx.Document(self.file_path)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)

    def extract_text_from_pdf(self):
        full_text = []
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text.append(page_text)
        return '\n'.join(full_text)

    def extract_info_with_spacy(self, document_text):
        doc = self.nlp(document_text)
        info = {
            "Name": None,
            "Education": [],
            "Work Experience": [],
            "Email": None,
            "Phone": None
        }

        # Extract Name
        for ent in doc.ents:
            if ent.label_ == "PERSON" and not info["Name"]:
                info["Name"] = ent.text  # Take the first person entity found as the name

        # Extract Email and Phone
        email_match = re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', document_text)
        phone_match = re.search(r'\b(?:\+?\d{1,3}[-.\s]?)?\d{9,12}\b', document_text)

        if email_match:
            info["Email"] = email_match.group(0)
        if phone_match:
            info["Phone"] = phone_match.group(0)

        # Enhanced Education Section Extraction with Work Experience Adjustment
        education_keywords = ["education", "university", "college", "bachelor", "master", "degree"]
        work_keywords = ["company", "worked", "role", "experience", "manager", "developer"]

        work_experience_found = False  # Flag to detect start of work experience within education section

        for sentence in doc.sents:
            sentence_text = sentence.text.lower()
            if any(keyword in sentence_text for keyword in education_keywords) and not work_experience_found:
                # Check if "Work Experience" is mentioned within Education
                if "work experience" in sentence_text:
                    work_experience_found = True
                    info["Work Experience"].append(sentence.text)  # Move this sentence to Work Experience
                else:
                    info["Education"].append(sentence.text)
            elif work_experience_found or any(keyword in sentence_text for keyword in work_keywords):
                info["Work Experience"].append(sentence.text)

        return info

    def analyze(self):
        # Extract document text based on file type
        if self.file_path.endswith('.docx'):
            document_text = self.extract_text_from_docx()
        elif self.file_path.endswith('.pdf'):
            document_text = self.extract_text_from_pdf()
        else:
            return "Unsupported file format."

        if document_text:
            # Extract structured information using spaCy and regex
            extracted_info = self.extract_info_with_spacy(document_text)
            return extracted_info
        else:
            return "No text found in the document."

def get_file_path():
    Tk().withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a PDF or Word Document",
        filetypes=(("PDF files", "*.pdf"), ("Word files", "*.docx"))
    )
    return file_path

def display_in_gui(extracted_information):
    window = Toplevel()
    window.title("Extracted Information")

    # Display Name
    Label(window, text="Name").grid(row=0, column=0, padx=10, pady=5)
    name_text = Text(window, height=2, width=50)
    name_text.insert(END, extracted_information['Name'] if extracted_information['Name'] else "Not found")
    name_text.grid(row=0, column=1, padx=10, pady=5)

    # Display Email
    Label(window, text="Email").grid(row=1, column=0, padx=10, pady=5)
    email_text = Text(window, height=2, width=50)
    email_text.insert(END, extracted_information['Email'] if extracted_information['Email'] else "Not found")
    email_text.grid(row=1, column=1, padx=10, pady=5)

    # Display Phone
    Label(window, text="Phone").grid(row=2, column=0, padx=10, pady=5)
    phone_text = Text(window, height=2, width=50)
    phone_text.insert(END, extracted_information['Phone'] if extracted_information['Phone'] else "Not found")
    phone_text.grid(row=2, column=1, padx=10, pady=5)

    # Display Education
    Label(window, text="Education").grid(row=3, column=0, padx=10, pady=5)
    edu_text = Text(window, height=8, width=50)
    edu_scroll = Scrollbar(window, command=edu_text.yview)
    edu_text.configure(yscrollcommand=edu_scroll.set)
    for edu in extracted_information['Education']:
        edu_text.insert(END, f"- {edu}\n")
    edu_text.grid(row=3, column=1, padx=10, pady=5)
    edu_scroll.grid(row=3, column=2, padx=5, pady=5, sticky='ns')

    # Display Work Experience
    Label(window, text="Work Experience").grid(row=4, column=0, padx=10, pady=5)
    exp_text = Text(window, height=8, width=50)
    exp_scroll = Scrollbar(window, command=exp_text.yview)
    exp_text.configure(yscrollcommand=exp_scroll.set)
    for exp in extracted_information['Work Experience']:
        exp_text.insert(END, f"- {exp}\n")
    exp_text.grid(row=4, column=1, padx=10, pady=5)
    exp_scroll.grid(row=4, column=2, padx=5, pady=5, sticky='ns')

    Button(window, text="Close", command=window.destroy).grid(row=5, column=1, pady=10)

if __name__ == "__main__":
    file_path = get_file_path()

    if file_path:
        analyzer = DocumentAnalyzer(file_path)
        extracted_information = analyzer.analyze()

        if isinstance(extracted_information, dict):
            root = Tk()
            root.withdraw()
            display_in_gui(extracted_information)
            root.mainloop()
        else:
            print(extracted_information)
    else:
        print("No file selected.")
