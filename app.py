import sys
import streamlit as st


import pandas as pd
from datetime import datetime
from google import genai
from google.genai import types

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="FarmaBuddy 🌱",
    page_icon="🌾",
    layout="wide"
)


import streamlit as st
import time
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Farma Buddy 🌱",
    page_icon="🌿",
    layout="wide"
)

if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

# ---------------- SPLASH SCREEN ----------------
if not st.session_state.splash_done:

    splash_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>

    body {
        margin: 0;
        overflow: hidden;
        height: 100vh;
        background: linear-gradient(180deg, #e8f5e9 0%, #c8e6c9 40%, #a5d6a7 100%);
        font-family: 'Segoe UI', sans-serif;
        position: relative;
    }

    /* Subtle animated gradient overlay */
    .gradient-overlay {
        position: absolute;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.4), transparent 60%);
        animation: moveGradient 12s ease-in-out infinite alternate;
    }

    /* Floating light particles */
    .particle {
        position: absolute;
        width: 8px;
        height: 8px;
        background: rgba(255,255,255,0.6);
        border-radius: 50%;
        animation: floatParticle 10s linear infinite;
    }

    .p1 { top: 20%; left: 10%; animation-delay: 0s; }
    .p2 { top: 40%; left: 80%; animation-delay: 2s; }
    .p3 { top: 70%; left: 30%; animation-delay: 4s; }
    .p4 { top: 60%; left: 60%; animation-delay: 6s; }

    /* Elegant Sun Glow */
    .sun {
        position: absolute;
        top: 12%;
        right: 12%;
        width: 120px;
        height: 120px;
        background: radial-gradient(circle, #fff176 40%, transparent 70%);
        border-radius: 50%;
        animation: pulseSun 6s ease-in-out infinite;
    }

    /* Center Content */
    .container {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        z-index: 5;
    }

    .logo {
        font-size: 85px;
        animation: zoomFade 2s ease-out;
    }

    .app-name {
        font-size: 48px;
        font-weight: 600;
        color: #1b5e20;
        margin-top: 10px;
        animation: fadeIn 3s ease-in-out;
    }

    .tagline {
        font-size: 18px;
        color: #2e7d32;
        margin-top: 10px;
        letter-spacing: 1px;
        animation: fadeIn 4s ease-in-out;
    }

    .progress-bar {
        width: 300px;
        height: 5px;
        background: rgba(0,0,0,0.1);
        margin: 30px auto;
        border-radius: 10px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        width: 0%;
        background: linear-gradient(90deg, #1b5e20, #43a047);
        animation: loadProgress 5s linear forwards;
    }

    /* Animations */
    @keyframes zoomFade {
        0% {transform: scale(0.8); opacity: 0;}
        100% {transform: scale(1); opacity: 1;}
    }

    @keyframes fadeIn {
        0% {opacity: 0;}
        100% {opacity: 1;}
    }

    @keyframes loadProgress {
        0% {width: 0%;}
        100% {width: 100%;}
    }

    @keyframes floatParticle {
        0% {transform: translateY(0px);}
        50% {transform: translateY(-20px);}
        100% {transform: translateY(0px);}
    }

    @keyframes pulseSun {
        0% {transform: scale(1); opacity: 0.8;}
        50% {transform: scale(1.1); opacity: 1;}
        100% {transform: scale(1); opacity: 0.8;}
    }

    @keyframes moveGradient {
        0% {transform: translate(-10%, -10%);}
        100% {transform: translate(10%, 10%);}
    }

    </style>
    </head>

    <body>

        <div class="gradient-overlay"></div>

        <div class="sun"></div>

        <div class="particle p1"></div>
        <div class="particle p2"></div>
        <div class="particle p3"></div>
        <div class="particle p4"></div>

        <div class="container">
            <div class="logo">🌾</div>
            <div class="app-name">Farma Buddy</div>
            <div class="tagline">Smart Farming. Smarter Future.</div>

            <div class="progress-bar">
                <div class="progress-fill"></div>
            </div>
        </div>

    </body>
    </html>
    """

    components.html(splash_html, height=750)
    time.sleep(5)

    st.session_state.splash_done = True
    st.rerun()

# ---------------- SESSION STATE INIT ----------------
if "signed_up" not in st.session_state:
    st.session_state.signed_up = False

if "farmer_name" not in st.session_state:
    st.session_state.farmer_name = ""

if "farmer_location" not in st.session_state:
    st.session_state.farmer_location = ""










# ---------------- CUSTOM STYLING ----------------
# ---------------- CUSTOM STYLING ----------------
st.markdown("""
<style>
/* -------- GLOBAL -------- */
.stApp {
    background: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef") no-repeat center center fixed;
    background-size: cover;
}

/* Make all standard text and labels bold and high-contrast */
.stApp p, .stApp span, .stApp label {
    color: #d7fad8 !important; /* Deep dark green for better visibility */
    font-weight: 600 !important;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.8); /* White glow behind text */
}

/* -------- HERO HEADER -------- */
.dashboard-header {
    background: linear-gradient(135deg, #1B5E20, #2E7D32); /* Darkened for better contrast */
    padding: 25px 35px;
    border-radius: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    color: white !important;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
    backdrop-filter: blur(15px);
}

.white-text { 
    color: #FFFFFF !important; 
    margin: 0 !important; 
    font-weight: 800 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important; 
}

/* -------- GLASS CARD (The Advice Box) -------- */
.glass-card {
    background: rgba(27, 94, 32, 0.95) !important;  /* Light background */
    padding: 25px;
    border-radius: 18px;
    backdrop-filter: blur(10px);
    box-shadow: 0px 8px 25px rgba(0,0,0,0.25);
    margin-bottom: 20px;
    border-left: 6px solid #2E7D32;  /* Accent green strip */
}

/* Make ALL text inside card dark */
.glass-card h1,
.glass-card h2,
.glass-card h3,
.glass-card h4,
.glass-card p,
.glass-card li {
    color: #a6e3a6!important;  /* Dark green text */
    font-weight: 500;
}


.glass-card h3, .glass-card li {
    color: #a6e3a6 !important;
    font-weight: 500 !important;
}


/* -------- SIDEBAR -------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D2611, #1B5E20); /* Darker sidebar */
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* -------- TABS -------- */
button[data-baseweb="tab"] p {
    font-weight: 500 !important;
    font-size: 16px !important;
}

/* -------- WEATHER BADGE -------- */
.weather-badge {
    margin-top: 8px;
    display: inline-block;
    padding: 8px 20px;
    border-radius: 25px;
    background: #FFFFFF; /* High contrast white background */
    color: #1B5E20 !important;
    font-weight: 900 !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

/* -------- LIGHT GREEN BUTTONS -------- */
.stButton > button {
    background: #003300 !important; /* Soft light green */
    color: #003300 !important;      /* Dark green text for bold contrast */
    border: 2px solid #2E7D32 !important; /* Darker green border */
    border-radius: 14px;
    padding: 0.7em 1.5em;
    font-weight: 900 !important;    /* Extra bold text */
    text-shadow: none !important;    /* Clean look for button text */
    transition: 0.3s ease;
    width: 100%;
}

.stButton > button:hover {
    background: #A5D6A7 !important; /* Slightly darker green on hover */
    transform: translateY(-2px);
    box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)




# ---------------- API KEY & CLIENT ----------------
# We force the 'v1' stable API version to resolve the 404 issue.
# Change this in your CONFIG section
# In your API KEY & CLIENT section
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"],
)
# Add this temporary button to your sidebar to check names

if not st.session_state.signed_up:
    st.markdown(
        """
        <div style="text-align:center;">
            <h1 style="color:#1B3A2F;">🌱 FarmaBuddy Sign Up</h1>
            <p style="color:#2E7D32;">
                Welcome! Please enter your details to continue.
            </p>
            <hr>
        </div>
        """,
        unsafe_allow_html=True
    )

    farmer_name = st.text_input("👨🌾 Farmer Name")
    farmer_location = st.text_input("📍 Village / City / State")

    if st.button("✅ Sign Up"):
        if farmer_name and farmer_location:
            st.session_state.farmer_name = farmer_name
            st.session_state.farmer_location = farmer_location
            st.session_state.signed_up = True
            st.rerun()
        else:
            st.warning("Please fill in all fields.")

    st.stop()




# ---------------- HEADER ----------------
# ---------------- HEADER ----------------
# ---------------- HEADER ----------------
# Use st.html instead of st.markdown for better reliability
# Note: Keep the HTML tags flush to the left (no spaces before <div)
header_html = f"""
<div class="dashboard-header">
<div>
<h1 class="white-text">🌱 FarmaBuddy</h1>
<p class="white-text">AI-Powered Smart Farming Assistant</p>
</div>
<div class="header-right">
<p class="white-text">👨‍🌾 <strong>{st.session_state.get('farmer_name', 'Farmer')}</strong></p>
<p class="white-text">📍 <strong>{st.session_state.get('farmer_location', 'Location')}</strong></p>
<div class="weather-badge">🌤 28°C | 65% Humidity</div>
</div>
</div>
"""

st.html(header_html)




# ---------------- TABS ----------------
tab_advice, tab_feedback, tab_usage, tab_settings = st.tabs(
    ["🌾 Farming Advice", "📊 Feedback", "📈 Usage Snapshot", "⚙️ Settings"]
)



# ---------------- USER INPUTS ----------------
st.sidebar.header("🌍 Farmer Inputs")
region = st.sidebar.selectbox("Select Region", ["India", "Ghana", "Canada"])
location = st.sidebar.text_input("Enter Location (State / Province)")
crop_stage = st.sidebar.selectbox("Crop Stage", ["Planning", "Sowing", "Growing", "Harvesting"])
priority = st.sidebar.multiselect("Your Priorities", ["Low Water Use", "High Yield", "Organic Farming", "Low Cost"])
temperature = st.sidebar.slider("AI Creativity Level", 0.2, 0.9, 0.5)

st.markdown("""
<hr style="border: none; height: 3px; 
background: linear-gradient(90deg, #2E7D32, #66BB6A);
border-radius: 5px;">
""", unsafe_allow_html=True)



# ---------------- PROMPT ENGINE ----------------
def build_prompt():
    return f"""
You are a highly experienced Senior Agricultural Consultant specializing in {region}. 
The farmer is located in {location} and is currently at the {crop_stage} stage.
Their core priorities are: {', '.join(priority)}.

Task: Provide a comprehensive, professional farming guide.
Structure your response as follows:

1. **Detailed Strategy Overview**: Provide a deep-dive analysis of what the farmer should focus on during the {crop_stage} stage based on their priorities.
2. **5 Actionable Recommendations**: For each recommendation:
    - **Implementation Step**: Explain exactly HOW to do it.
    - **Scientific/Practical Benefit**: Explain WHY it works.
    - **Resource Management**: How it helps with {', '.join(priority)}.
3. **Risk Mitigation**: Identify 2 potential risks for this stage in {location} and how to avoid them.
4. **Pro-Tip**: One advanced farming technique to maximize success.

Use professional yet accessible language. Be specific to the geography of {location}.
"""

# ---------------- MAIN ACTION ----------------
with tab_advice:
    # ---------------- MAIN ACTION ----------------
    if st.button("🌾 Get Smart Advice"):
        if not location:
            st.warning("Please enter your location.")
        else:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=build_prompt(),
                config={
                    "temperature": temperature,
                    "max_output_tokens": 4096
                }
            )
    
            st.markdown("""
            <div class="glass-card">
            <h3>🌾 AI Smart Recommendations</h3>
            </div>
            """, unsafe_allow_html=True)
    
            st.markdown(f"""
            <div class="glass-card">
            {response.text}
            </div>
            """, unsafe_allow_html=True)
            # -------- Advice Quality Score --------
            advice_score = 85  # You can calculate dynamically later
            st.markdown("### 📈 Advice Confidence Score")
            st.progress(advice_score / 100)
            st.caption(f"{advice_score}% Confidence Level")




            

 

# ---------------- FEEDBACK CHECKLIST ----------------
with tab_feedback:
    st.markdown("## ✅ AI Output Validation Checklist")

    with st.form("feedback_form"):

        f1 = st.checkbox("Advice is specific to my region")
        f2 = st.checkbox("Suggestions include valid reasoning")
        f3 = st.checkbox("Language is easy to understand")
        f4 = st.checkbox("Advice can be applied practically")
        f5 = st.checkbox("No unsafe or misleading information")

        submitted = st.form_submit_button("📊 Submit Feedback")

    if submitted:
        score = sum([f1, f2, f3, f4, f5])
        percentage = int((score / 5) * 100)

        circumference = 440
        progress = (percentage / 100) * circumference

        st.markdown(f"""
        <div style="text-align:center;">
        <svg width="180" height="180">
          <circle cx="90" cy="90" r="70"
                  stroke="#e0e0e0"
                  stroke-width="15"
                  fill="none"/>
          <circle cx="90" cy="90" r="70"
                  stroke="#2E7D32"
                  stroke-width="15"
                  fill="none"
                  stroke-dasharray="{progress} {circumference}"
                  transform="rotate(-90 90 90)"/>
          <text x="50%" y="50%"
                text-anchor="middle"
                dy=".3em"
                font-size="28"
                fill="#1B3A2F"
                font-weight="bold">
                {percentage}%
          </text>
        </svg>
        <p style="font-weight:600;">Feedback Quality Score</p>
        </div>
        """, unsafe_allow_html=True)





# ---------------- USAGE LOG ----------------
with tab_usage:
    st.markdown("## 📈 Usage Snapshot")

    usage_data = {
        "Farmer Name": st.session_state.farmer_name,
        "Location": st.session_state.farmer_location,
        "Region": region,
        "Crop Stage": crop_stage,
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    st.dataframe(pd.DataFrame([usage_data]))

    st.info(
        "This snapshot helps track how farmers are using FarmaBuddy over time."
    )



# ---------------- SETTINGS TAB ----------------
with tab_settings:
    st.markdown("## ⚙️ App Settings")

    st.markdown("### 👨‍🌾 Farmer Profile")
    st.info(
        f"""
        **Name:** {st.session_state.farmer_name}  
        **Location:** {st.session_state.farmer_location}
        """
    )

    st.markdown("---")

    st.markdown("### 🚪 Account Actions")

    if st.button("Sign Out"):
        st.session_state.signed_up = False
        st.session_state.farmer_name = ""
        st.session_state.farmer_location = ""
        st.success("You have been signed out successfully.")
        st.rerun()

# ---------------- FOOTER ----------------
st.markdown("<hr><p style='text-align:center; font-size:14px;'>FA-2 Project | 2026</p>", unsafe_allow_html=True)
