import os
from google import genai

def generate_lore_bible(parsed_data):
    """Takes parsed narrative data and uses Gemini to synthesize a Lore Bible & Character Profiles."""
    client = genai.Client()
    
    narrative_summary_str = str(parsed_data)
    
    prompt = f"""
    You are an expert Narrative Designer and Video Game Lore Master. 
    Review the following extracted dialogue lines, text strings, and file data from a narrative game project:
    
    {narrative_summary_str}
    
    Based on this text, generate a professional Lore Bible and Narrative Overview covering:
    1. **World Background & Setting** (what kind of universe or underground realm this implies).
    2. **Key Character Profiles** (deduced personalities, roles, and tones from the dialogue lines).
    3. **Thematic Summary** (the core emotional or narrative hook of the game).
    
    Keep it engaging, beautifully structured with markdown headings, and ready for a pitch deck.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error generating Lore Bible via AI: {str(e)}"