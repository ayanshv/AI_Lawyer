import streamlit as st
import pypdf
from pdf_reader import extract_pdf

st.set_page_config(
    page_title = "Rights AI",
    layout = "wide"
)

st.title("_Rights AI_. Your companion in the :red[legal] world.")

uploaded_pdf = st.file_uploader("Upload your legal document", type = "pdf")
document_text = ""
if uploaded_pdf is not None:
    document_text = extract_pdf(uploaded_pdf)

    if document_text:
        with st.spinner("Analyzing the document"):
            st.markdown(document_text)

