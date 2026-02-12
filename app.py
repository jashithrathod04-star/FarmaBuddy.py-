import sys
import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai
from google.genai import types


# ---------------- SESSION STATE INIT ----------------
if "signed_up" not in st.session_state:
    st.session_state.signed_up = False

if "farmer_name" not in st.session_state:
    st.session_state.farmer_name = ""

if "farmer_location" not in st.session_state:
    st.session_state.farmer_location = ""






# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="FarmaBuddy 🌱",
    page_icon="🌾",
    layout="wide"
)



# ---------------- CUSTOM STYLING ----------------
# ---------------- CUSTOM STYLING ----------------
st.markdown("""
<style>

/* -------- GLOBAL -------- */
.stApp {
    background: linear-gradient(180deg, #f8faf6 0%, #eef6ec 100%);
    color: #1B3A2F;
    font-family: 'Segoe UI', sans-serif;
}

/* -------- SIDEBAR -------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1B5E20, #2E7D32);
    color: white;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* -------- HERO HEADER -------- */
.dashboard-header {
    background: linear-gradient(135deg, #2E7D32, #66BB6A);
    padding: 25px 35px;
    border-radius: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    color: white;
    box-shadow: 0px 10px 30px rgba(46,125,50,0.25);
    backdrop-filter: blur(10px);
}

/* -------- TABS -------- */
button[data-baseweb="tab"] {
    font-weight: 600;
    color: #2E7D32;
    background-color: #ffffff;
    border-radius: 10px;
    padding: 6px 16px;
    margin-right: 8px;
    transition: 0.3s ease;
}

button[data-baseweb="tab"]:hover {
    background-color: #e8f5e9;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(90deg, #2E7D32, #66BB6A);
    color: white;
}

/* -------- BUTTONS -------- */
.stButton > button {
    background: linear-gradient(90deg, #2E7D32, #66BB6A);
    color: white;
    border-radius: 14px;
    padding: 0.7em 1.5em;
    font-weight: 600;
    border: none;
    box-shadow: 0px 4px 15px rgba(46,125,50,0.3);
    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0px 8px 25px rgba(46,125,50,0.4);
}

/* -------- GLASS CARD -------- */
.glass-card {
    background: rgba(255,255,255,0.7);
    padding: 20px;
    border-radius: 18px;
    backdrop-filter: blur(8px);
    box-shadow: 0px 6px 20px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

/* -------- INPUT LABELS -------- */
label {
    color: #1B3A2F !important;
    font-weight: 600;
}

/* -------- CHECKBOX -------- */
div[data-testid="stCheckbox"] label p {
    color: #1B3A2F !important;
}

/* -------- DATAFRAME -------- */
.stDataFrame {
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.05);
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
# ---------------- DASHBOARD HEADER ----------------
st.markdown(f"""
<div class="dashboard-header">
    <div class="dashboard-left">
        <span class="dashboard-icon">🌱</span>
        <div>
            <h1>FarmaBuddy</h1>
            <p>AI-Powered Smart Farming Assistant</p>
        </div>
    </div>
    <div class="dashboard-right">
        <p>👨🌾 Farmer: <strong>{st.session_state.farmer_name}</strong></p>
        <p>📍 Location: <strong>{st.session_state.farmer_location}</strong></p>
    </div>
</div>
""", unsafe_allow_html=True)




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


col1, col2, col3 = st.columns(3)

col1.metric("Farmer", st.session_state.farmer_name)
col2.metric("Region", region)
col3.metric("Crop Stage", crop_stage)


# ---------------- PROMPT ENGINE ----------------
def build_prompt():
    return f"""
You are an expert agricultural advisor.
Farmer details:
Region: {region}
Location: {location}
Crop stage: {crop_stage}
Priorities: {', '.join(priority)}

Task:
1. Give 3 clear farming recommendations.
2. Format as bullet points.
3. After each recommendation, explain WHY it is useful.
4. Keep language simple and practical.
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
                    "max_output_tokens": 512
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



            

 

# ---------------- FEEDBACK CHECKLIST ----------------
with tab_feedback:
    st.markdown("## ✅ AI Output Validation Checklist")

    feedback = {
        "Region-specific advice": st.checkbox("Advice is specific to my region"),
        "Logical reasoning": st.checkbox("Suggestions include valid reasoning"),
        "Simple language": st.checkbox("Language is easy to understand"),
        "Actionable steps": st.checkbox("Advice can be applied practically"),
        "Safe & ethical": st.checkbox("No unsafe or misleading information")
    }

    if st.button("📊 Submit Feedback"):
        score = sum(feedback.values())
        st.success(f"Feedback Score: {score}/5")


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
