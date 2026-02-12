import os
import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FarmaBuddy 🌱",
    page_icon="🌾",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #F4F9F4;
}

/* Header Styling */
h1 {
    color: #1B3A2F;
    font-weight: 700;
}

h2, h3 {
    color: #2E7D32;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #E8F5E9;
    border-right: 2px solid #C8E6C9;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #2E7D32, #66BB6A);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.6em 1.2em;
    font-weight: 600;
    transition: 0.3s ease;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #1B5E20, #43A047);
    transform: scale(1.03);
}

/* Tabs */
button[data-baseweb="tab"] {
    font-weight: 600;
    color: #2E7D32;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #C8E6C9;
    border-radius: 8px;
}

/* Cards */
div[data-testid="stMetric"],
div[data-testid="stDataFrameContainer"] {
    background-color: white;
    padding: 15px;
    border-radius: 14px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}

/* Footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------
if "signed_up" not in st.session_state:
    st.session_state.signed_up = False
if "farmer_name" not in st.session_state:
    st.session_state.farmer_name = ""
if "farmer_location" not in st.session_state:
    st.session_state.farmer_location = ""

# ---------------- GEMINI CLIENT ----------------
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# ---------------- SIGNUP PAGE ----------------
if not st.session_state.signed_up:

    st.markdown("""
    <div style="
        background: linear-gradient(120deg, #2E7D32, #66BB6A);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    ">
        <h1>🌱 FarmaBuddy</h1>
        <p>Smart AI Farming Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Create Your Profile")

    name = st.text_input("Farmer Name")
    location_signup = st.text_input("Village / City / State")

    if st.button("Sign Up"):
        ...

# ---------------- HEADER ----------------
st.markdown("""
<div style="
    background: linear-gradient(90deg, #2E7D32, #66BB6A);
    padding: 25px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.08);
">
    <h1 style="margin-bottom: 5px;">🌱 FarmaBuddy</h1>
    <p style="font-size: 1.1rem; opacity: 0.95;">
        AI Powered Smart Farming Assistant
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
col1.write(f"👨‍🌾 Farmer: **{st.session_state.farmer_name}**")
col2.write(f"📍 Location: **{st.session_state.farmer_location}**")

# ---------------- SIDEBAR INPUTS ----------------
st.sidebar.header("🌍 Farming Inputs")

region = st.sidebar.selectbox("Region", ["India", "Ghana", "Canada"])
location = st.sidebar.text_input("Farm Location")
crop_stage = st.sidebar.selectbox(
    "Crop Stage",
    ["Planning", "Sowing", "Growing", "Harvesting"]
)
priority = st.sidebar.multiselect(
    "Priorities",
    ["Low Water Use", "High Yield", "Organic Farming", "Low Cost"]
)

# ---------------- PROMPT ----------------
def build_prompt():
    return f"""
You are an expert agricultural advisor.

Farmer Region: {region}
Farm Location: {location}
Crop Stage: {crop_stage}
Priorities: {', '.join(priority)}

Give 3 farming recommendations.
Use simple language.
Explain WHY after each point.
Format using bullet points.
"""

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["🌾 Farming Advice", "📊 Feedback", "📈 Usage", "⚙️ Settings"]
)

# ---------------- FARMING ADVICE ----------------
with tab1:
    st.header("Get AI Farming Advice")

    if st.button("Generate Advice 🌾"):

        if not location:
            st.warning("Please enter farm location")
        else:
            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=build_prompt()
                )

                st.success("AI Recommendations:")
                st.markdown(response.text)

            except Exception as e:
                st.error("AI Error — check API key in Streamlit secrets")
                st.exception(e)

# ---------------- FEEDBACK ----------------
with tab2:
    st.header("AI Output Checklist")

    checks = {
        "Region specific": st.checkbox("Advice matches my region"),
        "Logical reasoning": st.checkbox("Advice makes sense"),
        "Simple language": st.checkbox("Easy to understand"),
        "Actionable": st.checkbox("Can apply in real life"),
        "Safe": st.checkbox("No risky suggestions"),
    }

    if st.button("Submit Feedback"):
        score = sum(checks.values())
        st.success(f"Feedback Score: {score}/5")

# ---------------- USAGE SNAPSHOT ----------------
with tab3:
    st.header("Usage Snapshot")

    data = {
        "Farmer": st.session_state.farmer_name,
        "Location": st.session_state.farmer_location,
        "Region": region,
        "Crop Stage": crop_stage,
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    st.dataframe(pd.DataFrame([data]))

# ---------------- SETTINGS ----------------
with tab4:
    st.header("Settings")

    st.write("Profile")
    st.info(
        f"Name: {st.session_state.farmer_name}\n\nLocation: {st.session_state.farmer_location}"
    )

    if st.button("Sign Out"):
        st.session_state.signed_up = False
        st.session_state.farmer_name = ""
        st.session_state.farmer_location = ""
        st.rerun()

# ---------------- FOOTER ----------------
st.divider()
st.caption("FarmaBuddy • 2026")
