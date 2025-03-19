# TalentScout - AI-Powered Hiring Assistant

TalentScout is a user-friendly, AI-powered hiring assistant chatbot built with Streamlit, OpenAI API, and SQLite. It collects candidate details step by step, suggests suitable job positions based on your skills and experience, and securely stores your data in a local database.

---

## Features
- **Interactive Chatbot:** Seamlessly collects your details.
- **Job Suggestions:** Provides AI-generated job recommendations tailored to your tech stack and experience.
- **Data Storage:** Safely saves your candidate information in an SQLite database.
- **Modular Code:** Clean separation of database logic and UI code for easier maintenance.

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/TalentScout.git
   cd TalentScout
   
2. **Set Up a Virtual Environment (Optional)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

4. **Configure Environment Variables Create a .env file in the project root with your OpenAI API key:**
   ```bash
   OPENAI_API_KEY=your_openai_api_key


5. ##How to Run the App
**Start the Streamlit application:**
   ```bash
   Start the Streamlit application

##Project Structure
   ```bash
  /TalentScout
  ├── app.py            # Main Streamlit application
  ├── db.py             # Database-related functions
  ├── requirements.txt  # Project dependencies
  ├── .env              # Environment variables (API keys)
  └── README.md         # Project documentation
