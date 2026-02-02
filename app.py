import sys
import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai

st.write(sys.version)
st.session_state.clear()

# ---------------- SESSION STATE ----------------
if "quota_exhausted" not in st.session_state:
    st.session_state.quota_exhausted = False

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="FarmaBuddy 🌱",
    page_icon="🌾",
    layout="wide"
)

# ---------------- API KEY ----------------
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

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

region = st.sidebar.selectbox(
    "Select Region",
    ["India", "Ghana", "Canada"]
)

location = st.sidebar.text_input(
    "Enter Location (State / Province)"
)

crop_stage = st.sidebar.selectbox(
    "Crop Stage",
    ["Planning", "Sowing", "Growing", "Harvesting"]
)

priority = st.sidebar.multiselect(
    "Your Priorities",
    ["Low Water Use", "High Yield", "Organic Farming", "Low Cost"]
)

temperature = st.sidebar.slider(
    "AI Creativity Level",
    0.2, 0.9, 0.5
)

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
5. Avoid unsafe or misleading advice.
"""

# ---------------- MAIN ACTION ----------------
if st.button("🌾 Get Smart Advice"):
    if not location:
        st.warning("Please enter your location.")
    else:
        # 🚫 If quota already exhausted → NO API CALL
        if st.session_state.quota_exhausted:
            st.warning("⚠️ AI quota exhausted. Showing expert fallback advice.")

            st.markdown(f"""
- **Select crops suitable for {region}**  
  Region-specific crops perform better under local climate and soil conditions.

- **Follow best practices during the {crop_stage.lower()} stage**  
  Each crop stage needs specific irrigation, nutrients, and care.

- **Balance inputs based on priorities**  
  Focusing on {', '.join(priority) if priority else 'sustainable practices'} improves yield and reduces waste.
            """)

            st.info("ℹ️ Fallback advice ensures uninterrupted support even when AI services are unavailable.")

        else:
            with st.spinner("Consulting AI farming expert..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=build_prompt(),
                        config={
                            "temperature": temperature,
                            "max_output_tokens": 512
                        }
                    )

                    st.success("Here’s your AI-generated farming advice:")
                    st.markdown(response.text)

                except Exception as e:
                    # 🚨 Lock AI for rest of session
                    st.session_state.quota_exhausted = True

                    st.warning("⚠️ AI quota reached. Switching to expert fallback advice.")

                    st.markdown(f"""
- **Adopt climate-resilient farming methods**  
  These reduce dependency on unpredictable weather conditions.

- **Monitor soil health regularly**  
  Healthy soil improves nutrient absorption and long-term productivity.

- **Apply stage-specific techniques during {crop_stage.lower()}**  
  Correct timing of irrigation and fertilization improves yield quality.
                    """)

                    st.info("ℹ️ The system automatically switches to offline guidance when AI is unavailable.")

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
    st.markdown("Thank you! This helps improve AI reliability.")

# ---------------- USAGE LOG ----------------
st.markdown("## 📈 Usage Snapshot")

log_data = {
    "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "Region": region,
    "Crop Stage": crop_stage
}

df = pd.DataFrame([log_data])
st.dataframe(df)

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <p style='text-align:center; font-size:14px;'>
    FA-2 Project | CRS Artificial Intelligence | Generative AI<br>
    Built responsibly for real-world farmers 🌍
    </p>
    """,
    unsafe_allow_html=True
)
