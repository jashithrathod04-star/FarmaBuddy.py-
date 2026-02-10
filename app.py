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
        <h1 style='text-align:center;'>🌱 FarmaBuddy Sign Up</h1>
        <p style='text-align:center;'>Welcome! Please enter your details to continue.</p>
        <hr>
        """,
        unsafe_allow_html=True
    )

    farmer_name = st.text_input("👨‍🌾 Farmer Name")
    farmer_location = st.text_input("📍 Village / City / State")

    if st.button("✅ Sign Up"):
        if farmer_name and farmer_location:
            st.session_state.farmer_name = farmer_name
            st.session_state.farmer_location = farmer_location
            st.session_state.signed_up = True
            st.rerun()
        else:
            st.warning("Please fill in all fields.")

    st.stop()   # ⛔ Prevents rest of app from loading



# ---------------- HEADER ----------------
st.markdown(
    f"""
    <h1 style='text-align:center;'>🌱 FarmaBuddy</h1>
    <h4 style='text-align:center;'>Welcome, {st.session_state.farmer_name} 👋</h4>
    <p style='text-align:center;'>Location: {st.session_state.farmer_location}</p>
    <p style='text-align:center;'>AI-Powered Smart Farming Assistant</p>
    <hr>
    """,
    unsafe_allow_html=True
)



# ---------------- TABS ----------------
tab_advice, tab_feedback = st.tabs(
    ["🌾 Farming Advice", "📊 Feedback"]
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
st.markdown("## 📈 Usage Snapshot")
log_data = {"Time": datetime.now().strftime("%Y-%m-%d %H:%M"), "Region": region, "Crop Stage": crop_stage}
st.dataframe(pd.DataFrame([log_data]))

# ---------------- FOOTER ----------------
st.markdown("<hr><p style='text-align:center; font-size:14px;'>FA-2 Project | 2026</p>", unsafe_allow_html=True)
