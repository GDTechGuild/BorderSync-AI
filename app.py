import os
import streamlit as st
import agents.parser as parser
import agents.gdd_generator as gdd
import agents.lore as lore
import agents.character_emotion as sentiment

st.set_page_config(page_title="IndieGen", page_icon="🎮", layout="wide")

st.title("IndieGen 🎮")
st.subheader("Automated Game Design Document & Lore Synthesizer")

# Initialize session state for persistence across reruns
if "discovered_files" not in st.session_state:
    st.session_state.discovered_files = None
if "parse_triggered" not in st.session_state:
    st.session_state.parse_triggered = False
if "parsed_data" not in st.session_state:
    st.session_state.parsed_data = {}
if "ai_gdd" not in st.session_state:
    st.session_state.ai_gdd = ""
if "ai_lore" not in st.session_state:
    st.session_state.ai_lore = ""
if "ai_sentiment" not in st.session_state:
    st.session_state.ai_sentiment = ""

with st.sidebar:
    st.header("Configuration")
    entered_path = st.text_input("Repository Path", placeholder="path/to/game/source")
    
    # Robust path sanitization: strip quotes, whitespace, and normalize OS path separators
    repo_path = os.path.normpath(entered_path.strip().strip('"').strip("'"))
    
    parse_btn = st.button("Generate GDD & Lore", type="primary")

# Handle button click and execution
if parse_btn and repo_path:
    with st.spinner("Analyzing repository, synthesizing narrative, and evaluating sentiments..."):
        discovered_files = parser.scan_repository(repo_path)
        st.session_state.discovered_files = discovered_files
        
        if discovered_files:
            parsed_data = parser.extract_game_mechanics(discovered_files)
            st.session_state.parsed_data = parsed_data
            
            # Run all three AI agents concurrently/sequentially
            st.session_state.ai_gdd = gdd.generate_gdd_narrative(parsed_data)
            st.session_state.ai_lore = lore.generate_lore_bible(parsed_data)
            st.session_state.ai_sentiment = sentiment.analyze_character_sentiments(parsed_data)
        else:
            st.session_state.parsed_data = {}
            st.session_state.ai_gdd = "No files available to generate GDD."
            st.session_state.ai_lore = "No narrative files found."
            st.session_state.ai_sentiment = "No sentiment data available."
            
        st.session_state.parse_triggered = True

# Static layout columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Source Code & Dialogue Files")
    if not st.session_state.parse_triggered:
        st.info("Files detected will appear here once parsed.")
    else:
        files = st.session_state.discovered_files
        if files:
            st.success(f"Found {len(files)} files!")
            for f in files[:15]:
                st.text(f)
        else:
            st.warning("No .cs, .gd, or .json files found in that path.")

with col2:
    st.subheader("Generated GDD, Lore & Character Matrix")
    if not st.session_state.parse_triggered:
        st.info("Your reverse-engineered documentation will render here.")
    else:
        # 1. AI Synthesized GDD
        ai_gdd_text = st.session_state.get("ai_gdd", "")
        if ai_gdd_text:
            with st.expander("🤖 AI Synthesized GDD", expanded=True):
                st.markdown(ai_gdd_text)
            st.divider()
            
        # 2. AI Lore Bible
        ai_lore_text = st.session_state.get("ai_lore", "")
        if ai_lore_text:
            with st.expander("📖 World Lore Bible", expanded=False):
                st.markdown(ai_lore_text)
            st.divider()

        # 3. Character Sentiment & Alignment Matrix
        ai_sentiment_text = st.session_state.get("ai_sentiment", "")
        if ai_sentiment_text:
            with st.expander("🎭 Character Sentiment & Alignment Matrix", expanded=False):
                st.markdown(ai_sentiment_text)
            st.divider()
            
        # 4. Technical Variable Breakdown
        parsed_data = st.session_state.get("parsed_data", {})
        if parsed_data:
            st.markdown("### 🔍 Technical Variable Breakdown")
            for filename, data in parsed_data.items():
                with st.expander(f"📄 {filename}"):
                    if "error" in data:
                        st.error(f"Error reading file: {data['error']}")
                    else:
                        st.write(f"**Line Count:** {data['line_count']}")
                        
                        # Show snippets if narrative strings exist
                        snippets = data.get("narrative_snippets", [])
                        if snippets:
                            st.markdown("**Extracted Narrative Snippets:**")
                            st.write(snippets[:5])
                            
                        # Show code variables if they exist
                        vars_dict = data.get("variables", {})
                        if vars_dict:
                            st.markdown("**Extracted Variables:**")
                            st.json(vars_dict)
                        elif not snippets:
                            st.caption("No matching variables or text snippets found.")
        else:
            st.warning("No valid files available to parse.")