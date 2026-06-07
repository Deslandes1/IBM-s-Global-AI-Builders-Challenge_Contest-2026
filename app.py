import streamlit as st
import re
from groq import Groq

# ================== CONFIGURATION ==================
st.set_page_config(
    page_title="Pathfinder AI | GlobalInternet.py",
    page_icon="🧭",
    layout="wide"
)

# Language texts
TEXTS = {
    "English": {
        "title": "🧭 Pathfinder AI – Intelligent Career Guidance",
        "subtitle": "Discover your ideal career path with AI‑powered advice",
        "video_tab": "🎬 Video Introduction",
        "ai_tab": "🤖 AI Career Coach",
        "video_title": "Watch the full introduction video",
        "video_desc": "This video explains how Pathfinder AI helps you find the right career.",
        "question_title": "Tell us about yourself",
        "skills_label": "What are your top skills or interests? (e.g., programming, healthcare, teaching, design, business)",
        "experience_label": "What is your current education or experience level? (e.g., high school, university, self‑taught, professional)",
        "goals_label": "What are your career goals? (e.g., find a stable job, start a business, get a certification)",
        "submit_button": "Get AI Career Advice",
        "thinking": "AI is analyzing your profile and generating recommendations...",
        "response_title": "🧠 Your Personalized Career Plan",
        "error_fallback": "AI service temporarily unavailable. Please try again later.",
        "sidebar_howto": "How to use",
        "howto_list": ["Watch the video intro", "Answer the questions", "Get AI‑powered career advice", "Explore recommended resources"],
        "footer": "© 2026 GlobalInternet.py – Powered by Groq AI",
        "security_badge": "🔐 End‑to‑end encryption active",
        "security_caption": "All data is secured and anonymized",
        "price_title": "Our Services",
        "price_list": [
            "Full source code – $499 USD",
            "Source + customization – $1,499 USD",
            "Enterprise plan – $2,999 USD"
        ]
    },
    "Français": {
        "title": "🧭 Pathfinder AI – Orientation professionnelle intelligente",
        "subtitle": "Découvrez votre parcours idéal avec des conseils IA",
        "video_tab": "🎬 Introduction vidéo",
        "ai_tab": "🤖 Coach IA carrière",
        "video_title": "Regardez la vidéo d'introduction complète",
        "video_desc": "Cette vidéo explique comment Pathfinder AI vous aide à trouver la bonne carrière.",
        "question_title": "Parlez‑nous de vous",
        "skills_label": "Quelles sont vos principales compétences ou centres d'intérêt ? (ex. programmation, santé, enseignement, design, affaires)",
        "experience_label": "Quel est votre niveau d'éducation ou d'expérience actuel ? (ex. lycée, université, autodidacte, professionnel)",
        "goals_label": "Quels sont vos objectifs de carrière ? (ex. trouver un emploi stable, créer une entreprise, obtenir une certification)",
        "submit_button": "Obtenir des conseils IA",
        "thinking": "L'IA analyse votre profil et génère des recommandations...",
        "response_title": "🧠 Votre plan de carrière personnalisé",
        "error_fallback": "Service IA temporairement indisponible. Veuillez réessayer plus tard.",
        "sidebar_howto": "Comment utiliser",
        "howto_list": ["Regardez l'intro vidéo", "Répondez aux questions", "Obtenez des conseils IA", "Explorez les ressources recommandées"],
        "footer": "© 2026 GlobalInternet.py – Propulsé par Groq AI",
        "security_badge": "🔐 Chiffrement de bout en bout actif",
        "security_caption": "Toutes les données sont sécurisées et anonymisées",
        "price_title": "Nos services",
        "price_list": [
            "Code source complet – 499 USD",
            "Code + personnalisation – 1 499 USD",
            "Formule Entreprise – 2 999 USD"
        ]
    },
    "Español": {
        "title": "🧭 Pathfinder AI – Orientación profesional inteligente",
        "subtitle": "Descubre tu camino ideal con asesoría IA",
        "video_tab": "🎬 Introducción en video",
        "ai_tab": "🤖 Coach IA de carrera",
        "video_title": "Vea el video de introducción completo",
        "video_desc": "Este video explica cómo Pathfinder AI te ayuda a encontrar la carrera correcta.",
        "question_title": "Cuéntanos sobre ti",
        "skills_label": "¿Cuáles son tus principales habilidades o intereses? (ej. programación, salud, enseñanza, diseño, negocios)",
        "experience_label": "¿Cuál es tu nivel actual de educación o experiencia? (ej. secundaria, universidad, autodidacta, profesional)",
        "goals_label": "¿Cuáles son tus metas profesionales? (ej. encontrar un trabajo estable, iniciar un negocio, obtener una certificación)",
        "submit_button": "Obtener asesoría IA",
        "thinking": "La IA está analizando tu perfil y generando recomendaciones...",
        "response_title": "🧠 Tu plan de carrera personalizado",
        "error_fallback": "Servicio IA temporalmente no disponible. Inténtalo de nuevo más tarde.",
        "sidebar_howto": "Cómo usar",
        "howto_list": ["Vea la introducción en video", "Responda las preguntas", "Obtenga asesoría IA", "Explore los recursos recomendados"],
        "footer": "© 2026 GlobalInternet.py – Desarrollado con Groq AI",
        "security_badge": "🔐 Cifrado de extremo a extremo activo",
        "security_caption": "Todos los datos están seguros y anonimizados",
        "price_title": "Nuestros servicios",
        "price_list": [
            "Código fuente completo – $499 USD",
            "Código + personalización – $1,499 USD",
            "Plan Empresarial – $2,999 USD"
        ]
    }
}

# ================== CUSTOM CSS ==================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a192f 0%, #112240 100%); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f2a48 0%, #0a192f 100%);
        border-right: 2px solid #e94560;
    }
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stCaption { color: #ffffff !important; }
    [data-testid="stSidebar"] .stSelectbox label {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 1rem !important;
    }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    div[data-baseweb="select"] ul { background-color: #1f2a48 !important; }
    div[data-baseweb="select"] ul li {
        color: #ffffff !important;
        font-weight: bold !important;
        background-color: #1f2a48 !important;
    }
    div[data-baseweb="select"] ul li:hover { background-color: #e94560 !important; }
    h1, h2, h3 { color: #ffd966 !important; }
    p, li, .stMarkdown { color: #ffffff !important; }
    .stButton>button {
        background-color: #e94560 !important;
        color: white !important;
        border-radius: 30px !important;
        font-weight: bold !important;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #ff6b6b !important;
        transform: scale(1.02);
    }
    .security-badge {
        background: #0a192f;
        border: 1px solid #00ebc7;
        border-radius: 30px;
        padding: 8px 15px;
        margin: 10px 0;
        text-align: center;
        color: #00ebc7;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ================== SIDEBAR ==================
with st.sidebar:
    st.image("https://raw.githubusercontent.com/Deslandes1/Color-Software-Game/main/Gesner%20Deslandes.png", width=80)
    st.markdown("## **GlobalInternet.py**")
    st.markdown("**Pathfinder AI**")
    st.markdown("---")
    
    language = st.selectbox("🌐 Language / Idioma / Langue", ["English", "Français", "Español"])
    texts = TEXTS[language]
    
    st.markdown("---")
    st.markdown("### 🛡️ Global Security Shield active")
    st.markdown(f'<div class="security-badge">{texts["security_badge"]}</div>', unsafe_allow_html=True)
    st.caption(texts["security_caption"])
    
    st.markdown("---")
    st.markdown("Built by **Gesner Deslandes**, Engineer-in-Chief")
    st.markdown("📞 (509) 4738 5663")
    st.markdown("✉️ deslandes78@gmail.com")
    st.markdown("---")
    
    st.markdown(f"### 💰 {texts['price_title']}")
    for item in texts["price_list"]:
        st.markdown(f"- {item}")
    st.markdown("---")
    
    st.markdown(f"### {texts['sidebar_howto']}")
    for i, step in enumerate(texts["howto_list"], 1):
        st.markdown(f"{i}. {step}")

# ================== MAIN TITLE ==================
st.title(texts["title"])
st.markdown(f"### {texts['subtitle']}")
st.markdown("---")

# ================== GROQ CLIENT ==================
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ Missing Groq API key. Add `GROQ_API_KEY` to your Streamlit secrets.")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ================== AI FUNCTION (ONLY GROQ) ==================
def get_career_advice(skills, experience, goals, language):
    prompt = f"""You are an expert career counselor. Based on the following user information, provide a personalized career recommendation (3-5 sentences). Suggest specific job titles, skills to develop, and actionable steps. Respond in {language}.

Skills/Interests: {skills}
Education/Experience: {experience}
Career Goals: {goals}

Career Advice:"""
    
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return texts["error_fallback"] + f" ({str(e)})"

# ================== TABS ==================
tab1, tab2 = st.tabs([texts["video_tab"], texts["ai_tab"]])

# --- Tab 1: Video Introduction (UPDATED WITH YOUR LINK) ---
with tab1:
    st.markdown(f"### {texts['video_title']}")
    st.markdown(texts['video_desc'])
    # Your narrated Pathfinder AI video link (using dl=1 for direct streaming)
    video_link = "https://www.dropbox.com/scl/fi/w5c4hxj0gldttd7ks3vcq/Pathfinder.mp4?rlkey=bqx234mre5bj30fwydruu4pm6&st=q3qrenrn&dl=1"
    st.video(video_link)
    st.caption("If the video does not play, click the three dots → Download to save it locally.")

# --- Tab 2: AI Career Coach ---
with tab2:
    st.markdown(f"### {texts['question_title']}")
    with st.form("career_form"):
        skills = st.text_area(texts["skills_label"], height=80)
        experience = st.text_area(texts["experience_label"], height=80)
        goals = st.text_area(texts["goals_label"], height=80)
        submitted = st.form_submit_button(texts["submit_button"])
    
    if submitted:
        if not skills.strip() or not experience.strip() or not goals.strip():
            st.warning("Please fill in all fields.")
        else:
            with st.spinner(texts["thinking"]):
                advice = get_career_advice(skills, experience, goals, language)
            st.markdown(f"### {texts['response_title']}")
            st.markdown(advice)
            st.info("Powered by Groq AI")

# ================== FOOTER ==================
st.markdown("---")
st.markdown(texts["footer"])
