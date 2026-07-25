import base64
import os
import json
import streamlit as st
from agents.parser import (
    extract_text_from_image,
    extract_text_from_pdf,
    # parse_trade_document_with_crew,
    parse_document
)

def display_document_preview(uploaded_file):
    if uploaded_file is None:
        return

    file_type = uploaded_file.type
    bytes_data = uploaded_file.getvalue()
    base64_data = base64.b64encode(bytes_data).decode("utf-8")

    # 1. Handle PDF preview
    if file_type == "application/pdf":
        pdf_display = f"""
            <iframe 
                src="data:application/pdf;base64,{base64_data}" 
                width="100%" 
                height="650px" 
                type="application/pdf"
                style="border: 1px solid #e6e6e6; border-radius: 8px;">
            </iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)

    # 2. Handle Images (PNG / JPG / JPEG)
    elif file_type in ["image/png", "image/jpeg", "image/jpg"]:
        st.image(
            uploaded_file, caption=uploaded_file.name, use_container_width=True
        )
    else:
        st.warning(f"Preview not available for file type: {file_type}")


def main():
    st.set_page_config(page_title="BorderSync-AI", layout="centered")

    st.title("BorderSync-AI")
    st.write("Simple demo UI for BorderSync-AI")

    st.sidebar.header("Options")
    mode = st.sidebar.selectbox("Mode", ["Upload File", "Enter Text"])

    raw_text = ""

    # --- Mode 1: File Upload ---
    if mode == "Upload File":
        uploaded_file = st.file_uploader(
            "Upload Document", type=["pdf", "png", "jpg", "jpeg"]
        )

        if uploaded_file:
            st.subheader("Document Preview")
            display_document_preview(uploaded_file)

            # Save temporary file to extract text
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Extract raw string based on file type
            try:
                if uploaded_file.type == "application/pdf":
                    raw_text = extract_text_from_pdf(temp_path)
                else:
                    raw_text = extract_text_from_image(temp_path)
            except Exception as e:
                st.error(f"Text extraction failed: {e}")
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    # --- Mode 2: Raw Text Input ---
    else:
        user_text = st.text_area("Enter raw invoice text here:", height=200)
        if user_text.strip():
            raw_text = user_text.strip()

    # --- Run Parser Agent ---
    if st.button("Run Compliance Audit"):
        with st.spinner("Extracting text and parsing via Gemini..."):
                    try:
                        # 1. Extract text from uploaded PDF bytes
                        raw_text = extract_text_from_pdf(uploaded_file)
                        
                        # 2. Call Gemini
                        json_string_response = parse_document(raw_text)
                        
                        # 3. Parse JSON to ensure validity
                        parsed_data = json.loads(json_string_response)
                        
                        # Store in session state to persist across reruns
                        st.session_state.parsed_data = parsed_data
                        st.session_state.json_output_str = json.dumps(parsed_data, indent=4, ensure_ascii=False)
                        
                    except Exception as e:
                        st.error(f"An error occurred during parsing: {e}")
    
    # Display JSON output if it exists in session state
    if "parsed_data" in st.session_state:
        st.subheader("Extracted JSON Output:")
        st.json(st.session_state.parsed_data)
        
        # 4. Streamlit Download Button
        st.download_button(
            label="Download Extracted JSON",
            data=st.session_state.json_output_str,
            file_name="extracted_output.json",
            mime="application/json"
        )

if  __name__ == "__main__":
    main()