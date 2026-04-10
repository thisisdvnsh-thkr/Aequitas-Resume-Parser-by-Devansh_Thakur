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

# ==================== SESSION STATE ====================
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# ==================== CSS ====================
def get_css():
    is_dark = st.session_state.theme == 'dark'

    if is_dark:
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* App Background */
        .stApp {
            background: #080c14;
            background-image:
                radial-gradient(ellipse at 10% 10%, rgba(0,212,255,0.12) 0%, transparent 50%),
                radial-gradient(ellipse at 90% 90%, rgba(120,40,200,0.12) 0%, transparent 50%);
        }

        /* Hide sidebar */
        [data-testid="stSidebar"] { display: none !important; }

        /* Hide Streamlit chrome */
        #MainMenu, footer, header { visibility: hidden !important; }

        /* Remove top padding */
        .main .block-container {
            padding-top: 2rem;
            padding-left: 4rem;
            padding-right: 4rem;
            max-width: 1300px;
        }

        /* ===== HEADER ===== */
        .aequitas-header {
            text-align: center;
            padding: 3.5rem 0 0.5rem;
        }

        .aequitas-title {
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(120deg, #00d4ff, #7928ca);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -2px;
            margin: 0;
        }

        .aequitas-subtitle {
            font-size: 1.15rem;
            color: #8899aa;
            margin-top: 0.5rem;
            letter-spacing: 1px;
            font-weight: 400;
        }

        /* ===== FEATURE CARDS ===== */
        .features-row {
            display: flex;
            gap: 1.5rem;
            margin: 2.5rem 0;
        }

        .feature-card {
            flex: 1;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 1.8rem;
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }

        .feature-card:hover {
            background: rgba(0,212,255,0.07);
            border-color: rgba(0,212,255,0.3);
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(0,212,255,0.1);
        }

        .feature-icon {
            font-size: 2rem;
            line-height: 1;
            flex-shrink: 0;
        }

        .feature-content h4 {
            color: #ffffff;
            font-size: 1rem;
            font-weight: 600;
            margin: 0 0 0.4rem;
        }

        .feature-content p {
            color: #7788aa;
            font-size: 0.85rem;
            margin: 0;
            line-height: 1.5;
        }

        /* ===== UPLOAD SECTION ===== */
        .upload-section {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 24px;
            padding: 2.5rem;
            margin: 1rem 0;
            backdrop-filter: blur(10px);
        }

        .upload-section-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .upload-label {
            font-size: 0.95rem;
            font-weight: 600;
            color: #aabbcc;
            margin-bottom: 0.6rem;
            display: block;
        }

        /* ===== FORCE HIDE 200MB - AGGRESSIVE ===== */
        [data-testid="stFileUploaderDropzoneInput"] + div,
        [data-testid="stFileUploader"] > div > div > div > small,
        [data-testid="stFileUploader"] small,
        .uploadedFileName + small,
        section[data-testid="stFileUploader"] small,
        div[data-testid="stFileDropzone"] small,
        div[data-testid="stFileDropzone"] span:last-child {
            display: none !important;
            visibility: hidden !important;
        }

        /* Restyle the uploader dropzone */
        div[data-testid="stFileDropzone"] {
            border: 2px dashed rgba(0,212,255,0.3) !important;
            border-radius: 14px !important;
            background: rgba(0,212,255,0.03) !important;
            transition: all 0.3s ease !important;
        }

        div[data-testid="stFileDropzone"]:hover {
            border-color: rgba(0,212,255,0.7) !important;
            background: rgba(0,212,255,0.07) !important;
        }

        div[data-testid="stFileDropzone"] button {
            background: linear-gradient(135deg, #00d4ff, #7928ca) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.5rem !important;
        }

        /* File size label replacement */
        .file-size-label {
            font-size: 0.78rem;
            color: #556677;
            margin-top: 0.4rem;
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }

        /* ===== RESULTS ===== */
        .results-container {
            background: linear-gradient(135deg, rgba(0,212,255,0.08), rgba(120,40,200,0.08));
            border: 1px solid rgba(0,212,255,0.2);
            border-radius: 24px;
            padding: 3rem 2.5rem;
            margin: 2rem 0;
            text-align: center;
        }

        .score-display {
            font-size: 6rem;
            font-weight: 800;
            background: linear-gradient(120deg, #00d4ff, #7928ca);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1;
            letter-spacing: -4px;
        }

        .score-label {
            font-size: 1rem;
            color: #7788aa;
            margin-top: 0.5rem;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        /* ===== SKILL PILLS ===== */
        .skills-box {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 1.8rem;
            min-height: 150px;
        }

        .skills-box h4 {
            font-size: 1rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 1rem;
        }

        .skill-tag {
            display: inline-block;
            background: rgba(0,212,255,0.12);
            color: #00d4ff;
            border: 1px solid rgba(0,212,255,0.25);
            border-radius: 20px;
            padding: 0.4rem 1rem;
            margin: 0.3rem;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }

        .skill-tag:hover {
            background: rgba(0,212,255,0.25);
            transform: scale(1.05);
        }

        .skill-tag.missing {
            background: rgba(255,80,80,0.12);
            color: #ff8080;
            border-color: rgba(255,80,80,0.25);
        }

        /* ===== DOCS SECTION ===== */
        .docs-section {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 24px;
            padding: 2.5rem;
            margin: 1.5rem 0;
        }

        .docs-section h3 {
            color: #ffffff;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
        }

        .doc-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }

        .doc-card:hover {
            border-color: rgba(0,212,255,0.3);
            transform: translateY(-3px);
        }

        .doc-card h4 {
            color: #00d4ff;
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0.8rem;
        }

        .doc-card p {
            color: #7788aa;
            font-size: 0.88rem;
            line-height: 1.7;
            margin: 0;
        }

        /* ===== FOOTER ===== */
        .site-footer {
            text-align: center;
            padding: 3rem 2rem 4rem;
            margin-top: 4rem;
            border-top: 1px solid rgba(255,255,255,0.08);
        }

        .footer-team {
            font-size: 0.95rem;
            color: #7788aa;
            margin-bottom: 1.2rem;
            line-height: 1.8;
        }

        .footer-team strong {
            color: #aabbcc;
        }

        .footer-links-row {
            margin: 1.2rem 0;
        }

        .footer-links-row a {
            color: #00d4ff;
            text-decoration: none;
            margin: 0 1rem;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }

        .footer-links-row a:hover {
            color: #7928ca;
        }

        .footer-copy {
            font-size: 0.8rem;
            color: #445566;
            margin-top: 1.2rem;
        }

        /* ===== THEME TOGGLE ===== */
        .toggle-wrap {
            position: fixed;
            bottom: 28px;
            right: 28px;
            z-index: 9999;
        }

        .toggle-wrap button {
            background: rgba(255,255,255,0.06) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            border-radius: 50px !important;
            color: #ffffff !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            padding: 0.6rem 1.4rem !important;
            backdrop-filter: blur(12px) !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
        }

        .toggle-wrap button:hover {
            border-color: rgba(0,212,255,0.5) !important;
            background: rgba(0,212,255,0.08) !important;
        }

        /* Progress bar */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #00d4ff, #7928ca);
            border-radius: 10px;
        }
        </style>
        """
    else:
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: #f0f4f8;
            background-image:
                radial-gradient(ellipse at 10% 10%, rgba(0,100,210,0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 90% 90%, rgba(120,40,200,0.06) 0%, transparent 50%);
        }

        [data-testid="stSidebar"] { display: none !important; }
        #MainMenu, footer, header { visibility: hidden !important; }

        .main .block-container {
            padding-top: 2rem;
            padding-left: 4rem;
            padding-right: 4rem;
            max-width: 1300px;
        }

        .aequitas-header { text-align: center; padding: 3.5rem 0 0.5rem; }

        .aequitas-title {
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(120deg, #0066cc, #7928ca);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -2px;
            margin: 0;
        }

        .aequitas-subtitle {
            font-size: 1.15rem;
            color: #6677aa;
            margin-top: 0.5rem;
            letter-spacing: 1px;
            font-weight: 400;
        }

        .features-row {
            display: flex;
            gap: 1.5rem;
            margin: 2.5rem 0;
        }

        .feature-card {
            flex: 1;
            background: rgba(255,255,255,0.9);
            border: 1px solid rgba(0,0,0,0.08);
            border-radius: 18px;
            padding: 1.8rem;
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 2px 16px rgba(0,0,0,0.06);
        }

        .feature-card:hover {
            border-color: rgba(0,102,204,0.3);
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(0,102,204,0.12);
        }

        .feature-icon { font-size: 2rem; line-height: 1; flex-shrink: 0; }

        .feature-content h4 {
            color: #1a1a2e;
            font-size: 1rem;
            font-weight: 600;
            margin: 0 0 0.4rem;
        }

        .feature-content p {
            color: #6677aa;
            font-size: 0.85rem;
            margin: 0;
            line-height: 1.5;
        }

        .upload-section {
            background: rgba(255,255,255,0.95);
            border: 1px solid rgba(0,0,0,0.08);
            border-radius: 24px;
            padding: 2.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 20px rgba(0,0,0,0.06);
        }

        .upload-section-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: #1a1a2e;
            margin-bottom: 2rem;
        }

        .upload-label {
            font-size: 0.95rem;
            font-weight: 600;
            color: #445577;
            margin-bottom: 0.6rem;
            display: block;
        }

        /* ===== FORCE HIDE 200MB ===== */
        [data-testid="stFileUploaderDropzoneInput"] + div,
        [data-testid="stFileUploader"] > div > div > div > small,
        [data-testid="stFileUploader"] small,
        section[data-testid="stFileUploader"] small,
        div[data-testid="stFileDropzone"] small,
        div[data-testid="stFileDropzone"] span:last-child {
            display: none !important;
            visibility: hidden !important;
        }

        div[data-testid="stFileDropzone"] {
            border: 2px dashed rgba(0,102,204,0.3) !important;
            border-radius: 14px !important;
            background: rgba(0,102,204,0.03) !important;
        }

        div[data-testid="stFileDropzone"]:hover {
            border-color: rgba(0,102,204,0.6) !important;
            background: rgba(0,102,204,0.06) !important;
        }

        div[data-testid="stFileDropzone"] button {
            background: linear-gradient(135deg, #0066cc, #7928ca) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }

        .file-size-label {
            font-size: 0.78rem;
            color: #99aabb;
            margin-top: 0.4rem;
        }

        .results-container {
            background: linear-gradient(135deg, rgba(0,102,204,0.06), rgba(120,40,200,0.06));
            border: 1px solid rgba(0,102,204,0.15);
            border-radius: 24px;
            padding: 3rem 2.5rem;
            margin: 2rem 0;
            text-align: center;
        }

        .score-display {
            font-size: 6rem;
            font-weight: 800;
            background: linear-gradient(120deg, #0066cc, #7928ca);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1;
            letter-spacing: -4px;
        }

        .score-label {
            font-size: 1rem;
            color: #6677aa;
            margin-top: 0.5rem;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .skills-box {
            background: rgba(255,255,255,0.95);
            border: 1px solid rgba(0,0,0,0.08);
            border-radius: 20px;
            padding: 1.8rem;
            min-height: 150px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        }

        .skills-box h4 { font-size: 1rem; font-weight: 600; color: #1a1a2e; margin-bottom: 1rem; }

        .skill-tag {
            display: inline-block;
            background: rgba(0,102,204,0.1);
            color: #0066cc;
            border: 1px solid rgba(0,102,204,0.2);
            border-radius: 20px;
            padding: 0.4rem 1rem;
            margin: 0.3rem;
            font-size: 0.85rem;
            font-weight: 500;
        }

        .skill-tag.missing {
            background: rgba(220,50,50,0.08);
            color: #cc3333;
            border-color: rgba(220,50,50,0.2);
        }

        .docs-section {
            background: rgba(255,255,255,0.95);
            border: 1px solid rgba(0,0,0,0.08);
            border-radius: 24px;
            padding: 2.5rem;
            margin: 1.5rem 0;
            box-shadow: 0 2px 20px rgba(0,0,0,0.06);
        }

        .docs-section h3 { color: #1a1a2e; font-size: 1.3rem; font-weight: 700; margin-bottom: 1.5rem; }

        .doc-card {
            background: rgba(0,102,204,0.04);
            border: 1px solid rgba(0,102,204,0.1);
            border-radius: 14px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }

        .doc-card:hover { border-color: rgba(0,102,204,0.3); transform: translateY(-3px); }

        .doc-card h4 { color: #0066cc; font-size: 1rem; font-weight: 600; margin-bottom: 0.8rem; }
        .doc-card p { color: #6677aa; font-size: 0.88rem; line-height: 1.7; margin: 0; }

        .site-footer {
            text-align: center;
            padding: 3rem 2rem 4rem;
            margin-top: 4rem;
            border-top: 1px solid rgba(0,0,0,0.08);
        }

        .footer-team { font-size: 0.95rem; color: #6677aa; margin-bottom: 1.2rem; line-height: 1.8; }
        .footer-team strong { color: #445577; }
        .footer-links-row { margin: 1.2rem 0; }
        .footer-links-row a { color: #0066cc; text-decoration: none; margin: 0 1rem; font-size: 0.9rem; font-weight: 500; }
        .footer-links-row a:hover { color: #7928ca; }
        .footer-copy { font-size: 0.8rem; color: #99aabb; margin-top: 1.2rem; }

        .toggle-wrap {
            position: fixed;
            bottom: 28px;
            right: 28px;
            z-index: 9999;
        }

        .toggle-wrap button {
            background: rgba(255,255,255,0.95) !important;
            border: 1px solid rgba(0,0,0,0.12) !important;
            border-radius: 50px !important;
            color: #1a1a2e !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            padding: 0.6rem 1.4rem !important;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1) !important;
        }

        .toggle-wrap button:hover {
            border-color: rgba(0,102,204,0.4) !important;
        }

        .stProgress > div > div > div {
            background: linear-gradient(90deg, #0066cc, #7928ca);
            border-radius: 10px;
        }
        </style>
        """

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
    elif "wordprocessingml" in file.type:
        return extract_text_from_docx(file)
    return ""

# ==================== SKILLS ====================
def extract_skills(text):
    skills = [
        'Python', 'Java', 'C++', 'JavaScript', 'SQL', 'R', 'Machine Learning',
        'Deep Learning', 'NLP', 'Data Science', 'TensorFlow', 'PyTorch', 'Keras',
        'Scikit-learn', 'Pandas', 'NumPy', 'Matplotlib', 'Power BI', 'Tableau',
        'Excel', 'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Git',
        'Flask', 'Django', 'React', 'Node.js', 'MongoDB', 'PostgreSQL', 'MySQL',
        'Data Analysis', 'Statistics', 'Computer Vision', 'Time Series',
        'ETL', 'Big Data', 'Spark', 'Hadoop', 'Linux', 'Bash', 'HTML', 'CSS'
    ]
    text_lower = text.lower()
    return [s for s in skills if s.lower() in text_lower]

# ==================== MATCH SCORE ====================
def calculate_match(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    vecs = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vecs[0:1], vecs[1:2])[0][0]
    return round(score * 100, 1)

# ==================== MAIN ====================
def main():
    # Inject CSS
    st.markdown(get_css(), unsafe_allow_html=True)

    # ── HEADER ──
    st.markdown("""
    <div class="aequitas-header">
        <h1 class="aequitas-title">⚖️ Aequitas: AI Resume Auditor</h1>
        <p class="aequitas-subtitle">Intelligent & Fair Resume Screening System</p>
    </div>
    """, unsafe_allow_html=True)

    # ── FEATURE CARDS ──
    st.markdown("""
    <div class="features-row">
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-content">
                <h4>Instant Match Calculation</h4>
                <p>Get precise resume-JD alignment scores powered by TF-IDF in seconds</p>
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <div class="feature-content">
                <h4>Fair & Unbiased Screening</h4>
                <p>AI-powered objective evaluation removing human bias from hiring</p>
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-content">
                <h4>Detailed Skill Gap Analysis</h4>
                <p>Identify exactly which qualifications are missing from a candidate</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── UPLOAD SECTION ──
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown('<div class="upload-section-title">📄 Upload Documents</div>', unsafe_allow_html=True)

    MAX_SIZE = 5 * 1024 * 1024  # 5MB

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<span class="upload-label">Candidate Resume</span>', unsafe_allow_html=True)
        resume_file = st.file_uploader(
            "resume_upload",
            type=['pdf', 'docx'],
            key='resume',
            label_visibility="collapsed"
        )
        st.markdown('<div class="file-size-label">📎 &nbsp;PDF or DOCX &nbsp;•&nbsp; Max 5MB</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<span class="upload-label">Job Description</span>', unsafe_allow_html=True)
        jd_file = st.file_uploader(
            "jd_upload",
            type=['pdf', 'docx'],
            key='jd',
            label_visibility="collapsed"
        )
        st.markdown('<div class="file-size-label">📎 &nbsp;PDF or DOCX &nbsp;•&nbsp; Max 5MB</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── ANALYSIS ──
    if resume_file and jd_file:
        if resume_file.size > MAX_SIZE:
            st.error(f"❌ Resume too large: {resume_file.size/(1024*1024):.1f}MB. Limit is 5MB.")
            return
        if jd_file.size > MAX_SIZE:
            st.error(f"❌ JD too large: {jd_file.size/(1024*1024):.1f}MB. Limit is 5MB.")
            return

        with st.spinner("Analyzing..."):
            r_text = extract_text(resume_file)
            j_text = extract_text(jd_file)

            if not r_text or not j_text:
                st.error("❌ Could not extract text. Please use a readable PDF or DOCX.")
                return

            score = calculate_match(r_text, j_text)
            r_skills = extract_skills(r_text)
            j_skills = extract_skills(j_text)
            missing = list(set(j_skills) - set(r_skills))

        # Score display
        if score >= 75:
            verdict = "✅ Strong Match"
            verdict_desc = "Candidate is highly aligned with this role"
        elif score >= 50:
            verdict = "⚠️ Moderate Match"
            verdict_desc = "Candidate meets several key requirements"
        else:
            verdict = "❌ Weak Match"
            verdict_desc = "Significant skill gaps detected"

        st.markdown(f"""
        <div class="results-container">
            <div class="score-display">{score}%</div>
            <div class="score-label">Resume — JD Compatibility Score</div>
            <div style="margin-top:1.5rem; font-size:1.2rem; font-weight:600;">{verdict}</div>
            <div style="color:#7788aa; font-size:0.9rem; margin-top:0.3rem;">{verdict_desc}</div>
        </div>
        """, unsafe_allow_html=True)

        st.progress(score / 100)

        # Skills
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="skills-box"><h4>✅ Skills Matched</h4>', unsafe_allow_html=True)
            if r_skills:
                pills = "".join([f'<span class="skill-tag">{s}</span>' for s in r_skills])
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:#7788aa;font-size:0.85rem;">No common skills detected</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="skills-box"><h4>❌ Skills Missing</h4>', unsafe_allow_html=True)
            if missing:
                pills = "".join([f'<span class="skill-tag missing">{s}</span>' for s in missing])
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:#00d4ff;font-size:0.85rem;">🎉 No skill gaps found!</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── DOCUMENTATION ──
    st.markdown('<div class="docs-section">', unsafe_allow_html=True)
    st.markdown('<h3>📚 Technical Documentation</h3>', unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)

    with d1:
        st.markdown("""
        <div class="doc-card">
            <h4>🔬 Algorithm</h4>
            <p>Uses <strong>TF-IDF vectorization</strong> to convert text into numerical vectors, then applies <strong>cosine similarity</strong> to measure alignment between resume and job description.</p>
        </div>
        """, unsafe_allow_html=True)

    with d2:
        st.markdown("""
        <div class="doc-card">
            <h4>🛠️ Tech Stack</h4>
            <p><strong>Frontend:</strong> Streamlit<br>
            <strong>ML Engine:</strong> Scikit-learn<br>
            <strong>PDF Parser:</strong> PDFMiner<br>
            <strong>DOCX Parser:</strong> docx2txt<br>
            <strong>Hosting:</strong> Streamlit Cloud</p>
        </div>
        """, unsafe_allow_html=True)

    with d3:
        st.markdown("""
        <div class="doc-card">
            <h4>📋 How to Use</h4>
            <p>1. Upload your <strong>Resume</strong> (PDF/DOCX)<br>
            2. Upload the <strong>Job Description</strong><br>
            3. View your <strong>match score</strong><br>
            4. Check <strong>skill gaps</strong> to improve<br>
            5. Reapply with a better resume!</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── FOOTER ──
    st.markdown("""
    <div class="site-footer">
        <div class="footer-team">
            <strong>Lead Architect:</strong> Devansh Thakur &nbsp;|&nbsp;
            <strong>Co-Developer:</strong> Arpit Upadhyay
        </div>
        <div class="footer-links-row">
            <a href="https://github.com/thisisdvnsh-thkr/Aequitas_Resume-Parser" target="_blank">📂 GitHub Repository</a>
            <a href="https://github.com/thisisdvnsh-thkr" target="_blank">👤 GitHub Profile</a>
            <a href="https://linkedin.com/in/devansh-thakur" target="_blank">💼 LinkedIn</a>
        </div>
        <div class="footer-copy">
            Aequitas v2.0 © 2026 &nbsp;|&nbsp; Built with Streamlit & Python &nbsp;|&nbsp;
            Powered by TF-IDF & Cosine Similarity
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── THEME TOGGLE ──
    icon = "☀️ Light Mode" if st.session_state.theme == 'dark' else "🌙 Dark Mode"

    st.markdown('<div class="toggle-wrap">', unsafe_allow_html=True)
    if st.button(icon, key="theme_btn"):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
