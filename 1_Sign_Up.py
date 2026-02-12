import streamlit as st

st.set_page_config(
    page_title="Sign Up | FarmaBuddy",
    page_icon="🌱",
    layout="centered"
)

# Initialize session state
if "signed_up" not in st.session_state:
    st.session_state.signed_up = False
if "farmer_name" not in st.session_state:
    st.session_state.farmer_name = ""
if "farmer_location" not in st.session_state:
    st.session_state.farmer_location = ""

# Design Header
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
    if name and location_signup:
        st.session_state.farmer_name = name
        st.session_state.farmer_location = location_signup
        st.session_state.signed_up = True
        st.success("Account created! Go to Dashboard.")
    else:
        st.warning("Please fill all fields")
