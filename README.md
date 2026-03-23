# Aequitas — AI Resume Auditor
### Python • NLP • Streamlit • Scikit-learn

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat)

An intelligent and fair AI system for 
resume screening — analyses resumes against 
job descriptions using NLP to provide 
match scores and skill gap analysis.

---

## 📌 Problem Statement

Traditional resume screening relies on 
keyword matching which introduces bias 
based on phrasing, gender and background 
rather than actual skills and competency.

Aequitas solves this by using **Cosine 
Similarity** and **NLP techniques** to 
calculate match percentage purely based 
on technical skills and content — 
removing human and keyword bias.

---

## ✨ Key Features

- 📄 **Multi-Format Support** — Accepts 
  PDF and DOCX files for both resumes 
  and job descriptions
- 🔍 **Intelligent Parsing** — Extracts 
  and cleans text using Regex and 
  Tokenization
- 📊 **Compatibility Score** — Calculates 
  match percentage (0-100%) using 
  vector similarity
- ✅ **Matched Skills** — Shows skills 
  present in both resume and JD
- ❌ **Missing Skills** — Highlights 
  critical skills absent from resume
- ⚖️ **Bias Reduction** — Focuses purely 
  on technical skills and content

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python 3.10 |
| NLP & ML | Scikit-learn (Cosine Similarity, CountVectorizer) |
| PDF Parsing | pdfminer.six |
| DOCX Parsing | docx2txt |
| Text Processing | Regex, Tokenization |

---

## 🔄 How It Works
```
Resume (PDF/DOCX) ──┐
                    ├──► Text Extraction
JD (PDF/DOCX) ─────┘         │
                              ▼
                    NLP Processing
                    (Tokenization + Cleaning)
                              │
                              ▼
                    Cosine Similarity
                    (CountVectorizer)
                              │
                              ▼
                    Match Score (0-100%)
                    + Skill Gap Analysis
```

---

## 📊 Output

- **Match Score** — Percentage compatibility 
  between resume and job description
- **Matched Skills** — Common technical 
  keywords found in both
- **Missing Skills** — Skills in JD 
  not found in resume
- **Bias-free analysis** — No demographic 
  or formatting bias

---

## 🚀 How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/thisisdvnsh-thkr/aequitas-fair-hiring-nlp.git
cd aequitas-fair-hiring-nlp
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

---

## 📁 Project Structure
```
├── .devcontainer/     # Dev container config
├── images/            # UI screenshots
├── app.py             # Main Streamlit app
├── requirements.txt   # Dependencies
├── runtime.txt        # Python version
└── README.md
```

---

## 👥 Contributors

**Devansh Thakur**
[LinkedIn](https://linkedin.com/in/devansh-thakur) •
[GitHub](https://github.com/thisisdvnsh-thkr)

**Arpit Upadhyay**
[GitHub](https://github.com/Arpit7088)

---

*Built with Python & Streamlit*
```

---
