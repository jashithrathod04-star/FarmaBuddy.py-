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
    st.title("🌱 FarmaBuddy Sign Up")
    st.write("Enter your details to continue")

    name = st.text_input("Farmer Name")
    location_signup = st.text_input("Village / City / State")

    if st.button("Sign Up"):
        if name and location_signup:
            st.session_state.farmer_name = name
            st.session_state.farmer_location = location_signup
            st.session_state.signed_up = True
            st.rerun()
        else:
            st.warning("Please fill all fields")

    st.stop()

# ---------------- HEADER ----------------
st.title("🌱 FarmaBuddy")
st.caption("AI Powered Smart Farming Assistant")

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
