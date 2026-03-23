import streamlit as st
import pdfminer
from pdfminer.high_level import extract_text
import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(
    page_title="Aequitas: AI Resume Auditor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SKILL DATABASE ---
SKILL_DB = [
    "python", "java", "c++", "c", "javascript", "typescript", "php", "ruby", "swift", "kotlin", "go", "rust", "sql", "r", "matlab",
    "html", "css", "react", "angular", "vue", "node.js", "django", "flask", "fastapi", "bootstrap", "tailwind", "jquery",
    "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "pytorch", "opencv", "nltk", "spacy", "matplotlib", "seaborn", "tableau", "power bi", "excel",
    "aws", "azure", "google cloud", "docker", "kubernetes", "jenkins", "git", "github", "gitlab", "linux", "unix", "bash", "terraform",
    "mysql", "postgresql", "mongodb", "oracle", "sqlite", "redis", "cassandra",
    "communication", "leadership", "problem solving", "agile", "scrum", "project management", "critical thinking"
]

# --- 3. INJECT CUSTOM CSS (THEME ADAPTIVE) ---
st.markdown("""
    <style>
    /* Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Hide default deploy button */
    .stDeployButton {display:none;}

    /* ===== THEME ADAPTIVE VARIABLES ===== */
    /* These use Streamlit's built-in CSS variables that 
       automatically switch between light and dark mode */

    /* Header Strip - adapts to theme */
    .header-strip {
        background: linear-gradient(90deg, #0078D4 0%, #005a9e 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        display: flex;
        align-items: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .header-logo {
        font-size: 45px;
        margin-right: 20px;
    }
    .header-text h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        letter-spacing: 1px;
    }
    .header-text p {
        margin: 5px 0 0 0;
        font-size: 1rem;
        color: #e2e8f0;
    }

    /* Developer Name Cards - theme adaptive */
    .dev-container {
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .dev-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: var(--text-color);
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 12px;
        opacity: 0.6;
    }
    .dev-name-card {
        background-color: var(--background-color);
        padding: 12px 15px;
        margin-bottom: 8px;
        border-radius: 8px;
        border-left: 5px solid #0078D4;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-color);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: default;
    }
    .dev-name-card:hover {
        background-color: #0078D4;
        color: white;
        transform: translateX(5px);
        box-shadow: 0 4px 10px rgba(0,120,212,0.4);
    }

    /* Score Card - theme adaptive */
    .score-card {
        background-color: var(--background-color);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid rgba(0,120,212,0.2);
    }

    /* Skill Tags - theme adaptive */
    .skill-tag {
        display: inline-block;
        padding: 6px 12px;
        margin: 4px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
    }
    .match-tag {
        background-color: rgba(25, 135, 84, 0.15);
        color: #198754;
        border: 1px solid rgba(25, 135, 84, 0.3);
    }
    .missing-tag {
        background-color: rgba(220, 53, 69, 0.15);
        color: #dc3545;
        border: 1px solid rgba(220, 53, 69, 0.3);
    }

    /* Landing page info box - theme adaptive */
    .info-box {
        background-color: rgba(0, 120, 212, 0.1);
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #0078D4;
        color: var(--text-color);
    }

    /* Landing page text - theme adaptive */
    .landing-heading {
        color: var(--text-color);
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .landing-text {
        color: var(--text-color);
        font-size: 1.05rem;
        line-height: 1.7;
        opacity: 0.85;
    }
    .landing-list {
        color: var(--text-color);
        font-size: 1rem;
        line-height: 1.9;
        opacity: 0.9;
    }

    /* Streamlit built-in theme variables */
    :root {
        --text-color: #1e293b;
        --background-color: #f8fafc;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --text-color: #e2e8f0;
            --background-color: #1e293b;
        }
    }

    [data-theme="dark"] {
        --text-color: #e2e8f0;
        --background-color: #1e293b;
    }

    [data-theme="light"] {
        --text-color: #1e293b;
        --background-color: #f8fafc;
    }
    </style>

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
""", unsafe_allow_html=True)

# --- 4. HELPER FUNCTIONS ---
def get_text_from_pdf(file):
    return extract_text(file)

def get_text_from_docx(file):
    return docx2txt.process(file)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    return text

def extract_skills(text):
    found_skills = set()
    cleaned_text = clean_text(text)
    words = set(cleaned_text.split())
    for skill in SKILL_DB:
        if skill in words:
            found_skills.add(skill)
        elif " " in skill and skill in cleaned_text:
            found_skills.add(skill)
    return found_skills

# --- 5. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/924/924915.png", width=60)
    st.title("Control Panel")

    st.markdown("### 1. Upload Documents")
    uploaded_jd = st.file_uploader("Job Description (JD)", type=["pdf", "docx"])
    uploaded_resume = st.file_uploader("Candidate Resume", type=["pdf", "docx"])

    st.markdown("---")

    st.markdown("""
        <div class="dev-container">
            <div class="dev-title">Created By</div>
            <div class="dev-name-card">Devansh Thakur</div>
            <div class="dev-name-card">Arpit Upadhyay</div>
            <div class="dev-name-card">Arjun Kumar</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Aequitas v1.0 | Final Year Project")

# --- 6. MAIN PAGE HEADER ---
st.markdown("""
    <div class="header-strip">
        <i class="fas fa-balance-scale header-logo" style="color: white;"></i>
        <div class="header-text">
            <h1>Aequitas: AI Resume Auditor</h1>
            <p>Intelligent & Fair Resume Screening System</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 7. LOGIC & DASHBOARD ---
if uploaded_jd and uploaded_resume:
    with st.spinner('⚡ AI is auditing the resume...'):
        try:
            if uploaded_jd.type == "application/pdf":
                jd_text = get_text_from_pdf(uploaded_jd)
            else:
                jd_text = get_text_from_docx(uploaded_jd)

            if uploaded_resume.type == "application/pdf":
                resume_text = get_text_from_pdf(uploaded_resume)
            else:
                resume_text = get_text_from_docx(uploaded_resume)

            jd_skills = extract_skills(jd_text)
            resume_skills = extract_skills(resume_text)
            matched_skills = jd_skills.intersection(resume_skills)
            missing_skills = jd_skills.difference(resume_skills)

            jd_clean = clean_text(jd_text)
            resume_clean = clean_text(resume_text)
            cv = CountVectorizer()
            count_matrix = cv.fit_transform([jd_clean, resume_clean])
            match_percentage = round(cosine_similarity(count_matrix)[0][1] * 100, 2)

            # --- RESULT SECTION ---
            col1, col2 = st.columns([1, 1.5])

            with col1:
                st.markdown('<div class="score-card">', unsafe_allow_html=True)
                st.write("### 🎯 Match Score")
                if match_percentage >= 75:
                    st.markdown(f"<h1 style='color: #198754; font-size: 3.5rem;'>{match_percentage}%</h1>", unsafe_allow_html=True)
                    st.success("✅ Excellent Match")
                    st.balloons()
                elif match_percentage >= 50:
                    st.markdown(f"<h1 style='color: #fd7e14; font-size: 3.5rem;'>{match_percentage}%</h1>", unsafe_allow_html=True)
                    st.warning("⚠️ Average Match")
                else:
                    st.markdown(f"<h1 style='color: #dc3545; font-size: 3.5rem;'>{match_percentage}%</h1>", unsafe_allow_html=True)
                    st.error("❌ Low Match")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.write("### 🧬 Skill Audit")
                st.write("**✅ Matched Skills:**")
                if matched_skills:
                    st.markdown("".join([f'<span class="skill-tag match-tag">{s.upper()}</span>' for s in matched_skills]), unsafe_allow_html=True)
                else:
                    st.warning("No skills matched directly.")

                st.write("---")

                st.write("**❌ Missing Skills:**")
                if missing_skills:
                    st.markdown("".join([f'<span class="skill-tag missing-tag">{s.upper()}</span>' for s in missing_skills]), unsafe_allow_html=True)
                else:
                    st.success("No key skills missing!")

            with st.expander("📄 View Resume Snippet"):
                st.info(resume_text[:600] + "...")

        except Exception as e:
            st.error(f"❌ Error: {e}")

else:
    # --- LANDING PAGE ---
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.image(
            "https://website-artificio.s3.us-west-2.amazonaws.com/Resume_Parsing_a180290fcd.jpg",
            use_column_width=True
        )

    with col2:
        st.markdown("""
        <div style="padding-top: 20px; padding-left: 10px;">
            <p class="landing-heading">Automated Resume Parsing</p>
            <p class="landing-text">
                <b>Aequitas AI</b> is a powerful tool designed to help recruiters 
                and candidates by providing an unbiased, automated analysis of 
                resumes against job descriptions.
            </p>
            <ul class="landing-list">
                <li>🚀 <b>Instant Match Calculation</b></li>
                <li>⚖️ <b>Fair & Unbiased Screening</b></li>
                <li>🔍 <b>Detailed Skill Gap Analysis</b></li>
            </ul>
            <br>
            <div class="info-box">
                <small>👈 <b>Start Audit:</b> Upload JD & Resume from the Sidebar.</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
