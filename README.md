Project IndieGen

Automated Game Design Document & Lore Synthesizer


Bridging the gap between raw game source code and readable, up-to-date Game Design Documents (GDDs).

The Problem:

Writing Game Design Documents (GDDs) and synthesizing deep lore from chaotic, multi-file game source code manually is tedious, slow, and prone to becoming entirely out-of-sync the moment iteration begins. Developers are often forced to choose between actually building the game or documenting it.


The Solution:

IndieGen is an automated multi-agent pipeline and Streamlit-powered dashboard that acts as your robotic technical writer. It scans local game codebases (.cs, .gd, .json), extracts core mechanics and narrative structure, and reverse-engineers clean, cohesive game documentation.

Core Features:

•	Robust Path Sanitization & Ingestion: Seamlessly connects to local repository directories. Native support for Windows paths without breaking.
•	Automated Code Parsing: Traverses project directories to specifically hunt for crucial logic files. It strips boilerplate noise, reads code contents, and aggregates file metrics and previews.
•	Multi-Agent AI Synthesis: Mechanics Analyst scans player controllers and physics scripts to map out gameplay loops. Lore Master parses JSON dialog trees and item arrays to weave narrative context.
•	Developer-Friendly Dashboard: Built on Streamlit with structured state management. Features a side-by-side data rendering view to verify raw code snippets against generated GDD sections.

Tech Stack:
•	Frontend: Streamlit
•	Backend Parsing: Python (os, re, custom parsers)
•	AI/LLM: Multi-Agent Pipeline (e.g., LangChain / OpenAI APIs)
•	Supported Game Engines (Targets): Unity (.cs), Godot (.gd), Custom (.json)


How to Run Locally:

1. Clone the repository
git clone https://github.com/yourusername/Project-IndieGen.git
cd Project-IndieGen

2. Install Dependencies
pip install -r requirements.txt

3. Set up Environment Variables
Create a .env file in the root directory and add your LLM API keys:
OPENAI_API_KEY=your_api_key_here

4. Run the Streamlit Dashboard
streamlit run app.py

Roadmap / Future Features

•	Export to PDF and Notion integrations.
•	Support for Unreal Engine C++ and Blueprints.
•	Visual node-graph generation for dialogue trees.
•	Real-time file watching (auto-update GDD on file save).
