import streamlit as st
import docx2txt
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Page Config for a Modern Look
st.set_page_config(page_title="Aequitas | Resume Auditor", page_icon="⚖️", layout="wide")

# --- ACTIVE THEORY INSPIRED CSS ---
st.markdown("""
    <style>
    /* Full Page Background with 4K Texture */
    .stApp {
        background: radial-gradient(circle at center, #1a1a1a 0%, #000000 100%);
        background-attachment: fixed;
    }

    /* Cinematic Section Containers */
    .section {
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        scroll-snap-align: start;
        padding: 50px;
    }

    /* Typography: Large & Minimalist */
    .hero-title {
        font-size: 85px;
        font-weight: 800;
        letter-spacing: -3px;
        color: white;
        text-transform: uppercase;
        margin-bottom: 0px;
        background: -webkit-linear-gradient(#fff, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Glassmorphic Interaction Card */
    .interaction-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 40px;
        padding: 50px;
        width: 80%;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }

    /* Active Theory Styled Button */
    .stButton>button {
        background: transparent;
        color: white;
        border: 2px solid #00c7ff;
        padding: 15px 40px;
        border-radius: 0px; /* Sharp edges for high-end look */
        font-size: 18px;
        letter-spacing: 2px;
        transition: 0.5s all;
        width: 100%;
    }
    .stButton>button:hover {
        background: #00c7ff;
        color: black;
        box-shadow: 0 0 30px #00c7ff;
    }

    /* Hide UI Clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- ENGINE LOGIC ---
def extract_skills(text):
    skills = ['Python', 'Machine Learning', 'SQL', 'NLP', 'Data Science', 'Docker', 'AWS']
    text = text.lower()
    return [skill for skill in skills if skill.lower() in text]

# --- SECTION 1: HERO ---
st.markdown("""
    <div class="section">
        <h1 class="hero-title">Aequitas</h1>
        <p style='color: #00c7ff; letter-spacing: 10px; font-weight: 300; margin-top: -20px;'>RESUME AUDITOR</p>
        <div style='margin-top: 50px; color: grey;'>Scroll to Audit ⟱</div>
    </div>
""", unsafe_allow_html=True)

# --- SECTION 2: AUDIT ENGINE ---
st.markdown("<div id='engine' class='section'>", unsafe_allow_html=True)
st.markdown("<div class='interaction-card'>", unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    jd_file = st.file_uploader("TARGET: JOB DESCRIPTION", type=['pdf', 'docx'])
with col_b:
    res_file = st.file_uploader("SOURCE: CANDIDATE RESUME", type=['pdf', 'docx'])

audit_trigger = st.button("INITIATE AI AUDIT")
st.markdown("</div></div>", unsafe_allow_html=True)

# --- SECTION 3: INSIGHTS & SCORING ---
if audit_trigger:
    if res_file and jd_file:
        # Processing Logic (Simplified for brevity)
        res_text = extract_text(res_file) if res_file.name.endswith('.pdf') else docx2txt.process(res_file)
        jd_text = extract_text(jd_file) if jd_file.name.endswith('.pdf') else docx2txt.process(jd_file)
        
        cv = CountVectorizer()
        count_matrix = cv.fit_transform([res_text, jd_text])
        score = round(cosine_similarity(count_matrix)[0][1] * 100, 2)

        st.markdown("<div class='section'>", unsafe_allow_html=True)
        
        # Scoring Information Block
        st.markdown(f"""
            <div style='text-align: center; max-width: 800px;'>
                <h2 style='color: grey; font-size: 14px; letter-spacing: 5px;'>COMPATIBILITY INDEX</h2>
                <h1 style='font-size: 120px; color: white;'>{score}%</h1>
                <p style='color: rgba(255,255,255,0.6); line-height: 1.8;'>
                    <b>How this score is generated:</b> Aequitas utilizes <b>Vector Space Modeling</b>. 
                    Your documents are converted into multi-dimensional vectors using <i>Count Vectorization</i>. 
                    The final percentage represents the <b>Cosine Similarity</b>—calculating the angle between your 
                    skills and the job's demands to ensure an unbiased, mathematical match.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Matching Logic
        res_s = extract_skills(res_text)
        jd_s = extract_skills(jd_text)
        match = set(res_s).intersection(set(jd_s))
        
        st.markdown(f"""
            <div style='margin-top: 50px; border-top: 1px solid #333; padding-top: 30px;'>
                <p style='color: #00c7ff;'>AUDIT SUCCESSFUL: {len(match)} CORE COMPETENCIES VALIDATED</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)