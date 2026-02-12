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

/* Main background */
.stApp {
    background-color: #f7d80a;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1B5E20;
    color: white;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Dashboard Header */
.dashboard-header {
    background: linear-gradient(90deg, #2E7D32, #66BB6A);
    padding: 20px 30px;
    border-radius: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    color: white;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
}

/* Headings */
h1, h2, h3 {
    color: #1B3A2F;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #2E7D32, #66BB6A);
    color: yellow;
    border-radius: 12px;
    padding: 0.6em 1.2em;
    font-weight: 600;
    border: none;
    transition: 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1B5E20, #43A047);
    transform: scale(1.03);
}

/* Tabs */
button[data-baseweb="tab"] {
    font-weight: 600;
    color: #2E7D32;
    background-color: #E8F5E9;
    border-radius: 8px;
    margin-right: 5px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #f0f7f0;
    color: #1B5E20;
}

/* Cards & Dataframes */
.stDataFrame, 
div[data-testid="stDataFrameContainer"],
div[data-testid="stSuccess"],
div[data-testid="stInfo"] {
    background-color: blue;
    border-radius: 14px;
    padding: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}


/* Make input labels black */
label {
    color: #1B3A2F !important;
    font-weight: 600;
}

/* Force all main page text to dark */
.stApp {
    color: #1B3A2F;
}

/* Checkbox labels */
div[data-testid="stCheckbox"] label {
    color: #1B3A2F !important;
    font-weight: 500;
}

/* Markdown headers */
h2 {
    color: #1B3A2F !important;
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
                config={"temperature": temperature, "max_output_tokens": 512}
            )
            st.success("Here’s your AI-generated farming advice:")
            st.markdown(response.text)
            

 

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
