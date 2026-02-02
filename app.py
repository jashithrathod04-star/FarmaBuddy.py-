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

# ---------------- SESSION STATE ----------------
# DO NOT CLEAR session state at the top. It wipes your quota protection.
if "quota_exhausted" not in st.session_state:
    st.session_state.quota_exhausted = False

# ---------------- API KEY & CLIENT ----------------
# We force the 'v1' stable API version to resolve the 404 issue.
# Change this in your CONFIG section
# In your API KEY & CLIENT section
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"],
)
# Add this temporary button to your sidebar to check names
if st.sidebar.button("🔍 List Available Models"):
    models = client.models.list()
    for m in models:
        st.sidebar.write(m.name)
# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;'>🌱 FarmaBuddy</h1>
    <h4 style='text-align:center;'>AI-Powered Smart Farming Assistant</h4>
    <p style='text-align:center;'>Built using Gemini | Deployed with Streamlit</p>
    <hr>
    """,
    unsafe_allow_html=True
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
if st.button("🌾 Get Smart Advice"):
    if not location:
        st.warning("Please enter your location.")
    else:
        if st.session_state.quota_exhausted:
            st.warning("⚠️ AI quota exhausted. Showing expert fallback advice.")
            st.markdown(f"""
- **Select crops suitable for {region}** Local varieties thrive in specific soil types.
- **Follow best practices during the {crop_stage.lower()} stage** Stage-specific care is vital.
- **Prioritize {', '.join(priority) if priority else 'sustainability'}** This ensures long-term farm health.
            """)
        else:
            with st.spinner("Consulting AI farming expert..."):
                try:
                    # FIX: Switch to gemini-2.0-flash (The standard for 2026)
                    # Inside your try block
                    # ---------------- MAIN ACTION ----------------
                    response = client.models.generate_content(
            model="gemini-2.5-flash", # <--- UPDATE THIS
            contents=build_prompt(),
            config={"temperature": temperature, "max_output_tokens": 512}
        )
                    st.success("Here’s your AI-generated farming advice:")
                    st.markdown(response.text)
 
        # Debugging and Fallback logic...

                except Exception as e:
                    # Capture 429 specifically for quota
                    if "429" in str(e):
                        st.session_state.quota_exhausted = True
                        st.warning("⚠️ AI quota reached. Switching to fallback.")
                    else:
                        st.error(f"Developer Debug Info: {e}")
                    
                    # Displaying Fallback immediately upon error
                    st.markdown(f"""
- **Adopt climate-resilient methods.** These reduce dependency on unpredictable weather.
- **Monitor soil health regularly.** Healthy soil improves nutrient absorption.
- **Apply stage-specific techniques during {crop_stage.lower()}.** Correct timing improves yield.
                    """)

# ---------------- FEEDBACK CHECKLIST ----------------
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
    st.info(f"Feedback Score: {score}/5")

# ---------------- USAGE LOG ----------------
st.markdown("## 📈 Usage Snapshot")
log_data = {"Time": datetime.now().strftime("%Y-%m-%d %H:%M"), "Region": region, "Crop Stage": crop_stage}
st.dataframe(pd.DataFrame([log_data]))

# ---------------- FOOTER ----------------
st.markdown("<hr><p style='text-align:center; font-size:14px;'>FA-2 Project | 2026</p>", unsafe_allow_html=True)
