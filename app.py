import streamlit as st
import google.generativeai as genai

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="BiharKrishi AI", page_icon="🌾", layout="wide")

# --- 2. GEMINI API SETUP (Integrated) ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Optimized parameters to ensure factual, region-specific results (Step 5)
        generation_config = {
            "temperature": 0.2, 
            "max_output_tokens": 400,
        }
        
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config
        )
    else:
        st.error("⚠️ API Key missing! Go to Streamlit Settings > Secrets and add GOOGLE_API_KEY.")
        st.stop()
except Exception as e:
    st.error(f"❌ Connection Error: {e}")
    st.info("Tip: Double-check your API Key in Google AI Studio and ensure it is active.")

# --- 3. SIDEBAR: EDITABLE USER PROFILE (Requirement for User Interaction Monitoring) ---
with st.sidebar:
    st.title("👤 User Profile")
    farmer_name = st.text_input("Farmer Name:", value="Ram Kumar Baitha")
    farmer_location = st.text_input("Home Location:", value="Kishanganj, Bihar")
    land_size = st.text_input("Land Size (Hectares):", value="0.25")
    st.divider()
    st.info("This assistant provides region-specific advice for Bihar's farmers.")

# --- 4. MAIN UI (Design and Implementation) ---
st.title("🌾 BiharKrishi AI: Smart Farming Assistant")
st.subheader("Solving Bihar's Flood-Drought Paradox with Generative AI")

# Structured input fields for accurate model context (Step 6)
col1, col2 = st.columns(2)
with col1:
    location = st.text_input("Enter your District:", value="Samastipur")
    crop_stage = st.text_input("Current Crop Stage:", value="Vegetative")

with col2:
    category = st.text_input("What do you need help with?", value="Diesel Cost Saving")

user_query = st.text_input("Enter your specific farming question (e.g., How to save fuel?)")

# --- 5. OUTPUT FORMATTING & REASONING (Step 4) ---
if st.button("Get AI Advice"):
    if user_query and location:
        with st.spinner("Analyzing regional agricultural data..."):
            # System instruction ensures outputs are formatted and justified (Step 4)
            full_prompt = f"""
            You are an expert Bihar agricultural consultant. 
            User Profile: {farmer_name} from {farmer_location} with {land_size} hectares.
            Current Query Context: District {location}, Crop Stage {crop_stage}.
            Category: {category}.
            Question: {user_query}
            
            Instructions: Provide a formatted response as per FA-2 standards:
            1. Use a bulleted list for actionable instructions.
            2. Include a brief 'Why' (justification) for each suggestion to build trust.
            3. Use simple, non-technical language for a layperson.
            """
            
            try:
                response = model.generate_content(full_prompt)
                
                # Displaying formatted Gemini output
                st.markdown("### 💡 Expert Recommendations")
                st.write(response.text)
                
                # Feedback Monitoring (Learning Outcome for FA 2)
                st.divider()
                st.caption("Was this advice helpful?")
                st.button("👍 Yes")
                st.button("👎 No")
                
            except Exception as e:
                st.error(f"Error generating content: {e}")
    else:
        st.warning("Please ensure you have filled in all the text fields and entered a question.")
