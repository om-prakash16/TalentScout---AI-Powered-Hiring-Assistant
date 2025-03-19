import os
import streamlit as st
import openai
from db import init_db, save_candidate_data
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# -------------------------------------------------------------------
# Database Connection
# -------------------------------------------------------------------
conn, cursor = init_db()

# -------------------------------------------------------------------
# OpenAI API Configuration
# -------------------------------------------------------------------
openai.api_key = os.getenv("OPENAI_API_KEY", "your_openai_api_key")

# -------------------------------------------------------------------
# Streamlit UI Setup
# -------------------------------------------------------------------
st.title("TalentScout Hiring Assistant 🤖")
st.write("Welcome! I am **TalentScout**, your hiring assistant chatbot.")

# -------------------------------------------------------------------
# Session State Initialization
# -------------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {}

# Step 0: Full Name Collection
if st.session_state.step == 0:
    with st.form(key="form_name"):
        full_name = st.text_input("What is your full name?")
        submitted = st.form_submit_button("Next")
        if submitted and full_name:
            st.session_state.candidate_data["name"] = full_name
            st.session_state.step = 1

# Step 1: Email Address Collection
if st.session_state.step == 1:
    first_name = st.session_state.candidate_data["name"].split()[0]
    with st.form(key="form_email"):
        email = st.text_input(f"Hi {first_name}, please enter your email address:")
        submitted = st.form_submit_button("Next")
        if submitted and email:
            st.session_state.candidate_data["email"] = email
            st.session_state.step = 2

# Step 2: Phone Number Collection
if st.session_state.step == 2:
    with st.form(key="form_phone"):
        phone = st.text_input("Enter your phone number:")
        submitted = st.form_submit_button("Next")
        if submitted and phone:
            st.session_state.candidate_data["phone"] = phone
            st.session_state.step = 3

# Step 3: Location Collection
if st.session_state.step == 3:
    with st.form(key="form_location"):
        location = st.text_input("Where are you currently located?")
        submitted = st.form_submit_button("Next")
        if submitted and location:
            st.session_state.candidate_data["location"] = location
            st.session_state.step = 4

# Step 4: Tech Stack Collection
if st.session_state.step == 4:
    with st.form(key="form_tech_stack"):
        tech_stack_input = st.text_area("Enter your Tech Stack (comma-separated):")
        submitted = st.form_submit_button("Next")
        if submitted and tech_stack_input:
            tech_stack_list = [tech.strip() for tech in tech_stack_input.split(",") if tech.strip()]
            st.session_state.candidate_data["tech_stack"] = tech_stack_list
            st.session_state.step = 5

# Step 5: Experience Collection
if st.session_state.step == 5:
    with st.form(key="form_experience"):
        experience = st.number_input("How many years of experience do you have?", min_value=0, max_value=50, step=1)
        submitted = st.form_submit_button("Next")
        if submitted:
            st.session_state.candidate_data["experience"] = experience
            st.session_state.step = 6

# Step 6: Generate Job Suggestions and Save Data
if st.session_state.step == 6:
    st.write("Thank you for providing your details!")
    
    tech_stack_str = ", ".join(st.session_state.candidate_data["tech_stack"])
    experience = st.session_state.candidate_data["experience"]
    
    if experience < 2:
        candidate_level = "Junior"
    elif 2 <= experience < 5:
        candidate_level = "Early Career"
    elif 5 <= experience < 10:
        candidate_level = "Intermediate"
    else:
        candidate_level = "Senior"

    prompt_query = (
        f"A candidate has the following skills: {tech_stack_str} and {experience} years of experience, "
        f"which corresponds to a {candidate_level} level. Suggest 3-5 suitable job positions."
    )
    
    st.write("Generating job suggestions based on your tech stack and experience...")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert career advisor."},
                {"role": "user", "content": prompt_query}
            ]
        )
        suggestions = response.choices[0].message.content
        st.session_state.candidate_data["suggested_positions"] = suggestions
    except Exception as e:
        suggestions = f"Error generating job suggestions: {str(e)}"
    
    st.subheader("Job Suggestions and Candidate Level")
    st.write(f"**Candidate Level:** {candidate_level}")
    st.write(suggestions)
    
    if save_candidate_data(conn, cursor, st.session_state.candidate_data) == True:
        st.success("Your details have been saved successfully!")
    else:
        st.error("Error saving data.")

    if st.button("Restart Chat"):
        st.session_state.step = 0
        st.session_state.candidate_data = {}
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
