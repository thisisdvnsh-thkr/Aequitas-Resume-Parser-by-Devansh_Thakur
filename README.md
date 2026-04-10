# ⚖️ Aequitas — AI Resume Auditor

### Intelligent & Fair Resume Screening System

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org) [![Streamlit](https://img.shields.io/badge/Streamlit-v2.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io) [![NLP](https://img.shields.io/badge/NLP-TF--IDF-00d4ff?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org) [![Live App](https://img.shields.io/badge/Live%20App-Online-00C851?style=for-the-badge&logo=streamlit&logoColor=white)](https://aequitas-by-thisisdvnshthkr.streamlit.app) [![License](https://img.shields.io/badge/License-MIT-7928CA?style=for-the-badge)](LICENSE)

<br>

> An intelligent AI system for resume screening — analyses resumes against job descriptions using NLP to provide match scores and skill gap analysis, with a strong focus on **reducing hiring bias**.

<br>

### 🔗 [Launch Live App →](https://aequitas-by-thisisdvnshthkr.streamlit.app)

<br>

</div>

---

## 📌 Problem Statement

Traditional resume screening relies on simple keyword matching, which introduces bias based on phrasing, formatting, gender and background — rather than actual skills and competency.

**Aequitas** solves this by using **Cosine Similarity** and **NLP techniques** to calculate a match percentage purely based on technical skills and content, removing human and keyword-based bias from the initial screening process.

---

## ✨ Key Features

- 📄 **Multi-Format Support** — Accepts PDF and DOCX files for both resumes and job descriptions
- 🔍 **Intelligent Parsing** — Extracts and cleans text using Regex and Tokenization
- 📊 **Compatibility Score** — Calculates match percentage (0–100%) using vector similarity
- ✅ **Matched Skills** — Shows skills present in both resume and job description
- ❌ **Missing Skills** — Highlights critical skills absent from the resume
- 🎨 **Dark / Light Theme** — Toggle between themes with a fixed floating button
- ⚖️ **Bias Reduction** — Focuses purely on technical skills and content, ignoring demographic signals

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Backend** | Python 3.11 |
| **NLP & ML** | Scikit-learn (TF-IDF Vectorizer, Cosine Similarity) |
| **PDF Parsing** | pdfminer.six |
| **DOCX Parsing** | docx2txt |
| **Text Processing** | Regex, Tokenization |
| **Deployment** | Streamlit Community Cloud |

---

## 🔄 How It Works

```
Resume (PDF/DOCX) ──┐
├──► Text Extraction & Cleaning
JD (PDF/DOCX) ─────┘ │
▼
NLP Processing
(Tokenization + Regex Cleaning)
│
▼
TF-IDF Vectorization
(Term Frequency — Inverse Document Frequency)
│
▼
Cosine Similarity Score
│
▼
┌──────────────────────────┐
│ Match Score (0–100%) │
│ + Matched Skills │
│ + Missing Skills │
└──────────────────────────┘
```

---

## 📊 Output

- **Match Score** — Percentage compatibility between resume and job description
- **Matched Skills** — Common technical keywords found in both documents
- **Missing Skills** — Skills present in JD but missing from resume
- **Bias-free Analysis** — No demographic, formatting or keyword-phrasing bias

---

## 🚀 Run Locally

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
**4. Open in browser**
```bash
http://localhost:8501
```
---

## 📁 Project Structure

```
Aequitas_Resume-Parser/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version → python-3.11
└── README.md               # Project documentation
```

---

## 👥 Contributors

<table> <tr> <td align="center"> <strong>Devansh Thakur</strong><br> <em>Lead Architect & Developer</em><br> <a href="https://linkedin.com/in/devansh-thakur">💼 LinkedIn</a> • <a href="https://github.com/thisisdvnsh-thkr">👤 GitHub</a> </td> <td align="center"> <strong>Arpit Upadhyay</strong><br> <em>Co-Developer</em><br> <a href="https://github.com/ArpitUpadhyay">👤 GitHub</a> </td> </tr> </table>
<div align="center">
Aequitas v2.0 © 2026  |  Built with Python & Streamlit
Powered by TF-IDF Vectorization & Cosine Similarity

⭐ Star this repo if you found it useful!

</div>
