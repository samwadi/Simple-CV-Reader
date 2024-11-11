import spacy
import docx

class DocumentAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.nlp = spacy.load("en_core_web_sm")  # Load the pre-trained spaCy model

    def extract_text_from_docx(self):
        """Extracts and returns text from a .docx file."""
        doc = docx.Document(self.file_path)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)

    def extract_info_with_spacy(self, document_text):
        """Uses spaCy to extract structured information from text."""
        doc = self.nlp(document_text)
        info = {
            "Name": None,
            "Education": [],
            "Work Experience": []
        }

        # Extract Personal Information (e.g., name)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and not info["Name"]:
                info["Name"] = ent.text

        # Extract Education and Work Experience based on keywords
        education_keywords = ["university", "college", "bachelor", "master", "degree"]
        work_keywords = ["company", "worked", "role", "experience", "manager", "developer"]

        # Simple rule-based extraction (can be enhanced)
        for sentence in doc.sents:
            sentence_text = sentence.text.lower()
            if any(keyword in sentence_text for keyword in education_keywords):
                info["Education"].append(sentence.text)
            elif any(keyword in sentence_text for keyword in work_keywords):
                info["Work Experience"].append(sentence.text)

        return info

    def analyze(self):
        """Main method to extract text from the document and analyze it with spaCy."""
        # Step 1: Extract text from the .docx file
        document_text = self.extract_text_from_docx()

        if document_text:
            # Step 2: Use spaCy for AI-based extraction
            extracted_info = self.extract_info_with_spacy(document_text)
            return extracted_info
        else:
            return "No text found in the document."


if __name__ == "__main__":
    import argparse

    # Parse the .docx file from the command line argument
    parser = argparse.ArgumentParser(description="Resume Analyzer using spaCy and python-docx")
    parser.add_argument('--file', type=str, required=True, help='Path to the .docx file')
    args = parser.parse_args()

    # Create an instance of DocumentAnalyzer
    analyzer = DocumentAnalyzer(args.file)

    # Analyze the document and get extracted information
    extracted_information = analyzer.analyze()

    # Display the extracted information
    print("\nExtracted Information:\n")

    # Print Name
    print(f"Name: {extracted_information['Name']}")

    # Print Education
    print("\nEducation:")
    if extracted_information['Education']:
        for edu in extracted_information['Education']:
            print(f"- {edu}")
    else:
        print("No education information found.")

    # Print Work Experience
    print("\nWork Experience:")
    if extracted_information['Work Experience']:
        for exp in extracted_information['Work Experience']:
            print(f"- {exp}")
    else:
        print("No work experience information found.")
