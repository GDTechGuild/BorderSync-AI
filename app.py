import os
import streamlit as st
import agents.parser as parser
import agents.gdd_generator as gdd
import agents.lore as lore
import agents.character_emotion as sentiment
import FileDownloader as dwnld
import agents.metrics as metrics

st.set_page_config(page_title="IndieGen", page_icon="👾", layout="wide")
st.divider()
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        font-family: 'Outfit', sans-serif;
    }
    .stApp {
        background-color: #0c0e14;
        background-image: 
            radial-gradient(circle at 50% -20%, rgba(56, 189, 248, 0.08) 0%, transparent 60%),
            radial-gradient(circle at 100% 100%, rgba(14, 165, 233, 0.04) 0%, transparent 50%);
    }
    [data-testid="stSidebar"] {
        background-color: rgba(12, 14, 20, 0.95);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-right: 1px solid rgba(56, 189, 248, 0.1);
    }

    div.stButton > button[key="main_launch_btn"] {
        width: 100% !important;
        background: linear-gradient(180deg, #4ade80 0%, #16a34a 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        letter-spacing: 0.05em;
        padding: 12px 20px !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[key="main_launch_btn"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 28px rgba(34, 197, 94, 0.5) !important;
    }

    .hover-card {
        background: linear-gradient(145deg, rgba(20, 24, 33, 0.7) 0%, rgba(12, 14, 20, 0.8) 100%);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.12);
        border-radius: 12px;
        padding: 20px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        min-height: 220px;
        max-height: 220px;
        overflow: hidden;
        position: relative;
        margin-top: 10px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .hover-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.5), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .hover-card:hover {
        transform: translateY(-4px);
        background: linear-gradient(145deg, rgba(25, 30, 42, 0.95) 0%, rgba(15, 18, 26, 0.98) 100%);
        border-color: rgba(56, 189, 248, 0.5);
        box-shadow: 0 12px 40px -10px rgba(56, 189, 248, 0.25);
        max-height: 500px; /* Expands smoothly on hover */
    }

    .hover-card:hover::before {
        opacity: 1;
    }

    .card-preview {
        font-size: 0.85rem;
        color: #cbd5e1;
        margin-top: 10px;
        line-height: 1.5;
        max-height: 220px;
        overflow-y: auto;
        overflow-x: hidden;
        padding-right: 8px;
        transition: all 0.3s ease;
    }

    .hover-card:hover .card-preview {
        max-height: 380px;
    }

    /* Module inspect buttons above cards */
    [data-testid="column"] div.stButton > button {
        width: 100% !important;
        background: rgba(56, 189, 248, 0.1) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 8px !important;
        color: #38bdf8 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em;
        padding: 10px 16px !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="column"] div.stButton > button:hover {
        background: rgba(56, 189, 248, 0.25) !important;
        border-color: rgba(56, 189, 248, 0.8) !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
        transform: translateY(-1px);
    }

    /* Input styling */
    .stTextInput input {
        background-color: rgba(9, 11, 16, 0.8) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
    }

    /* Download button styling */
    div.stDownloadButton > button {
        width: 100% !important;
        background: rgba(56, 189, 248, 0.15) !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        border-radius: 8px !important;
        color: #38bdf8 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em;
        padding: 10px 16px !important;
        transition: all 0.2s ease !important;
    }
    div.stDownloadButton > button:hover {
        background: rgba(56, 189, 248, 0.3) !important;
        border-color: rgba(56, 189, 248, 0.9) !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
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
if "repo_name" not in st.session_state:
    st.session_state.repo_name = "IndieGen"
if "selected_view" not in st.session_state:
    st.session_state.selected_view = "Overview"

# Main Grid Layout
left_main, right_sidebar = st.columns([2.8, 1.2], gap="small")

with left_main:
    st.markdown(f"<h1 style='font-size: 3.5rem; margin-bottom: 0;'>⚡ {st.session_state.repo_name}</h1>", unsafe_allow_html=True)
    st.caption("Automated Source-to-GDD Pipeline & Architecture Hub")

    # Native Streamlit container to replace html div tag
    with st.container():
        hero_col1, hero_col2 = st.columns([3, 1], gap="medium")
        
        with hero_col1:
            st.caption("TARGET REPOSITORY PATH")
            entered_path = st.text_input("Repository Path Input", placeholder="path/to/game/source", label_visibility="collapsed")
            repo_path = os.path.normpath(entered_path.strip().strip('"').strip("'")) if entered_path else ""

        with hero_col2:
            st.caption("RUN EXECUTION PIPELINE")
            parse_btn = st.button("LAUNCH GAME PARSER", key="main_launch_btn", use_container_width=True)

    # Parser 
    if parse_btn and repo_path:
        if not os.path.exists(repo_path):
            st.error("Invalid path. Folder does not exist.")
        else:
            with st.spinner("Analyzing repository & parsing AST..."):
                discovered_files = parser.scan_repository(repo_path)
                st.session_state.discovered_files = discovered_files
                
                normalized_path = os.path.normpath(repo_path)
                folder_name = os.path.basename(normalized_path) or os.path.basename(os.path.dirname(normalized_path))
                st.session_state.repo_name = folder_name if folder_name else "IndieGen"
                
                if discovered_files:
                    parsed_data = parser.extract_game_mechanics(discovered_files)
                    st.session_state.parsed_data = parsed_data
                    
                    st.session_state.ai_gdd = gdd.generate_gdd_narrative(parsed_data)
                    st.session_state.ai_lore = lore.generate_lore_bible(parsed_data)
                    st.session_state.ai_sentiment = sentiment.analyze_character_sentiments(parsed_data)
                else:
                    st.session_state.parsed_data = {}
                    st.session_state.ai_gdd = "No files available to generate GDD."
                    st.session_state.ai_lore = "No narrative files found."
                    st.session_state.ai_sentiment = "No sentiment data available."
                    
                st.session_state.parse_triggered = True
                st.session_state.selected_view = "Overview"
                st.rerun()

    if not st.session_state.parse_triggered:
        st.info("Input a repository path in the launcher above and click **LAUNCH GAME PARSER** to synthesize your modules.")
    else:
        sections = {
            "Game Design Document": st.session_state.get("ai_gdd", "No data."),
            "World Lore Bible": st.session_state.get("ai_lore", "No data."),
            "Character Matrix": st.session_state.get("ai_sentiment", "No data."),
            "Technical Breakdown": "Technical statistics, extracted variables, and code file line metrics parsed from your source repository."
        }

        if st.session_state.selected_view != "Overview":
            st.markdown("### Module Navigation")
            st.markdown(
                """
                <style>
                div.stButton > button:disabled {
                    background-color: #40A2A3;
                    color: #ffffff;
                    border-color: #15803d;
                }
                div.stButton > button:disabled:hover {
                    background-color: #629986;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            nav_cols = st.columns(4)
            for i, mod_title in enumerate(sections.keys()):
                with nav_cols[i]:
                    is_current = (st.session_state.selected_view == mod_title)
                    btn_label = mod_title if is_current else f" {mod_title.split()[0]}"
                    if st.button(btn_label, key=f"nav_top_btn_{i}", use_container_width=True, disabled=is_current):
                        st.session_state.selected_view = mod_title
                        st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.selected_view == "Overview":
            st.caption("Click the inspect button above any module to open full focus mode, or hover to preview contents.")
            
            # 4-column layout for cards
            cols = st.columns(4)
            card_keys = list(sections.keys())
            
            for i, col in enumerate(cols):
                title = card_keys[i]
                content = sections[title]
                
                clean_lines = [line.strip() for line in content.split("\n") if line.strip()]
                preview_snippet = "<br>".join(clean_lines[:8]) if clean_lines else "Click to inspect module details..."
                
                with col:
                    if st.button(f"Inspect {title.split()[0]} →", key=f"hover_inspect_btn_{i}", use_container_width=True):
                        st.session_state.selected_view = title
                        st.rerun()

                    # hover preview
                    st.markdown(f"""
                        <div class="hover-card">
                            <h4 style="margin: 0 0 6px 0; font-size: 1.05rem; font-weight: 700; color: #f8fafc;">{title}</h4>
                            <div class="card-preview">
                                {preview_snippet}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

        else:
            active_title = st.session_state.selected_view
            st.markdown(f"## {active_title}")
            st.divider()
            
            if active_title != "Technical Breakdown":
                st.markdown(sections[active_title])
            else:
                parsed_data = st.session_state.get("parsed_data", {})
                if parsed_data:
                    for filename, data in parsed_data.items():
                        with st.expander(f"{filename}"):
                            if "error" in data:
                                st.error(f"Error: {data['error']}")
                            else:
                                st.write(f"**Line Count:** {data['line_count']}")
                                snippets = data.get("narrative_snippets", [])
                                if snippets:
                                    st.markdown("**Snippets:**")
                                    st.write(snippets[:5])
                                vars_dict = data.get("variables", {})
                                if vars_dict:
                                    st.markdown("**Variables / Code Preview:**")
                                    st.json(vars_dict)
                else:
                    st.caption("No technical breakdown available.")

            st.markdown("<br><hr>", unsafe_allow_html=True)
            col_left, col_center, col_right = st.columns([2, 3, 2])
            with col_center:
                if st.button("Return to Main Overview Dashboard", use_container_width=True):
                    st.session_state.selected_view = "Overview"
                    st.rerun()

with right_sidebar:
    st.markdown("### 📄 Found Files")
    st.markdown("")
    st.markdown("")
    if not st.session_state.parse_triggered:
        st.caption("No repository indexed yet. Enter path and click Launch Parser.")
    else:
        files = st.session_state.discovered_files
        if files:
            st.success(f"Indexed {len(files)} files successfully.")
            for f in files:
                file_name = os.path.basename(f)
                ext = os.path.splitext(f)[1]
                icon = "⚙️" if ext in ['.cs', '.gd', '.py'] else "📜" if ext == '.json' else "📄"
                st.markdown(f"**{icon} `{file_name}`**")
        else:
            st.warning("No valid code or narrative files found.")

        # export
        st.divider()
        st.markdown("### 💾 Export Options")
        
        sections = {
            "Game Design Document": st.session_state.get("ai_gdd", "No data."),
            "World Lore Bible": st.session_state.get("ai_lore", "No data."),
            "Character Matrix": st.session_state.get("ai_sentiment", "No data."),
            "Technical Breakdown": "Technical statistics, extracted variables, and code file line metrics parsed from your source repository."
        }

        export_content = dwnld.build_txt_export(
            st.session_state.repo_name,
            sections,
            st.session_state.get("parsed_data", {})
        )
        export_filename = dwnld.generate_export_filename(st.session_state.repo_name)

        st.download_button(
            label="📥 Download Documentation (.txt)",
            data=export_content,
            file_name=export_filename,
            mime="text/plain",
            use_container_width=True
        )

        # Metrics
        st.divider()
        st.markdown("### 📊 Parsed Repository Metrics")
        parsed_data = st.session_state.get("parsed_data", {})
        repo_metrics = metrics.calculate_repository_metrics(parsed_data)

        st.markdown(f"* **Total lines parsed:** {repo_metrics['total_lines']}")
        st.markdown(f"* **Extracted Narrative Snippets:** {repo_metrics['snippet_count']}")
        
        st.markdown(
            f"* **Code vs Narrative ratio:** {repo_metrics['ratio_str']}",
            help="Measures the balance between raw source code logic (lines) and written story content (dialogue, lore strings, JSON text). A higher code ratio indicates a mechanics-focused game, while a higher narrative ratio indicates a story-heavy game."
        )

        st.caption("Code vs. Narrative Balance")
        st.progress(repo_metrics['code_pct'] / 100.0)