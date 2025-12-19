import streamlit as st
import docx2txt
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

def extract_skills(text):
    skills = [
    'Python', 'Java', 'C++', 'SQL', 'Machine Learning', 'Data Analysis', 'Deep Learning',
    'NLP', 'Communication', 'Teamwork', 'Leadership', 'Problem Solving', 'Docker', 'Kubernetes',
    'Project Management', 'Linux', 'Git', 'HTML', 'CSS', 'JavaScript', 'Excel', 'Power BI',
    'Tableau', 'Data Visualization', 'Pandas', 'NumPy', 'TensorFlow', 'PyTorch', 'R',
    'Statistical Analysis', 'AWS', 'Azure', 'Google Cloud', 'DevOps', 'Agile', 'Scrum',
    'REST APIs', 'GraphQL', 'JSON', 'XML', 'Bootstrap', 'React', 'Angular', 'Vue.js',
    'Node.js', 'Django', 'Flask', 'Ruby on Rails', 'SQL Server', 'PostgreSQL', 'MongoDB',
    'Cassandra', 'Redis', 'Hadoop', 'Spark', 'Kafka', 'Jenkins', 'CI/CD', 'JIRA',
    'MATLAB', 'Simulink', 'Computer Vision', 'OpenCV', 'Natural Language Processing', 'Spacy',
    'Gensim', 'AWS S3', 'AWS Lambda', 'Terraform', 'Ansible', 'Apache Beam', 'BigQuery',
    'Keras', 'Scikit-learn', 'XGBoost', 'LightGBM', 'Time Series Analysis', 'Hyperparameter Tuning',
    'Cross-Validation', 'A/B Testing', 'Market Basket Analysis', 'Churn Prediction', 'Customer Segmentation',
    'Business Intelligence', 'ETL', 'Data Warehousing', 'Data Mining', 'Database Management', 'NoSQL Databases',
    'MySQL', 'Oracle', 'PL/SQL', 'SSIS', 'SSRS', 'SSAS', 'Data Cleaning', 'Feature Engineering',
    'Regression Analysis', 'Classification', 'Clustering', 'Dimensionality Reduction', 'Principal Component Analysis',
    'Linear Regression', 'Logistic Regression', 'Decision Trees', 'Random Forests', 'Support Vector Machines',
    'Ensemble Methods', 'Bayesian Methods', 'Monte Carlo Simulation', 'Financial Modeling', 'Risk Management',
    'Blockchain', 'Cryptography', 'Cybersecurity', 'Penetration Testing', 'Ethical Hacking', 'Network Security',
    'IoT', 'Embedded Systems', 'Robotics', 'Automation', 'Control Systems', 'Digital Signal Processing',
    'Image Processing', 'Video Processing', 'Augmented Reality', 'Virtual Reality', '3D Modeling', 'Unity',
    'Unreal Engine', 'Game Development', 'Mobile App Development', 'Android', 'iOS', 'Swift', 'Kotlin',
    'Objective-C', 'React Native', 'Flutter', 'Machine Translation', 'Speech Recognition', 'Voice Assistants',
    'Chatbots', 'AI Ethics', 'Data Governance', 'Data Privacy', 'GDPR Compliance', 'Business Analysis'
]

    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)

    matched_skills = [skill for skill in skills if skill.lower() in text]

    return matched_skills

# Streamlit App
st.markdown("""
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    </head>
    <div style='text-align: center; padding: 15px;'>
        <h1 style='color: white;'><i class="fas fa-balance-scale" style="color: #0078D4;"></i> Aequitas: AI Resume Auditor</h1>
        <p style='color: #CCCCCC; font-size: 18px;'>Developed by Devansh Thakur, Arpit Upadhyay & Arjun Kumar</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <h3 style='font-size: 20px; color: #FFFFFF; text-align: center;'>Upload the Job Description and your Resume to begin analysis.</h3>
""", unsafe_allow_html=True)

job_desc_file = st.file_uploader("Upload Job description (PDF or DOCX)", type = ['pdf', 'docx'])
resume_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type = ['pdf', 'docx'])


if st.button("Calculate"):
    if resume_file and job_desc_file:
        if resume_file.name.endswith('.pdf'):
            resume_text = extract_text_from_pdf(resume_file)
        else:
            resume_text = docx2txt.process(resume_file)

        if job_desc_file.name.endswith('.pdf'):
            job_desc_text = extract_text_from_pdf(job_desc_file)
        else:
            job_desc_text = docx2txt.process(job_desc_file)


        # Calculate similarity
        text = [resume_text, job_desc_text]
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text)
        similarity_scores = cosine_similarity(count_matrix)

        similarity_score = similarity_scores[0][1] * 100 
        similarity_score = round(similarity_score, 2)

        # Display the similarity score with custom styling
        st.markdown(f"""
    <div style='background-color: #262730; padding: 20px; border-radius: 10px; border: 1px solid #4CAF50;'>
        <h2 style='color: #4CAF50;'>📝 Aequitas Score</h2>
        <p style='font-size: 24px; color: white;'>
         Your resume matches <strong>{similarity_score}%</strong> of the job description.
        </p>
    </div>
""", unsafe_allow_html=True)

        # Skills Comparison
        resume_skills = extract_skills(resume_text)
        job_desc_skills = extract_skills(job_desc_text)

        matching_skills = set(resume_skills).intersection(set(job_desc_skills))
        missing_skills = set(job_desc_skills) - set(resume_skills)

        
        col1, col2 = st.columns(2)

        with col1:
            # Display matching skills
            if matching_skills:
                st.markdown("### Matching Skills: ")
                st.markdown(f"<p style='color:#1f77b4; font-size:16px;'> {' | '.join(matching_skills)} </p>", unsafe_allow_html=True)
            else:
                st.error("No matching skills found.")

        with col2:
            # Display missing skills
            if missing_skills:
                st.markdown("### Missing Skills: ")
                st.markdown(f"<p style='color:#1f77b4; font-size:16px;'> {' | '.join(missing_skills)} </p>", unsafe_allow_html=True)
            else:
                st.success("You have all the required skills!")

    
    else:
        st.write("Please upload both the job description and your resume files. ")
        # --- FINAL FOOTER SECTION ---
# This line creates a visual horizontal separator
st.markdown("---") 

st.markdown("""
    <div style='text-align: center; color: #888888; padding: 20px;'>
        <p style='font-size: 16px; font-weight: bold;'>Aequitas AI Resume Auditor</p>
        <p>© 2025 | B.Tech AIML Final Year Minor Project</p>
        <p>Developed by <b>Devansh Thakur</b> & [Partner Names]</p>
        <p style='font-size: 12px;'>Kashipur, Uttarakhand</p>
    </div>
""", unsafe_allow_html=True)