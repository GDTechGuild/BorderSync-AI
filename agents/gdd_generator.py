import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # Load environment variables from .env file

def generate_gdd_narrative(parsed_data):
    """Takes parsed code data and uses Gemini to generate a professional GDD summary."""
    # Initialize the client (it automatically picks up os.environ["GEMINI_API_KEY"])
    client = genai.Client()
    
    code_summary_str = str(parsed_data)
    
    prompt = f"""
    You are an expert Lead Game Designer and Technical Writer. 
    Review the following extracted code variables and file metrics from a game project:
    
    {code_summary_str}
    
    Based on this data, write a clean, professional Game Design Document (GDD) section covering:
    1. **Core Mechanics & Player Stats** (derived from the variables).
    2. **Gameplay Overview** (what kind of game this appears to be).
    3. **Technical Architecture Notes** (based on file structure and parameters).
    
    Keep it engaging, structured with markdown headings, and ready for a project presentation.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error generating GDD via AI: {str(e)}"