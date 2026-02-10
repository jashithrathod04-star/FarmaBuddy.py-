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
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0d0552;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #2E7D32;
    color: white;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white;
}

/* Headings */
h1, h2, h3, h4 {
    color: #1B5E20;
}

/* Buttons */
.stButton > button {
    background-color: #66BB6A;
    color: white;
    border-radius: 10px;
    padding: 0.6em 1.2em;
    font-weight: bold;
    border: none;
}

.stButton > button:hover {
    background-color: #388E3C;
    color: white;
}

/* Tabs */
button[data-baseweb="tab"] {
    background-color: #E8F5E9;
    color: #1B5E20;
    font-weight: 600;
    border-radius: 8px;
    margin-right: 4px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #A5D6A7;
    color: #1B5E20;
}

/* Success, info boxes */
div[data-testid="stSuccess"] {
    background-color: #C8E6C9;
    color: #1B5E20;
}

div[data-testid="stInfo"] {
    background-color: #E3F2FD;
    color: #0D47A1;
}

/* Dataframe container */
.stDataFrame {
    background-color: white;
    border-radius: 10px;
    padding: 10px;
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
tab_advice, tab_feedback, tab_usage = st.tabs(
    ["🌾 Farming Advice", "📊 Feedback", "📈 Usage Snapshot"]
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


# ---------------- FOOTER ----------------
st.markdown("<hr><p style='text-align:center; font-size:14px;'>FA-2 Project | 2026</p>", unsafe_allow_html=True)
