import streamlit as st
import pypdf
from pdf_reader import extract_pdf
from analyze import analyze_document

st.set_page_config(
    page_title = "Rights AI",
    layout = "wide"
)

st.title("_Rights AI_. Your companion in the :yellow[legal] world.")

uploaded_pdf = st.file_uploader("Upload your legal document", type = "pdf")
user_question = st.chat_input("What is your inquiry?") 
if uploaded_pdf is not None:
    with st.spinner("Extracting text..."):
        document_info = extract_pdf(uploaded_pdf) 

    if document_info.strip():
        with st.spinner("Analyzing the document..."):
            document_analysis = analyze_document(document_info, user_question)
            st.markdown(document_analysis)
    else:
        st.error("No readable text found in this PDF.")

