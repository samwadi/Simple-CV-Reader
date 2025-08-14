# 📄 CV Scanner & Information Extractor

This project extracts structured information from CVs and resumes in **PDF** or **Word (.docx)** formats.  
It comes with **two versions**:
1. 🧩 **Regex-based version (`main1.py`)** – Simple, lightweight, no dependencies beyond parsing libraries.  
2. 🤖 **AI-powered version (`main2.py`)** – Uses **spaCy** and NLP techniques for smarter entity recognition, plus a **GUI** built with Tkinter.  

---

## ✨ Features
- ✅ Extracts key details:
  - Name  
  - Email  
  - Phone number  
  - Education  
  - Work experience  
- 📂 Supports **PDF** and **DOCX** formats  
- 🖥️ **CLI output** in `main1.py`  
- 🖼️ **GUI display** in `main2.py`  
- 🧠 Uses **regex** in version 1, and **spaCy NLP models** in version 2  

---

## 🚀 How to Run

### Option 1: Regex-based (Simple)
```bash
python main1.py


Opens a file dialog to select a PDF or DOCX CV.

Prints extracted information directly in the terminal.

Option 2: AI-powered with GUI

python main2.py


Opens a file dialog to select a PDF or DOCX CV.

Uses spaCy to extract entities and additional details.

Displays results in a clean Tkinter GUI.

CV-Extractor/
│── main1.py        # Regex-based version (no GUI)
│── main2.py        # AI/NLP version with GUI
│── requirements.txt
│── README.md


🛠️ Requirements
Install dependencies with:

pip install -r requirements.txt

Example requirements.txt:

spacy
pdfplumber
python-docx
tkinter

And download the spaCy model (needed for main2.py):

python -m spacy download en_core_web_sm


📌 Notes
Custom CV formats may lead to slightly mixed or misaligned data, especially if the layout is unconventional.

For most standard CV templates, extraction should work effectively.

main1.py is better for quick, lightweight usage.

main2.py is more robust and accurate, but requires installing spaCy and loading the NLP model.

🧑‍💻 Author
Made with ❤️ by Bassam Wadi
📧 Contact: samwadi97@gmail.com
