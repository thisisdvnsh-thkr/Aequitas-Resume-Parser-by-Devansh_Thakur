# Resume Parsing WebApp
 

## Introduction
This project creates a web application designed to evaluate the compatibility of a resume with a job description. Utilizing Natural Language Processing (NLP) techniques, the app extracts and compares key skills from both documents to provide a compatibility score. The app employs machine learning models and text analysis methods to assist users in tailoring their resumes to better fit job requirements.

You can check your job comatibility through this link:  
https://resume-parsing-webapp-xlsuqzsijc3fjjanr5lw3d.streamlit.app/

*Test Situation:*
![test2](https://github.com/user-attachments/assets/572d38d6-7c46-4cfb-a436-d0adb2f7625a)

## Features
- **File Upload:** Users can upload job descriptions and resumes in PDF or DOCX format.
- **Text Extraction:** Extracts text from uploaded documents using `pdfminer` and `docx2txt`.
- **Skill Extraction:** Identifies and extracts relevant skills from the text using a predefined skill set.
- **Compatibility Score:** Calculates a similarity score between the resume and the job description.
- **Skills Comparison:** Displays matching and missing skills based on the extracted data.
  
## Technical Details
1. Text Extraction:

- PDF text extraction is performed using `pdfminer`.
- DOCX text extraction is done using `docx2txt`.
2. Skill Extraction:

- Skills are matched against a predefined list using regular expressions.
3. Similarity Calculation:

- Utilizes `CountVectorizer` and `cosine_similarity` from `sklearn` to compute the compatibility score.
4. Streamlit WebApp:

- Provides an interactive interface for users to upload files and view results.
- Displays the compatibility score and skill comparison using custom styling.

## Installation
1. Clone the repository:

```python
git clone <repository-url>
cd <repository-folder>
```
2. Install the required packages:

```python
pip install streamlit docx2txt pdfminer.six scikit-learn
```
3. Run the Streamlit app:

```python
streamlit run app.py
```

## Usage
1. Upload the job description and resume files in PDF or DOCX format.
2. Click the "Calculate" button to compute the compatibility score and view the results.
3. Review the matching and missing skills to assess how well your resume aligns with the job description.
   
## Conclusion
The Resume Parsing WebApp provides an intuitive platform for comparing resumes with job descriptions, helping users improve their job application materials. By analyzing text and extracting key skills, it aids in identifying areas of strength and gaps, enhancing overall job application effectiveness.

For recruiters, this tool is invaluable as it streamlines the candidate screening process by quickly identifying how well a resume matches job requirements. This reduces the time spent manually reviewing resumes and ensures that candidates with the most relevant skills are prioritized, ultimately improving the efficiency and accuracy of the hiring process.

For any questions or further assistance, please feel free to contact me.

Dhananjaya Mudunkotuwa  
dhananjayamudunkotuwa1998@gmail.com
