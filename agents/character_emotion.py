import os
from google import genai

def analyze_character_sentiments(parsed_narrative_data):
    """Uses Gemini to perform sentiment analysis and generate psychological sketches of characters."""
    client = genai.Client()
    
    data_str = str(parsed_narrative_data)
    
    prompt = f"""
    You are a game narrative and character analyst. Analyze the following extracted code snippets and dialogue strings from a specific game file.
   
    {data_str}
    
    Your task is to generate a **Character Alignment & Sentiment Sketch Matrix** (similar to analyzing characters like Flowey as manipulative/hostile or Asgore as tragic/misunderstood). For each character or narrative node detected:
    1. **Primary Alignment / Sentiment Vector** (e.g., Malevolent, Misunderstood, Melancholic, Cheerful).
    2. **Emotional Tone & Subtext** (what their word choice and sentiment scores reveal beneath the surface).
    3. **Thematic Role** (how their dialogue dynamics reflect their relationship with the player or world).

    CRITICAL INSTRUCTIONS:
    1. Analyze ONLY the exact text and dialogue provided in the current file snippet. 
    2. Do NOT assume external lore, future game events, or cross-file plotlines (e.g., do not assume a character is dead or a battle has happened unless explicitly stated in these specific lines).
    3. If an emotional tone or sentiment is ambiguous, focus strictly on the literal subtext of the provided strings.
    
    Structure the output cleanly using Markdown, bold headers, and vivid, pitch-ready narrative descriptions.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error running sentiment analysis: {str(e)}"