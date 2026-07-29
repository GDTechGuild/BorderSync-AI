IndieGen
IndieGen is an automated, AI-powered Game Design Document (GDD) and narrative lore synthesizer designed for indie developers and hackathons. It scans your game repository—parsing both code logic (variables, functions, structure) and narrative assets (dialogue JSONs, scripts)—to instantly generate professional documentation, World Lore Bibles, and Character Sentiment & Alignment Matrices.

Key Features
Universal Repository Scanner: Recursively crawls project directories supporting code files (.cs, .gd, .py) and narrative assets (.json, .txt).

Automated GDD Generation: Extracts structural variables and game mechanics to auto-draft clean, comprehensive markdown documentation.

World Lore Synthesizer: Parses dialogue trees and narrative files to map out cohesive world-building overviews and backstories.

Character Sentiment & Alignment Matrix: Evaluates extracted character dialogue snippets to map out emotional vectors, subtext, and psychological profiles module-by-module.

Streamlit Frontend: A developer-friendly interface providing real-time generation and visualization of your game's documentation.

Tech Stack
Frontend/UI: Streamlit

AI Intelligence: Google GenAI SDK (gemini-3.5-flash)

Core Language: Python

Parsing: Custom Regex & JSON traversal engines

Getting Started
1. Installation
Clone the repository and install the required dependencies:

Bash
git clone https://github.com/your-username/indiegen.git
cd indiegen
pip install -r requirements.txt
2. Set Up Environment Variables
Configure your Google Gemini API key:

Bash
export GEMINI_API_KEY="your_api_key_here"
3. Run the App
Launch the Streamlit interface:

Bash
streamlit run app.py
How to Use
Point the Repository Path input in the sidebar toward your game project folder (e.g., a directory containing your .cs scripts or dialogue .json files).

Click Generate GDD & Lore.

Review your auto-generated Game Design Document, World Lore Bible, and Character Sentiment Matrix instantly.