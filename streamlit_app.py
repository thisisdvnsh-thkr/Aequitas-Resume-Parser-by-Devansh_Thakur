import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfminer.high_level
import docx2txt
import io

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Aequitas | AI Resume Auditor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== THEME TOGGLE ====================
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

def toggle_theme():
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

# ==================== CUSTOM CSS ====================
def load_css():
    theme = st.session_state.theme
    
    if theme == 'dark':
        bg_color = "#0e1117"
        card_bg = "rgba(28, 31, 40, 0.8)"
        text_color = "#ffffff"
        secondary_text = "#b4b4b4"
        accent_color = "#00d4ff"
        border_color = "rgba(255, 255, 255, 0.15)"
        shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.4)"
        gradient_bg = "radial-gradient(at 0% 0%, rgba(0, 212, 255, 0.15) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(138, 43, 226, 0.15) 0px, transparent 50%)"
    else:
        bg_color = "#f8f9fa"
        card_bg = "rgba(255, 255, 255, 0.9)"
        text_color = "#1a1a1a"
        secondary_text = "#666666"
        accent_color = "#0066cc"
        border_color = "rgba(0, 102, 204, 0.2)"
        shadow = "0 4px 24px 0 rgba(0, 0, 0, 0.08)"
        gradient_bg = "radial-gradient(at 0% 0%, rgba(0, 102, 204, 0.08) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(138, 43, 226, 0.08) 0px, transparent 50%)"
    
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Hide Sidebar */
    [data-testid="stSidebar"] {{
        display: none !important;
    }}
    
    .stApp {{
        background: {bg_color};
        background-image: {gradient_bg};
        color: {text_color};
    }}
    
    .main .block-container {{
        padding: 2rem 3rem;
        max-width: 1400px;
    }}
    
    /* Glassmorphism Cards */
    .glass-card {{
        background: {card_bg};
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 24px;
        border: 1px solid {border_color};
        padding: 2rem;
        box-shadow: {shadow};
        margin-bottom: 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .glass-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 16px 48px 0 rgba(0, 212, 255, 0.2);
        border-color: {accent_color};
    }}
    
    /* Header */
    .main-header {{
        text-align: center;
        padding: 3rem 0 1rem 0;
        background: linear-gradient(135deg, {accent_color}, #8a2be2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.8rem;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 0.5rem;
    }}
    
    .sub-header {{
        text-align: center;
        color: {secondary_text};
        font-size: 1.3rem;
        font-weight: 400;
        margin-bottom: 3rem;
        letter-spacing: 0.5px;
    }}
    
    /* Feature Cards */
    .feature-box {{
        background: {card_bg};
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 1.8rem;
        border: 1px solid {border_color};
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 1.2rem;
        transition: all 0.3s ease;
        box-shadow: {shadow};
    }}
    
    .feature-box:hover {{
        border-color: {accent_color};
        transform: translateX(10px);
        box-shadow: 0 8px 24px rgba(0, 212, 255, 0.15);
    }}
    
    .feature-icon {{
        font-size: 2.5rem;
        min-width: 60px;
        text-align: center;
    }}
    
    .feature-text {{
        flex: 1;
    }}
    
    .feature-title {{
        font-weight: 600;
        font-size: 1.1rem;
        color: {text_color};
        margin-bottom: 0.3rem;
    }}
    
    .feature-desc {{
        font-size: 0.9rem;
        color: {secondary_text};
    }}
    
    /* Results Card */
    .result-card {{
        background: linear-gradient(135deg, {accent_color}15, #8a2be225);
        backdrop-filter: blur(16px);
        border-radius: 24px;
        padding: 3rem 2rem;
        border: 1px solid {accent_color}40;
        margin: 2rem 0;
        box-shadow: {shadow};
    }}
    
    .match-score {{
        font-size: 5rem;
        font-weight: 800;
        background: linear-gradient(135deg, {accent_color}, #8a2be2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 1rem 0;
        letter-spacing: -3px;
    }}
    
    /* Skill Pills */
    .skill-pill {{
        display: inline-block;
        background: {accent_color}25;
        color: {accent_color};
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        margin: 0.5rem;
        font-size: 0.95rem;
        font-weight: 500;
        border: 1px solid {accent_color}50;
        transition: all 0.3s ease;
    }}
    
    .skill-pill:hover {{
        background: {accent_color}40;
        transform: scale(1.05);
    }}
    
    /* Theme Toggle */
    .theme-toggle {{
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: {card_bg};
        backdrop-filter: blur(16px);
        border: 1px solid {border_color};
        border-radius: 60px;
        padding: 14px 24px;
        cursor: pointer;
        box-shadow: {shadow};
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.1rem;
        font-weight: 500;
        color: {text_color};
        transition: all 0.3s ease;
    }}
    
    .theme-toggle:hover {{
        transform: scale(1.1);
        border-color: {accent_color};
        box-shadow: 0 8px 32px {accent_color}40;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        padding: 3rem 2rem;
        margin-top: 5rem;
        border-top: 1px solid {border_color};
    }}
    
    .footer-credits {{
        font-size: 1rem;
        margin-bottom: 1.5rem;
        color: {text_color};
        line-height: 1.8;
    }}
    
    .footer-link {{
        color: {accent_color};
        text-decoration: none;
        margin: 0 0.8rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    
    .footer-link:hover {{
        text-decoration: underline;
    }}
    
    .footer-meta {{
        font-size: 0.85rem;
        color: {secondary_text};
        margin-top: 1rem;
        line-height: 1.6;
    }}
    
    /* Documentation Cards */
    .doc-card {{
        background: {card_bg};
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid {border_color};
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: {shadow};
    }}
    
    .doc-card:hover {{
        border-color: {accent_color};
        transform: translateY(-5px);
    }}
    
    .doc-title {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {text_color};
        margin-bottom: 0.8rem;
    }}
    
    .doc-desc {{
        font-size: 0.9rem;
        color: {secondary_text};
        line-height: 1.7;
    }}
    
    /* Buttons */
    .stButton>button {{
        background: linear-gradient(135deg, {accent_color}, #8a2be2);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: {shadow};
    }}
    
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 8px 24px {accent_color}50;
    }}
    
    /* Progress Bar */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, {accent_color}, #8a2be2);
        border-radius: 10px;
    }}
    
    /* FILE UPLOADER - HIDE 200MB TEXT */
    [data-testid="stFileUploader"] {{
        background: {card_bg};
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid {border_color};
    }}
    
    [data-testid="stFileUploader"] section {{
        border: 2px dashed {border_color};
        border-radius: 12px;
        padding: 2rem;
    }}
    
    /* CRITICAL: Hide the "200MB per file" text */
    [data-testid="stFileUploader"] small {{
        display: none !important;
    }}
    
    [data-testid="stFileUploader"] span[data-testid="stMarkdownContainer"] small {{
        display: none !important;
    }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    header {{visibility: hidden !important;}}
    
    .upload-title {{
        font-size: 1.4rem;
        font-weight: 600;
        color: {text_color};
        margin-bottom: 1.5rem;
    }}
    
    /* Custom file size text */
    .file-limit {{
        font-size: 0.85rem;
        color: {secondary_text};
        margin-top: 0.5rem;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ==================== TEXT EXTRACTION ====================
def extract_text_from_pdf(file):
    try:
        return pdfminer.high_level.extract_text(io.BytesIO(file.read()))
    except:
        return ""

def extract_text_from_docx(file):
    try:
        return docx2txt.process(io.BytesIO(file.read()))
    except:
        return ""

def extract_text(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file)
    else:
        return ""

# ==================== SKILL EXTRACTION ====================
def extract_skills(text):
    common_skills = [
        'Python', 'Java', 'C++', 'JavaScript', 'SQL', 'R', 'Machine Learning',
        'Deep Learning', 'NLP', 'Data Science', 'TensorFlow', 'PyTorch', 'Keras',
        'Scikit-learn', 'Pandas', 'NumPy', 'Matplotlib', 'Power BI', 'Tableau',
        'Excel', 'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Git', 'CI/CD',
        'Agile', 'Scrum', 'REST API', 'Flask', 'Django', 'React', 'Node.js',
        'MongoDB', 'PostgreSQL', 'MySQL', 'Data Analysis', 'Statistics',
        'Computer Vision', 'Time Series', 'A/B Testing', 'ETL', 'Big Data',
        'Spark', 'Hadoop', 'Kafka', 'Airflow', 'Linux', 'Bash', 'HTML', 'CSS'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in common_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return found_skills

# ==================== MATCHING LOGIC ====================
def calculate_match(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(similarity * 100, 2)

# ==================== MAIN APP ====================
def main():
    load_css()
    
    # Header
    st.markdown('<h1 class="main-header">⚖️ Aequitas: AI Resume Auditor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Intelligent & Fair Resume Screening System</p>', unsafe_allow_html=True)
    
    # Features Section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🎯</div>
            <div class="feature-text">
                <div class="feature-title">Instant Match Calculation</div>
                <div class="feature-desc">Get precise resume-JD alignment scores in seconds</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🔍</div>
            <div class="feature-text">
                <div class="feature-title">Fair & Unbiased Screening</div>
                <div class="feature-desc">AI-powered objective evaluation system</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">📊</div>
            <div class="feature-text">
                <div class="feature-title">Detailed Skill Gap Analysis</div>
                <div class="feature-desc">Identify missing qualifications instantly</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Upload Section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="upload-title">📄 Upload Documents</div>', unsafe_allow_html=True)
    
    col_resume, col_jd = st.columns(2)
    
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    
    with col_resume:
        st.markdown("**Candidate Resume**")
        resume_file = st.file_uploader(
            "Upload Resume",
            type=['pdf', 'docx'],
            key='resume',
            label_visibility="collapsed"
        )
        st.markdown('<p class="file-limit">📎 PDF or DOCX • Maximum 5MB</p>', unsafe_allow_html=True)
    
    with col_jd:
        st.markdown("**Job Description**")
        jd_file = st.file_uploader(
            "Upload Job Description",
            type=['pdf', 'docx'],
            key='jd',
            label_visibility="collapsed"
        )
        st.markdown('<p class="file-limit">📎 PDF or DOCX • Maximum 5MB</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis Section
    if resume_file and jd_file:
        # File size validation
        if resume_file.size > MAX_FILE_SIZE:
            st.error(f"❌ Resume file is {resume_file.size / (1024*1024):.1f}MB. Maximum allowed is 5MB.")
            return
        if jd_file.size > MAX_FILE_SIZE:
            st.error(f"❌ Job Description file is {jd_file.size / (1024*1024):.1f}MB. Maximum allowed is 5MB.")
            return
        
        with st.spinner("🔄 Analyzing documents..."):
            resume_text = extract_text(resume_file)
            jd_text = extract_text(jd_file)
            
            if not resume_text or not jd_text:
                st.error("❌ Failed to extract text. Please check your file format.")
                return
            
            match_score = calculate_match(resume_text, jd_text)
            resume_skills = extract_skills(resume_text)
            jd_skills = extract_skills(jd_text)
            missing_skills = list(set(jd_skills) - set(resume_skills))
        
        # Results
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Match Results")
        st.markdown(f'<div class="match-score">{match_score}%</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 1.3rem; opacity: 0.8; margin-bottom: 1.5rem;">Resume-JD Compatibility Score</p>', unsafe_allow_html=True)
        
        st.progress(match_score / 100)
        
        if match_score >= 75:
            st.success("✅ **Strong Match** — Candidate is highly qualified")
        elif match_score >= 50:
            st.warning("⚠️ **Moderate Match** — Partial requirements met")
        else:
            st.error("❌ **Weak Match** — Significant gaps detected")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Skills Analysis
        col_found, col_missing = st.columns(2)
        
        with col_found:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### ✅ Skills Found")
            if resume_skills:
                skills_html = "".join([f'<span class="skill-pill">{skill}</span>' for skill in resume_skills])
                st.markdown(skills_html, unsafe_allow_html=True)
            else:
                st.info("No common skills detected")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_missing:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### ❌ Missing Skills")
            if missing_skills:
                skills_html = "".join([f'<span class="skill-pill">{skill}</span>' for skill in missing_skills])
                st.markdown(skills_html, unsafe_allow_html=True)
            else:
                st.success("🎉 No skill gaps!")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Documentation Section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📚 Technical Documentation")
    
    doc_col1, doc_col2 = st.columns(2)
    
    with doc_col1:
        st.markdown("""
        <div class="doc-card">
            <div class="doc-title">🔬 How It Works</div>
            <div class="doc-desc">
                Aequitas uses <strong>TF-IDF vectorization</strong> and <strong>cosine similarity</strong> 
                to compare resumes against job descriptions. Text is extracted from PDF/DOCX files, 
                converted into numerical vectors, and similarity scores (0-100%) are calculated.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with doc_col2:
        st.markdown("""
        <div class="doc-card">
            <div class="doc-title">🛠️ Technology Stack</div>
            <div class="doc-desc">
                <strong>Frontend:</strong> Streamlit<br>
                <strong>ML Engine:</strong> Scikit-learn<br>
                <strong>Text Processing:</strong> PDFMiner, docx2txt<br>
                <strong>Deployment:</strong> Streamlit Community Cloud
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Theme Toggle
    theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    theme_text = "Dark Mode" if st.session_state.theme == 'light' else "Light Mode"
    
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("🔄", key="theme_btn", help="Toggle theme"):
            toggle_theme()
            st.rerun()
    
    st.markdown(f"""
    <div class="theme-toggle" onclick="document.querySelector('[data-testid=baseButton-secondary]').click()">
        {theme_icon} {theme_text}
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-credits">
            <strong>Lead Architect:</strong> Devansh Thakur &nbsp;|&nbsp; 
            <strong>Co-Developer:</strong> Arpit Upadhyay<br>
            <strong>Project Guide:</strong> [Your Guide Name Here]
        </div>
        
        <div style="margin: 1.5rem 0;">
            <a href="https://github.com/thisisdvnsh-thkr/Aequitas_Resume-Parser" target="_blank" class="footer-link">📂 GitHub Repository</a>
            <a href="https://linkedin.com/in/devansh-thakur" target="_blank" class="footer-link">💼 LinkedIn</a>
        </div>
        
        <div class="footer-meta">
            Aequitas v2.0 © 2024 | Built with Streamlit & Python<br>
            Powered by TF-IDF & Cosine Similarity Algorithm
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
