# Aequitas - AI-Powered Resume Screening & Fairness Auditor
 

## Introduction
Aequitas is an AI-driven web application designed to evaluate the alignment between a candidate's resume and a specific job description. Developed as a minor project for the 7th-semester B.Tech curriculum in Artificial Intelligence & Machine Learning, the system utilizes Natural Language Processing (NLP) and vector space modeling to provide a quantifiable compatibility score and detailed skill-gap analysis.

You can check your job comatibility through this link:  
**[PASTE_YOUR_STREAMLIT_URL_HERE]**

## Features
- **Dual-Format Support:** Seamlessly handles both PDF and DOCX files for Job Descriptions and Resumes.
- **Automated Skill Extraction:** Uses specialized NLP parsing to identify relevant technical and soft skills.
- **Similarity Scoring:** Employs mathematical vectorization to compute a compatibility percentage.
- **Skill-Gap Analytics:** Visually differentiates between matching competencies and missing requirements.
- **Aequitas Auditor Interface:** A custom-styled UI designed for professional fairness auditing.

## Technical Details
1. **Text Extraction:**
   - PDF text extraction is performed using `pdfminer.six`.
   - DOCX text extraction is performed using `docx2txt`.

2. **Skill Extraction:**
   - Relevant skills are identified from the text using a predefined skill set and regular expression matching.

3. **Similarity Calculation:**
   - Utilizes `CountVectorizer` to transform raw text into numerical feature vectors.
   - Implements **Cosine Similarity** from `sklearn` to compute the compatibility score between the two documents.

4. **Streamlit WebApp:**
   - Provides an interactive, dark-themed interface for real-time analysis and result visualization.



For any questions or further assistance, please feel free to contact me.

Devansh Thakur
devil.devthakur9999@gmail.com


