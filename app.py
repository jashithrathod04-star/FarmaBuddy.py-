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
    st.session_state.page = "landing"
    st.rerun()




# ---------------- PAGE CONTROLLER ----------------
if "page" not in st.session_state:
    st.session_state.page = "landing"   # default first screen after splash

# ---------------- LANDING PAGE ----------------
if st.session_state.page == "landing":

    st.markdown("""
    <style>
    .hero {
        text-align: center;
        padding-top: 120px;
    }

    .headline {
        font-size: 52px;
        font-weight: 700;
        color: #1b5e20;
    }

    .subtext {
        font-size: 20px;
        color: #2e7d32;
        margin-top: 20px;
    }

    .stButton > button {
        background-color: #2e7d32;
        color: white;
        padding: 12px 28px;
        font-size: 18px;
        border-radius: 10px;
        border: none;
        transition: 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #1b5e20;
        transform: scale(1.05);
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="hero">', unsafe_allow_html=True)

    st.markdown('<div class="headline">AI-Powered Smart Farming</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtext">Optimize yield. Reduce waste. Make data-driven decisions.</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🌿 Get Started"):
            st.session_state.page = "persona"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
# ---------------- SESSION STATE INIT ----------------
if "signed_up" not in st.session_state:
    st.session_state.signed_up = False

if "farmer_name" not in st.session_state:
    st.session_state.farmer_name = ""

if "farmer_location" not in st.session_state:
    st.session_state.farmer_location = ""


# ---------------- CHAT SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


if "query_mode" not in st.session_state:
    st.session_state.query_mode = False


if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = False











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

# ---------------- PERSONA PAGE ----------------
# ---------------- PERSONA PAGE ----------------
if st.session_state.page == "persona":

    st.markdown(""" 
    <style>
    ...
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="persona-bg">', unsafe_allow_html=True)

    st.markdown('<div class="profile-img">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=140)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="persona-title">Create Your Farmer Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="persona-subtitle">Tell us about your farm</div>', unsafe_allow_html=True)

    name = st.text_input("👤 Name")
    age = st.text_input("🎂 Age")
    location = st.text_input("📍 Location")
    farm_size = st.text_input("🏡 Farm Size")
    crops = st.text_input("🌾 Crops")
    dairy = st.text_input("🐄 Dairy")

    if st.button("🚀 Continue to Dashboard"):

        if not name or not location:
            st.warning("Please fill in at least Name and Location.")
        else:
            # Save profile
            st.session_state.user_profile = {
                "name": name,
                "age": age,
                "location": location,
                "farm_size": farm_size,
                "crops": crops,
                "dairy": dairy
            }
    
            # Save dashboard header values
            st.session_state.farmer_name = name
            st.session_state.farmer_location = location
    
            st.session_state.page = "dashboard"
            st.rerun()









# ---------------- HEADER ----------------
# ---------------- HEADER ----------------
# ---------------- HEADER ----------------
# Use st.html instead of st.markdown for better reliability
# Note: Keep the HTML tags flush to the left (no spaces before <div)
elif st.session_state.page == "dashboard":

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
    
    


    # ---------------- QUERY MODE PAGE ----------------
    if st.session_state.query_mode:

        col_title, col_back = st.columns([6, 1])
    
        with col_title:
            st.markdown("## 💬 Ask FarmaBuddy AI")
    
        with col_back:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⬅ Dashboard"):
                st.session_state.query_mode = False
                st.rerun()
    
        st.info("Click a quick question or type your own below.")

    
        col1, col2 = st.columns(2)
    
        # Quick questions
        if col1.button("🌾 Best crop this season?"):
            st.session_state.chat_history.append(
                {"role": "user", "content": "What is the best crop to grow this season in my region?"}
            )
    
        if col2.button("💧 Improve soil fertility?"):
            st.session_state.chat_history.append(
                {"role": "user", "content": "How can I naturally improve soil fertility?"}
            )
    
        if col1.button("🐛 Natural pest control?"):
            st.session_state.chat_history.append(
                {"role": "user", "content": "What are effective natural pest control methods?"}
            )
    
        if col2.button("🌦 Protect crops from climate risks?"):
            st.session_state.chat_history.append(
                {"role": "user", "content": "How can I protect crops from extreme weather conditions?"}
            )
    
        st.markdown("---")
    
        # Show chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
        # Input box
        user_prompt = st.chat_input("Type your farming question...")
    
        if user_prompt:
            st.session_state.chat_history.append(
                {"role": "user", "content": user_prompt}
            )
    
        # Generate AI reply
        if st.session_state.chat_history:
            if st.session_state.chat_history[-1]["role"] == "user":
    
                conversation = [
                    {
                        "role": m["role"],
                        "parts": [{"text": m["content"]}]
                    }
                    for m in st.session_state.chat_history
                ]
    
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=conversation,
                    config={
                        "temperature": 0.6,
                        "max_output_tokens": 2048
                    }
                )
    
                ai_reply = response.text
    
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": ai_reply}
                )
                
                with st.chat_message("assistant"):
                    st.markdown(f"""
                    <div class="glass-card">
                        <h3>💬 AI Response</h3>
                        {ai_reply}
                    </div>
                    """, unsafe_allow_html=True)
    
        st.stop()

    
    # ---------------- TABS ----------------
    tab_advice, tab_feedback, tab_usage, tab_settings = st.tabs(
        ["🌾 Farming Advice", "📊 Feedback", "📈 Usage Snapshot", "⚙️ Settings"]
    )
    
    
    
    # ---------------- USER INPUTS ----------------
    
    
    st.markdown("""
    <hr style="border: none; height: 3px; 
    background: linear-gradient(90deg, #2E7D32, #66BB6A);
    border-radius: 5px;">
    """, unsafe_allow_html=True)

   
    

    with st.sidebar:
        st.markdown("### 📘 For more Information, double click below 👇")
    
        if st.button("💬 Query AI"):
            st.session_state.query_mode = True
            st.rerun()
    
    


    
    
    
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

        st.markdown("## 🌾 Farm Details")
    
        col1, col2 = st.columns(2)
    
        with col1:
            region = st.selectbox(
                "Select Region",
                ["North", "South", "East", "West"]
            )
    
            location = st.text_input("Enter Your Farm Location")
    
            crop_stage = st.selectbox(
                "Crop Growth Stage",
                ["Seedling", "Vegetative", "Flowering", "Harvesting"]
            )
    
        with col2:
            priority = st.multiselect(
                "Your Priority",
                ["Increase Yield", "Pest Control", "Save Water", "Improve Soil"]
            )
    
            temperature = st.slider(
                "AI Creativity Level",
                0.0, 1.0, 0.7
            )
    
        st.markdown("---")
    
        if st.button("🌾 Get Smart Advice"):
    
            if not location:
                st.warning("Please enter your details.")
    
            else:
                # 1️⃣ Place loader here
                loading_placeholder = st.empty()  # Placeholder for loader
        
                loading_placeholder.markdown("""
                <div class="glass-card" style="text-align:center;">
                    <h3>🌾 AI is generating your smart advice...</h3>
                    <div class="loader">
                        <div></div><div></div><div></div>
                    </div>
                </div>
        
                <style>
                .loader { display: flex; justify-content: center; margin-top: 15px; }
                .loader div { width: 12px; height: 12px; margin: 0 5px; background: #43a047; border-radius: 50%; animation: bounce 1.2s infinite ease-in-out; }
                .loader div:nth-child(1) { animation-delay: 0s; }
                .loader div:nth-child(2) { animation-delay: 0.2s; }
                .loader div:nth-child(3) { animation-delay: 0.4s; }
                @keyframes bounce { 0%,80%,100% { transform: scale(0); } 40% { transform: scale(1); } }
                </style>
                """, unsafe_allow_html=True)
        
                # 2️⃣ Call the API
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=build_prompt(),
                    config={"temperature": temperature, "max_output_tokens": 4096}
                )
        
                # 3️⃣ Replace loader with AI response
                loading_placeholder.markdown(f"""
                <div class="glass-card">
                    <h3>🌾 AI Smart Recommendations</h3>
                    {response.text}
                </div>
                """, unsafe_allow_html=True)
    
                advice_score = 85
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
            st.session_state.page = "landing"
            st.success("You have been signed out successfully.")
            st.rerun()

    # ---------------- CHATBOT INTERFACE ----------------
    if st.session_state.chat_mode:
    
        st.markdown("## 💬 FarmaBuddy AI Chatbot")
    
        # Show previous messages
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
        # Chat input box
        user_prompt = st.chat_input("Ask me anything about farming...")
    
        if user_prompt:
    
            # Save user message
            st.session_state.chat_history.append(
                {"role": "user", "content": user_prompt}
            )
    
            with st.chat_message("user"):
                st.markdown(user_prompt)
    
            # Build full conversation for Gemini
            conversation = [
                {
                    "role": m["role"],
                    "parts": [{"text": m["content"]}]
                }
                for m in st.session_state.chat_history
            ]
    
            # Get Gemini response
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=conversation,
                config={
                    "temperature": 0.6,
                    "max_output_tokens": 2048
                }
            )
    
            ai_reply = response.text
    
            # Save AI message
            st.session_state.chat_history.append(
                {"role": "assistant", "content": ai_reply}
            )
    
            with st.chat_message("assistant"):
                st.markdown(ai_reply)

    # ---------------- FOOTER ----------------
    st.markdown("<hr><p style='text-align:center; font-size:14px;'>FA-2 Project | 2026</p>", unsafe_allow_html=True)
